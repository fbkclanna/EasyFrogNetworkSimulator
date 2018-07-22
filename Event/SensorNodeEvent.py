#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Event import Event
# from Communication.L2.CSMACA import *
# from Communication.L3.L3SendMsg import *
from Message.DataMessage import DataMessage as DataMsg
from Communication.L3.AODV.AODV_Methods import *
import random

debug = True


class EvtSendMsg(Event):
    def __init__(self, node, time, msg=None):
        self._init__(event_name='start_send_data', node=node, func=self.start, time=time,
                     necessary_time=self.calc_necessary_time())
        self.msg = msg
        self.resend = False

    def calc_necessary_time(self):
        return -1

    def start(self, context):
        if self.node.isFSCStateActive and not self.node.isSending:
            if self.msg is None:
                self.msg = self.node.send_msg_list[0]

            self.node.isSending = True
            self.func = self.exe
            self.node.last_send_msg_time = context['engine']['now_time']

            if debug:
                print context['engine']['now_time'], '\texe\tL3Evt \t', self.event_name, '\tNode:', self.node.nodeid

            event_list = []

            if self.msg.dist_ip == '255.255.255.255' or (
                    self.node.isRouteExist(context['engine']['now_time'], self.msg.dist_ip)[0] is True):

                necessary_time = ((float(self.msg.size) / self.node.sn_settings['Communication']['stream_data_rate']))
                assert necessary_time >= 0
                self.time = self.time + necessary_time

                if self.msg.dist_ip != '255.255.255.255':
                    route_info = self.node.isRouteExist(context['engine']['now_time'], self.msg.dist_ip)
                    if route_info[0] and route_info[1] is None:
                        # now routing
                        return []
                    self.msg.next_ip = route_info[1]
                self.msg.soruce_ip = self.node.ip_address
                for neighbor in self.node.neighbor_list:
                    if neighbor.isActive or neighbor.attribute == 'SinkNode':
                        neighbor.last_recv_msg_time = context['engine']['now_time']
                        event_list.extend(
                            [EvtRecvMsg(neighbor, context['engine']['now_time'] + necessary_time, self.msg)])
                    elif neighbor.ip_address == self.msg.next_ip:
                        self.resend = True
                event_list.append(self)
                return event_list
            else:
                # start routing
                source_ip = self.node.ip_address
                RREQ_source_ip = self.node.ip_address
                dist_ip = self.msg.dist_ip
                event_list.extend(start_AODV_routing(self.node, context, source_ip, dist_ip))
                return event_list
        else:
            return []

    def exe(self, context):
        if not self.node.isFSCStateActive:
            raise Exception
        self.node.isSending = False
        event_list = []
        self.node.tiredness += 3
        self.node.energy -= self.node.sn_settings['Energy']['enegy_send_msg']
        if self.msg.type == 'Data':
            if self.msg in self.node.send_msg_list:
                pass
            else:
                # assert self.msg in self.node.send_msg_list
                pass
            if self.resend:
                event_list.extend([EvtSendMsg(self.node, context['engine']['now_time'] + 1, self.msg)])
            else:
                if self.msg in self.node.send_msg_list:
                    self.node.send_msg_list.remove(self.msg)

                self.node.send_data_len -= self.msg.data_size
                if self.msg.data_occur_node == self.node.ip_address:
                    self.node.data_amount -= self.msg.data_size

        if len(self.node.send_msg_list) > 0:
            event_list.extend([EvtSendMsg(self.node, context['engine']['now_time'], self.node.send_msg_list[0])])

        return event_list


