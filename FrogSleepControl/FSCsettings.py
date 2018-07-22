import math


class FSCsettings():
    def __init__(self):
        self.omega = 8 * math.pi
        self.K = 0.5
        self.alpha = 0.15 * self.omega / (2 * math.pi)
        self.E_max = 3000
        self.T_max = 50
        self.a = 1
        self.b = 0.08
        self.T = 15
        self.p_high = 0.80
        self.p_low = 0.01
        self.delta_T_call = 3 * math.pi / self.omega
        self.delta_T_update = 16 * math.pi / self.omega
