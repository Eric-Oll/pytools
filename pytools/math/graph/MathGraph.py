# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 12:08:14 2018

@author: Eric
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

import logging as log

class MathGraph:
    class ALIGNEMENT:
        CENTRE = 'center'
        HAUT = 'top'
        BAS = 'bottom'
        DROITE = 'right'
        GAUCHE = 'left'

    def __init__(self, ax=None):
        self._ax = ax

    def cadre(self, actif=False):
        """
        Définit les propriétés du cadre de l'objet Axes
        """
        if not actif:
            self._ax.set_axis_off()
        return self

    def titre(self,texte=""):
        """
        Ajoute un titre au graphique
        """
        self._ax.set_title(texte)
        return self

    def texte(self, position, texte,
              align_vertical=ALIGNEMENT.CENTRE,
              align_horizontal=ALIGNEMENT.CENTRE):
        """
        Ajoute du texte au graphique
        """
        self._ax.annotate(texte, xy=position,
                          va=align_vertical, ha=align_horizontal)
        return self

    def repere(self, origine=(0,0),
                     xmin=-10, xmax=10,
                     ymin=-10, ymax=10,
                     xunit=1, yunit=1,
                     couleur='black',
                     libelle_origine=None):
        """
        Création d'un repère graphique dans un objet de type Axes.
        Paramètre :
            ax : objet Axes où doit être dessiné le repère. Par défaut prend l'objet défini lors de la création de l'objet MathGraph
            origin : tuple (x,y) définissant l'origine du repère. Par défaut (x,y) = (0,0)
            x_limit : tuple (borne_inf, borne_sup) définissant les limites inférieur et supérieur de l'axe des abscisses'
            y_limit : tuple (borne_inf, borne_sup) définissant les limites inférieur et supérieur de l'axe des ordonnées'
            x_unit : distance entre les marques sur l'axe des abscisses
            y_unit : distance entre les marques sur l'axe des ordonnées
            return : Retourne l'objet MathGraph (Retourne None si erreur)
        """
        ax = self._ax

        if self._ax is None:
            log.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        # Axe des abscisses
        ax.hlines(y=origine[1], xmin=xmin, xmax=xmax, colors=couleur)
        for i in range(int(origine[0])-1, int(xmin), -xunit):
            ax.vlines(x=i,
                      ymin=origine[1]-(ymax-ymin)/200,
                      ymax=origine[1]+(ymax-ymin)/200,
                      colors=couleur)
            ax.annotate(str(i), xy=(i, origine[1]), va='top', ha='center')

        for i in range(int(origine[0])+1, int(xmax), xunit):
            ax.vlines(x=i,
                      ymin=origine[1]-(ymax-ymin)/200,
                      ymax=origine[1]+(ymax-ymin)/200,
                      colors=couleur)
            ax.annotate(str(i), xy=(i, origine[1]), va='top', ha='center')

        # Axe des ordonnées
        ax.vlines(x=origine[0], ymin=ymin, ymax=ymax, colors=couleur)
        for i in range(int(origine[1])-1, int(ymin), -yunit):
            ax.hlines(y=i,
                      xmin=origine[0]-(xmax-xmin)/200,
                      xmax=origine[0]+(xmax-xmin)/200,
                      colors=couleur)
            ax.annotate(str(i), xy=(origine[1], i), va='center', ha='right')

        for i in range(int(origine[1])+1, int(ymax), yunit):
            ax.hlines(y=i,
                      xmin=origine[0]-(xmax-xmin)/200,
                      xmax=origine[0]+(xmax-xmin)/200,
                      colors=couleur)
            ax.annotate(str(i), xy=(origine[1], i), va='center', ha='right')

        if libelle_origine is None:
            libelle_origine="({},{})".format(*origine)
        ax.annotate(libelle_origine, xy=origine, va='top', ha='right')

        return self

    def disque(self, centre=(0,0), rayon=1, couleur='black'):
        """
        Dessine un cercle de centre 'centre' et de rayon 'rayon'
        """
        ax = self._ax
        if self._ax is None:
            log.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        ax.add_collection(PatchCollection(
                [Circle(centre, rayon, color=couleur, fill=True)],
                match_original=True))
        return self

    def cercle(self, centre=(0,0), rayon=1, epaisseur=0.02, couleur='black'):
        """
        Dessine un cercle de centre 'centre' et de rayon 'rayon'
        """
        ax = self._ax
        if self._ax is None:
            log.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        ax.add_collection(PatchCollection(
                [Circle(centre, rayon, color=couleur, fill=False)],
                match_original=True))
        return self

    def arc(self, centre=(0,0), rayon=1, angle_debut=0, angle_fin=90 ,
            epaisseur=0.02, couleur='black'):
        """
        Dessine un cercle de centre 'centre' et de rayon 'rayon'
        """
        ax = self._ax
        if self._ax is None:
            log.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        p = PatchCollection(
                [Wedge(centre, rayon, angle_debut, angle_fin, fill=False, color=couleur)],
                match_original=True)
        #p.set_array(np.array([color]))
        ax.add_collection(p)
        return self

    def polygone(self, liste_points=[(0,0), (1,0), (1,1), (0,1)],
                                              couleur='black'):
        """
        Dessine un polygone à partir d'une liste de points
        """
        ax = self._ax
        if self._ax is None:
            log.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        ax.add_collection(PatchCollection(
                [Polygon(liste_points, color=couleur, fill=False)],
                match_original=True))

        return self

