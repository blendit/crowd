import shapely.geometry as S
import math
from geometric_tools import *
import unittest
import random
from math import pi
from matplotlib import pyplot as plt
from velocity_field import *
import classes as C

# random.seed()


class TestGeometricTools(unittest.TestCase):
    # self.assertEqual
    def test_angle(self):
        """Test the function angle"""
        # A set of points
        p1 = S.Point(1, 0)
        p2 = S.Point(0, 1)
        p3 = S.Point(1, 1)
        p4 = S.Point(-1, -1)
        p5 = S.Point(-1, 1)
        p6 = S.Point(1, -1)
        # Test 1 :
        self.assertAlmostEqual(angle(p1, p2), pi / 2)
        self.assertAlmostEqual(angle(p2, p1), 3 * pi / 2)
        # Test 2 :
        self.assertAlmostEqual(angle(p1, p3), pi / 4)
        self.assertAlmostEqual(angle(p3, p1), 7 * pi / 4)
        # Test 3 :
        self.assertAlmostEqual(angle(p1, p4), 5 * pi / 4)
        self.assertAlmostEqual(angle(p4, p1), 3 * pi / 4)
        # Test 4 :
        self.assertAlmostEqual(angle(p5, p4), pi / 2)
        self.assertAlmostEqual(angle(p4, p5), 3 * pi / 2)
        # Test 5 :
        self.assertAlmostEqual(angle(p3, p6), 3 * pi / 2)
        self.assertAlmostEqual(angle(p6, p3), pi / 2)

    def test_find_projection_segment(self):
        """Test the find_projection_segment function"""
        p1 = (1, 0)
        p2 = (0, 1)
        p3 = (2, 1)
        p4 = (2, 1.5)
        p5 = (-1, 2)
        p6 = (2, -1)
        p7 = (0.5, 0.5)
        p8 = (-1, -1)
        # Test 1 :
        result = find_projection_segment(p1, p2, p3)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 2 :
        result = find_projection_segment(p1, p2, p4)
        answer = (0.75, 0.25)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 3 :
        result = find_projection_segment(p1, p2, p5)
        answer = (0, 1)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 4 :
        result = find_projection_segment(p1, p2, p6)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 5 :
        result = find_projection_segment(p1, p2, p7)
        answer = (0.5, 0.5)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 6 :
        result = find_projection_segment(p1, p2, p8)
        answer = (0.5, 0.5)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 7 :
        result = find_projection_segment(p3, p2, p8)
        answer = (0, 1)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])

    # TODO : automatic test for the create_truncated_cone (no idea how for now)

    def test_find_projection_half_line(self):
        p1 = (1, 0)
        p2 = (0, 1)
        p3 = (2, 1)
        p4 = (2, 1.5)
        p5 = (-1, 2)
        p6 = (2, -1)
        p7 = (0.5, 0.5)
        p8 = (-1, -1)
        # Test 1 :
        result = find_projection_half_line(p1, p2, p3)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 2 :
        result = find_projection_half_line(p1, p2, p4)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 3 :
        result = find_projection_half_line(p1, p2, p5)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 4 :
        result = find_projection_half_line(p1, p2, p6)
        answer = (2, -1)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 5 :
        result = find_projection_half_line(p1, p2, p7)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 6 :
        result = find_projection_half_line(p1, p2, p8)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 7 :
        result = find_projection_half_line(p3, p2, p8)
        answer = (2, 1)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])

    def test_in_half_plane(self):
        """Test the in_half_plane function"""
        p0 = S.Point(0, 0)
        p1 = S.Point(1, 0)
        p2 = S.Point(0, 1)
        p3 = S.Point(2, 1)
        # Test 1 :
        result = in_half_plane(p0, p1, p1)
        answer = True
        self.assertEqual(result, answer)
        # Test 2 :
        result = in_half_plane(p3, p3, p1)
        answer = False
        self.assertEqual(result, answer)
        # Test 3 :
        result = in_half_plane(p1, p3, p3)
        answer = True
        self.assertEqual(result, answer)

    def test_intersection_line_line(self):
        """Test the intersection_line_line function"""
        p0 = S.Point(0, 0)
        p1 = S.Point(1, 0)
        p2 = S.Point(0, 1)
        p3 = S.Point(2, 1)
        # Test 1 :
        result = intersection_line_line(p0, p1, p1, p2, 10)
        answer = (0, 1)
        self.assertEqual(result[0].x, answer[0])
        self.assertEqual(result[0].y, answer[1])
        # Test 2 :
        result = intersection_line_line(p3, p3, p1, p2, 10)
        answer = (4, -3)
        self.assertEqual(result[0].x, answer[0])
        self.assertEqual(result[0].y, answer[1])
        # Test 3 :
        result = intersection_line_line(p3, p3, p1, p2, 3)
        answer = []
        self.assertEqual(result, answer)
        # Test 4 :
        result = intersection_line_line(p0, p1, p0, p2, 3)
        answer = []
        self.assertEqual(result, answer)

    def test_intersection_not_empty(self):
        """Test the intersection_not_empty function"""
        p0 = S.Point(0, 0)
        p1 = S.Point(1, 1)
        p2 = S.Point(1, -1)
        p3 = S.Point(2, 2)
        circle = p0.buffer(1)  # Circle of center (0,0) and radius 1
        line1 = S.LineString([(p0.x, p0.y), (p1.x, p1.y)])
        line2 = S.LineString([(p3.x, p3.y), (p1.x, p1.y)])
        # Test 1 :
        result = intersection_not_empty(circle, line1)
        answer = True
        self.assertEqual(result, answer)
        # Test 2 :
        result = intersection_not_empty(circle, line2)
        answer = False
        self.assertEqual(result, answer)
        # Test 3 :
        result = intersection_not_empty(circle, p2)
        answer = False
        self.assertEqual(result, answer)

    def test_find_closest_to_optimal(self):
        """Test the find_closest_to_optimal function"""
        individual = C.Individual(0, 0, 0, 5, 2, 2.23, 1.26, 2, S.Point(10, 20))
        vopt = 2
        p0 = S.Point(0, 0)
        angle = math.pi / 3
        circle1 = p0.buffer(1)
        circle2 = p0.buffer(3)
        # Test 1 :
        result = find_closest_to_optimal(vopt, circle1, p0, angle, 5)
        answer = S.Point(1 / 2, math.sqrt(3) / 2)
        self.assertAlmostEqual(result.x, answer.x, places=2)
        self.assertAlmostEqual(result.y, answer.y, places=2)
        # Test 2 :
        result = find_closest_to_optimal(vopt, circle2, p0, angle, 5)
        answer = S.Point(1, math.sqrt(3))
        self.assertAlmostEqual(result.x, answer.x, places=2)
        self.assertAlmostEqual(result.y, answer.y, places=2)


class AffichePolygon():
    """Plot a polygon"""
    def plot_poly(self, poly, xrange=[-10, 10], yrange=[-10, 10]):
        x, y = poly.exterior.xy

        fig = plt.figure(1, figsize=(5, 5), dpi=90)
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_title('Polygon Edges')

        ax.set_xlim(*xrange)
        ax.set_ylim(*yrange)
        ax.set_aspect(1)
        plt.show()


class AfficheLineString():
    """Plot a LineString"""
    def plot_poly(self, poly, xrange=[-10, 10], yrange=[-10, 10]):
        x, y = poly.exterior.xy

        fig = plt.figure(1, figsize=(5, 5), dpi=90)
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_title('Polygon Edges')

        ax.set_xlim(*xrange)
        ax.set_ylim(*yrange)
        ax.set_aspect(1)
        plt.show()
