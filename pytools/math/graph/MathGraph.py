# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 12:08:14 2018

@author: Eric OLLIVIER
________________________
0.1 : Version initial
0.2 :*
0.3 :*
0.4 :
    - TODO Ajout de la fonction point pour affiche un point ou une liste de points (scatter)
    - Amélioration de l'affichage des labels sur les axes
        (avec ajout des nouveaux paramètres voffset et hoffset)
    - Ajout du paramètre titre dans la création du graphique (via __init__)
    - Ajout de la représentation de l'objet (surdéfnition de __repr__)
        (affiche le titre si défini + affiche le graphique)
0.5 : Changement de système de journalisation des messages. Utilisation des objets Duck.
"""
__version__ = 0.5

from pytools.info.logger.duck import Duck

from matplotlib.patches import Circle, Wedge, Polygon

import matplotlib.pyplot as plt
import numpy as np


#from matplotlib.collections import PatchCollection
#import logging as logger
#logger.basicConfig(level=logger.DEBUG)
logger = Duck(level = Duck.INFO)

class MathGraph:

    class ALIGNEMENT:
        CENTRE = 'center'
        HAUT = 'top'
        BAS = 'bottom'
        DROITE = 'right'
        GAUCHE = 'left'

    def __init__(self, ax=None, taille=None, titre=""):
        """
        Initialise le graphique.
        - Si ax n'est pas définit, MathGraph crée automatiquement un nouvel Axes
          Sinon on utilise celui qui est définit
        - taille : définit la taille du graphique en pouce. Par défaut (5,5)
        """
        if ax is None:
            if taille is None:
                taille = (5, 5)
            self._fig, self._ax = plt.subplots(figsize=taille)
        else:
            self._ax = ax
            self._fig = ax.get_figure()
            if taille is not None:
                self._fig.set_size_inches(taille)
        self.titre(titre)

    def __repr__(self):
        if self._ax is not None:
            self.get_figure().show()

        if self._titre == "":
            return f"{self.__class__.__name__}"
        else:
            return f"{self.__class__.__name__} : {self._titre}"

    def get_axes(self):
        """
        Return l'objet Axes associé à l'objet MathGraph
        """
        return self._ax

    def get_figure(self):
        """
        Return l'objet Figure associé à l'objet MathGraph
        """
        return self._fig

    def cadre(self, actif=False):
        """
        Définit les propriétés du cadre de l'objet Axes
        """
        if not actif:
            self._ax.set_axis_off()
        return self

    def titre(self, texte=""):
        """
        Ajoute un titre au graphique
        """
        self._titre = texte
        self._ax.set_title(self._titre)
        return self

    def texte(self, position, texte,
              align_vertical=ALIGNEMENT.CENTRE,
              align_horizontal=ALIGNEMENT.CENTRE, **kwargs):
        """
        Ajoute du texte au graphique
        """
        self._ax.annotate(texte, xy=position,
                          va=align_vertical, ha=align_horizontal, **kwargs)
        return self

    def repere(self, origine=(0, 0),
                     xmin=-10, xmax=10,
                     ymin=-10, ymax=10,
                     xunit=1, yunit=1,
                     couleur='black',
                     libelle_origine=None,
                     echelle_auto=False,
                     **kwargs):
        """
        Création d'un repère graphique dans un objet de type Axes.
        Paramètre :
            ax : objet Axes où doit être dessiné le repère. Par défaut prend l'objet défini lors de la création de l'objet MathGraph
            origin : tuple (x,y) définissant l'origine du repère. Par défaut (x,y) = (0,0)
            x_limit : tuple (borne_inf, borne_sup) définissant les limites inférieur et supérieur de l'axe des abscisses'
            y_limit : tuple (borne_inf, borne_sup) définissant les limites inférieur et supérieur de l'axe des ordonnées'
            x_unit : distance entre les marques sur l'axe des abscisses
            y_unit : distance entre les marques sur l'axe des ordonnées
            couleur : définit la couleur des axes et des libellés
            libelle_origine : Définit le libelle pour le point d'origine
            echelle_auto : indicateur de mise à l'échelle automatique
            return : Retourne l'objet MathGraph (Retourne None si erreur)

            Autres paramètres :
                voffset : distance de l'étuquette à  l'axe des abscisses
                hoffset : distance de l'étiquettes à l'axe des ordonnées
        """
        ax = self._ax

        if 'voffset' in kwargs.keys():
            voffset = kwargs['voffset']
        else:  # Valeur par défaut
            voffset = (ymax - ymin) / 200

        if 'hoffset' in kwargs.keys():
            hoffset = kwargs['hoffset']
        else:  # Valeur par défaut
            hoffset = (xmax - xmin) / 200

        if self._ax is None:
            logger.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        # Axe des abscisses
        ax.hlines(y=origine[1], xmin=xmin, xmax=xmax, colors=couleur)
        for i in range(int(origine[0]) - 1, int(xmin - 1), -xunit):
            ax.vlines(x=i,
                      ymin=origine[1] - (ymax - ymin) / 200,
                      ymax=origine[1] + (ymax - ymin) / 200,
                      colors=couleur)
            ax.annotate(str(i), xy=(i, origine[1] - voffset), va='top', ha='center')

        for i in range(int(origine[0]) + 1, int(xmax + 1), xunit):
            ax.vlines(x=i,
                      ymin=origine[1] - (ymax - ymin) / 200,
                      ymax=origine[1] + (ymax - ymin) / 200,
                      colors=couleur)
            ax.annotate(str(i), xy=(i, origine[1] - voffset), va='top', ha='center')

        # Axe des ordonnées
        ax.vlines(x=origine[0], ymin=ymin, ymax=ymax, colors=couleur)
        for i in range(int(origine[1]) - 1, int(ymin - 1), -yunit):
            ax.hlines(y=i,
                      xmin=origine[0] - (xmax - xmin) / 200,
                      xmax=origine[0] + (xmax - xmin) / 200,
                      colors=couleur)
            ax.annotate(str(i), xy=(origine[1] - hoffset, i), va='center', ha='right')

        for i in range(int(origine[1]) + 1, int(ymax + 1), yunit):
            ax.hlines(y=i,
                      xmin=origine[0] - (xmax - xmin) / 200,
                      xmax=origine[0] + (xmax - xmin) / 200,
                      colors=couleur)
            ax.annotate(str(i), xy=(origine[1] - hoffset, i), va='center', ha='right')

        if libelle_origine is None:
            libelle_origine = "({},{})".format(*origine)
        ax.annotate(libelle_origine, xy=(origine[1] - hoffset, origine[1] - voffset),
                    va='top', ha='right')

        # Traitement de l'échelle
        if not echelle_auto:
            self._ax.set_xlim(left=xmin, right=xmax)
            self._ax.set_ylim(bottom=ymin, top=ymax)

        return self

    def segment(self, point1, point2, couleur='black', **kwargs):
        """
        Dessine le segment ['point1', 'point2']
        """
        self._ax.add_patch(Polygon(xy=[point1, point2], closed=False, color=couleur, **kwargs))

        return self

    def point(self, points, couleur='black', **kwargs):
        """
        Dessine un point ou une liste de points
        points : itérable (list ou array) de dimension n x 2
        """
        X = []
        Y = []
        for p in points:
            X.append(p[0])
            Y.append(p[1])
        self._ax.scatter(X, Y, c=couleur, **kwargs)

        return self

    def disque(self, centre=(0, 0), rayon=1, couleur='black', **kwargs):
        """
        Dessine un cercle de centre 'centre' et de rayon 'rayon'
        """
        if self._ax is None:
            logger.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        self._ax.add_patch(
                Circle(centre, rayon, color=couleur, fill=True, **kwargs))
        return self

    def cercle(self, centre=(0, 0), rayon=1, epaisseur=0.02, couleur='black', **kwargs):
        """
        Dessine un cercle de centre 'centre' et de rayon 'rayon'
        """
        if self._ax is None:
            logger.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        self._ax.add_patch(
                Circle(centre, rayon, color=couleur, fill=False, **kwargs))
        return self

    def arc(self, centre=(0, 0), rayon=1, angle_debut=0, angle_fin=90 ,
            epaisseur=0.02, couleur='black', **kwargs):
        """
        Dessine un cercle de centre 'centre' et de rayon 'rayon'
        """
        ax = self._ax
        if self._ax is None:
            logger.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        ax.add_patch(Wedge(centre, rayon, angle_debut, angle_fin, fill=False,
                           color=couleur, **kwargs))
        return self

    def polygone(self, liste_points=[(0, 0), (1, 0), (1, 1), (0, 1)],
                       couleur='black', style='-', **kwargs):
        """
        Dessine un polygone à partir d'une liste de points
        """
        if self._ax is None:
            logger.error("Aucun objet Axes n'est défini. Préciser le paramètre 'ax'")
            return None

        self._ax.add_patch(
                Polygon(liste_points, color=couleur, linestyle=style, fill=False, **kwargs))

#        ax.add_collection(PatchCollection(
#                [Polygon(liste_points, color=couleur, linestyle=style, fill=False)],
#                match_original=True, **kwargs))

        return self

    def vecteur(self, origine=(0, 0),
                vecteur=None, destination=None,
                couleur='black', **kwargs):
        """
        Dessine un vecteur
        """
        if vecteur is None and destination is None:
            vecteur = (1, 1);
        if vecteur is None:
            vecteur = (destination[0] - origine[0], destination[1] - origine[1])

        arrow_size = 0.02 * np.linalg.norm(self._ax.get_xlim())
        self._ax.arrow(*origine, *vecteur,
                       head_width=arrow_size, head_length=arrow_size,
                       color=couleur, length_includes_head=True, **kwargs)
        return self

    def fonction(self, f, xmin=None, xmax=None, nb_points=50, couleur='black', **kwargs):
        """
        Dessine la fonction f entre les bornes [xmin, xmax]
        avec un échantillon de 'nb_points' sur l'intervalle.

        """
        # Identification des bornes
        _xmin, _xmax = self._ax.get_xlim()
        if xmin is None:
            xmin = _xmin
        if xmax is None:
            xmax = _xmax

        # Calcul de la fonction
        X = np.linspace(xmin, xmax, nb_points).tolist()
        Y = []
        _err = []
        for x in X:
            try:
                Y.append(f(x))
                logger.debug(f"Point ({x},{Y[-1]})")
            except Exception as err:
                logger.debug(err)
                logger.warning(f"La valeur de x={x} n'est pas définie pour la fonction. Elle sera ignorée.")
                _err.append(x)
        for x in _err:
            X.remove(x)

        # Affichage de la fonction
        if len(X)>0:
            logger.debug('Affichage de la fonction pour les valeurs suivantes :', 
                      'X='+','.join([str(x) for x in X]),
                      'Y='+','.join([str(y) for y in Y]))
            self._ax.plot(X, Y, color=couleur, **kwargs)
        else:
            logger.info("Aucune valeur retenue pour cette fonction.")

        return self

# End of module MathGraph
