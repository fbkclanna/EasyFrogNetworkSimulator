#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import copy
import numpy as np
import time
import datetime
import pandas as pd

from Nodes.SensorNode import SensorNode
from Nodes.SinkNode import SinkNode
from Settings.Settings import Settings
from Settings.SensorNodeSettings import *
from Output.OutputEngine import OutputEngine

from Event.SensorNodeEvent import *


# time: now time
# event_list:

class Engine():
    def __init__(self, debug=False):
        self.debug = debug
        self.context = self.create_context()
        self.reset()

        self.thread = threading.Thread(target=self.run)
        self.thread.setDaemon(True)
        ##call run method
        self.thread.start()

    def reset(self):
        del self.context['sensornode_list'][:]
        del self.context['event_list'][:]
        self.context['engine']['last_time'] = 0.0
        self.context['engine']['now_time'] = 0.0
        self.context['engine']['next_time'] = 0.0
        self.context['engine']['isRunning'] = False
        self.context['engine']['state'] = 'Stop'

        # reset_output
        self.context['output']['engine'] = OutputEngine(self.context)
        self.context['output']['filepath'] = './data/' + datetime.datetime.now().strftime('%Y-%m-%d_%H,%M,%S') + '/'

    def run(self):
        now_time = 0
        while True:
            if self.context['engine']['isRunning'] or self.context['engine']['step_exe'] > 0:
                if self.context['engine']['step_exe'] > 0:
                    self.context['engine']['step_exe'] -= 1

                event = self.context['event_list'].pop(0)

                if self.context['engine']['last_time'] != event.time:
                    for node in self.context['sensornode_list']:
                        node.refresh_energys(self.context['engine']['now_time'])
                    self.context['output']['engine'].add_output()
                    self.context['output']['engine'].output_all_files()

                if event.time >= 1000:
                    return

                if self.debug:
                    if event.node is not None:
                        print event.time, '\tpop\tEvent:\t', event.event_name, '\t Node:', event.node.nodeid
                    else:
                        print event.time, '\tpop\tEvent:\t', event.event_name

                assert event.time >= self.context['engine']['now_time']
                self.context['engine']['last_time'] = self.context['engine']['now_time']
                self.context['engine']['now_time'] = event.time

                next_events = event.func(self.context)

                if next_events is None:
                    raise Exception('next_events is None.')

                for each in next_events:
                    self.context['event_list'].insert(self.search_time(self.context['event_list'], each.time), each)
                    '''
                    if debug:
                        print 'set', each.time, '\tset\tEvent:\t', each.event_name
                    '''
                '''
                if self.debug:
                    for node in self.context['sensornode_list']:
                        print node.ip_address, node.isActive, node.isFSCStateActive
                        for each in node.routing_table:
                            print '\tdist\t', each['dist_ip'], '\tnext\t', each['next_ip'], '\thop\t', each['hop']
                    for node in self.context['sinknode_list']:
                        print node.ip_address
                        for each in node.routing_table:
                            print '\tdist\t', each['dist_ip'], '\tnext\t', each['next_ip'], '\thop\t', each['hop']
                '''


            else:
                pass

    def search_time(self, event_list, time):
        for i, event in enumerate(event_list):
            if event.time > time:
                return i
        return len(event_list)

    def handler(self, func, *args):
        if hasattr(self, func):
            self.func(*args)
        else:
            sys.stderr.write()
            raise Exception('handler exception')

    def create_context(self):
        context = {
            'engine': {
                'engine': self,
                'last_time': 0.0,
                'now_time': 0.0,
                'next_time': 0.0,
                'isRunning': False,
                'state': None,
                'step_exe': 0,
            },
            'output': {
                'filepath': None,
                'engine': None,
                'DataAmountFP': None,
                'BatteryFP': None,
            },
            'sensornode_list': [],
            'sinknode_list': [],
            'event_list': [],
        }
        return context

    def start(self):
        self.context['engine']['isRunning'] = True

    def stop(self):
        self.context['engine']['isRunning'] = False


if __name__ == '__main__':
    debug = False

    e = Engine(debug)
    ##add_sensornode
    sn_settings = create_sensornode_context()
    for i in range(0, 4, 2):
        for j in range(0, 4, 2):
            e.context['sensornode_list'].append(SensorNode((i, j), len(e.context['sensornode_list']), sn_settings))
            print 'new sensor node ', i, j

    ##add task
    for node in e.context['sensornode_list']:
        event = EvtGetData(node, 0)
        e.context['event_list'].append(event)

    e.start()

    while True:
        pass

    ##add_sinknode
