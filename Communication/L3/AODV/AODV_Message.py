#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ad hoc On-Demand Distance Vector

from Message.Message import Message
from Utils.RoutingUtil import *


# RREQ, RREP, RERR, RREP_ACK

class RREQ_Message(Message):
    '''
    RREQ: Route Request
    '''

    def __init__(self, source_ip, RREQ_source, RREQ_dist, RREQ_ID=0, hop_count=0):
        self._init__(source_ip, '255.255.255.255', data_size=24, hop_count=hop_count)
        self.RREQ_dist_ip = RREQ_dist
        self.RREQ_source_ip = RREQ_source
        self.type = 'RREQ'
        self.RREQ_ID = RREQ_ID
        self.destination_only_flag = False
        self.is_broadcast = True


class RREP_Message(Message):
    '''
    RREP: Route Reply
    '''

    def __init__(self, source_ip, dist_ip, RREP_source_ip, RREP_dist_ip, hop_count=0):
        self._init__(source_ip, dist_ip, data_size=0, hop_count=hop_count)
        self.RREP_source_ip = RREP_source_ip
        self.RREP_dist_ip = RREP_dist_ip
        self.type = 'RREP'
        self.RREP_ID = id


class RERR_Message(Message):
    '''
    RERR: Route Error
    '''

    def __init__(self, source_ip, dist_ip, data_size=20):
        self._init__(source_ip, dist_ip, hop_count=0)
        self.type = 'RERR'


class RREP_ACK_Message(Message):
    '''
    RREP_ACK: Route Reply Ack
    '''

    def __init__(self, source_ip, dist_ip, data_size=1.5):
        self._init__(source_ip, dist_ip, hop_count=0)
        self.type = 'RREP_ACK'
