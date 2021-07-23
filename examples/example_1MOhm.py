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


import matplotlib.pyplot as plt
import numpy

import tiasim

if __name__ == "__main__":
    
    """
        This example shows data from a photodetector built 2020-05
        PCB:            One-Inch-Photodetector, https://github.com/aewallin/One-Inch-Photodetector
        Opamp:          OPA657, SOT23-5
        Transimpedance: 1 MOhm
        CF:             not installed
        Photodiode:     S5971
    """
    P = 2.5e-6
    R_F = 1e6
    C_F = 0e-12
    C_parasitic = 0.05e-12
    
    diode = tiasim.S5971()
    #diode.capacitance = 1.6e-12
    
    opamp = tiasim.OPA657()
    opamp.AOL_gain = pow(10,70.0/20.0) # NOTE: modify to make it fit data!?
    # this could be because of capacitive load on the output??
    # MMCX connector on PCB, followed by ca 150mm thin coax, to SMA-connector.
    
    tia = tiasim.TIA( opamp, diode, R_F  , C_F, C_parasitic) 
    
    f = numpy.logspace(3,8,100)
    bw = tia.bandwidth() # bandwidth
    zm = numpy.abs( tia.ZM(f) ) # transimpedance
    
    # load experimental data
    d = numpy.genfromtxt('measurement_data/OPA657_S5791_1MOhm.csv',comments='#',delimiter=',')


    df = d.T[0]         # frequency
    d_bright =  d.T[3]
    d_bright2 = d.T[4]
    d_dark =    d.T[2]
    d_sa =      d.T[1]
    #"""
    
    print "P optical ", P*1e6 , " uW"
    print "Photocurrent ", P*0.4, " uA"
    print "DC signal (unterminated) ", R_F*P*0.4, " V"
    
    print "I shot %.2g A/sqrt(Hz)" % (numpy.sqrt(0.4*P*tiasim.q*2.0))
    print "R_F voltage ", tia.dc_output(P,100e3)
    print "Bandwidth ", bw/1e6, " MHz"
 
    print "simple bw model ", tia.bandwidth_approx()/1e6, " MHz"


    # transimpedance plot
    plt.figure(figsize=(12,10))
    plt.loglog(f,zm,'-', label='Transimpedance')
    
    plt.loglog( bw, numpy.abs(tia.ZM( bw )), 'o',label='-3 dB BW')
    plt.loglog( 0.1*bw, numpy.abs(tia.ZM( 0.1*bw )), 'o',label='BW/10')
    plt.text( bw, numpy.abs(tia.ZM( bw )), '%.3f MHz'%(bw/1e6))
    plt.ylabel('Transimpedance / Ohm')
    plt.xlabel('Frequency / Hz')
    plt.title('1 MOhm, 4 MHz Photodetector: OPA657 / S5791 / 1 MOhm (AW2020-05-02)')
    plt.xlim((1e3,30e6))
    plt.legend()
    plt.grid()
    
    # output voltage noise
    plt.figure(figsize=(12,10))
    print "amp_i"
    amp_i = tia.amp_current_noise(f)
    amp_v = tia.amp_voltage_noise(f)
    john = tia.johnson_noise(f)
    dark = tia.dark_noise(f)
    shot = tia.shot_noise(P,f)
    bright = tia.bright_noise(P, f)

    plt.loglog(f,amp_i,label='amp i-noise')
    plt.loglog(f,amp_v,label='amp v-noise')

    plt.loglog(f,john,'-.',label='R_F Johnson')
    plt.loglog(f,dark,label='Dark')
    plt.loglog(f,shot,label='shot noise P=%f uW'%(P*1e6))

    plt.loglog(f,bright,label='Bright')
    plt.loglog( tia.bandwidth(), tia.dark_noise(tia.bandwidth()),'o',label='f_-3dB = %.3f MHz'%(bw/1e6))
    plt.loglog( 0.1*tia.bandwidth(), tia.dark_noise(0.1*tia.bandwidth()),'o',label='0.1*f_-3dB')
    
    plt.ylim((1e-10,1e-5))
    plt.xlim((1e3,30e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('Output-referred voltage noise / V/sqrt(Hz)')
    plt.title('1 MOhm, 4 MHz Photodetector: OPA657 / S5791 / 1 MOhm (AW2020-05-02)')
    plt.grid()
    plt.legend()
    
    # plot measured data and compare to model
    plt.figure(figsize=(12,10))
    plt.plot(df, d_bright,'o',label='Measured bright noise @ 1 VDC output')
    plt.plot(df, d_bright2,'o',label='Measured response')
    plt.plot(df, d_dark,'o',label='Measured dark')
    plt.plot(df, d_sa,'o',label='Measured SA floor')

    rbw = 10e3
    plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f), RBW = rbw),'-',label='TIASim Dark')
    
    resistor = tiasim.v_to_dbm( numpy.sqrt( 4*tiasim.kB*tiasim.T/R_F )*R_F, RBW = rbw )
    plt.semilogx([f[0], f[-1]], [resistor, resistor],'--',label='R_F noise')
    
    
    for p in 1e-6*numpy.logspace(-1, 7, 9):
        bright = tiasim.v_to_dbm( tia.bright_noise(p, f), RBW = rbw)
        plt.plot(f, bright, label='TIASim P_shot =%.3g W'%(p))
    
    plt.xlim((1e3,30e6))
    #plt.ylim((-120,-30))
    plt.title('1 MOhm, 4 MHz Photodetector: OPA657 / S5791 / 1 MOhm (AW2020-05-02)')
    #plt.xlim((10e6,100e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    plt.grid()
    plt.legend()
    plt.show()


 
