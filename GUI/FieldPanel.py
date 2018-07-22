#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class FieldPanel(wx.Panel):
    def __init__(self, parent, width, height):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(width, height))

    def set_field_panel_size(self, size):
        self.SetSize(size)
