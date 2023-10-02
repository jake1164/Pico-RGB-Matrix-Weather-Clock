import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch

sys.modules['time'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['adafruit_ds3231'] = MagicMock()

verbose = int(os.getenv('TESTVERBOSE', '2'))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from date_utils import DateTimeProcessing

class TestDateTime(unittest.TestCase):
    SENSOR_DATA = (300, 3000)

    def make_a_DateTimeProcessing(self):
        settings = Mock()
        network = Mock()

        dtp = DateTimeProcessing(settings, network)
        return dtp


    def test_get_interval(self):
        dtp = self.make_a_DateTimeProcessing()
        interval = dtp.get_interval()
        print(f'interval: {interval}')


    def test_days_before_year(self):
        dtp = self.make_a_DateTimeProcessing()
        days = dtp._days_before_year(2001)
        print(f'days: {days}')

if __name__ == '__main__':
    unittest.main(verbosity=verbose)