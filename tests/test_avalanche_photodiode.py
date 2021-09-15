import unittest
from tiasim.avalanche_photodiode import AvalanchePhotodiode, estimate_thermal_carrier_currents
from scipy import constants

class DemoApd(AvalanchePhotodiode):
    def __init__(self):
        super().__init__(
            k=0.01,
            effective_area=1,
            capacitance = 0,
            leakage = 0,
            dark_current = 10e-9,
            t_dark_current = constants.convert_temperature(23, old_scale="celsius", new_scale="kelvin"),
            dark_measurement_bw = 1e6,
            gain = 100,
        )


class TestApd(unittest.TestCase):
    def setUp(self):
        self.apd = DemoApd()

    def test_estimate_thermal_carrier_currents(self):
        temp = self.apd.t_dark_current_
        F = 1#self.apd.F

        bw = 1
        dark_measurement_bw = 1
        dark_current = 1e-9
        t_dark_current = temp
        gain=self.apd.gain
        dark_current_calc = estimate_thermal_carrier_currents(temp, bw, dark_measurement_bw, dark_current, t_dark_current)
        self.assertEqual(dark_current, dark_current_calc)
        dark_current_calc_high = estimate_thermal_carrier_currents(2*temp, bw, dark_measurement_bw, dark_current, t_dark_current)
        dark_current_calc_low = estimate_thermal_carrier_currents(temp/2, bw, dark_measurement_bw, dark_current, t_dark_current)
        self.assertGreater(dark_current_calc_high, dark_current_calc)
        self.assertLess(dark_current_calc_low, dark_current_calc)


    def test_snr(self):
        self.assertEqual(self.apd.calculate_snr(il=0, bandwidth=1), 0)

if __name__ == "__main__":
    unittest.main()
