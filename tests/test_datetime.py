import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch

verbose = int(os.getenv('TESTVERBOSE', '2'))

class TestDateTime(unittest.TestCase):
    SENSOR_DATA = (300, 3000)

    def test_get_interval(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=verbose)