import shapely.geometry as S
import math
from geometric_tools import *
import unittest
import random
from math import pi
from matplotlib import pyplot as plt
from velocity_field import *

# random.seed()


class TestGeometricTools(unittest.TestCase):
    # self.assertEqual
    def test_angle(self):
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
    # TODO : test/repare the rest of the geometric_tools file


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
        # plt.show()


class AfficheLineString():
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
        # plt.show()

"""
T = TestGeometricTools()
T.test_angle()
print("###")
#T.test_create_cone()
#T.test_create_truncate_cone()
T.test_find_projection_segment()

tau = 0.5
vmax = 10
dmax = vmax * tau
rA = rB = 4
pA = S.Point(-12,6)
pB = S.Point(0,0)
A = AffichePolygon()

print(distance(pA,pB))
cone = TruncatedCone(pA, rA, pB, rB, dmax, tau)
plt.plot([pB.x -pA.x,0], [pB.y -pA.y,0], 'ro')
plt.plot([(pB.x -pA.x) /tau,0], [(pB.y -pA.y) /tau,0], 'ro')


center = S.Point(pB.x - pA.x, pB.y - pA.y)
theta_c = argument(center)
norm = distance(center, S.Point(0, 0))
r = rA + rB
if norm > 0:
    cos_theta = math.sqrt(norm ** 2 - r ** 2) / norm
    sin_theta = r / norm
    norm2 = math.sqrt(norm ** 2 - r ** 2)
    # Trigo !
    point1 = S.Point(norm2 * (math.cos(theta_c) * cos_theta + sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta - sin_theta * math.cos(theta_c)))
    point2 = S.Point(norm2 * (math.cos(theta_c) * cos_theta - sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta + sin_theta * math.cos(theta_c)))
    plt.plot([point1.x,point2.x], [point1.y,point2.y], 'go')
    norm2 = math.sqrt(norm ** 2 - r ** 2) / tau
    # Trigo !
    point1 = S.Point(norm2 * (math.cos(theta_c) * cos_theta + sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta - sin_theta * math.cos(theta_c)))
    point2 = S.Point(norm2 * (math.cos(theta_c) * cos_theta - sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta + sin_theta * math.cos(theta_c)))
    plt.plot([point1.x,point2.x], [point1.y,point2.y], 'yo')



coords = list(cone.arc.coords)
coords_x = []
coords_y = []
for i in coords:
    coords_x.append(i[0])
    coords_y.append(i[1])
    
plt.plot(coords_x, coords_y, 'b.')
A.plot_poly(center.buffer(r), xrange = [-30, 30], yrange = [-30, 30])
A.plot_poly(S.Point((pB.x -pA.x) /tau, (pB.y -pA.y) /tau).buffer(r/tau), xrange = [-30, 30], yrange = [-30, 30])

v_opt = (-5,-4)
u = cone.find_closest(v_opt)
plt.plot([u.x,v_opt[0]], [u.y,v_opt[1]], 'mo')
print(u.x, u.y)

class Indiv:
    def __init__(self, i):
        if i == 1:
            self.x = -12
            self.y = 6
            self.vmax = 25
            self.v = S.Point(10, -10)
            self.radius = 4
        else:
            self.x = 0
            self.y = 0
            self.vmax = 25
            self.v = S.Point(0, 10)
            self.radius = 4
    
    
ind = Indiv(0)
nei = Indiv(1)
V = VelocityField(ind, tau, [])
poly = V.orca(nei, tau)
A.plot_poly(poly, xrange = [-30, 30], yrange = [-30, 30])
plt.show()
"""
