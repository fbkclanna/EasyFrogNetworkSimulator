#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Communication.L3.AODV.AODV_Message import *
from Communication.L3.L3SendMsg import *
from Communication.L2.L2SendMsg import *

import random

# Ad hoc On-Demand Distance Vector

debug = True

'''
class L3EvtRecvRREQ(Event):
    def __init__(self, node, time):
        self._init__(event_name = 'L3_recv_RREQ', node = node, func = self.exe, time = time, necessary_time = 0)
'''


def start_AODV_routing(node, context, source_ip, dist_ip):
    from Event.SensorNodeEvent import *
    source_ip = node.ip_address
    RREQ_source = source_ip
    RREQ_dist_ip = dist_ip

    node.add_route(dist_ip, next_ip=None, hop=0)
    RREQ_ID = random.randint(0, 2 ** 32)
    node.add_RREQID(RREQ_ID)
    RREQ_msg = RREQ_Message(source_ip, RREQ_source, RREQ_dist_ip, RREQ_ID)
    node.send_msg_list.insert(0, RREQ_msg)
    # return [L2EvtSendMsg(node, context['engine']['now_time'], RREQ_msg)]

    return [EvtSendMsg(node, context['engine']['now_time'], RREQ_msg)]


def recv_RREQ(context, node, RREQ_message):
    from Event.SensorNodeEvent import *
    # RREQ_IDの登録

    if not node.isExistRREQID(RREQ_message.RREQ_ID):
        node.add_RREQID(RREQ_message.RREQ_ID)
    else:
        # すでに受信したRREQ IDであれば破棄
        return []
        pass

    # ルーティングテーブルへの登録
    route_info = node.isRouteExist(context['engine']['now_time'], RREQ_message.RREQ_source_ip)
    if route_info[0] is False:
        node.add_route(RREQ_message.RREQ_source_ip, RREQ_message.source_ip, hop=RREQ_message.hop_count + 1, enable=True,
                       last_time=context['engine']['now_time'])

    msg = None
    # 自分がdistの時
    if RREQ_message.RREQ_dist_ip == node.ip_address:
        msg = RREP_Message(node.ip_address, RREQ_message.RREQ_source_ip, node.ip_address, RREQ_message.RREQ_source_ip,
                           hop_count=0)

    else:
        # もし自分がRREQ_distへのルーティング情報を保持していたら
        if (route_info[0] and route_info[1] is not None):
            msg = RREP_Message(node.ip_address, RREQ_message.RREQ_source_ip, RREQ_message.RREQ_dist_ip,
                               RREQ_message.RREQ_source_ip, hop_count=route_info[2] + 1)
        # not has the info of RREQ_dist
        # RREQメッセージの転送
        else:
            msg = RREQ_Message(node.ip_address, RREQ_message.RREQ_source_ip, RREQ_message.dist_ip, RREQ_message.RREQ_ID,
                               hop_count=RREQ_message.hop_count + 1)

    # return [L3EvtSendMsg(node, context['engine']['now_time'], msg)]
    return [EvtSendMsg(node, context['engine']['now_time'], msg)]


def recv_RREP(context, node, RREP_message):
    from Event.SensorNodeEvent import *
    # add_route(self, dist_ip, next_ip, hop):

    event_list = []

    node.add_route(RREP_message.RREP_source_ip, RREP_message.source_ip, hop=RREP_message.hop_count + 1, enable=True,
                   last_time=context['engine']['now_time'])
    if len(node.send_msg_list) > 0:
        if node.isRouteExist(context['engine']['now_time'], node.send_msg_list[0].dist_ip):
            msg = node.send_msg_list.pop(0)
            # event_list.append(L3EvtSendMsg(node, context['engine']['now_time'], msg))
            event_list.append(EvtSendMsg(node, context['engine']['now_time'], msg))

    if RREP_message.RREP_dist_ip != node.ip_address:
        # 転送
        # RREP_Message(source_ip, dist_ip, RREP_source_ip, RREP_dist_ip)
        msg = RREP_Message(node.ip_address, RREQ_message.source_ip, RREP_message.RREP_source_ip,
                           RREP_message.RREP_dist_ip, hop_count=RREP_message.hop_count + 1)
        # event_list.append(L3EvtSendMsg(node, context['engine']['now_time'], msg))
        event_list.append(EvtSendMsg(node, context['engine']['now_time'], msg))
    else:
        pass
    return event_list
