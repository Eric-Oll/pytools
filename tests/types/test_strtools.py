"""
Ce module test les fonctions du module 'strtools'
-----------------------------------------------------
Créé le 27 juil. 2022

@author: Eric Ollivier
-----------------------------------------------------
Histotique des versions :
0.1 :  Création de la fonction test_cutter qui teste la fonction cutter
"""

import unittest
from pytools.types.strtools import cutter


class TestStrTools(unittest.TestCase):
    def test_cutter(self):
        STR_TEST = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.assertListEqual(cutter(STR_TEST), [STR_TEST], "Pas de model spécifié")

        self.assertListEqual(cutter(STR_TEST, model=[0]), [STR_TEST], "Model avec césure au début")

        self.assertListEqual(cutter(STR_TEST, model=[len(STR_TEST)]), [STR_TEST], "Model avec césure à la fin")

        self.assertListEqual(cutter(STR_TEST, model=[-1]), [STR_TEST[:-1], 'Z'], "Model avec césure à l'avant dernier")
        
        self.assertListEqual(cutter(STR_TEST, model=[10]), ["1234567890", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"], "Model au milieu")
        
        self.assertListEqual(cutter(STR_TEST, model=[10,15]), ["1234567890", "ABCDE", "FGHIJKLMNOPQRSTUVWXYZ"], "Model avec césure multiple")




        
        
