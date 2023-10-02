import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch

sys.modules['board'] = MagicMock()
sys.modules['analogio'] = MagicMock()

verbose = int(os.getenv('TESTVERBOSE', '2'))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from light_sensor import LightSensor



class TestLightSensor(unittest.TestCase):
    """
        Tests for the LightSensor Class
    """
    # constants go here.
    SENSOR_DATA = (999, 3000)
    def make_a_LightSensor(self):
        settings = Mock()

        light_sensor = LightSensor(settings)

        return light_sensor


    def test_get_voltage(self):
        ls = self.make_a_LightSensor()
        volts = ls._get_voltage()

        print(f'volts: {volts}')



if __name__ == '__main__':
    unittest.main(verbosity=verbose)