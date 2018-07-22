#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
event_name:
node: 
func: the pointer of function when pop this event firstly
time: the time this event execute
necessary_time: 
'''


class Event:
    def __init__(self):
        pass

    def _init__(self, event_name='', node=None, func=None, time=0, necessary_time=0):
        self.time = time
        self.necessary_time = necessary_time
        self.event_name = event_name
        self.func = func
        self.node = node

    def calc_necessry_time(self):
        raise Exception('this method must be overrided.')

    def start(self, context):
        raise Exception('this method must be overrided.')

    def exe(self, context):
        raise Exception('this method must be overrided.')
