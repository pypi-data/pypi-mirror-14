#!/usr/bin/python
# Copyright (c) 2015 Monty Taylor
# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import logging
import os
import platform
import re
import subprocess
import sys
import time

from glean import systemlock

log = logging.getLogger("glean")

post_up = "    post-up route add -net {net} netmask {mask} gw {gw} || true\n"
pre_down = "    pre-down route del -net {net} netmask {mask} gw {gw} || true\n"


def _exists_rh_interface(name):
    file_to_check = '/etc/sysconfig/network-scripts/ifcfg-{name}'.format(
        name=name
        )
    return os.path.exists(file_to_check)


def _write_rh_interface(name, interface, has_vlan):
    files_to_write = dict()
    results = """# Automatically generated, do not edit
DEVICE={name}
BOOTPROTO=static
HWADDR={hwaddr}
IPADDR={ip_address}
NETMASK={netmask}
ONBOOT=yes
NM_CONTROLLED=no
""".format(
        name=name,
        hwaddr=interface['mac_address'],
        ip_address=interface['ip_address'],
        netmask=interface['netmask'],

    )
    if has_vlan:
        results += "VLAN=yes\n"
    routes = []
    for route in interface['routes']:
        if route['network'] == '0.0.0.0' and route['netmask'] == '0.0.0.0':
            results += "DEFROUTE=yes\n"
            results += "GATEWAY={gw}\n".format(gw=route['gateway'])
        else:
            routes.append(dict(
                net=route['network'], mask=route['netmask'],
                gw=route['gateway']))

    if routes:
        route_content = ""
        for x in range(0, len(routes)):
            route_content += "ADDRESS{x}={net}\n".format(x=x, **routes[x])
            route_content += "NETMASK{x}={mask}\n".format(x=x, **routes[x])
            route_content += "GATEWAY{x}={gw}\n".format(x=x, **routes[x])
        files_to_write['/etc/sysconfig/network-scripts/route-{name}'.format(
            name=name)] = route_content
    files_to_write['/etc/sysconfig/network-scripts/ifcfg-{name}'.format(
        name=name)] = results
    return files_to_write


def _write_rh_dhcp(name, hwaddr, has_vlan):
    filename = '/etc/sysconfig/network-scripts/ifcfg-{name}'.format(name=name)
    results = """# Automatically generated, do not edit
DEVICE={name}
BOOTPROTO=dhcp
HWADDR={hwaddr}
ONBOOT=yes
NM_CONTROLLED=no
TYPE=Ethernet
""".format(name=name, hwaddr=hwaddr)
    if has_vlan:
        results += "VLAN=yes\n"
    return {filename: results}


def write_redhat_interfaces(interfaces, sys_interfaces):
    files_to_write = dict()
    # Sort the interfaces by id so that we'll have consistent output order
    for iname, interface in sorted(
            interfaces.items(), key=lambda x: x[1]['id']):
        if interface['type'] == 'ipv6':
            continue
        if iname not in sys_interfaces:
            continue
        interface_name = sys_interfaces[iname]
        has_vlan = False
        if 'vlan_id' in interface:
            interface_name = "{0}.{1}".format(
                interface_name, interface['vlan_id'])
            has_vlan = True
        if interface['type'] == 'ipv4':
            files_to_write.update(
                _write_rh_interface(interface_name, interface, has_vlan))
        if interface['type'] == 'ipv4_dhcp':
            files_to_write.update(
                _write_rh_dhcp(
                    interface_name, interface['mac_address'], has_vlan))
    for mac, iname in sorted(
            sys_interfaces.items(), key=lambda x: x[1]):
        if _exists_rh_interface(iname):
            # This interface already has a config file, move on
            log.debug("%s already has config file, skipping" % iname)
            continue
        if mac in interfaces:
            # We have a config drive config, move on
            log.debug("%s configured via config-drive" % mac)
            continue
        files_to_write.update(_write_rh_dhcp(iname, mac, False))
    return files_to_write


