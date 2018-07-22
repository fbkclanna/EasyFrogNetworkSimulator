#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from Nodes.SensorNode import SensorNode
from Nodes.SinkNode import SinkNode


class SettingsFrame(wx.Frame):
    def __init__(self, parent, context, sn_settings, GUIsettings):
        self.context = context
        self.GUIsettings = GUIsettings
        self.sn_settings = sn_settings

        frame = wx.Frame(parent, wx.ID_ANY, 'Settings')
        notebook = wx.Notebook(frame, wx.ID_ANY)

        # environment_panel
        # localization_panel
        field_panel = FieldPanel(notebook, self.context, self.GUIsettings)
        sensornode_panel = SensorNodePanel(notebook, context, self.sn_settings)

        notebook.InsertPage(0, field_panel, 'Field')
        notebook.InsertPage(1, sensornode_panel, 'Microphone')
        # notebook.InsertPage(2,Environmet_panel,'Environment')
        frame.Show()


class FieldPanel(wx.Panel):
    def __init__(self, parent, context, GUIsettings):
        self.context = context
        self.GUIsettings = GUIsettings

        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.text_square_size = wx.StaticText(self, wx.ID_ANY, 'square size')
        self.textbox_square_size = wx.TextCtrl(self, wx.ID_ANY)
        self.text_square_scale = wx.StaticText(self, wx.ID_ANY, 'square scale')
        self.textbox_square_scale = wx.TextCtrl(self, wx.ID_ANY)

        # button
        self.button_apply = wx.Button(self, wx.ID_ANY, 'Apply')
        self.button_apply.Bind(wx.EVT_BUTTON, self.click_apply)
        self.button_reset = wx.Button(self, wx.ID_ANY, 'Reset')
        self.button_reset.Bind(wx.EVT_BUTTON, self.click_reset)

        # ----layout---
        button_layout = wx.FlexGridSizer(5, 2)
        button_layout.AddMany([
            (self.text_square_size), (self.textbox_square_size),
            (self.text_square_scale), (self.textbox_square_scale),
        ])
        button_layout.Add(self.button_apply)
        button_layout.Add(self.button_reset)

        self.SetSizer(button_layout)

        self.reload()

    def click_apply(self, event):
        self.GUIsettings.square_size = int(self.textbox_square_size.GetValue())
        self.GUIsettings.square_scale = int(self.textbox_square_scale.GetValue())

    def click_cancel(self, event):
        pass

    def click_reset(self, event):
        self.reload()
        pass

    def reload(self):
        self.textbox_square_size.SetValue(str(self.GUIsettings.square_size))
        self.textbox_square_scale.SetValue(str(self.GUIsettings.square_scale))


class SensorNodePanel(wx.Panel):
    def __init__(self, parent, context, sn_settings):
        # listbox
        # wx.Panel(notebook, wx.ID_ANY)
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.sensornode_list = context['sensornode_list']
        self.sn_settings = sn_settings

        self.listbox = wx.ListBox(self, wx.ID_ANY, style=wx.LB_SINGLE)
        self.listbox.Bind(wx.EVT_LISTBOX, self.listbox_select)
        self.refresh_sensornode_list()

        self.text_nodeid = wx.StaticText(self, wx.ID_ANY, 'Node ID')
        self.textbox_nodeid = wx.TextCtrl(self, wx.ID_ANY, str(len(self.sensornode_list)))
        self.text_x = wx.StaticText(self, wx.ID_ANY, 'x')
        self.textbox_xcoordinate = wx.TextCtrl(self, wx.ID_ANY, '')
        self.text_y = wx.StaticText(self, wx.ID_ANY, 'y')
        self.textbox_ycoordinate = wx.TextCtrl(self, wx.ID_ANY, '')
        self.text_battery = wx.StaticText(self, wx.ID_ANY, 'battery')
        self.textbox_battery = wx.TextCtrl(self, wx.ID_ANY, '')

        self.button_add_node = wx.Button(self, wx.ID_ANY, 'Add')
        self.button_add_node.Bind(wx.EVT_BUTTON, self.click_add_node)
        self.button_delete_node = wx.Button(self, wx.ID_ANY, 'Delete')
        self.button_delete_node.Bind(wx.EVT_BUTTON, self.click_delete_node)
        self.button_delete_node.Disable()

        button_layout = wx.FlexGridSizer(5, 2)
        button_layout.AddMany([(self.text_nodeid), (self.textbox_nodeid),
                               (self.text_x), (self.textbox_xcoordinate),
                               (self.text_y), (self.textbox_ycoordinate),
                               (self.text_battery), (self.textbox_battery)])
        button_layout.Add(self.button_add_node)
        button_layout.Add(self.button_delete_node)

        layout = wx.FlexGridSizer(1, 2)
        layout.AddMany([(self.listbox, wx.GROW), (button_layout)])

        self.SetSizer(layout)

    def refresh_sensornode_list(self):
        self.listbox.Clear()
        for node in self.sensornode_list:
            self.listbox.Append(str(node.nodeid), node)

    def listbox_select(self, event):
        obj = event.GetEventObject()
        self.selected_node = obj.GetClientData(obj.GetSelection())
        self.textbox_nodeid.SetValue(str(self.selected_node.nodeid))
        self.textbox_xcoordinate.SetValue(str(self.selected_node.pos[0]))
        self.textbox_ycoordinate.SetValue(str(self.selected_node.pos[1]))
        self.textbox_battery.SetValue(str(self.selected_node.max_energy))

        print self.selected_node
        self.button_delete_node.Enable()

    def click_add_node(self, event):
        nodeid = int(self.textbox_nodeid.GetValue())
        xcoordinate = float(self.textbox_xcoordinate.GetValue())
        ycoordinate = float(self.textbox_ycoordinate.GetValue())
        max_energy = float(self.textbox_battery.GetValue())

        for i in range(len(self.sensornode_list) + 1):
            if i == len(self.sensornode_list):
                self.sensornode_list.append(SensorNode((xcoordinate, ycoordinate), nodeid, self.sn_settings))
            elif nodeid == self.sensornode_list[i].nodeid:
                self.sensornode_list[i].pos = (xcoordinate, ycoordinate)
                self.sensornode_list[i].max_energy = max_energy
                break

        self.textbox_nodeid.SetValue(str(len(self.sensornode_list)))
        self.textbox_xcoordinate.Clear()
        self.textbox_ycoordinate.Clear()
        self.textbox_battery.Clear()

        self.refresh_sensornode_list()

    def click_delete_node(self, event):
        self.button_delete_node.Disable()
        self.sensornode_list.remove(self.selected_node)
        self.refresh_sensornode_list()
        pass
