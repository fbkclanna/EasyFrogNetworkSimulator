#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Settings.CommunicationSettings import *

header_size = 10


class Message:
    def __init__(self):
        pass

    def _init__(self, source_ip, dist_ip, next_ip=None, data_size=None, hop_count=0):
        self.dist_ip = dist_ip
        self.source_ip = source_ip
        self.next_ip = next_ip

        self.dist_mac = None
        self.source_mac = None

        self.type = ''

        self.hop_count = hop_count
        self.TTL = 32

        self.is_broadcast = False

        self.data_size = data_size  # [byte]
        self.size = header_size + data_size  # [byte]
