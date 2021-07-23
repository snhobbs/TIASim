import numpy
from tiasim import Opamp

class OPA855(Opamp):
    """
         8-GHz Gain Bandwidth Product, Gain of 7-V/V Stable, Bipolar Input Amplifier
         https://www.ti.com/lit/ds/symlink/opa855.pdf
    """
    def __init__(self):
        AOL_gain = 10093.79531159
        AOL_bw = 941445.81175752
        GBWP = 8e9
        super().__init__(AOL_gain, AOL_bw, GBWP)

    def gain(self,f):
        """ gain """
        #return numpy.abs( self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) )
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw )

    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        # FIXME, not a good fit to the datasheet
        a0 = 0.98e-9
        a1 = 60e-9
        return a0+a1/numpy.sqrt(f)

    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        i0 = 2.5e-12
        i1 = 1000e-12

        return i0+i1/numpy.sqrt(f)

    def input_capacitance(self):
        cm = 0.6e-12
        diff= 0.2e-12
        return cm+diff


class OPA858(Opamp):
    """
        5.5 GHz Gain Bandwidth Product, Decompensated Transimpedance Amplifier with FET Input
        https://www.ti.com/lit/ds/symlink/opa858.pdf
    """
    def __init__(self):
        AOL_gain =  6645.80643846   # pow(10,66.0/20.0)
        AOL_bw = 1091348.67318369
        GBWP = 5.5e9
        super().__init__(AOL_gain, AOL_bw, GBWP)

    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw )

    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        # FIXME, not a good fit to the datasheet
        # fit vnoise:  [  2.15623045e-09   9.28064032e-07]

        a0 = 2.5e-9
        a1 = 72e-8

        return a0+a1/numpy.sqrt(f)

    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        i0 = 3.22683744e-20

        return i0*f

    def input_capacitance(self):
        cm = 0.6e-12
        diff= 0.2e-12
        return cm+diff


class OPA859(Opamp):
    """
        1.8 GHz Unity-Gain Bandwidth, 3.3-nV/sqrt(Hz), FET Input Amplifier
        https://www.ti.com/product/OPA859
    """
    def __init__(self):
        AOL_gain = 2152.02871113
        AOL_bw = 519231.04490493
        GBWP = 1.8e9
        super().__init__(AOL_gain, AOL_bw, GBWP)

    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw )

    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        # FIXME, not a good fit to the datasheet
        a0 = 3.3e-9
        a1 =  93e-8

        return a0+a1/numpy.sqrt(f)

    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        i0 = 1e-17
        i1 = 3e-20
        return i0*numpy.sqrt(f)+i1*f

    def input_capacitance(self):
        cm = 0.62e-12
        diff= 0.2e-12
        return cm+diff

class OPA657(Opamp):
    """
        1.6-GHz, Low-Noise, FET-Input Operational Amplifier
        https://www.ti.com/lit/ds/symlink/opa657.pdf

        4.8 nV/sqrt(Hz) voltage noise
        1.3 fA/sqrt(Hz) current noise
        Gain of +7 stable
    """
    def __init__(self):
        AOL_gain = pow(10,75.0/20.0)
        AOL_bw = 10*45626.55598007
        self.AOL_pole = 300e6
        GBWP = 1.6e9
        super().__init__(AOL_gain, AOL_bw, GBWP)

    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) * (1.0/ (1.0+ 1j * f/self.AOL_pole ) )

    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        #return numpy.array(len(f)*[4.8e-9]) # FIG 13
        a0 = 4.8e-9
        a1 =  93e-9
        return a0+a1/pow(f,0.5)

    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        return 1.3e-15

    def input_capacitance(self):
        cm = 0.7e-12
        diff= 4.5e-12
        return cm+diff

class OPA818(Opamp):
    """
        OPA818 2.7-GHz, High-Voltage, FET-Input, Low Noise, Operational Amplifier
        https://www.ti.com/lit/ds/symlink/opa818.pdf
        Gain of +7 stable
    """
    def __init__(self):
        AOL_gain = pow(10,94.3/20.0)
        AOL_bw = 50e3
        self.AOL_pole = 500e6
        GBWP = 2.7e9
        super().__init__(AOL_gain, AOL_bw, GBWP)

    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) * (1.0/ (1.0+ 1j * f/self.AOL_pole ) )

    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        #return numpy.array(len(f)*[4.8e-9]) # FIG 13
        a0 = 2.0e-9
        a1 =  400e-9
        return a0+a1/pow(f,0.6)

    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        return 1.0e-12*pow(f,0.8)/pow(28e6,0.8) # numpy.ones((len(f),1))

    def input_capacitance(self):
        cm = 1.9e-12
        diff= 0.5e-12
        return cm+diff

class OPA847(Opamp):
    """
        3.8GHz GBWP  Ultra-Low Noise, Voltage-Feedback, Bipolar Input
        stable for gains >=12
        https://www.ti.com/lit/ds/symlink/opa847.pdf
    """
    def __init__(self):
        AOL_gain = 57666.09586591
        AOL_bw = 65178.06837912
        GBWP = 3.9e9
        super().__init__(AOL_gain, AOL_bw, GBWP)

    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw )

    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        #return numpy.array(len(f)*[0.85e-9])
        return 0.85e-9

    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        #return numpy.array(len(f)*[2.7e-12])
        return 2.7e-12

    def input_capacitance(self):
        cm = 1.7e-12
        diff= 2.0e-12
        return cm+diff
