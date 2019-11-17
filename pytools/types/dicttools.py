"""
Ce module regroupe des fonctions utilitaires qui opére sur des dictionnaires.

-----------------------------------------------------
Created on 17 nov. 2019

@author: Eric
-----------------------------------------------------
Histotique des versions :
0.1 :  Création de la fonction inverse_dict
"""
__version__ = 0.1

def inverse_dict(dictionnary):
    """
    Inverse les clés et les valeurs d'un dictionnaire

    A noter : Les valeurs de type 'list' sont transformés en type tuple pour les clés.

    Exemple :
    a_dict = {
        'key1': 'value_of_key1',
        'key2': ['value1_of_key2', 'value2_of_key2'],
        'key3': 'value_of_key1',
        }

    inverse_dict(a_dict) return
    {
        'value_of_key1' : ['key1', 'key3'],
        ('value1_of_key2', 'value2_of_key2'): 'key2'
    }

    :param dictionnary: Dictionnaire à inverser
    :return: Dictionnaire inverse
    """
    dict_inv = {}
    for key, value in dictionnary.items():
        if isinstance(value, list):
            value = tuple(value)
        if value in dict_inv.keys():
            if isinstance(dict_inv[value], list):
                dict_inv[value].append(key)
            else:
                dict_inv[value] = [dict_inv[value], key]
        else:
            dict_inv[value] = key
    return dict_inv

