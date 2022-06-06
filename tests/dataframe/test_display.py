import unittest
from pytools.dataframe.display import *
import pandas as pd
import numpy as np

class TestShowInBrowser(unittest.TestCase):
    def setUp(self) -> None:
        # Création d'un DataFrame de 10 colonnes x 20 lignes
        self.df = pd.DataFrame(columns=[f"Col_{i}" for i in range(10)])
        for i in range(20):
            self.df = self.df.append(dict(zip(self.df.columns, np.random.random_sample(20))), ignore_index=True)

    def test_showInBrowser(self):
        self.assertIsNone(showInBrowser(self.df, name="DF de test"))


if __name__ == '__main__':
    unittest.main()
