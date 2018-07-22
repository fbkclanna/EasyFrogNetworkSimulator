#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Event.Event import Event
from Communication.L2.L2SendMsg import *
from Communication.L3.L3RcvMsg import *
from Message.AckMessage import *
import random

'''
Non sloted CSMA/CA
http://ecee.colorado.edu/~liue/teaching/comm_standards/2015S_zigbee/802.15.4-2011.pdf
p43, 
'''

debug = True

macMinBE = 3  # 0-3, default = 3
BE = 3
NB = 0

aMaxBE = 5  # 5

# bc = 0# backoff counter
aCWmin = 0  # given by the physical layer
aCWmax = 1023
MAXBACOFF = 6

macMaxCSMABackoffs = 4  # 0-5, default = 4

DIFS = 128 * 10 ** (-6)  # 128 micro second
backoff = random.randint(0, 2 ** BE)
sifs = 28 * 10 ** (-6)  # 28 micro second

symbol_period = 4 / 250.0
macAckWaitDuration = 0
aMaxFrameRetries = 3
aTurnaroundTime = 12  # [symbol periods]

noAckMode = False  # Default: False

'''
--------CSMA/CA algorithm-----------
1.Initialisation: If a device wishes to transmit a frame using CSMA-CA, it first initialises the local variables BE:=macMinBE for the backoff exponent and NB:=0 for the number of successive backoffs before the current transmission.

2.Backoff: Before a station attempts to send a frame, it waits for a random integer number between 0 and 2^BE-1 complete backoff periods of length aUnitBackoffPeriod. If slotted CSMA-CA is used, transmissions are synchronised with the beacon, and therefore the backoff starts at the beginning of the next backoff period; if unslotted CSMA-CA is used, the backoff starts immediately. The first backoff period of each superframe starts with the transmission of the beacon. If the backoff has not been completed at the end of the CAP, it resumes at the start of the next superframe.

3.Clear Channel Assessment: After completing its backoff, the station performs a clear channel assessment (CCA). If, after eight symbol periods, the channel is assessed to be busy, both BE and NB are incremented by one, up to a maximum of aMaxBE for BE and macMaxCSMABackoffs+1 for NB. If NB exceeds macMaxCSMABackoffs, the protocol terminates with a channel access failure; if not, the protocol returns to the backoff step. If the channel is assessed to be free, the data frame can be transmitted. In slotted CSMA-CA, two CCAs, each starting at the beginning of a backoff period, have to be performed.

4.Starting the transmission: In slotted CSMA-CA, a transmission can only start at a backoff period boundary and only if all steps (two CCAs, frame transmission, and acknowledgement) can be completed at least one interframe space (IFS) period before the end of the CAP.

5.Acknowledgement: If the originator has not requested an acknowledgement, the transmission is assumed to have been successful. If an acknowledgement has been requested, the sender needs aTurnaroundTime to switch from sending to receiving mode and vice versa. The recipient starts the transmission of the acknowledgement aTurnaroundTime after the reception of the last symbol of the data or MAC command frame if unslotted CSMA-CA is used; it starts at a backoff period boundary between aTurnaroundTime and aTurnaroundTime + aUnitBackoffPeriod after the reception of the last symbol of the data or MAC command frame if slotted CSMA-CA is used. If the originator receives an acknowledgement from the recipient within a time of macAckWaitDuration, the data transfer has been successful. If no acknowledge is received within that time, the frame will be retransmitted up to a maximum of aMaxFrameRetries times, after which the protocol terminates and a communications failure is issued. 

'''

'''
class SendEvent(Event):
    def __init__(self, node, time):
        self._init__(event_name = 'get_data', node = node, func = node.get_data, time = time, necessary_time = self.calc_necessary_time())

    def calc_necessary_time(self):
        return 0
'''

'''
CSMA state

CarrierSense
WaitDIFS
WaitBackoff
SendMsg
'''

'''
class L2EvtSendAck(Event):
    def __init__(self, node, context):
        self._init__(event_name = 'L2_start_send_ack', node = node, func = self.start, time = time, necessary_time = 0)

    def exe(self, context):
        self.node.start_send_data()
        return [L2EvtCarrierSense(self.node, context['engine']['now_time'])]
'''


class L2EvtCarrierSense(Event):
    def __init__(self, node, time, msg=None):
        self._init__(event_name='L2_carriersense', node=node, func=self.exe, time=time, necessary_time=0)

        self.msg = msg

        if debug:
            print time, '\tset\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

    def start(self, context):
        pass

    def exe(self, context):
        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid
        now_time = context['engine']['now_time']
        self.state = 'CarrierSense'
        if DIFS == 0:
            return [L2EvtWaitBackoff(self.node, now_time, self.msg)]
        else:
            if self.node.num_of_sensing_signal == 0:
                return [L2EvtWaitDIFS(self.node, now_time, self.msg)]
            else:
                # return [L2EvtCarrierSense(self.node, now_time, self.msg, self.isAck)]
                self.node.event_list.append(L2EvtCarrierSense(self.node, -1, self.msg))
                return []


