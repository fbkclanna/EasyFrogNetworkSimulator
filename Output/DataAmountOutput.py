#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv


class DataAmountOutput:

    def __init__(self, context):
        self.sensornode_list = context['sensornode_list']

        pass

    def reset(self, context):
        fp = open('DataAmount.csv')
        csvWriter = csv.writer(fp, lineterminator='\n')
        context['output']['DataAmountCsvWriter'] = csvWriter

    def output(self, context):
        for node in context['sensornode_list']:
            context['output']['DataAmountCsvWriter'].writerow(node.data_amount_output[0], node.data_amount_output[1])

        context['output']['DataAmountFp'].writerow(context['engine']['now_time'], )
