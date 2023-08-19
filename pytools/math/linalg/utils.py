"""
Outils sur les espaces vectoriels
"""
import numpy as np
from numpy import ndarray

def produit_scalaire(x, y):
    """
    Retourne le produit scalaire de 2 vecteurs
    Args:
        x (iteravble[float]): Vecteur
        y (iteravble[float]): Vecteur

    Returns (float): produit scalaire des vecteur x et y
    """
    return sum(x_*y_ for x_, y_ in zip(x, y))

def sum_vectors(*vectors):
    """
    Somme les vecteurs passés en argument
    Les vecteurs doivent être de même dimension
    Args:
        vectors (list[float]): liste de vecteurs

    Returns (: vecteur
    """
    result = np.zeros(len(vectors[0])) # Initialisation au vecteur nul de la même taille que le premier
    for vector in vectors:
        if isinstance(vector, ndarray):
            vector = np.array(vector)
        result = result + vector
    return result

def gram_schmidt(matrice):
    """
    Orthoganalisation par la méthode de Gram-Schmidt
    Args:
        matrice (list[list] | numpy.array): Matrice à 2 dimensions

    Returns: None
    """
    for k in range(1, len(matrice)):
        matrice[k] = matrice[k] - sum_vectors(
            *(produit_scalaire(matrice[i], matrice[k]) / produit_scalaire(matrice[i], matrice[i]) * matrice[i] for i in range(k))
        )
    