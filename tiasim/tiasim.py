"""
    This file is part of TIASim.
    https://github.com/aewallin/TIASim

    TIASim is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TIASim is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TIASim.  If not, see <https://www.gnu.org/licenses/>.
"""


import numpy
import abc
from scipy import constants

room_temperature=constants.convert_temperature(25, 'celsius', 'kelvin')

def calc_feedback_transimpedance(frequency, r_f, c_f):
    """
    feedback impedance ZF = R_F || C_F
    """
    w = 2.0*numpy.pi*frequency
    return r_f / ( 1j*r_f*c_f*w + 1.0 );

def calc_closed_loop_transimpedance(f, gain_f, z_f, c_tot):
    """
    closed loop transimpedance, Hobbs (18.15)
    f: frequency
    gain_f: gain at f
    z_f: total feedback impedance at f
    c_tot: total source capacitance (diode capacitance + input capacitance)
    """
    w = 2.0*numpy.pi*f
    return gain_f*z_f / ( 1.0 + gain_f + 1j*w*z_f*c_tot);

'''
Opamp is an abstract base class. Each of the members with the
@abc.abstractmethod decorator must be defined for each derived type
otherwise instantiation of an object with that type will cause
an exception.
'''
class Opamp(metaclass=abc.ABCMeta):
    def __init__(self, AOL_gain, AOL_bw, GBWP):
        self._AOL_gain = AOL_gain
        self._AOL_bw = AOL_bw
        self._GBWP = GBWP

    @property
    def AOL_gain(self):
        return self._AOL_gain

    @property
    def AOL_bw(self):
        return self._AOL_bw

    @property
    def GBWP(self):
        return self._GBWP

    @abc.abstractmethod
    def gain(self,f):
        pass

    @abc.abstractmethod
    def voltage_noise(self,f):
        pass

    @abc.abstractmethod
    def current_noise(self,f):
        pass

    @abc.abstractmethod
    def input_capacitance(self):
        pass


class Photodiode:
    def __init__(self, capacitance, responsivity):
        self.capacitance = capacitance
        self.responsivity = responsivity # A/W

    def current(self, P):
        """ photocurrent (A) produced by input optical power P """
        return self.responsivity*P