class L2EvtWaitDIFS(Event):
    def __init__(self, node, time, msg=None):
        self._init__(event_name='L2_wait_difs', node=node, func=self.start, time=time, necessary_time=DIFS)
        self.CSMA_failed = False

        self.msg = msg
        if debug:
            print time, '\tset\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

    def start(self, context):
        if self.node.num_of_sensing_signal > 0:
            self.CSMA_failed = True
        self.time = self.time + self.necessary_time
        self.func = self.exe
        self.node.state = 'WaitDIFS'
        self.node.on_execution_list.append(self)

        if self.node.num_of_sensing_signal > 0:
            self.CSMA_failed = True

        if debug:
            print context['engine']['now_time'], '\tstart\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

        return [self]

    def exe(self, context):
        self.node.on_execution_list.remove(self)
        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

        if self.node.num_of_sensing_signal > 0:
            self.CSMA_failed = True

        now_time = context['engine']['now_time']
        if self.CSMA_failed:
            self.node.event_list.append(L2EvtCarrierSense(self.node, -1, self.msg))
            # return [L2EvtCarrierSense(self.node, now_time, self.msg)]
            return []
        else:
            return [L2EvtWaitBackoff(self.node, now_time, self.msg)]


class L2EvtWaitBackoff(Event):
    def __init__(self, node, time, msg=None):
        backoff = random.randint(0, 2 ** node.BE) * 10 ** (-6)
        self.CSMA_failed = False
        self._init__(event_name='L2_wait_backoff', node=node, func=self.start, time=time, necessary_time=backoff)
        self.msg = msg
        if debug:
            print time, '\tset\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

    def start(self, context):
        if self.node.num_of_sensing_signal > 0:
            self.node.CSMA_failed = True
        self.node.on_execution_list.append(self)

        self.time = self.time + self.necessary_time
        self.func = self.exe
        self.node.state = 'WaitBackoff'
        if debug:
            print context['engine']['now_time'], '\tstart\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid
        return [self]

    def exe(self, context):
        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid
        self.node.on_execution_list.remove(self)
        if self.node.num_of_sensing_signal > 0:
            self.node.CSMA_failed = True
        now_time = context['engine']['now_time']
        if self.CSMA_failed:
            self.node.NB += 1
            self.node.BE = min(self.node.BE + 1, macMinBE)
            if self.node.NB > macMaxCSMABackoffs:
                self.node.reset_CSMACA()
                self.node.event_list.append(L2EvtCarrierSense(self.node, -1, self.msg))
                # return [L2EvtCarrierSense(self.node, now_time, self.msg)]
                return []

            else:
                self.node.event_list.append(L2EvtCarrierSense(self.node, -1, self.msg))
                return []
                # return [L2EvtWaitBackoff(self.node, now_time, self.msg)]
        else:
            return [L2EvtSendMsg(self.node, now_time, self.msg)]


