import unittest
import sys


from pytools.math.tree.node import Node

class TestNode(unittest.TestCase):
    def test__len__(self):
        # Cas de la racine
        self.assertEqual(0, len(Node("root")))

        # 1 élément
        self.assertEqual(1, len(Node("root", Node("niveau 1 - Item 1"))))

    def test_nb_children(self):
        # Cas de la racine
        self.assertEqual(0, Node("root").nb_children(),
                         "Test avec uniquement la racine")

        # 1 Niveau
        self.assertEqual(1, Node("root", Node("niveau 1 - Item 1")).nb_children(),
                         "Test avec 1 niveau et 1 éléments sur le niveau 1")

        self.assertEqual(2, Node("root",
                                 Node("niveau 1 - Item 1"),
                                 Node("Niveau 1 - Item 2"),
                                 ).nb_children(),
                         "Test avec 1 niveau et 2 éléments sur le niveau 1")

        # Niveau 2
        self.assertEqual(2, Node("root",
                                 Node("niveau 1 - Item 1",
                                      Node("Niveau 2 - 1"),
                                      item2=Node("Niveau 2 - 2")),
                                 Node("Niveau 1 - Item 2"),
                                 ).nb_children(),
                         "Test avec 2 niveau et 2 éléments sur le niveau 1")

        self.assertEqual(4, Node("root",
                                 Node("niveau 1 - Item 1",
                                      item1=Node("Niveau 2 - 1"),
                                      item2=Node("Niveau 2 - 2")),
                                 Node("Niveau 1 - Item 2"),
                                 ).nb_children(level=2),
                         "Test avec 2 niveau et 2 éléments sur le niveau 1")

        self.assertEqual(4, Node("root",
                                 Node("niveau 1 - Item 1",
                                      Node("Niveau 2 - 1"),
                                      Node("Niveau 2 - 2")),
                                 Node("Niveau 1 - Item 2"),
                                 ).nb_children(None),
                         "Test avec 2 niveau et 2 éléments sur le niveau 1")


    def test_get_depth(self):
        # Cas de la racine
        self.assertEqual(0, Node("root").get_depth(),
                         "Test avec uniquement la racine")

        # 1 Niveau
        self.assertEqual(1, Node("root", Node("niveau 1 - Item 1")).get_depth(),
                         "Test avec 1 niveau et 1 éléments sur le niveau 1")

        self.assertEqual(1, Node("root",
                                 Node("niveau 1 - Item 1"),
                                 Node("Niveau 1 - Item 2"),
                                 ).get_depth(),
                         "Test avec 1 niveau et 2 éléments sur le niveau 1")
        # Niveau 2
        self.assertEqual(2, Node("root",
                                 Node("niveau 1 - Item 1",
                                      Node("Niveau 2 - 1"),
                                      Node("Niveau 2 - 2")),
                                 Node("Niveau 1 - Item 2"),
                                 ).get_depth(),
                         "Test avec 2 niveau et 2 éléments sur le niveau 1")

if __name__ == '__main__':
    unittest.main()