def _exists_gentoo_interface(name):
    file_to_check = '/etc/conf.d/net.{name}'.format(name=name)
    return os.path.exists(file_to_check)


def _enable_gentoo_interface(name):
    log.debug('rc-update add {name} default'.format(name=name))
    subprocess.call(['rc-update', 'add',
                     'net.{name}'.format(name=name), 'default'])


def _write_gentoo_interface(name, interface, vlans):
    files_to_write = dict()
    results = "# Automatically generated, do not edit\n"
    if vlans:
        results += 'vlans_{name}="{vlans}"\n'.format(
            # get the base interface name
            name=name.split('_')[0],
            vlans=' '.join(str(vlan) for vlan in vlans))
    results += """config_{name}="{ip_address} netmask {netmask}"
mac_{name}="{hwaddr}\"\n""".format(
        name=name,
        ip_address=interface['ip_address'],
        netmask=interface['netmask'],
        hwaddr=interface['mac_address']
    )
    routes = list()
    for route in interface['routes']:
        if route['network'] == '0.0.0.0' and route['netmask'] == '0.0.0.0':
            # add default route if it exists
            routes.append('default via {gw}'.format(
                name=name,
                gw=route['gateway']
            ))
        else:
            # add remaining static routes
            routes.append('{net} netmask {mask} via {gw}'.format(
                net=route['network'],
                mask=route['netmask'],
                gw=route['gateway']
            ))
    if routes:
        routes_string = '\n'.join(route for route in routes)
        results += 'routes_{name}="{routes}"'.format(
            name=name,
            routes=routes_string
            # routes='\n'.join(str(route) for route in routes)
        )
        results += '\n'
    files_to_write['/etc/conf.d/net.{name}'.format(
        name=name.split('_')[0])] = results
    return files_to_write


def _setup_gentoo_network_init(name, vlans):
    for vlan in vlans:
        interface_name = 'net.{name}.{vlan}'.format(
            name=name.split('_')[0],
            vlan=vlan)
        log.debug('vlan {vlan} found, interface named {name}'.
                  format(vlan=vlan, name=interface_name))
        if not os.path.islink('/etc/init.d/{name}'.format(
                name=interface_name)):
            log.debug('ln -s /etc/init.d/net.lo /etc/init.d/{name}'.
                      format(name=interface_name))
            os.symlink('/etc/init.d/net.lo',
                       '/etc/init.d/{name}'.format(name=interface_name))
            _enable_gentoo_interface(interface_name)
    if not vlans:
        if not os.path.islink('/etc/init.d/net.{name}'.format(name=name)):
            log.debug('vlan not found, interface named {name}'.
                      format(name=name))
            log.debug('ln -s /etc/init.d/net.lo /etc/init.d/net.{name}'.
                      format(name=name))
            os.symlink('/etc/init.d/net.lo',
                       '/etc/init.d/net.{name}'.format(name=name))
            _enable_gentoo_interface(name)


def _write_gentoo_dhcp(name, hwaddr, vlans):
    filename = '/etc/conf.d/net.{name}'.format(name=name.split('_')[0])
    results = "# Automatically generated, do not edit\n"
    if vlans:
        results += 'vlans_{name}="{vlans}"\n'.format(
            # get the base interface name
            name=name.split('_')[0],
            vlans=' '.join(str(vlan) for vlan in vlans))
    results += """config_{name}="dhcp"
mac_{name}="{hwaddr}"
""".format(name=name, hwaddr=hwaddr)
    _enable_gentoo_interface(name)
    return {filename: results}


