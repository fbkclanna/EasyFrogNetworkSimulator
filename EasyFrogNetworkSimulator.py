#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import sys
import wx
import threading
import pandas as pd

import Engine as E
from GUI.MainFrame import MainFrame as MF
from Nodes.SensorNode import SensorNode
from Nodes.SinkNode import SinkNode
from Settings.Settings import Settings
from Settings.SensorNodeSettings import *
from FrogSleepControl.FSCsettings import FSCsettings as FSCs

from Event.SensorNodeEvent import *


def create_argparse():
    '''
    create_argpasre 
    '''
    parser = argparse.ArgumentParser(description='This script is ....')
    parser.add_argument('-c', '--configfile',
                        action='store',
                        nargs='?',
                        const=None,
                        default='config.ini',
                        type=str,
                        choices=None,
                        help='ConfigurationFile path. (default: "config.ini" in source directory)', \
                        metavar=None)
    return parser

    parser.add_argument('-d', '--debug',
                        action='store',
                        nargs='?',
                        const=None,
                        default=False,
                        type=str,
                        choices=None,
                        help='Debug. (default: False)',
                        metavar=None)
    return parser


if __name__ == '__main__':
    parser = create_argparse()
    args = parser.parse_args()

    e = E.Engine(debug=True)
    sn_settings = create_sensornode_context()
    fscs = FSCs()

    application = wx.App()
    mainframe = MF(None, wx.ID_ANY, e.context, sn_settings)

    mainframe.Center()
    mainframe.Show()

    ##add_sensornode
    '''
    for i in range(-1, 201, 50):
        for j in range(-1, 201, 50):
            e.context['sensornode_list'].append(SensorNode((i,j), len(e.context['sensornode_list']), sn_settings, fscs))
            
            if (i - 1) ** 2 + (j - 1) ** 2 < 100 **2:
                e.context['sensornode_list'][-1].add_route('192.168.0.200', '192.168.0.200', 1, enable = True, last_time = 0)
            else:
                id = len(e.context['sensornode_list'])
                e.context['sensornode_list'][-1].add_route('192.168.0.200', '192.168.0.' + str(int((id + 1)/ 2)), 1, enable = True, last_time = 0)
            
            print 'new sensor node ', i, j
    '''
    df = pd.read_csv('routing_table.csv', index_col=0)
    print df.head
    for i, row in df.iterrows():
        e.context['sensornode_list'].append(
            SensorNode((row.x, row.y), len(e.context['sensornode_list']), sn_settings, fscs))
        e.context['sensornode_list'][-1].add_route(row.dist_ip, row.next_ip, 1, enable=True, last_time=0)

    ##add_sinknode
    i, j = 1, 1
    sink = SinkNode((i, j), len(e.context['sinknode_list']), sn_settings)
    print 'new sink node', i, j, sink.ip_address
    e.context['sinknode_list'].append(sink)

    for each in e.context['sensornode_list']:
        each.create_neighbor_list(e.context['sensornode_list'], e.context['sinknode_list'])
    for each in e.context['sinknode_list']:
        each.create_neighbor_list(e.context['sensornode_list'], e.context['sinknode_list'])

    ##add task
    for node in e.context['sensornode_list']:
        e.context['event_list'].append(EvtFSCUpdate(node, 0))
    e.context['event_list'].append(EvtDataOccur((0, 0), 1000, 0))

    for node in e.context['sensornode_list']:
        # e.context['event_list'].append(EvtFSCUpdate(node, 15))
        e.context['event_list'].append(EvtWakeUp(node, 10))
        # event =

    sorted(e.context['event_list'], key=lambda event: event.time)

    # e.start()

    application.MainLoop()
