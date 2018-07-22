#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
::Basis::
    
::Observation::
get_data_interval: [sec]
get_data_size [byte]


::Energy::
max_enegy: 
energy_carrier_sense: [w/s]
enegy_send_msg: [w/times]
energy_get_data: [w/times]


::Communication::
communication_range: [m]
MTU: [byte] must be in 573 - 1473 byte
        127[byte] in Zegbee
frequency [MHz]
band_width [range]
stream_data_rate [bps]
'''


def create_sensornode_context():
    context = {
        'Observation': {
            'get_data_interval': 100,
            'get_data_size': 100
        },
        'Energy': {
            'max_energy': 3000.0,
            'energy_consumption_active': 0.1,
            'enegy_send_msg': 1,
            'energy_get_data': 0.1,
            'sleep_duration': 5,
            'wake_up_duration': 1
        },
        'Communication': {
            'communication_range': 100.0,
            'MTU': 127,
            # 'frequency': 2.4,
            # 'band_width' [range],
            'stream_data_rate': 250.0,
        },
        'DataSend': {
            'send_data_size': 1000,
            'send_data_threshold': 1000,
        }
    }

    return context
