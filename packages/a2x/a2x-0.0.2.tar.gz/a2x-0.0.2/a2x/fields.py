# -*- coding: utf-8 -*-

# Author: Konstantin Kruglov <kruglovk@gmail.com>
# License: Apache License Version 2.0

import struct


class Field:
    fmt = None

    def __init__(self, value):
        self.value = value

    def encode(self):
        return struct.pack(self.fmt, self.value)

    def decode(self):
        pass


class StringField(Field):
    fmt = '<s'

    def encode(self):
        return self.value.encode(encoding='utf-8')

    def decode(self):
        pass


class ByteField(Field):
    fmt = '<B'


class ShortFiled(Field):
    fmt = '<h'


class LongField(Field):
    fmt = '<l'


class Header:
    fields = {
        LongField(-1)
    }


class A2SInfo:
    fields = (
        ByteField(0x54),
        StringField('Source Engine Query')
    )

    def request(self):
        pass
