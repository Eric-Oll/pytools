# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 11:59:25 2018

@author: Eric
"""

import unittest
from pytools.info.conditions import between, is_iterable


class TestBetween(unittest.TestCase):
    def test_valeur_hors_bornes(self):
        self.assertFalse(between(0, 0.5, 10))
        self.assertFalse(between(1, -1, 0))

    def test_valeur_hors_bornes_exclusif(self):
        self.assertFalse(between(0,0,1,exclusif=True))
        self.assertFalse(between(1,0,1,exclusif=True))

    def test_value_dans_bornes(self):
        self.assertTrue(between(0.5, -1,1))

    def test_value_dans_bornes_exclusif(self):
        self.assertTrue(between(0.5, -1,1, exclusif=True))

    def test_iterable_value_all(self):
        self.assertTrue(between([0, 1, 2, 3, 4, 5],
                                borne_inf=0,
                                borne_sup=10,
                                exclusif=False,
                                evaluation=all
                                )
                        )

    def test_iterable_value_all_exclusif(self):
        self.assertFalse(between([0, 1, 2, 3, 4, 5],
                                borne_inf=0,
                                borne_sup=10,
                                exclusif=True,
                                evaluation=all
                                )
                        )

    def test_iterable_value_any(self):
        self.assertTrue(between([0, 1, 2, 3, 4, 5],
                                borne_inf=0,
                                borne_sup=3,
                                exclusif=False,
                                evaluation=any
                                )
                        )

    def test_iterable_value_any_exclusif(self):
        self.assertFalse(between([0, 1, 2, 3, 4, 5],
                                borne_inf=0,
                                borne_sup=1,
                                exclusif=True,
                                evaluation=any
                                )
                        )

class TestIsIterable(unittest.TestCase):
    def testIterable(self):
        self.assertTrue(is_iterable([1,2,3,]))      # list
        self.assertTrue(is_iterable({1: 'toto'}))   # dict
        self.assertTrue(is_iterable(range(2)))      # range
        self.assertTrue(is_iterable([]))            # empty list
        self.assertTrue(is_iterable("toto"))        # string

    def testNoIterable(self):
        self.assertFalse(is_iterable(1))            # number
        self.assertFalse(is_iterable(True))         # boolean


if __name__ == '__main__':
    unittest.main()
