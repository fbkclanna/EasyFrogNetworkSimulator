#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GUI.GUI_Utils import *
import wx
import copy
# from Event.SensorNodeEvent import *
from Utils.Utils import *
from GUI.GUI_Utils import *
from Message.DataMessage import DataMessage
import copy
import wx
from Event.SensorNodeEvent import EvtWakeUp

debug = True


class Node:
    def reset(self):
        raise Exception('"reset" method must be overrided.')

    def _reset(self):
        del self.event_list[:]
        del self.on_execution_list[:]
        del self.neighbor_list[:]
        del self.routing_table[:]
        del self.send_msg_list[:]
        del self.L2_recieving_list[:]
        self.num_of_sensing_signal = 0
        self.reset_CSMACA()
        self.last_send_msg = None
        self.last_recv_msg = None
        self.last_send_msg_time = 0.0
        self.last_recv_msg_time = 0.0
        self.last_time = 0
        self.isActive = False
        self.send_request = False
        self.isSending = False
        self.isActiveNeighbor = False

        # AODV
        del self.RREQ_ID_list[:]

    def reset_CSMACA(self):
        # for CSMA/CA
        self.backoff_counter = 0
        self.send_data_len = 0
        self.CSMA_failed = False
        self.macMinBE = 3  # 0-3, default = 3
        self.BE = 3
        self.NB = 0

    def isExistRREQID(self, RREQ_ID):
        if RREQ_ID in self.RREQ_ID_list:
            return True
        else:
            return False

    def add_RREQID(self, RREQ_ID):
        if self.isExistRREQID(RREQ_ID):
            raise Exception
        else:
            self.RREQ_ID_list.append(RREQ_ID)

    def draw(self, dc, SQUARE_SIZE, SQUARE_SCALE, center):
        color = self.get_color()
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.Brush(color))
        # guipos = pos2GUIpos(SQUARE_SIZE,SQUARE_SCALE,center)
        guipos = pos2guipos(self.pos[0], self.pos[1], SQUARE_SIZE, SQUARE_SCALE, center)
        dc.DrawCircle(guipos[0], guipos[1], self.plotsize)

    def route_refresh(self, now_time):
        for route in self.routing_table:
            if route['last_time'] != -1 and route['last_time'] < now_time - 15:
                self.routing_table.remove(route)
            '''
            elif route['last_time'] != -1 and route['last_time'] < now_time - 3:
                route['enable'] = False
            '''

    def isRouteExist(self, now_time, dist_ip):
        # TODO
        # self.route_refresh(now_time)
        next = None
        hop = None
        for route_info in self.routing_table:
            if route_info['dist_ip'] == dist_ip:
                next = route_info['next_ip']
                hop = route_info['hop']
                return route_info['enable'], next, hop
                break
        else:
            return False, next, hop

    def add_route(self, dist_ip, next_ip, hop, enable=False, last_time=-1):
        if debug:
            print 'add_route dist:', dist_ip, 'next_ip', next_ip, 'hop', hop
        for each in self.routing_table:
            if each['dist_ip'] == dist_ip:
                if ((each['next_ip'] is None) or each['hop'] >= hop):
                    each['next_ip'] = next_ip
                    each['hop'] = hop
                    each['enable'] = enable
                    each['last_time'] = last_time
                break
        else:
            route = {
                'dist_ip': dist_ip,
                'next_ip': next_ip,
                'hop': hop,
                'enable': enable,
                'last_time': last_time,
            }
            self.routing_table.append(route)

    def disable_route(self, dist_ip, next_ip, hop):
        for each in self.routing_table:
            if each['dist_ip'] == dist_ip and each['next_ip'] == next_ip:
                each['enable'] = False

    def create_neighbor_list(self, sensornode_list, sinknode_list):
        communication_range = self.sn_settings['Communication']['communication_range']
        del self.neighbor_list[:]
        for each in sensornode_list:
            if each is self:
                continue
            if get_distance(self.pos, each.pos) <= communication_range:
                self.neighbor_list.append(each)
        for each in sinknode_list:
            if each is self:
                continue
            if get_distance(self.pos, each.pos) <= communication_range:
                self.neighbor_list.append(each)

    def finish_L2_recieving_msg(self, msg):
        for each in self.L2_recieving_list:
            if each['msg'] == msg:
                recieving_context = each
                break
        else:
            raise Exception
        self.L2_recieving_list.remove(recieving_context)
        if len(self.L2_recieving_list) == 0:
            self.state = 'Active'
        return recieving_context['success']

    def success_send_data(self):
        self.CSMACA_reset()
        pass

    def start_send_data(self):
        pass
        '''
        self.send_request = True
        self.send_data_len += self.data_amount
        self.data_amount -= self.data_amount
        while self.data_amount > 0:
            if self.data_amount > self.sn_settings['Communication']['MTU']:
                data_size = self.sn_settings['Communication']['MTU']
            else:
                data_size = self.data_amount
            #TODO: sinknode ip address
            dist_ip = '192.168.0.200'
            data_msg = DataMessage(self.ip_address, dist_ip, data_size)
            self.send_msg_list.append(data_msg)
            
            self.data_amount -= data_size
        
        '''

    def complete_send_msg(self, msg):
        '''
        if msg in self.send_msg_list:
            self.send_msg_list.remove(msg)
        else:
            raise Exception
        if msg.type == 'Data':
            self.send_data_len -= msg.size
        if len(self.send_msg_list) == 0:    
            self.send_request = False
        '''

    def start_L2_recieving_msg(self, msg):
        if len(self.L2_recieving_list) > 0:
            for each in self.L2_recieving_list:
                each['success'] = False
        self.state = 'Recieving'
        recieving_context = {
            'source_ip': msg.source_ip,
            'dist_ip': msg.dist_ip,
            'msg': msg,
            'success': True,
        }
        self.L2_recieving_list.append(recieving_context)

    def get_color(self):
        assert hasattr(self, 'color')
        return self.color

    def draw_communication(self, dc, SQUARE_SIZE, SQUARE_SCALE, center):
        if not self.isSending:
            return
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 0)))
        dc.SetBrush(wx.Brush(wx.Colour(0, 255, 255, 30)))
        # guipos = pos2GUIpos(SQUARE_SIZE,SQUARE_SCALE,center)
        guipos = pos2guipos(self.pos[0], self.pos[1], SQUARE_SIZE, SQUARE_SCALE, center)
        dc.DrawCircle(guipos[0], guipos[1],
                      self.sn_settings['Communication']['communication_range'] * SQUARE_SIZE / SQUARE_SCALE)

    def wake_up(self):
        self.isActive = True
        self.isActiveNeighbor = False
        for neighbor in self.neighbor_list:
            if neighbor.isFSCStateActive:
                self.isActiveNeighbor = True

    def sleep(self):
        self.isActive = False

    def handler(self, func, *args):
        # assert hasattr(self, func)
        print func
        self.func(*args)

    def _init(self, pos, id, attribute, ip_address='', mac_address='', debug=False):

        self.pos = pos
        self.nodeid = id
        self.attribute = ''
        self.time = 0
        self.last_time = 0

        self.ip_address = ip_address
        self.mac_address = mac_address

        self.debug = debug

        self.routing_table = []

        self.event_list = []
        self.on_execution_list = []
        self.neighbor_list = []
        ##
        self.send_msg_list = []
        ##for L2 CSMACA
        self.L2_recieving_list = []
        self.RREQ_ID_list = []

        self.state = ''

        self._reset()
