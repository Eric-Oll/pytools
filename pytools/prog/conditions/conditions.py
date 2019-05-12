# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 13:41:13 2018

@author: Eric
"""
__version__ = 0.1

import collections

def if_None(valeur, default):
    """
        Retour <valeur> si elle n'est pas nulle
        Sinon retour <default>
    """
    if valeur is None:
        return default
    else:
        return valeur

def is_iterable(an_iterable):
    """
    Défine if the variable 'an_iterable' is an iterable object.
    Return :
        True if 'an_iterable' is iterable
        False else
    """
    return isinstance(an_iterable, collections.Iterable)


def between(value, borne_inf, borne_sup, exclusif=False, evaluation=all):
    """
    Test if a value is between two values.
    """
    if is_iterable(value):
        result = []
        for val in value:
            result.append(between(value=val,
                                  borne_inf=borne_inf,
                                  borne_sup=borne_sup,
                                  exclusif=exclusif,
                                  evaluation=evaluation))
        return evaluation(result)
    else:
        if exclusif:
            return value > borne_inf and value < borne_sup
        else:
            return value >= borne_inf and value <= borne_sup