def write_gentoo_interfaces(interfaces, sys_interfaces):
    files_to_write = dict()
    # Sort the interfaces by id so that we'll have consistent output order
    for iname, interface in sorted(
            interfaces.items(), key=lambda x: x[1]['id']):
        if interface['type'] == 'ipv6':
            continue
        if iname not in sys_interfaces:
            continue
        interface_name = sys_interfaces[iname]
        vlans = list()
        if 'vlan_id' in interface:
            interface_name = "{0}_{1}".format(
                interface_name, interface['vlan_id'])
            vlans.append(interface['vlan_id'])
        if interface['type'] == 'ipv4':
            files_to_write.update(
                _write_gentoo_interface(interface_name, interface, vlans))
            _setup_gentoo_network_init(interface_name, vlans)
        if interface['type'] == 'ipv4_dhcp':
            files_to_write.update(
                _write_gentoo_dhcp(
                    interface_name, interface['mac_address'], vlans))
            _setup_gentoo_network_init(interface_name, vlans)
    for mac, iname in sorted(
            sys_interfaces.items(), key=lambda x: x[1]):
        if _exists_gentoo_interface(iname):
            # This interface already has a config file, move on
            log.debug("%s already has config file, skipping" % iname)
            continue
        if mac in interfaces:
            # We have a config drive config, move on
            log.debug("%s configured via config-drive" % mac)
            continue
        files_to_write.update(_write_gentoo_dhcp(iname, mac, []))
        _setup_gentoo_network_init(iname, [])
    return files_to_write


def systemd_enable(service, args):
    log.debug("Enabling %s via systemctl" % service)

    if args.noop:
        return

    rc = os.system('systemctl enable %s' % service)
    if rc != 0:
        log.error("Error enabling %s" % service)
        sys.exit(rc)


def _exists_debian_interface(name):
    file_to_check = '/etc/network/interfaces.d/{name}.cfg'.format(name=name)
    return os.path.exists(file_to_check)


def write_debian_interfaces(interfaces, sys_interfaces):
    eni_path = '/etc/network/interfaces'
    eni_d_path = eni_path + '.d'
    files_to_write = dict()
    files_to_write[eni_path] = "auto lo\niface lo inet loopback\n"
    files_to_write[eni_path] += "source /etc/network/interfaces.d/*.cfg\n"
    # Sort the interfaces by id so that we'll have consistent output order
    for iname, interface in sorted(
            interfaces.items(), key=lambda x: x[1]['id']):
        if iname not in sys_interfaces:
            continue
        interface = interfaces[iname]
        interface_name = sys_interfaces[iname]
        vlan_raw_device = None

        if 'vlan_id' in interface:
            vlan_raw_device = interface_name
            interface_name = "{0}.{1}".format(vlan_raw_device,
                                              interface['vlan_id'])

        if _exists_debian_interface(interface_name):
            continue

        iface_path = os.path.join(eni_d_path, '%s.cfg' % interface_name)

        if interface['type'] == 'ipv4_dhcp':
            result = "auto {0}\n".format(interface_name)
            result += "iface {0} inet dhcp\n".format(interface_name)
            if vlan_raw_device is not None:
                result += "    vlan-raw-device {0}\n".format(vlan_raw_device)
            files_to_write[iface_path] = result
            continue
        if interface['type'] == 'ipv6':
            link_type = "inet6"
        elif interface['type'] == 'ipv4':
            link_type = "inet"
        # We do not know this type of entry
        if not link_type:
            continue

        result = "auto {0}\n".format(interface_name)
        result += "iface {name} {link_type} static\n".format(
            name=interface_name, link_type=link_type)
        if vlan_raw_device:
            result += "    vlan-raw-device {0}\n".format(vlan_raw_device)
        result += "    address {0}\n".format(interface['ip_address'])
        result += "    netmask {0}\n".format(interface['netmask'])
        for route in interface['routes']:
            if route['network'] == '0.0.0.0' and route['netmask'] == '0.0.0.0':
                result += "    gateway {0}\n".format(route['gateway'])
            else:
                result += post_up.format(
                    net=route['network'], mask=route['netmask'],
                    gw=route['gateway'])
                result += pre_down.format(
                    net=route['network'], mask=route['netmask'],
                    gw=route['gateway'])
        files_to_write[iface_path] = result
    for mac, iname in sorted(
            sys_interfaces.items(), key=lambda x: x[1]):
        if _exists_debian_interface(iname):
            # This interface already has a config file, move on
            continue
        if mac in interfaces:
            # We have a config drive config, move on
            continue
        result = "auto {0}\n".format(iname)
        result += "iface {0} inet dhcp\n".format(iname)
        files_to_write[os.path.join(eni_d_path, "%s.cfg" % iname)] = result
    return files_to_write


