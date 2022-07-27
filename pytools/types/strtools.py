"""
Ce module contient des fonctions utiles pour les données de type 'str'

cutter : Découpe une chaine de caractère en segements
"""

__version__ = 0.1


def cutter(data_str:str, model:list=[])->list:
    """
    Coupe une chaine de caractère en plusieurs morceaux dont les positions de coupe sont définies selon le `model`
    
    Exemple :
        data_str := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        model := [2,6,10]
        
        la fonction cutter retourne la liste suivante :
        ['AB','CDEF','HIJK','LMNOPQRSTUVWXYZ']
    
    :param data_str: Chaine de caractères à découper
    :param model: liste des positions de coupe
        Par défaut -1 (pas de découpe)
    :type model: list
    :return: Liste des morceaux découpés
    :rtype: list
    """
    result = list()
    
    if len(model) == 0:
        result = [data_str]
    else:
        for debut, fin in zip([0]+model, model+[len(data_str)]):
            if debut!=fin:
                result += [data_str[debut:fin]]
            
    return result