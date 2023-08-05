"""Test case for pysentosa.volatility
- run run_test.sh in the top folder
"""

from pysentosa.volatility import *
from unittest import TestCase, main


class TestVolatility(TestCase):

    def test_next_business_day(self):
        self.assertTrue(next_business_day('2015-12-18') == '2015-12-21')
        self.assertTrue(next_business_day('2015-12-18', 2) == '2015-12-22')
        self.assertTrue(next_business_day('2015-12-18', 5) == '2015-12-28')
        self.assertTrue(next_business_day('2015-12-26', 1) == '2015-12-28')

    def test_prev_business_day(self):
        self.assertTrue(prev_business_day('2015-12-21') == '2015-12-18')
        self.assertTrue(prev_business_day('2015-12-21', 2) == '2015-12-17')
        self.assertTrue(prev_business_day('2015-12-28', 1) == '2015-12-24')

if __name__ == '__main__':
    main()
