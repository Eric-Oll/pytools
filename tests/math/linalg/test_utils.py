"""
Tests pour le module `math.linalg.utils`
"""
from unittest import TestCase
import numpy as np
from pytools.math.linalg.utils import produit_scalaire, sum_vectors, gram_schmidt
class TestLinAlgUtils(TestCase):
    def test_produit_scalaire(self):
        x = [1,2,3]
        y = [2,3,4]
        self.assertEqual(20, produit_scalaire(x,y), "Test du produit scalaire avec une liste d'entier")
        
        x = np.array(x)
        y = np.array(y)
        self.assertEqual(20, produit_scalaire(x, y), "Test du produit scalaire avec de tableau numpy d'entier")

    def test_sum_vectors(self):
        vectors_list = (
            [1, 2, 3, 4],
            [4, 3, 2, 1],
            [1, 0, 1, 0]
        )
        self.assertListEqual([6,5,6,5], sum_vectors(*vectors_list).tolist())
        
    def test_gram_schmidt(self):
        vectors_list = np.array([
            [0, 1, 1],
            [1, 1, 0],
            [1, 1, -1]
        ])
        gram_schmidt(vectors_list)
        self.assertListEqual([
            [0, 1, 1],
            [1, 0, 0],
            [0, 1, -1]
        ],
        vectors_list.tolist())