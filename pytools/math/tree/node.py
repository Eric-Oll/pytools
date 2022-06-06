"""
Module "node.py"

Structure de données pour la representation d'un arbre

------------------------------------------------------------------------------------------------------------------------
Author : Eric OLLIVIER
Create date : 04/10/2020
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : Verion initial
"""


class Node:
    _ID = 0

    @classmethod
    def getId(cls):
        cls._ID += 1
        return cls._ID

    def __init__(self, name=None,  *args, parent=None, **kwargs):
        """
        Initialise le noeud
        :param args: liste des noeuds enfant
        :param kwargs:
        :param parent: noeud parent s'il est défini
        """
        self.parent = parent
        self.name = name
        self._children = dict()
        for node in args:
            if isinstance(node, Node):
                self.add_child(node)

        for key, node in kwargs.items():
            if isinstance(node, Node):
                self.add_child(node, key=key)

    def __len__(self):
        return len(self.children)

    def __getitem__(self, item):
        return self._children[item]

    @property
    def children(self):
        return self._children.values()

    def set_parent(self, parent):
        """
        Met à jour le noeud parent
        :param parent:
        :return:
        """
        self.parent = parent

    def is_root(self):
        """
        Tests si le noeud a un parent (= noeud racine)
        :return: True si racine, False sinon
        """
        return self.parent is None

    def add_child(self, child, key=None):
        """
        Ajoute un enfant au noeud
        :param child: Noeud enfant
        :return:
        """
        if isinstance(child, Node):
            self._children[self.getId() if key is None else key] = child
            child.set_parent(self)

    def nb_children(self, level=1):
        """
        Retour le nombre d'enfant jusqu'au niveau "level"
        :param level: Profondeur du niveau de recheche (par defaut level=1)
            Si level = 1 : equivaut à len
            Si level = None : tous les niveaux sont comptés
        :return: Nombre d'enfant
        """
        if level==1 : return len(self)
        return len(self) + sum([child.nb_children(level-1 if level is not None else None)
                                for child in self.children])

    def get_depth(self):
        """
        Calcul la profondeur d'un arbre à partir du noeud courant
        :return: Nombre de niveau de l'arbre (0 = Feuille)
        """
        return max([0]+[node.get_depth()+1 for node in self.children])