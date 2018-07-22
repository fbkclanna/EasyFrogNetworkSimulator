#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Event.Event import Event
# from Communication.L2 import CSMACA
import CSMACA

debug = True


class L2EvtSendMsg(Event):
    def __init__(self, node, time, msg=None):
        self._init__(event_name='L2_start_send_data', node=node, func=self.exe, time=time, necessary_time=0)
        self.msg = msg

    def exe(self, context):
        if debug:
            print context['engine']['now_time'], '\texe\tL2Evt \t', self.event_name, '\tNode:', self.node.nodeid
        self.node.start_send_data()
        return [CSMACA.L2EvtCarrierSense(self.node, context['engine']['now_time'], msg=self.msg)]
