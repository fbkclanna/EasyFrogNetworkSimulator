#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.RoutingUtil import *
from Communication.L3.AODV import *
from Communication.L3.AODV.AODV_Methods import *
from Communication.L3.L3SendMsg import *
from Message.DataMessage import *

from Event.Event import Event

debug = True


class L3EvtRecvMsg(Event):
    def __init__(self, node, time, msg):
        self._init__(event_name='L3_start_send_data', node=node, func=self.exe, time=time, necessary_time=0)
        self.msg = msg

    def exe(self, context):
        self.node.last_recv_msg_time = self.time

        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

        msg = self.msg
        event_list = []
        msg.TTL -= 1

        # 自分で処理するメッセージ
        if msg.dist_ip == self.node.ip_address or msg.dist_ip == '255.255.255.255':
            if msg.type == 'Data':
                return []
            elif msg.type in ['RREQ', 'RREP', 'RERR', 'RREP_ACK']:
                if msg.type == 'RREQ':
                    if self.node.isExistRREQID(msg.RREQ_ID) or msg.RREQ_dist_ip == self.node.ip_address:
                        msg.TTL = 0
                    event_list.extend(recv_RREQ(context, self.node, msg))

                elif msg.type == 'RREP':
                    event_list.extend(recv_RREP(context, self.node, msg))
                    pass
                elif msg.type == 'RERR':
                    pass
                elif msg.type == 'RREP_ACK':
                    pass

        # 再転送すべきか
        elif (msg.dist_ip != self.node.ip_address or msg.dist_ip == '255.255.255.255') and msg.TTL > 0:
            # 再転送
            if msg.dist_ip != '255.255.255.255':
                # 次ホップの決定
                routing_info = self.node.isRouteExist(context['engine']['now_time'], msg.dist_ip)
                if routing_info[0] is True and routing_info[1] is not None:
                    msg.next_ip = routing_info[1]

            msg.source_ip = self.node.ip_address
            msg.TTL -= 1
            msg.hop_count += 1

            event_list.append(L3EvtSendMsg(self.node, context['engine']['now_time'], msg))
        if len(event_list) == 0:
            pass

        return event_list
