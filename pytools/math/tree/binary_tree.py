"""
Module "binary_tree.py"

Structure de données pour la representation d'un arbre binaire
------------------------------------------------------------------------------------------------------------------------
Author : Eric OLLIVIER
Create date : 04/10/2020
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : version initiale
"""

LEFT = "left"
RIGHT = "right"

class BinaryNode(Node):
    def __init__(self, name=None, left=None, right=None):
        Node.__init__(name=name, left=left, right=right)

    def get_depth_left(self):
        if self[LEFT] is None:
            return 0
        return self[LEFT].get_depth()+1

    def get_depth_rigth(self):
        if self[RIGHT] is None:
            return 0
        return self[RIGHT].get_depth()+1