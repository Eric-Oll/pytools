# -*- coding: utf-8 -*-

import unittest
import datetime as dt

from pytools.timetools import str_to_date
from pytools.timetools import diff_times


class TestTimetools(unittest.TestCase):

    def test_str_to_date(self):
        self.assertEqual(str_to_date('01/08/1972'), dt.date(1972, 8, 1))
        self.assertEqual(str_to_date('08/01/1972', format='MDY'), dt.date(1972, 8, 1))
        self.assertEqual(str_to_date('1972-01-08', sep='-', format='YDM'), dt.date(1972, 8, 1))
    
    def tests_prerequisite_diff_times(self):
        date1 = dt.time(1)
        date2 = 12
        self.assertRaises(TypeError, diff_times, date1, date2)
        
        date2 = dt.date(2018, 4, 15)
        self.assertRaises(TypeError, diff_times, date1, date2)
        
        date2 = dt.datetime(2018, 4, 15)
        self.assertRaises(TypeError, diff_times, date1, date2)
        
    def tests_diff_times(self):
        # time type
        date1 = dt.time(23, 30, 25)
        date2 = dt.time(18, 0)
        self.assertEqual(diff_times(date1, date2), 5 * 3600 + 30 * 60 + 25)
        self.assertEqual(diff_times(date1, date2, unit='second'), 5 * 3600 + 30 * 60 + 25)
        
        date1 = dt.time(23, 30)
        date2 = dt.time(18, 0)
        self.assertEqual(diff_times(date1, date2, unit='second'), 5 * 3600 + 30 * 60)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 330)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 5.5)
        self.assertEqual(diff_times(date1, date2, unit='day'), 5.5 / 24)
        
        # date type
        date1 = dt.date(2018, 3, 30)
        date2 = dt.date(2018, 4, 1)
        self.assertEqual(diff_times(date1, date2, unit='second'), 48 * 3600)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 48 * 60)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 48)
        self.assertEqual(diff_times(date1, date2, unit='day'), 2)

        date1 = dt.date(2018, 3, 1)
        date2 = dt.date(2018, 2, 28)
        self.assertEqual(diff_times(date1, date2, unit='second'), 24 * 3600)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 24 * 60)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 24)
        self.assertEqual(diff_times(date1, date2, unit='day'), 1)

        date1 = dt.date(2016, 4, 1)
        date2 = dt.date(2016, 2, 28)
        self.assertEqual(diff_times(date1, date2, unit='second'), 33 * 24 * 3600)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 33 * 24 * 60)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 33 * 24)
        self.assertEqual(diff_times(date1, date2, unit='day'), 33)

        # datetime type
        date1 = dt.datetime(2016, 4, 1)
        date2 = dt.datetime(2016, 2, 28)
        self.assertEqual(diff_times(date1, date2, unit='second'), 33 * 24 * 3600)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 33 * 24 * 60)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 33 * 24)
        self.assertEqual(diff_times(date1, date2, unit='day'), 33)

        date1 = dt.datetime(2018, 4, 1)
        date2 = dt.datetime(2018, 2, 28)
        self.assertEqual(diff_times(date1, date2, unit='second'), 32 * 24 * 3600)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 32 * 24 * 60)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 32 * 24)
        self.assertEqual(diff_times(date1, date2, unit='day'), 32)

        date1 = dt.datetime(2018, 4, 1, 3)
        date2 = dt.datetime(2018, 4, 2, 22)
        self.assertEqual(diff_times(date1, date2, unit='second'), 43 * 3600)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 43 * 60)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 43)
        self.assertEqual(diff_times(date1, date2, unit='day'), 43 / 24)

        date1 = dt.datetime(2018, 4, 1, 22)
        date2 = dt.datetime(2018, 4, 2, 3)
        self.assertEqual(diff_times(date1, date2, unit='second'), 5 * 3600)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 5 * 60)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 5)
        self.assertEqual(diff_times(date1, date2, unit='day'), 5 / 24)

        date1 = dt.datetime(2018, 4, 1, 22, 30)
        date2 = dt.datetime(2018, 4, 2, 3)
        self.assertEqual(diff_times(date1, date2, unit='second'), 270 * 60)
        self.assertEqual(diff_times(date1, date2, unit='minute'), 270)
        self.assertEqual(diff_times(date1, date2, unit='hour'), 270 / 60)
        self.assertEqual(diff_times(date1, date2, unit='day'), 270 / (24 * 60))


if __name__ == '__main__':
    unittest.main()
    
