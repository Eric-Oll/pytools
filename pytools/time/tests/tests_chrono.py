# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 11:18:49 2018

@author: Eric
"""

import unittest
import datetime as dt

from pytools.time.chrono import Chrono


class TestChrono(unittest.TestCase):

    def setUp(self):
        self.timer = Chrono()

    def test_add_mark_first(self):
        self.timer.add_mark()
        self.assertEqual(len(self.timer), 1)
        self.assertIn(Chrono.FIRST_MARK, self.timer._marks_.keys())

    def test_add_mark_first_valued(self):
        self.timer.add_mark(value=dt.time(23, 30, 25))
        self.assertEqual(len(self.timer), 1)
        self.assertIn(Chrono.FIRST_MARK, self.timer._marks_.keys())
        self.assertDictEqual(self.timer._marks_,
                             {Chrono.FIRST_MARK:dt.time(23, 30, 25)})

    def test_add_mark_last(self):
        self.timer.add_mark()
        self.timer.add_mark()
        self.assertEqual(len(self.timer), 2)
        self.assertIn(Chrono.LAST_MARK, self.timer._marks_.keys())

    def test_add_mark_named(self):
        mark_name = 'foo'
        self.timer.add_mark(name=mark_name)
        self.assertEqual(len(self.timer), 1)
        self.assertIn(mark_name, self.timer._marks_.keys())

    def test_delta(self):
        self.timer.add_mark('time1', dt.time(23, 30, 25))
        self.timer.add_mark('time2', dt.time(18, 0))
        self.assertEqual(self.timer.delta('time1', 'time2'), 5 * 3600 + 30 * 60 + 25)


if __name__ == '__main__':
    unittest.main()
