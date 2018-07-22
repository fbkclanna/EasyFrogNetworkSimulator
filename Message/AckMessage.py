#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Message import Message


# TODO: ACK message size
class L2AckMessage(Message):
    def __init__(self, source_ip, dist_ip, next_ip):
        self._init__(source_ip, dist_ip, next_ip, data_size=0)
        self.type = 'L2Ack'
