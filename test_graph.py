import unittest
from blendit.GraphPLE import Node, Edge, Graph, distance
from random import randint
from math import sqrt


class TestClassNode(unittest.TestCase):
    def test_distance(self):
        x1 = randint(1, 10000)
        x2 = randint(1, 10000)
        y1 = randint(1, 10000)
        y2 = randint(1, 10000)
        z1 = randint(1, 10000)
        z2 = randint(1, 10000)

        dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

        n1 = Node(x1, y1, z1)
        n2 = Node(x2, y2, z2)

        d1 = n1.distance_euclidian(n2)
        d2 = n2.distance_euclidian(n1)

        self.assertEqual(d1, dist)
        self.assertEqual(d2, dist)


class TestClassEdge(unittest.TestCase):
    def test_distance(self):
        x1 = randint(1, 10000)
        x2 = randint(1, 10000)
        y1 = randint(1, 10000)
        y2 = randint(1, 10000)
        z1 = randint(1, 10000)
        z2 = randint(1, 10000)

        dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

        n1 = Node(x1, y1, z1)
        n2 = Node(x2, y2, z2)
        e = Edge(n1, n2)
        e.base_distance_set(2)
        e.init_distance()
        self.assertEqual(e.distance, 2)

        dist *= 10.
        e.base_distance_gen(10.)
        e.init_distance()
        self.assertEqual(e.distance, dist)


class TestClassGraph(unittest.TestCase):
    def test_smallest_path(self):
        g = Graph(2, 10, 10)
        g.add_entry_point(0, 0)
        g.add_goal_point(10, 10)

        self.assertEqual(g.smallest_path_a_star(), 10 * sqrt(2))
        
        g.reset_graph()
        g.remove_entry_point()
        g.remove_goal_point()
        g.reset_graph()
        g.add_entry_point(1, 1)
        g.add_goal_point(9, 9)

        self.assertEqual(g.smallest_path_a_star(), 8 * sqrt(2))
