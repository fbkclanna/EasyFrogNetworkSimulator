#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
# from GUI.SettingsFrame import SettingsFrame as SF
from SettingsFrame import SettingsFrame as SF


class MenuBar(wx.MenuBar):
    # ------FILE------
    # ------new-------
    def click_file_new(self, event):
        pass

    # -----quit------
    def click_file_quit(self, event):
        self.parent.SetStatusText('Quit')
        self.parent.Close()

    # -------RUN-----
    def click_run_start(self, event):
        self.context['engine']['isRunning'] = True
        pass

    def click_run_stop(self, event):
        self.context['engine']['isRunning'] = False
        pass

    def click_step_over(self, event):
        self.context['engine']['step_exe'] += 1

        pass

    # --------SETTINGS--------
    # ------Field Settings------
    def click_settings_settings(self, event):
        settings_frame = SF.SettingsFrame(self, self.context, self.sn_settings, self.GUIsettings)

    # ------save------
    def click_settings_save(self, event):

        if len(self.mic_list) > 0:
            fp = open('current_setting.txt', 'w')
            for tmp_mic in self.mic_list:
                str = '%f,%f,%i,%f,\n' % (tmp_mic.pos_x, tmp_mic.pos_y, tmp_mic.micid, tmp_mic.angle)
                fp.write(str)
            fp.close()

    # ------load------
    def click_settings_load(self, event):

        if len(self.mic_list) > 0:
            del self.mic_list[0:len(self.mic_list)]

        fp = open('current_setting.txt', 'r')
        lines = fp.readlines()
        for line in lines:
            arr = line.split(',')
            print arr
            tmp_mic = M.Microphone(float(arr[0]), float(arr[1]), int(arr[2]), float(arr[3]))
            self.mic_list.append(tmp_mic)
        fp.close()

    # --------INIT-------
    def __init__(self, parent, context, sn_settings, GUIsettings):
        self.parent = parent
        self.context = context
        self.sn_settings = sn_settings
        self.GUIsettings = GUIsettings

        wx.MenuBar.__init__(self)
        menu_file = wx.Menu()
        menu_file_new = menu_file.Append(-1, 'New', 'New')
        menu_file_quit = menu_file.Append(-1, 'Quit', 'Quit application')
        self.Append(menu_file, '&File')

        menu_run = wx.Menu()
        menu_run_start = menu_run.Append(-1, '&Start\tF5', 'Start estimation')
        menu_run_step_over = menu_run.Append(-1, '&Step Over\tF10', 'Step Over')
        menu_run_stop = menu_run.Append(-1, '&Stop\tF7', 'Stop running')
        self.Append(menu_run, '&Run')

        menu_settings = wx.Menu()
        menu_settings_settings = menu_settings.Append(-1, 'Settings', 'Open field settings dialog')
        menu_settings_save = menu_settings.Append(-1, 'Save', 'Save setting file')
        menu_settings_load = menu_settings.Append(-1, 'Load', 'Load current setting')
        self.Append(menu_settings, '&Settings')

        # Bind
        self.Bind(wx.EVT_MENU, self.click_file_quit, menu_file_quit)

        self.Bind(wx.EVT_MENU, self.click_run_start, menu_run_start)
        self.Bind(wx.EVT_MENU, self.click_step_over, menu_run_step_over)
        self.Bind(wx.EVT_MENU, self.click_run_stop, menu_run_stop)

        self.Bind(wx.EVT_MENU, self.click_settings_settings, menu_settings_settings)
        self.Bind(wx.EVT_MENU, self.click_settings_load, menu_settings_load)
        self.Bind(wx.EVT_MENU, self.click_settings_save, menu_settings_save)
