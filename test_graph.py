import unittest
from GraphPLE import Node, Edge, Graph
from random import randint
from math import sqrt


class TestClassNode(unittest.TestCase):
    def test_distance(self):
        x1 = randint(1,10000)
        x2 = randint(1,10000)
        y1 = randint(1,10000)
        y2 = randint(1,10000)
        z1 = randint(1,10000)
        z2 = randint(1,10000)

        dist = sqrt((x1-x2) ** 2 + (y1-y2) ** 2 + (z1-z2) ** 2)

        n1 = Node(x1, y1, z1)
        n2 = Node(x2, y2, z2)

        d1 = n1.distance_euclidian(n2)
        d2 = n2.distance_euclidian(n1)

        self.assertEqual(d1, dist)
        self.assertEqual(d2, dist)
        

if __name__ == '__main__':
    unittest.main()
