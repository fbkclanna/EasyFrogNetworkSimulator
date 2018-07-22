#!/usr/bin/env python
# -*- coding: utf-8 -*-


def create_Communication_context():
    context = {
        'CSMACA': {
            'stream_data_rate': 250  # [kbps]
        },
        'Observation': {
            'get_data_interval': 10,
            'get_data_size': 10
        },
        'Energy': {
            'max_energy': 100.0,
            'energy_carrier_sense': 0.01,
            'enegy_send_msg': 0.1,
            'energy_get_data': 0.01
        },
        'Communication': {
            'communication_range': 150,
            'MTU': 1473,
            # 'frequency': 2.4,
            # 'band_width' [range],
            'stream_data_rate': 250,
        },
        'DataSend': {
            'send_data_size': 1000,
            'send_data_threshold': 1000,
        }

    }

    return context