class L2EvtSendMsg(Event):
    def __init__(self, node, time, msg=None):
        data_len = self.get_send_data_len(node)
        necessary_time = self.get_L1_delay() + self.get_sending_time(data_len, node.sn_settings['Communication'][
            'stream_data_rate'])
        self._init__(event_name='L2_send_msg', node=node, func=self.start, time=time, necessary_time=necessary_time)
        self.msg = msg
        if debug:
            print time, '\tset\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

    def start(self, context):
        self.time = self.time + self.necessary_time
        self.func = self.exe
        self.node.state = 'Sending'
        self.node.last_send_msg = self.msg
        self.node.last_send_msg_time = context['engine']['now_time']

        for neighbor in self.node.neighbor_list:
            neighbor.num_of_sensing_signal += 1
            neighbor.event_list.append(
                L2EvtRecvMsg(neighbor, context['engine']['now_time'], self.necessary_time, self.msg))

            if neighbor.state in ['CarrierSense', 'WaitDIFS', 'WaitBackoff']:
                for each in neighbor.on_execution_list:
                    each.CSMA_failed = True

            neighbor.start_L2_recieving_msg(self.msg)

        if debug:
            print context['engine']['now_time'], '\tstart\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid
        return [self]

    def get_send_data_len(self, node):
        if node.send_data_len > node.sn_settings['Communication']['MTU']:
            return node.sn_settings['Communication']['MTU']
        else:
            return node.send_data_len

    def get_L1_delay(self):
        return random.randint(0, 10) * (10 ** (-6))

    ## data_len[byte], rate[kbps]
    def get_sending_time(self, data_len, rate):
        return float(data_len) / float(rate * 1000)

    def finish_sending(self):
        self.node.state = 'Active'
        self.node.reset_CSMACA()
        self.node.data_amount -= self.node.send_data_len

    def finish_recieved(self, recieving_node, msg, event_list, now_time):

        if recieving_node.finish_L2_recieving_msg(msg):
            # if recieving_node.state == 'WaitL2Ack' and msg.type == 'L2Ack':
            event_list.append(L3EvtRecvMsg(recieving_node, now_time, msg))

            if recieving_node.ip_address == msg.next_ip and msg.type != 'L2Ack':
                l2_ack = L2AckMessage(recieving_node.ip_address, self.node.ip_address, 0)
                event_list.append(L2EvtSendMsg(recieving_node, now_time, l2_ack))
                if debug:
                    print 'Node:', self.node.nodeid, 'starts send ack to Node', msg.source_ip

    def exe(self, context):
        event_list = []
        for neighbor in self.node.neighbor_list:
            neighbor.num_of_sensing_signal -= 1
            self.finish_recieved(neighbor, self.msg, event_list, context['engine']['now_time'])

            if neighbor.num_of_sensing_signal == 0:
                for each_event in neighbor.event_list:
                    if each_event.event_name == 'L2_carriersense':
                        each_event.time = context['engine']['now_time']
                        neighbor.event_list.remove(each_event)
                        event_list.append(each_event)

        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

        if noAckMode or self.msg.is_broadcast:
            if debug:
                print context['engine'][
                    'now_time'], '\ta packet sended\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid, '\tremaining data:', self.node.send_data_len, '\tsended:', \
                self.node.sn_settings['Communication']['MTU']
            # if self.node.send_data_len > self.node.sn_settings['Communication']['MTU']:
            if self.msg.type == 'Data' and self.node.send_data_len > self.msg.data_size:
                data_size = self.msg.data_size
                # data_size = self.node.sn_settings['Communication']['MTU']
                self.node.send_data_len -= data_size
                self.node.data_amount -= data_size
                ##TODO
                msg = None
                event_list.append(L2EvtCarrierSense(self.node, context['engine']['now_time'], self.msg))
                return event_list
            else:
                self.finish_sending()
                if debug:
                    print 'send_complete'
                return event_list
        else:
            self.node.state = 'WaitL2Ack'

            return event_list


class L2EvtRecvMsg(Event):
    def __init__(self, node, time, necessary_time, msg=None):
        self._init__(event_name='L2_recv_msg', node=node, func=self.start, time=time, necessary_time=necessary_time)
        self.recv_failed = False
        self.msg = msg
        if debug:
            print time, '\tset\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

    def start(self, context):
        self.time = self.time + self.necessary_time
        self.func = self.exe
        if self.state != 'Sending':
            self.state = 'Recving'

        if self.node.state in ['Sleep', 'Sending'] or self.node.num_of_sensing_signal > 2:
            self.recv_failed = True

        if debug:
            print context['engine']['now_time'], '\tstart\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid
        return [self]

    def exe(self, context):
        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid

        event_list = []
        if self.node.state in ['Sleep', 'Sending'] or self.node.num_of_sensing_signal > 2:
            self.recv_failed = True

        if not self.recv_failed:
            # if recieving_node.state == 'WaitL2Ack' and msg.type == 'L2Ack':
            event_list.append(L3EvtRecvMsg(recieving_node, now_time, msg))

            if recieving_node.ip_address == msg.next_ip and msg.type != 'L2Ack':
                l2_ack = L2AckMessage(recieving_node.ip_address, self.node.ip_address, 0)
                event_list.append(L2EvtSendMsg(recieving_node, now_time, l2_ack))
                if debug:
                    print 'Node:', self.node.nodeid, 'starts send ack to Node', msg.source_ip

            if not noAckMode:
                ##send ack
                source_ip = self.node.ip_address
                dist_ip = self.msg.source_ip
                msg = L2AckMessage(source_ip, dist_ip)


class L2EvtSendFinish(Event):
    pass


class L2EvtWaitL2Ack(Event):
    def __init__(self, node, time):
        self._init__(event_name='L2_wait_ack', node=node, func=self.exe, time=time, necessary_time=0)
        self.msg = node.last_send_msg

    def exe(self, context):
        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid
        return [L2EvtCarrierSense(self.node, context['engine']['now_time'], self.msg)]
