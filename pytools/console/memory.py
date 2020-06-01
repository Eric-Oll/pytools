"""
Module regroupant des fonctions utilitaires de gestion de la mémoire

-----------------------------------------------------
Created on 14 déc. 2019

@author: Eric Ollivier
"""
import sys, re
import pandas as pd
from pytools.info.logger.duck import Duck
logger = Duck(level=Duck.DEBUG)

def history_size(dict_vars, filter_func=None):
    """
    Donne la taille de objet du dictionnaire `dict_vars` (utiliser la fonctions vars())
    :param dict_vars: dictionnaire donnant la liste des noms d'objet (key=nom, value=objet)
    :param filter_func: Fonctionn de filtrage sur le nom de l'objet.
        Doit retourné True si sélectionné, False sinon.
    :return: objet de type pandas.DataFrame avec les colonnes suivantes :
        - NAME : Nom de l'objet
        - SIZE : Taille mémoire de l'objet
    """
    result = pd.DataFrame(columns=['NAME', 'SIZE'])
    logger.debug(f"{__name__}.history_size : liste des variables",vars())
    for item in filter(filter_func, dict_vars.keys()):
        try:
            result = result.append({'NAME': item,
                                    'SIZE': sys.getsizeof(dict_vars[item])},
                                   ignore_index=True)
        except Exception as err:
            logger.error(f"{__name__}.history_size : Erreur sur l'objet '{item}'",
                         str(err))
    return result

def clear_history(objects_list, names_list=None, name_mask=None, min_size=None, max_size=None):
    """
    Supprime les objets du dictionnaire `objects_list` repondant aux critères de nom et de taille
    :param objects_list: dictionnarire fournissant la liste des objets.
    :param names_list: liste des noms d'objet éligibles à la suppression
    :param name_mask: Masque de noms d'objet éligible à la suppression
    :param min_size: Taille minimal d'éiligibilité pour la suppression
    :param max_size: Taille maximal d'éligibilité pour la suppression
    :return:
    """
    for obj_key in objects_list:
        to_delete = names_list is None or obj_key in names_list
        to_delete = to_delete and (name_mask is None or re.search(name_mask, obj_key))
        to_delete = to_delete and (min_size is None or sys.getsizeof(objects_list[obj_key])>=min_size)
        to_delete = to_delete and (max_size is None or sys.getsizeof(objects_list[obj_key])<=max_size)

        if to_delete:
            logger.debug(f"{__name__}.clear_history : Suppression de l'objet '{obj_key}'")
            try:
                del objects_list[obj_key]
            except Exception as err:
                logger.error(f"{__name__}.clear_history : Erreur sur l'objet '{obj_key}'.",
                             f'{obj_key}' : {repr(objects_list[obj_key])}',
                             str(err))

