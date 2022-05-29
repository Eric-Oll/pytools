import unittest
import pandas as pd
from io import StringIO

from pytools.console.data_analysis import summarize, _type_list
from IPython.display import HTML


# User type for tests
class CustomClass:
    def __init__(self, data):
        self._data = data
        
    def __str__(self):
        return str(self._data)
    
    def __repr__(self):
        return str(self)
    
class Summarize_Test(unittest.TestCase):
    def setUp(self) -> None:
        # Création du DataFrame
        self.dataframe = pd.DataFrame(
            {
                'Col A': range(1, 10 , 1), # Liste d'entier
                'Col B': [f"Elément {i}" for i in range(1,10)], # liste de chaines
                'Col C': [float(x) for x in range(9)], # liste de décimal
                'Col D': [x if x%2==1 else None for x in range(1,10,1)], # Entier avec trous
                'Col E': [f"Elément {i}" if i%2==1 else None  for i in range(1,10)], # Chaine avec trous
                'Col F': [float(x) if x%2==1 else None for x in range(9)], # liste de décimal avec trous
                'Col G': [x if x%3==0 else float(x) if x%3==1 else f"Elément {x}" for x in range(9)],
                'Col H': [CustomClass(i) for i in range(1, 10)],  # liste de CustomClass
            }
        )
        self.empty_dataframe = pd.DataFrame()
        self.nodata_dataframe = pd.DataFrame(columns=['Col A', 'Col B', 'Col C'])
    
    def test__type_list(self):
        self.assertEqual('int', _type_list(self.dataframe.loc[:,'Col A']), "Erreur sur la colonne A")
        self.assertEqual('str', _type_list(self.dataframe.loc[:, 'Col B']), "Erreur sur la colonne B")
        self.assertEqual('float', _type_list(self.dataframe.loc[:, 'Col C']), "Erreur sur la colonne C")
        self.assertEqual('float', _type_list(self.dataframe.loc[:, 'Col D']), "Erreur sur la colonne D")
        self.assertEqual('str', _type_list(self.dataframe.loc[:, 'Col E']), "Erreur sur la colonne E")
        self.assertEqual('float', _type_list(self.dataframe.loc[:, 'Col F']), "Erreur sur la colonne F")
        self.assertListEqual(['int', 'float', 'str'], _type_list(self.dataframe.loc[:, 'Col G']), "Erreur sur la colonne G")
        self.assertEqual('CustomClass', _type_list(self.dataframe.loc[:, 'Col H']), "Erreur sur la colonne H")
        
    def test_summarize_dict(self):
        shape, desc, index = summarize(self.dataframe, output='DICT').values()
        self.assertEqual((9,8), shape, "Erreur dans les dimensions du Dataframe de données")
        self.assertEqual((shape[1],7), desc.shape, "Erreur dans la taille du Dataframe résultat.")
        print('\n',desc)
   
    def test_summarize_html(self):
        html = summarize(self.dataframe, output='HTML')
        print(type(html))
        print('\n',html)
        self.assertIsInstance(html, HTML, "Erreur dans le type renvoyé")

        
    def test_summarize_IO(self):
        output = StringIO()
        self.assertIsNone(summarize(self.dataframe, output=output), "Sortie non nulle")
        print('\n',output.getvalue())
        output.close()

    def test_summarize_empty(self):
        try:
            summarize(self.empty_dataframe)
        except Exception as err:
            self.fail("Erreur sur un DataFrame vide.\n"+str(err))

    def test_summarize_nodata(self):
        try:
            summarize(self.nodata_dataframe)
        except Exception as err:
            self.fail("Erreur sur un DataFrame sans donnée.\n"+str(err))

            
        

if __name__ == '__main__':
    unittest.main()
