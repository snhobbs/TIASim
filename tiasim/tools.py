import math
from scipy import constants


def fermi_dirac_dist(t, ev=1):
    eV_per_T = constants.k/constants.electron_volt
    e1 = eV_per_T * t
    assert t > 0
    b = 1/(1+math.exp((ev-e1)/t * 1/eV_per_T))
    return b

def calc_joules_per_photon(wavelength):
    return constants.h*constants.c/(wavelength)

def photons_to_optical_power(photons, dt, wavelength):
    return photons/dt*(calc_joules_per_photon(wavelength))


'''
Calculate the johnson noise in the given bandwidth for a resistor of value rm and a temperature t in kelvin
'''
def calc_johnson_current_noise(t, rm, b):
    kb = constants.k
    return math.sqrt(4*kb*t*b/rm)

def calc_johnson_voltage_noise(t, rm, b):
    return calc_johnson_current_noise(t, rm, b)*rm