def write_dns_info(dns_servers):
    results = ""
    for server in dns_servers:
        results += "nameserver {0}\n".format(server)
    return {'/etc/resolv.conf': results}


def get_config_drive_interfaces(net):
    interfaces = {}

    if 'networks' not in net or 'links' not in net:
        log.debug("No config-drive interfaces defined")
        return interfaces

    # tmp_ifaces is a dict keyed on net id
    tmp_ifaces = {}
    tmp_links = {}
    for network in net['networks']:
        tmp_ifaces[network['link']] = network
    for link in net['links']:
        tmp_links[link['id']] = link
    keys_to_del = []
    for link in tmp_links.values():
        if link['type'] == 'vlan':
            keys_to_del.append(link['vlan_link'])
            new_link = dict(tmp_links.get(link['vlan_link'], {}))
            new_link.update(link)
            link.update(new_link)
        link['mac_address'] = link.get(
            'ethernet_mac_address', link.get('vlan_mac_address'))
        for old_key in ('ethernet_mac_address', 'vlan_mac_address'):
            if old_key in link:
                del link[old_key]
    for key in keys_to_del:
        del tmp_links[key]
    for link in tmp_links.values():
        tmp_ifaces[link['id']]['mac_address'] = link['mac_address']
        if 'vlan_id' in link:
            tmp_ifaces[link['id']]['vlan_id'] = link['vlan_id']
    for k, v in tmp_ifaces.items():
        v['link'] = k
        interfaces[v['mac_address'].lower()] = v
    return interfaces


def get_dns_from_config_drive(net):
    if 'services' not in net:
        log.debug("No DNS info available from config-drive")
        return []
    return [
        f['address'] for f in net['services'] if f['type'] == 'dns'
    ]


def write_static_network_info(
        interfaces, sys_interfaces, files_to_write, args):

    if args.distro in ('debian', 'ubuntu'):
        files_to_write.update(
            write_debian_interfaces(interfaces, sys_interfaces))
    elif args.distro in ('redhat', 'centos', 'fedora', 'suse', 'opensuse'):
        files_to_write.update(
            write_redhat_interfaces(interfaces, sys_interfaces))

        # glean configures interfaces via
        # /etc/sysconfig/network-scripts, so we have to ensure that
        # the LSB init script /etc/init.d/network gets started!
        systemd_enable('network.service', args)
    elif args.distro in 'gentoo':
        files_to_write.update(
            write_gentoo_interfaces(interfaces, sys_interfaces)
        )
    else:
        return False

    finish_files(files_to_write, args)


def finish_files(files_to_write, args):
    files = sorted(files_to_write.keys())
    for k in files:
        log.debug("Writing output file : %s" % k)
        if not files_to_write[k]:
            # Don't write empty files
            log.debug(" ... is blank, skipped")
            continue
        if args.noop:
            sys.stdout.write("### Write {0}\n{1}".format(k, files_to_write[k]))
        else:
            with open(k, 'w') as outfile:
                outfile.write(files_to_write[k])
        log.debug(" ... done")


def is_interface_live(interface, sys_root):
    try:
        if open('{root}/{iface}/carrier'.format(
                root=sys_root, iface=interface)).read().strip() == '1':
            return True
    except IOError as e:
        # We get this error if the link is not up
        if e.errno != 22:
            raise
    return False


def interface_live(iface, sys_root, args):
    if is_interface_live(iface, sys_root):
        return True

    if args.noop:
        return False

    subprocess.check_call(['ip', 'link', 'set', 'dev', iface, 'up'])

    # Poll the interface since it may not come up instantly
    for x in range(0, 50):
        if is_interface_live(iface, sys_root):
            return True
        time.sleep(.1)
    return False


def is_interface_vlan(iface):
    file_name = '/etc/network/interfaces.d/%s.cfg' % iface
    if os.path.exists(file_name):
        return 'vlan-raw-device' in open(file_name).read()
    return False


