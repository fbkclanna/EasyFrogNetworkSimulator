#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.RoutingUtil import *
from Communication.L3.AODV.AODV_Message import *
# from Communication.L3.AODV.AODV_Methods import start_AODV_routing
# from Communication.L3.AODV.AODV_Methods import *
from Communication.L3 import AODV as A
from Communication.L2.L2SendMsg import L2EvtSendMsg
# from Message.DataMessage import *
from Event.Event import Event

debug = True


class L3EvtSendMsg(Event):
    def __init__(self, node, time, msg):
        self._init__(event_name='L3_start_send_data', node=node, func=self.exe, time=time, necessary_time=0)
        self.msg = msg

    def exe(self, context):
        if debug:
            print context['engine']['now_time'], '\texe\tL3Evt \t', self.event_name, '\tNode:', self.node.nodeid

        self.node.start_send_data()

        event_list = []

        if self.msg.dist_ip == '255.255.255.255' or (
                self.node.isRouteExist(context['engine']['now_time'], self.msg.dist_ip)[0] is True):
            if self.msg.dist_ip != '255.255.255.255':
                route_info = self.node.isRouteExist(context['engine']['now_time'], self.msg.dist_ip)
                if route_info[0] and route_info[1] is None:
                    # now routing
                    return []
                next_ip = route_info[1]
            soruce_ip = self.node.ip_address
            event_list.extend([L2EvtSendMsg(self.node, context['engine']['now_time'], self.msg)])
            # return [L2EvtSendMsg(self.node, context['engine']['now_time'], self.msg)]
        else:
            # start routing
            # start_AODV_routing(node, context, source_ip, dist_ip):
            source_ip = self.node.ip_address
            RREQ_source_ip = self.node.ip_address
            dist_ip = self.msg.dist_ip
            # return A.AODV_Methods.start_AODV_routing(self.node, context, source_ip, dist_ip)
            event_list.extend(A.AODV_Methods.start_AODV_routing(self.node, context, source_ip, dist_ip))
        '''
        if self.node.send_data_len <= 0:
            event_list.extend([Evt])
        '''
        return event_list
