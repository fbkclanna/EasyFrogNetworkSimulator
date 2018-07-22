import random
import math
import copy

thresh = 20.0  # [s]


class FSC:
    def __init__(self, node, max_energy, fsc_settings):
        self.max_energy = max_energy
        self.fsc_settings = copy.deepcopy(fsc_settings)
        # self.reset()

    '''
    def reset(self):
        self.tiredness  = 0
        self.energy = self.max_energy
        

    def var_update(self, energy_diff, tiredness_diff):
        if self.isActive:
            self.energy -= energy_diff
            self.tiredness -= tiredness_diff
        else:
            self.tiredness += tiredness_diff
    '''

    def state_update(self, fsc_state, Tn, En, isExist):
        '''
        Tn = 
        En = 
        t = 
        now_time = 
        '''

        rand = random.random()
        if fsc_state:
            p = self.P_active2inactive(Tn)
            if rand <= p:
                return False
            else:
                return True
        else:
            p = self.P_inactive2active(Tn, En, isExist)
            if rand <= p:
                return True
            else:
                return False

    def P_inactive2active(self, Tn, En, exist):
        P = self.F1(Tn) * self.G(En) * self.H(exist)
        print 'p_inactive -> active', P, '=', self.F1(Tn), ',', self.G(En), ',', self.H(exist)
        return P

    def P_active2inactive(self, Tn):
        P = self.F2(Tn)
        print 'p active -> inactive', P, '=', self.F2(Tn)
        return P

    def F1(self, Tn):
        a = self.fsc_settings.a
        T = self.fsc_settings.T

        val = 1.0 / (math.exp(a * (Tn - T)) + 1)
        return val

    def G(self, En):
        b = self.fsc_settings.b
        return -2.0 / (math.exp(b * En) + 1) + 1

    def H(self, exist):
        if exist:
            return self.fsc_settings.p_high
        else:
            return self.fsc_settings.p_low

    def F2(self, Tn):
        a = self.fsc_settings.a
        T = self.fsc_settings.T
        try:
            val = 1.0 / (math.exp(-a * (Tn - T)) + 1)
        except OverflowError:
            val = float('inf')
        print val
        return val
