#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Nodes.Node import Node
import pandas as pd
import copy


class SinkNode(Node):
    def __init__(self, pos, id, sn_settings, debug=False):
        ip_address = '192.168.0.' + str(id + 200)

        self._init(pos, id + 200, 'SinkNode', ip_address=ip_address, mac_address='', debug=debug)

        self.max_energy = sn_settings['Energy']['max_energy']

        self.color = 'red'
        self.plotsize = 4

        self.event_list = []
        self.neighbor_sensornode_list = []

        self.state = ''

        ##get_data_evt
        self.sn_settings = copy.deepcopy(sn_settings)

        self.reset()

    def reset(self):
        self.energy = self.max_energy
        self.isActive = True
        self.data_amount = 0

        del self.event_list[:]
        del self.neighbor_sensornode_list[:]
        del self.routing_table[:]

        self.num_of_sensing_signal = 0
        self.CSMACA_reset()
        self.isFSCStateActive = False

        self.data_df = pd.DataFrame(index=[], columns=['data_occur_time', 'data_recieved_time', 'latency'])

    def CSMACA_reset(self):
        # for CSMA/CA
        self.backoff_counter = 0
        self.other_signals_finishing_time = 0
        self.send_request = False
        self.send_data_len = 0
        self.CSMA_failed = False

        self.macMinBE = 3  # 0-3, default = 3
        self.BE = 3
        self.NB = 0

    def add_data(self, context, msg):
        self.data_df = self.data_df.append({
            'data_occur_time': msg.data_occur_time,
            'data_recieved_time': context['engine']['now_time'],
            'data_occur_node': msg.data_occur_node,
            'data_size': msg.data_size,
            'latency': context['engine']['now_time'] - msg.data_occur_time,
        }, ignore_index=True)
