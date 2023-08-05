#!/usr/bin/env python

import argparse
import ipaddress
import os
import sys
import socket

from . import __version__

COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}


if sys.version_info < (3, 0):
    _bytes_type = str
else:
    _bytes_type = bytes


def main():
    parser = argparse.ArgumentParser(prog='pypcalc')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s v{0}'.format(__version__))
    mu = parser.add_mutually_exclusive_group(required=False)
    mu.add_argument('-a', '--show-all', action='store_true', help='Print a comprehensive overview (default')
    mu.add_argument('-n', '--show-network', action='store_true', help='Print network address')
    mu.add_argument('-m', '--show-netmask', action='store_true', help='Print netmask address')
    mu.add_argument('-p', '--show-prefix', action='store_true', help='Print prefix length')
    mu.add_argument('-b', '--show-broadcast', action='store_true', help='Print broadcast address')
    parser.add_argument('-H', '--show-false-flags', action='store_true', help='Show flags whose value is false')
    parser.add_argument('--color', choices=('never', 'auto', 'always'), default='auto',
                        help='When to colorize (default is "auto", which means to colorize if stdout is a TTY)')
    parser.add_argument('address', nargs='+', help='IP Address or Network')
    args = parser.parse_args()

    def colorize(string, color, bold=False):
        if args.color == 'never':
            return string
        if args.color == 'always' or os.isatty(sys.stdout.fileno()):
            return "\033[{0};{1}m{2}\033[0m".format(
                '1' if bold else '0',
                COLORS[color],
                string
            )

    addresses = []

    for address in args.address:
        if isinstance(address, _bytes_type):
            address = address.decode('ascii')
        try:
            if '/' in address:
                addr = ipaddress.ip_network(address, strict=False)
            else:
                addr = ipaddress.ip_address(address)
            addresses.append((addr, address))
        except ValueError:
            if ':' in address:
                raise
            else:
                try:
                    these_addresses = set()
                    for res in sorted(
                        socket.getaddrinfo(address, None, 0, 0, 0, socket.AI_ADDRCONFIG),
                        key=lambda f: f[4][0]
                    ):
                        numeric = res[4][0]
                        if isinstance(numeric, _bytes_type):
                            numeric = numeric.decode('ascii')
                        if numeric in these_addresses:
                            continue
                        these_addresses.add(numeric)
                        addr = ipaddress.ip_address(numeric)
                        addresses.append((addr, numeric))
                except Exception:
                    raise

    for i, (addr, address) in enumerate(addresses):

        if hasattr(addr, 'network_address'):
            base_addr = addr.network_address
            base_addr_full = addr.network_address.exploded
            hostmask = addr.hostmask
            prefixlen = addr.prefixlen
            hosts_per = 1 << (addr.max_prefixlen - prefixlen)
        else:
            base_addr = addr.compressed
            base_addr_full = addr.exploded
            if isinstance(addr, ipaddress.IPv4Address):
                hostmask = '255.255.255.255'
            elif isinstance(addr, ipaddress.IPv6Address):
                hostmask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
            prefixlen = addr.max_prefixlen
            hosts_per = 1

        if args.show_network:
            print('NETWORK={0}'.format(base_addr))
        elif args.show_netmask:
            print('NETMASK={0}'.format(hostmask))
        elif args.show_prefix:
            print('PREFIXLEN={0}'.format(prefixlen))
        elif args.show_broadcast:
            if hasattr(addr, 'broadcast_address'):
                print('BROADCAST={0}'.format(addr.broadcast_address))
            else:
                raise ValueError('{0} has no broadcast address'.format(addr))
        else:
            rows = []
            rows.append(('Input', address))
            rows.append(('Base Address', base_addr, 'yellow', True))
            rows.append(('Base Address (full)', base_addr_full, 'yellow'))
            rows.append(('Netmask', '{0} = {1}'.format(hostmask, prefixlen), 'red'))
            rows.append(('Hosts/Net', hosts_per, 'green'))
            if hosts_per > 1:
                rows.append(('Broadcast', addr.broadcast_address.exploded, 'green'))
                rows.append(('HostMin', addr.network_address + 1, 'green'))
                rows.append(('HostMin (full)', (addr.network_address + 1).exploded, 'green'))
                rows.append(('HostMax', addr.broadcast_address - 1, 'green'))
                rows.append(('HostMax (full)', (addr.broadcast_address - 1).exploded, 'green'))
            for prop in sorted(('is_link_local', 'is_multicast', 'is_private', 'is_global',
                                'is_loopback', 'is_reserved')):
                if hasattr(addr, prop):
                    prop_name = ''.join(x.capitalize() for x in prop.split('_')[1:])
                    if getattr(addr, prop):
                        rows.append(('Is' + prop_name, True, 'magenta', True))
                    elif args.show_false_flags:
                        rows.append(('IsNot' + prop_name, True, 'magenta'))
            if getattr(addr, 'ipv4_mapped', None) is not None:
                rows.append(('IPv4 Mapped Address', addr.ipv4_mapped, 'cyan'))
            if getattr(addr, 'sixtofour', None) is not None:
                rows.append(('SixToFour Mapped Address', addr.sixtofour, 'cyan'))
            if getattr(addr, 'teredo', None) is not None:
                rows.append(('Teredo Pair', '{0} <-> {1}'.format(*addr.teredo), 'cyan'))
            max_column_width = max(len(r[0]) for r in rows)

            for row in rows:
                if isinstance(row[1], bool):
                    output = colorize(row[0], *row[2:])
                else:
                    output = (row[0] + ': ').ljust(max_column_width + 2)
                    if len(row) > 2:
                        output += colorize(row[1], *row[2:])
                    else:
                        output += str(row[1])
                print(output)

        if len(addresses) > i + 1:
            print('\n')


if __name__ == '__main__':
    sys.exit(main())
