#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os


class OutputEngine:

    def __init__(self, context):
        self.context = context
        self.reset()
        pass

    def reset(self):
        self.sensor_df_list = []

        pass

    def add_output(self):
        if self.sensor_df_list == []:
            for i, each in enumerate(self.context['sensornode_list']):
                df = pd.DataFrame(index=[],
                                  columns=['time', 'data_amount', 'send_data_len', 'energy', 'state', 'tiredness',
                                           'fsc_state'])
                self.sensor_df_list.append(df)
        for i, node in enumerate(self.context['sensornode_list']):
            self.sensor_df_list[i] = self.sensor_df_list[i].append({
                'time': self.context['engine']['now_time'],
                'data_amount': node.data_amount,
                'send_data_len': node.send_data_len,
                'energy': node.energy,
                'state': node.isActive,
                'fsc_state': node.isFSCStateActive,
                'tiredness': node.tiredness,
            }, ignore_index=True)

    def output_all_files(self):
        if not os.path.exists(self.context['output']['filepath']):
            os.makedirs(self.context['output']['filepath'])

        for i, node in enumerate(self.context['sensornode_list']):
            self.sensor_df_list[i].to_csv(self.context['output']['filepath'] + 'SensorNode' + str(i) + '.csv')

        for i, each in enumerate(self.context['sinknode_list']):
            each.data_df.to_csv(self.context['output']['filepath'] + 'SinkNode' + str(i) + '.csv')