def get_sys_interfaces(interface, args):
    log.debug("Probing system interfaces")
    sys_root = os.path.join(args.root, 'sys/class/net')

    ignored_interfaces = ('sit', 'tunl', 'bonding_master', 'teql',
                          'ip6_vti', 'ip6tnl', 'bond', 'lo')
    sys_interfaces = {}
    if interface is not None:
        log.debug("Only considering interface %s from arguments" % interface)
        interfaces = [interface]
    else:
        interfaces = [f for f in os.listdir(sys_root)
                      if not f.startswith(ignored_interfaces)]
    for iface in interfaces:
        # if interface is for an already configured vlan, skip it
        if is_interface_vlan(iface):
            log.debug("Skipping vlan %s" % iface)
            continue

        mac_addr_type = open(
            '%s/%s/addr_assign_type' % (sys_root, iface), 'r').read().strip()
        if mac_addr_type != '0':
            continue
        mac = open('%s/%s/address' % (sys_root, iface), 'r').read().strip()
        if interface_live(iface, sys_root, args):
            sys_interfaces[mac] = iface
            log.debug("Adding system interface %s (%s)" % (iface, mac))
    return sys_interfaces


def get_network_info(args):
    """Retrieves network info from config-drive.

    If there is no meta_data.json in config-drive, it means that there
    is no config drive mounted- which means we know nothing.
    """
    config_drive = os.path.join(args.root, 'mnt/config')
    network_info_file = '%s/openstack/latest/network_info.json' % config_drive
    vendor_data_file = '%s/openstack/latest/vendor_data.json' % config_drive

    network_info = {}
    if os.path.exists(network_info_file):
        log.debug("Found network_info file %s" % network_info_file)
        network_info = json.load(open(network_info_file))
    elif os.path.exists(vendor_data_file):
        log.debug("Found vendor_data_file file %s" % vendor_data_file)
        vendor_data = json.load(open(vendor_data_file))
        if 'network_info' in vendor_data:
            log.debug("Found network_info in vendor_data_file")
            network_info = vendor_data['network_info']
    else:
        log.debug("Did not find vendor_data or network_info in config-drive")

    if not network_info:
        log.debug("Found no network_info in config-drive!  "
                  "Asusming DHCP interfaces")

    return network_info


def write_network_info_from_config_drive(args):
    """Write network info from config-drive.

    If there is no meta_data.json in config-drive, it means that there
    is no config drive mounted- which means we know nothing.

    Returns False on any issue, which will cause the writing of
    DHCP network files.
    """

    network_info = get_network_info(args)

    dns = write_dns_info(get_dns_from_config_drive(network_info))
    interfaces = get_config_drive_interfaces(network_info)
    sys_interfaces = get_sys_interfaces(args.interface, args)

    write_static_network_info(interfaces, sys_interfaces, dns, args)


def write_ssh_keys(args):
    """Write ssh-keys from config-drive.

    If there is no meta_data.json in config-drive, it means that there
    is no config drive mounted- which means we do nothing.
    """

    config_drive = os.path.join(args.root, 'mnt/config')
    ssh_path = os.path.join(args.root, 'root/.ssh')
    meta_data_path = '%s/openstack/latest/meta_data.json' % config_drive
    if not os.path.exists(meta_data_path):
        return 0

    meta_data = json.load(open(meta_data_path))
    if 'public_keys' not in meta_data:
        return 0

    keys_to_write = []

    # if we have keys already there, we want to preserve them
    if os.path.exists('/root/.ssh/authorized_keys'):
        with open('/root/.ssh/authorized_keys', 'r') as fk:
            for line in fk:
                keys_to_write.append(line.strip())
    for (name, key) in meta_data['public_keys'].items():
        key_title = "# Injected key {name} by keypair extension".format(
            name=name)
        if key_title not in keys_to_write:
            keys_to_write.append(key_title)

        if key not in keys_to_write:
            keys_to_write.append(key)

    files_to_write = {
        '/root/.ssh/authorized_keys': '\n'.join(keys_to_write) + '\n',
    }
    try:
        os.mkdir(ssh_path, 0o700)
    except OSError as e:
        if e.errno != 17:  # not File Exists
            raise
    finish_files(files_to_write, args)


