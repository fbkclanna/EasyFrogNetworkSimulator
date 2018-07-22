#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Nodes.Node import Node
from Event.SensorNodeEvent import *
from Utils.Utils import *
from GUI.GUI_Utils import *
from Message.DataMessage import DataMessage
from FrogSleepControl.FrogSleepControl import FSC
from Event import SensorNodeEvent as SNE
import copy
import wx

'''
max_enegy: 
communication_range: [m]
data_occurence_size: 
data_occurence_interval: 

送信
data_amount threshold:
transmission_rate: 

消費電力
energy_carrier_sense: [w/s]
enegy_send_msg: [w/times]

'''

'''
color
blue : active
gray : sleep
'''


##SensorNode Event -> Event.SensorNodeEvent

class SensorNode(Node):

    # pos: position of sensor node
    # energy: 
    # max_enegy:
    # operation_time: 
    # data_amount: 
    # time:

    def __init__(self, pos, id, sn_settings, fsc_settings=None, debug=False):
        if id > 200:
            raise Exception
        ip_address = '192.168.0.' + str(id + 1)
        mac_address = '00:00:00:00:00:' + str(id + 1)

        self._init(pos, id, 'SensorNode', ip_address=ip_address, mac_address='', debug=debug)

        self.max_energy = sn_settings['Energy']['max_energy']

        self.color = 'blue'
        self.plotsize = 6

        ##
        self.sn_settings = copy.deepcopy(sn_settings)

        ##output
        self.data_history = []

        if fsc_settings is not None:
            self.fsc = FSC(self, self.max_energy, fsc_settings)
        else:
            self.fsc = None

        self.reset()

    def refresh_energys(self, now_time):
        if self.isFSCStateActive:
            self.energy -= self.sn_settings['Energy']['energy_consumption_active'] * (now_time - self.last_time)
            '''
            self.tiredness += 1 * (now_time - self.last_time)   
            if self.tiredness > 50:
                self.tiredness = 100
            '''
        else:
            '''
            self.tiredness -= 0.5 * (now_time - self.last_time)
            if self.tiredness < 0:
                self.tiredness = 0
            '''
            pass
        tiredness_thresh = 200
        tiredness = tiredness_thresh - self.send_data_len
        if tiredness < 0:
            tiredness = 0
        elif tiredness > tiredness_thresh:
            tiredness = tiredness_thresh
        self.tiredness = (tiredness / tiredness_thresh) * 50
        self.last_time = now_time

    def reset(self):
        self.energy = self.max_energy
        self.isActive = False
        self.data_amount = 0.0
        self.tiredness = 0.0

        if self.fsc is not None:
            # self.fsc.reset()
            self.isFSCStateActive = False

        self._reset()

    def reset_output(self):
        del data_history[:]

    # override
    def get_color(self):
        if self.isFSCStateActive:
            return 'green'
        else:
            return 'gray'

    def fsc_update(self, now_time):
        event_list = []
        if self.isSending:
            return True, event_list
        else:
            # time = max(self.last_recv_msg_time , self.last_send_msg_time)

            tiredness_thresh = 200
            tiredness = tiredness_thresh - self.send_data_len
            if tiredness < 0:
                tiredness = 0
            elif tiredness > tiredness_thresh:
                tiredness = tiredness_thresh
            tiredness = (tiredness / tiredness_thresh) * 50
            # next_fsc_state = self.fsc.state_update(self.isFSCStateActive, self.data_amount , self.energy, time, now_time)
            next_fsc_state = self.fsc.state_update(self.isFSCStateActive, self.tiredness, self.energy,
                                                   self.isActiveNeighbor)

            if next_fsc_state != self.isFSCStateActive:
                if next_fsc_state is False:
                    # inactivate
                    # event_list.extend(self.sleep(now_time))
                    self.isActive = False
                    event_list.append(EvtWakeUp(self, now_time + self.sn_settings['Energy']['sleep_duration']))
                else:
                    # activate
                    self.isActive = True
                    if len(self.send_msg_list) > 0:
                        event_list.append(EvtSendMsg(self, now_time, self.send_msg_list[0]))

            self.isFSCStateActive = next_fsc_state
            return next_fsc_state, event_list
