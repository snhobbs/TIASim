import math
from scipy import constants
from .tools import *

def calc_excess_noise_factor(k, M):
    return M*k+(2-1/M)*(1-k)

'''Calculate the diodes effective photosensitive area'''
def calculate_effective_area(area, fill_factor):
    return area*fill_factor

def calculate_apd_snr(il, t, M, B, F, R, dark_current):
    '''
    Calculate the SNR floor of an APD with primary photocurrent il, at temperature t, gain M, bandwidth B, excess noise factor F, feedback resistor R,
    and thermally generated carriers idg
    '''
    k_B = constants.k
    q = constants.elementary_charge
    return M*il/(math.sqrt(4*k_B*t/R + 2*q*M**2*F*B*il + dark_current))

def estimate_thermal_carrier_currents(t, noise_bw, dark_measurement_bw, dark_current, t_dark_current):
    '''
    Estimate that the multiplied dark carriers >> the non-multiplied
    Then take the dark current to be purely a fermi-dirac distribution, remove the temperature
    dependace to get the number of carriers extrapolated to 0k.
    The use that to calculate the number of carriers at whatever current we're looking at
    '''
    t_0 = t_dark_current
    idg_t0_sq = pow(dark_current, 2) * noise_bw/dark_measurement_bw
    idg_0_sq = idg_t0_sq/fermi_dirac_dist(t_0)
    assert idg_0_sq > idg_t0_sq
    idg_sq = idg_0_sq*fermi_dirac_dist(t)
    idg = math.sqrt(idg_sq)
    return idg

class AvalanchePhotodiode:
    bandgap = 1.21 # eV silicon

    def __init__(self, k, effective_area, capacitance, leakage, dark_current, t_dark_current, dark_measurement_bw, gain):
        self.k_ = k
        self.effective_area_ = effective_area
        self.capacitance_ = capacitance
        self.leakage_ = leakage
        self.dark_current_ = dark_current
        self.t_dark_current_ = t_dark_current
        self.dark_measurement_bw_ = dark_measurement_bw
        self.gain_ = gain

    @property
    def capacitance(self):
        return self.capacitance_

    @property
    def eta(self):
        return 0.6 # FIXME

    @property
    def F(self):
        return calc_excess_noise_factor(k=self.k_, M=self.gain)

    @property
    def gain(self):
        return self.gain_

    def calculate_snr(self, il, bandwidth=1, t=None, R=1):
        if t is None:
            t = self.t_dark_current_
        dark_current = self.estimate_thermal_carrier_currents(t=t)
        return calculate_apd_snr(il, t, M=self.gain, B=bandwidth, F=self.F, R=R, dark_current=dark_current)

    def estimate_thermal_carrier_currents(self, t=0, bw=1):
        return estimate_thermal_carrier_currents(t, bw, self.dark_measurement_bw_, self.dark_current_, self.t_dark_current_)

    def calc_shot_noise_current(self, il, bandwidth, t=273):
        '''
        APD shot noise for a given photocurrent il
        q: electron charge -> As
        il: photocurrent -> A
        idg: multiplied thermal carriers -> A
        ids: non multiplied thermal carriers -> A
        M: gain -> unitless
        F: excess noise factor -> unitless
        k: ionization ratio (electrons/holes) -> unitless
        In: Apd shotnoise -> A
        B: bandwidth -> 1/s
        '''
        B = bandwidth
        sqrt = math.sqrt
        q = constants.elementary_charge
        M = self.gain

        dark_current = self.estimate_thermal_carrier_currents(t=t, bw=B) # no surface carrier contribution
        idg = dark_current/M
        F = calc_excess_noise_factor(k=self.k_, M=M)
        i_n_squared = 2*q*B*pow(M, 2)*F*(il+idg)
        return sqrt(i_n_squared)