def set_hostname_from_config_drive(args):
    if args.noop:
        return

    config_drive = os.path.join(args.root, 'mnt/config')
    meta_data_path = '%s/openstack/latest/meta_data.json' % config_drive
    if not os.path.exists(meta_data_path):
        return

    meta_data = json.load(open(meta_data_path))
    if 'name' not in meta_data:
        return

    hostname = meta_data['name']
    log.debug("Got hostname from meta_data.json : %s" % hostname)
    # underscore is not a valid hostname, but it's easy to name your
    # host with that on the command-line.  be helpful...
    if '_' in hostname:
        hostname = hostname.replace('_', '-')
        log.debug("Fixed up hostname to %s" % hostname)

    ret = subprocess.call(['hostname', hostname])

    if ret != 0:
        raise RuntimeError('Error setting hostname')
    else:
        # gentoo's hostname file is in a different location
        if args.distro is 'gentoo':
            with open('/etc/conf.d/hostname', 'w') as fh:
                fh.write("hostname=\"{host}\"\n".format(host=hostname))
        else:
            with open('/etc/hostname', 'w') as fh:
                fh.write(hostname)
                fh.write('\n')

        # generate the lists of hosts and ips
        hosts_to_add = {'localhost': '127.0.0.1'}

        # get information on the network
        hostname_ip = '127.0.1.1'
        network_info = get_network_info(args)
        if network_info:
            interfaces = get_config_drive_interfaces(network_info)
            key = sorted(interfaces.keys())[0]
            interface = interfaces[key]

            if interface and 'ip_address' in interface:
                hostname_ip = interface['ip_address']

        # check short hostname and generate list for hosts
        hosts_to_add[hostname] = hostname_ip
        short_hostname = hostname.split('.')[0]
        if short_hostname != hostname:
            hosts_to_add[short_hostname] = hostname_ip

        for host in hosts_to_add:
            host_value = hosts_to_add[host]
            # See if we already have a hosts entry for hostname
            prog = re.compile('^%s .*%s\n' % (host_value, host))
            match = None
            if os.path.isfile('/etc/hosts'):
                with open('/etc/hosts') as fh:
                    match = prog.match(fh.read())

            # Write out a hosts entry for hostname
            if match is None:
                with open('/etc/hosts', 'a+') as fh:
                    fh.write(u'%s %s\n' % (host_value, host))


def main():
    parser = argparse.ArgumentParser(description="Static network config")
    parser.add_argument(
        '-n', '--noop', action='store_true', help='Do not write files')
    parser.add_argument(
        '--distro', dest='distro',
        default=platform.dist()[0].lower(),
        help='Override distro (detected "%s")' % platform.dist()[0].lower())
    parser.add_argument(
        '--root', dest='root', default='/',
        help='Mounted root for config drive info, defaults to /')
    parser.add_argument(
        '-i', '--interface', dest='interface',
        default=None, help="Interface to process")
    parser.add_argument(
        '--ssh', dest='ssh', action='store_true', help="Write ssh key")
    parser.add_argument(
        '--hostname', dest='hostname', action='store_true',
        help="Set the hostname if name is available in config drive.")
    parser.add_argument(
        '--skip-network', dest='skip', action='store_true',
        help="Do not write network info")
    parser.add_argument(
        '--debug', dest='debug', action='store_true',
        help="Enable debugging output")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    log.debug("Starting glean")
    log.debug("Detected distro : %s" % args.distro)

    with systemlock.Lock('/tmp/glean.lock'):
        if args.ssh:
            write_ssh_keys(args)
        if args.hostname:
            set_hostname_from_config_drive(args)
        if args.interface != 'lo' and not args.skip:
            write_network_info_from_config_drive(args)
    log.debug("Done!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