class TIA():
    def __init__(self, opamp, diode, R_F, C_F=None, C_F_parasitic=None):
        """ build TIA from given opamp, diode and feedback resistance/capacitance """
        self.opamp = opamp
        self.diode = diode
        self.R_F = R_F # feedback resistance
        self.C_tot = self.diode.capacitance + self.opamp.input_capacitance() # total source capacitance
        if C_F_parasitic:
            self.C_F_parasitic=C_F_parasitic
        else:
            self.C_F_parasitic=0.01e-12 # minimum capacitance over R_F

        if C_F:
            self.C_F = C_F + self.C_F_parasitic
        else:
            self.set_CF()


    def ZF(self, f):
        """
            feedback impedance ZF = R_F || C_F
        """
        return calc_feedback_transimpedance(f, self.R_F, self.C_F)

    def ZM(self,f):
        """
            closed loop transimpedance, Hobbs (18.15)
        """
        A = self.opamp.gain(f)
        w = 2.0*numpy.pi*f

        return calc_closed_loop_transimpedance(f, gain_f=A, z_f=self.ZF(f), c_tot=self.C_tot)

    def amp_current_noise(self, f):
        """
            output-referred amplifier current noise, in V/sqrt(Hz)
            computed as amplifier input-referred noise thru transimpedance
        """
        return self.opamp.current_noise(f)*numpy.abs(self.ZM(f))

    def amp_voltage_noise(self, f):
        """
            output referred amplifier voltage noise, in V/sqrt(Hz)
        """
        A = self.opamp.gain(f)
        w = 2.0*numpy.pi*f
        Avcl = A / (1.0+A/(1.0+1j*w*self.ZF(f)*(self.C_tot)))  # closed loop voltage gain
        return self.opamp.voltage_noise(f) * numpy.abs(Avcl)

    def johnson_noise(self, f, T=room_temperature):
        """
            output-referred voltage noise due to R_F, in V/sqrt(Hz)
            Computed as johnson current noise thru transimpedance
        """
        return numpy.sqrt( 4*constants.k*T/self.R_F ) * numpy.abs(self.ZM(f))

    def shot_noise(self, P, f):
        """
            output-referred shot noise in V/sqrt(Hz) due to optical power P in W
            shot-noise current thru transimpedance.

            For the total TIA noise at power P use bright_noise()
        """
        I_PD = self.diode.current(P)
        return numpy.sqrt(2.0*constants.elementary_charge*I_PD) * numpy.abs(self.ZM(f))

    def dark_noise(self, f):
        """
            output referred TIA noise without any shot noise, in V/sqrt(Hz)
            quadrature sum of voltage, current, and RF johnson noise
        """
        c2 = self.amp_current_noise(f)**2
        v2 = self.amp_voltage_noise(f)**2
        j2 = self.johnson_noise(f)**2
        return numpy.sqrt( c2+v2+j2 )

    def bright_noise(self,P,f):
        """
            output referred TIA bright-noise with optical power P
            dark_noise + shot noise of photocurrent.
            Photocurrent computed as optical power times photodiode responsivity
        """
        d2 = self.dark_noise(f)**2
        s2 = self.shot_noise(P,f)**2
        return numpy.sqrt( d2+s2 )

    def dc_output(self, P, f):
        I_PD = self.diode.current(P)
        return I_PD*numpy.abs(self.ZM(f))

    def bandwidth_approx(self):
        """
            Simple bandwidth approximation - usually not correct
        """
        f3db = numpy.sqrt( self.opamp.GBWP /(2*numpy.pi*self.R_F*self.C_tot))
        return f3db

    def bandwidth(self):
        """
            The -3 dB bandwidth of the TIA
            Found by searching for the frequency where ZM(f) = ZM(0)/sqrt(2)
        """
        f = numpy.logspace(1,10,int(1e6))
        zm = numpy.abs( self.ZM(f) )
        z_3db = zm[0]/numpy.sqrt(2.0)
        try:
            ind = min( min(numpy.where( zm < z_3db) ) )
            #print zm[0], zm[ind], zm[ind]/zm[0]
            f_3dB= f[ind]
            return f_3dB
        except:
            print( "WARNING -3dB point not found" )
            return -1

    def set_CF(self):
        """
            set optimum value for C_F
            C_opt = sqrt( C_source / 2*pi*GBWP*R_F )

            design point is Q=1/sqrt(2) ~ 0.71 which is the maximally flat "Butterworth" frequency response
        """
        C_optimal = numpy.sqrt( self.C_tot / (2.0*numpy.pi*self.opamp.GBWP*self.R_F))
        if C_optimal > self.C_F_parasitic:
            self.C_F = C_optimal
        else:
            self.C_F = self.C_F_parasitic

        print( "optimum: %.3f pF, set C_F= %.3f pF" % (C_optimal*1e12, self.C_F*1e12) )

    def cnr(self, f):
        """ carrier to noise ratio """
        P = 1.0
        c = 10.0*numpy.log10( self.bright_noise(P, f) )
        n = 10.0*numpy.log10( self.bright_noise(0.0, f) )
        #print c,n
        return c,n,c-n

def v_to_dbm(v_psd, RBW = 1.0, termination=True):
    """
        convert voltage noise in v/sqrt(Hz)
        to dBm as displayed by Spectrum Analyzer
    """
    v2_psd = v_psd*v_psd # V^2 / Hz
    # P = UI = U^2 / R
    p_psd = v2_psd / 50.0 # W / Hz
    dbm = 10.0*numpy.log10( RBW*p_psd / 1.0e-3)
    if termination:
        dbm = dbm - 6.0 # 50-ohm termination halves voltage, so -6dB power
    return dbm


if __name__ == "__main__":
    pass
