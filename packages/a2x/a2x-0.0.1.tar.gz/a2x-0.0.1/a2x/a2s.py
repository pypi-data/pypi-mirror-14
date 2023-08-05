# -*- coding: utf-8 -*-

# Author: Konstantin Kruglov <kruglovk@gmail.com>
# License: Apache License Version 2.0

import socket
import select
import struct


class A2XRR:
    header = struct.pack('<l', -1)

    def request(self, request_type, host):
        """

        :param request_type:
        :type request_type: bytes
        :param host:
        :type host: tuple
        :return:
        """

        packet = b''.join([self.header, request_type, b'\x00'])
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.sendto(packet, host)
        return sock

    @staticmethod
    def response(sock, buff=1400, timeout=5):
        """

        :param sock:
        :type sock: socket
        :param buff:
        :type buff: int
        :param timeout:
        :type: timeout: int
        :return:
        """
        r = select.select([sock], [], [], timeout)
        try:
            data = r[0][0].recv(buff)
        except IndexError:
            return None

        if data:
            return data
        else:
            return None


class A2SInfo(A2XRR):
    readable_data = {}
    header_info = struct.pack('<B', 0x54)    # info
    payload = 'Source Engine Query'.encode(encoding='utf-8')
    request_type = b''.join([header_info, payload])
    fields = (
        ('header', '<l'),
        ('response_type', '<B'),
        ('protocol', '<B'),
        ('name', '<s'),
        ('map', '<s'),
        ('folder', '<s'),
        ('game', '<s'),
        ('id', '<h'),
        ('players', '<B'),
        ('max_players', '<B'),
        ('bots', '<B'),
        ('server_type', '<B'),
        ('environment', '<B'),
        ('visibility', '<B'),
        ('vac', '<B'),
        ('version', '<s')
    )       # EDF not support

    def get_info(self, host):
        sock = self.request(self.request_type, host)

        if sock is None:
            return False

        data = self.response(sock)

        if data is None:
            return False

        for field in self.fields:
            if field[1] == '<s':
                self.readable_data[field[0]] = data[:data.find(b'\x00')]
                self.readable_data[field[0]] = self.readable_data[field[0]].decode(
                    'utf-8', 'ignore')
                data = data[data.find(b'\x00') + 1:]
                continue

            self.readable_data[field[0]] = struct.unpack(
                field[1], data[:struct.calcsize(field[1])])[0]

            data = data[struct.calcsize(field[1]):]
        return True
