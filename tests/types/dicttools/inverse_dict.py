"""
Ce module test la fonction 'inverse_dict'
-----------------------------------------------------
Créé le 17 nov. 2019

@author: Eric
-----------------------------------------------------
Histotique des versions :
0.1 :  Création de la fonction test_inverse_dict qui teste la fonction inverse_dict
"""

import unittest
from pytools.types.dicttools import inverse_dict

class TestInverseDict(unittest.TestCase):
    def test_inverse_dict(self):
        # Cas simple : bijection key/value avec chaine de caractère
        a_dict = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }
        self.assertDictEqual(inverse_dict(a_dict),
                             {
                                 'value1': 'key1',
                                 'value2': 'key2',
                                 'value3': 'key3'
                             },
                             "Cas simple : bijection key/value avec chaine de caractère")

        # Cas simple : bijection key/value avec entier
        a_dict = {1: 11, 2: 22, 3: 33}
        self.assertDictEqual(inverse_dict(a_dict),
                             {
                                 11: 1,
                                 22: 2,
                                 33: 3
                             },
                             "Cas simple : bijection key/value avec entier")

        # Cas avec valeurs communes
        a_dict = {
            'key1': 'value_of_key1',
            'key2': ['value1_of_key2', 'value2_of_key2'],
            'key3': 'value_of_key1',
        }
        self.assertDictEqual(inverse_dict(a_dict),
                             {
                                 'value_of_key1' : ['key1', 'key3'],
                                 ('value1_of_key2', 'value2_of_key2'): 'key2'
                             },
                             "Cas avec valeurs communes")


if __name__ == '__main__':
    unittest.main()
