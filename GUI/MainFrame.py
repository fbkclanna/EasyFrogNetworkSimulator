#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import MenuBar as MB
import time
import math
import itertools
import sys

sys.path.append('C:\\Users\\y-hirano\\OneDrive\\workspace\\FrogNetworkSimulator')
from Settings import GUI_Settings as GS
from GUI_Utils import *
import FieldPanel as FP


# --------------------------------------
#    menu panel
# --------------------------------------

class MainFrame(wx.Frame):
    # ---------draw ----------
    def draw_on_timer(self, event):

        # field_size?̍X?V
        size = self.GetSize()
        self.field_panel.set_field_panel_size(size)

        # self.cdc = wx.ClientDC(self.field_panel)
        self.cdc = wx.ClientDC(self.field_panel)
        self.bmp = wx.EmptyBitmap(size[0], size[1])
        self.bdc = wx.BufferedDC(self.cdc, self.bmp)
        self.bdc = wx.GCDC(self.bdc)

        '''
        pdc = wx.PaintDC(self)
        bmp = wx.EmptyBitmap(size[0],size[1])
        bdc = wx.BufferedDC(pdc, bmp)
        
        
        try:
            dc = wx.GCDC(bdc)
            print 'gcdc'
        except:
            dc = bdc
        self.bdc = dc
        '''

        # self.bdc.Clear()

        self.bdc.SetPen(wx.Pen('gray'))

        center = getCenter(size[0], size[1])

        # draw background
        self.bdc.DrawRectangle(0, 0, size[0], size[1])
        # draw initial point
        self.bdc.DrawCircle(center[0], center[1], 10)

        # draw grid
        for i in xrange(0, center[1] / self.GUIsettings.square_size):
            y = self.GUIsettings.square_size * i
            self.bdc.DrawLine(0, center[1] + y, size[0], center[1] + y)
            self.bdc.DrawLine(0, center[1] + (-1) * y, size[0], center[1] + (-1) * y)

        for i in xrange(0, center[0] / self.GUIsettings.square_size):
            y = self.GUIsettings.square_size * i
            self.bdc.DrawLine(center[0] + y, 0, center[0] + y, size[1])
            self.bdc.DrawLine(center[0] + (-1) * y, 0, center[0] + (-1) * y, size[1])

        # draw SinkNode
        for node in self.context['sinknode_list']:
            node.draw_communication(self.bdc, self.GUIsettings.square_size, self.GUIsettings.square_scale, center)
            node.draw(self.bdc, self.GUIsettings.square_size, self.GUIsettings.square_scale, center)

        # Draw SensorNode
        for node in self.context['sensornode_list']:
            node.draw_communication(self.bdc, self.GUIsettings.square_size, self.GUIsettings.square_scale, center)
            node.draw(self.bdc, self.GUIsettings.square_size, self.GUIsettings.square_scale, center)

        self.SetStatusText('Time:' + str(self.context['engine']['now_time']))

    def __init__(self, parent, id, context, sn_settings):

        self.GUIsettings = GS.GUI_Settings()
        width = self.GUIsettings.field_width
        height = self.GUIsettings.field_height

        # frame
        wx.Frame.__init__(self, parent, id, 'FrogNetworkSimulator', size=(width, height), pos=(0, 0))
        self.CreateStatusBar()
        self.SetMenuBar(MB.MenuBar(self, context, sn_settings, self.GUIsettings))

        root_panel = wx.Panel(self, wx.ID_ANY)
        self.field_panel = FP.FieldPanel(root_panel, width, height)

        # timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.draw_on_timer)
        # self.Bind(wx.EVT_PAINT,self.draw_on_timer)
        self.timer.Start(100)

        # layout
        root_layout = wx.FlexGridSizer(3, 3)
        root_layout.Add(self.field_panel, 0, wx.GROW | wx.ALL, border=10)
        # root_layout.Add(handle_panel,0,wx.GROW|wx.ALL,border=20)
        root_panel.SetSizer(root_layout)
        root_layout.Fit(root_panel)

        self.context = context

        self.SetStatusText('Main Loop')
