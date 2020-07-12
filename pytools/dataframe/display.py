# -*- coding: utf-8 -*-
"""
Ce module contient des fonctions d'affichage des objets du module Pandas.
"""

from IPython.core.display import display, HTML

def show(dataframe):
    """
    Affiche au format HTML une dataframe
    :param dataframe: Objet DataFrame à afficher
    :return: None
    """
    display(HTML(dataframe.to_html()))

