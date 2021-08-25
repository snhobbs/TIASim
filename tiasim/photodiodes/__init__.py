from tiasim import Photodiode


class S5971(Photodiode):
    """
        Hamamatsu Si PIN Photodiode
        1.2 mm diameter detector
        https://www.hamamatsu.com/resources/pdf/ssd/s5971_etc_kpin1025e.pdf
    """
    def __init__(self):
        capacitance = 4e-12 # at VR = 5 V
        responsivity = 0.4 # A/W
        super().__init__(capacitance, responsivity)

class S5973(Photodiode):
    """
        Hamamatsu Si PIN Photodiode
        0.4 mm diameter detector
        https://www.hamamatsu.com/resources/pdf/ssd/s5971_etc_kpin1025e.pdf
    """
    def __init__(self):
        capacitance = 1.6e-12  # capacitance at Vr = 3.3V
        responsivity = 0.4     # A/W
        super().__init__(capacitance, responsivity)

class S905501(Photodiode):
    """
        Hamamatsu Si PIN Photodiode
        0.1 mm diameter detector
        https://www.hamamatsu.com/resources/pdf/ssd/s9055_series_kpin1065e.pdf
    """
    def __init__(self):
        capacitance = 0.5e-12  # capacitance at Vr = 3.3V
        responsivity = 0.25     # A/W
        super().__init__(capacitance, responsivity)

class FDS015(Photodiode):
    """
        Thorlabs FDS015 Si photodiode
        https://www.thorlabs.com/thorproduct.cfm?partnumber=FDS015
        150 um diameter active area

        0.65 pF capacitance at Vr = 5 V
        TO-46 package
    """
    def __init__(self):
        capacitance = 0.65e-12
        responsivity = 0.4
        super().__init__(capacitance, responsivity)

class FGA01FC(Photodiode):
    """
        Thorlabs FGA01FC InGaAs photodiode, with FC fiber-connector
        https://www.thorlabs.com/thorproduct.cfm?partnumber=FGA01FC
        120 um diameter active area

        2.0 pF capacitance at Vr = 5 V
        TO-46 package
    """
    def __init__(self):
        capacitance = 2.0e-12
        responsivity = 1.0
        super().__init__(capacitance, responsivity)


