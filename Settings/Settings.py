#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import ConfigParser


class Settings:
    def __init__(self):
        self.reset()
        return

    def LoadINI(self, inifile):
        if os.path.exists(inifile):
            ini = ConfigParser.SafeConfigParser()
            ini.read(inifile)
            self.GUI = GUI(ini)
            self.SensorNode = SensorNode(ini)
            self.Simulation = Simulation(ini)
            self.Output = Output(ini)
            self.Communication = Communication(ini)

        else:
            sys.stderr.write("Error: Can't find configfile '%s'." % INI_FILE)
            # raise Exception

    def reset(self):
        '''
        date_for_filename = datetime.datetime.now()
        self.filepath = './data/' + date_for_filename.strftime('%Y-%m-%d_%H,%M,%S')+'/'
        '''
        pass
