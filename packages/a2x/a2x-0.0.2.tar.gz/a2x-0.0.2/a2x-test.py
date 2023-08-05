#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Konstantin Kruglov <kruglovk@gmail.com>
# License: Apache License Version 2.0

import a2x.a2s
import argparse
from a2x import __version__


def cl():
    parse = argparse.ArgumentParser()

    group_host = parse.add_argument_group('Remote host')
    group_host.add_argument(
        '--host', help='remote host (default: localhost)', metavar='ip',
        type=str, default='localhost',
    )
    group_host.add_argument(
        '--port', help='remote port (default: 27015)', metavar='port', type=int,
        default=27015,
    )

    group_type = parse.add_argument_group('Request type')
    group_type.add_argument(
        '--info', help='Request A2S Info of server', action='store_true',
        default=False
    )

    group_other = parse.add_argument_group('Other')
    group_other.add_argument(
        '--version', action='version', version='%(prog)s -- v{version}'.format(
            version=__version__)
    )

    parse_keys = parse.parse_args()
    return parse, parse_keys


def main():
    parse, keys = cl()
    host = (keys.host, keys.port)

    if keys.info:
        info = a2x.a2s.A2SInfo()
        if info.get_info(host):
            print(info.readable_data)
        else:
            print('Data not received')
        exit()

    parse.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
