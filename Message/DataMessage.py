#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Message import Message


class DataMessage(Message):
    def __init__(self, source_ip, dist_ip, data_size, time):
        self._init__(source_ip, dist_ip, None, data_size)
        self.type = 'Data'
        self.data_occur_time = time
        self.data_size = data_size
        self.data_occur_node = source_ip
