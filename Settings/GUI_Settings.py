#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GUI_Settings:
    def __init__(self):
        self.reset()

    def reset(self):
        self.field_width = 480
        self.field_height = 320
        self.square_size = 50
        self.square_scale = 50

    def loadini(self, ini):
        self.field_height = ini.getint('GUI', 'DEFAULT_FIELD_HEIGHT')
        self.field_widhth = ini.getint('GUI', 'DEFAULT_FIELD_WIDTH')
        self.square_size = ini.getint('GUI', 'DEFAULT_SQUARESIZE')
        self.square_scale = ini.getfloat('GUI', 'DEFAULT_SQUARE_SCALE')