class EvtRecvMsg(Event):
    def __init__(self, node, time, msg):
        self._init__(event_name='recv_data', node=node, func=self.exe, time=time, necessary_time=0)
        assert msg is not None
        self.msg = msg

    def calc_necessary_time(self):
        return -1

    def exe(self, context):
        self.node.last_recv_msg_time = context['engine']['now_time']
        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

        event_list = []
        msg = self.msg

        # 自分で処理するメッセージ
        if msg.dist_ip == self.node.ip_address or msg.dist_ip == '255.255.255.255':
            if msg.type == 'Data':
                if self.node.attribute == 'SinkNode' or self.node.ip_address == '192.168.0.200':
                    self.node.add_data(context, msg)

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
        elif ((
                      msg.dist_ip != self.node.ip_address and msg.next_ip == self.node.ip_address) or msg.dist_ip == '255.255.255.255') and msg.TTL > 0:
            # 再転送
            if msg.dist_ip != '255.255.255.255':
                # 次ホップの決定
                routing_info = self.node.isRouteExist(context['engine']['now_time'], msg.dist_ip)
                if routing_info[0] is True and routing_info[1] is not None:
                    msg.next_ip = routing_info[1]

            msg.source_ip = self.node.ip_address
            msg.TTL -= 1
            msg.hop_count += 1
            self.node.send_msg_list.append(msg)
            self.node.send_data_len += msg.data_size
            event_list.append(EvtSendMsg(self.node, context['engine']['now_time'], msg))

        return event_list


# n秒間起きてその後スリープするか判断
class EvtWakeUp(Event):
    def __init__(self, node, time):
        self._init__(event_name='wake_up', node=node, func=self.start, time=time, necessary_time=0)

    def start(self, context):
        event_list = [self]
        self.node.wake_up()
        self.time = self.time + self.node.sn_settings['Energy']['wake_up_duration']
        self.func = self.exe
        event_list.extend(self.node.fsc_update(context['engine']['now_time'])[1])
        return event_list

    def exe(self, context):
        event_list = []
        if not self.node.isActiveNeighbor:
            self.node.wake_up()
        ret = self.node.fsc_update(context['engine']['now_time'])

        if not self.node.isFSCStateActive:
            self.node.sleep()
            event_list.append(
                EvtWakeUp(self.node, context['engine']['now_time'] + self.node.sn_settings['Energy']['sleep_duration']))
        else:
            # EvtFSCUpdate(self.node, context['engine']['now_time'])
            pass
        return event_list


class EvtDataOccur(Event):
    def __init__(self, coordinate, radius, time):
        self._init__(event_name='data_occur', node=None, func=self.exe, time=time, necessary_time=0)
        self.coordinate = coordinate
        self.radius = radius

    def exe(self, context):
        data_size = 100
        now_time = context['engine']['now_time']
        tmp_evt_list = []
        for node in context['sensornode_list']:
            if (node.pos[0] - self.coordinate[0]) ** 2 + (node.pos[1] - self.coordinate[1]) ** 2 <= self.radius ** 2:
                node.data_amount += data_size
                node.send_data_len += data_size
                node.energy -= node.sn_settings['Energy']['energy_get_data']
                # tmp_evt_list.extend(node.fsc_update(context['engine']['now_time'])[1])

                msg = DataMsg(node.ip_address, '192.168.0.200', data_size, now_time)
                node.send_msg_list.append(msg)
                if node.isFSCStateActive and not node.isSending:
                    tmp_evt_list.append(EvtSendMsg(node, now_time, msg))
                    pass

                node.send_request = True

        time_delta = 100
        tmp_evt_list.append(EvtDataOccur(self.coordinate, self.radius, self.time + time_delta))
        return tmp_evt_list


class EvtFSCUpdate(Event):
    def __init__(self, node, time):
        self._init__(event_name='fsc_update', node=node, func=self.exe, time=time, necessary_time=0)

    def exe(self, context):
        event_list = []
        ret = self.node.fsc_update(context['engine']['now_time'])
        if len(self.node.send_msg_list) > 0 and ret[0] is True:
            event_list.append(EvtSendMsg(self.node, context['engine']['now_time'], self.node.send_msg_list[0]))
            pass
        else:
            event_list.extend(ret[1])

        event_list.append(EvtFSCUpdate(self.node, context['engine']['now_time'] + 5))

        # return [EvtWakeUp(self.node, context['engine']['now_time'] + 10)]
        return event_list
