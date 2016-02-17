import shapely.geometry as S
import math
from geometric_tools import *
import unittest
import random
from math import pi
from matplotlib import pyplot as plt

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
            
    def test_create_cone(self):
        p1 = S.Point(1, 0)
        p2 = S.Point(0, 1)
        p3 = S.Point(2, 1)
        p4 = S.Point(-2, -1)
        p5 = S.Point(-1, 1)
        p6 = S.Point(-1, 2)
        p7 = S.Point(-1, -2)
        p8 = S.Point(2, -1)
        
        # Test 1 :
        polygon = create_cone(p1, p3, 0.5)
        answer = S.Polygon([(0, 0), (0.5, 0), (0.5, 0.25)])
        test_result = polygon.equals(answer)
        self.assertEqual(test_result, True)
        
        # Test 2 :
        polygon = create_cone(p1, p2, 1)
        answer = S.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        test_result = polygon.equals(answer)
        self.assertEqual(test_result, True)
        
        # Test 3 :
        polygon = create_cone(p4, p1, 2)
        answer = S.Polygon([(0, 0), (-2, -1), (-2, -2), (2, -2), (2, 0)])
        test_result = polygon.equals(answer)
        self.assertEqual(test_result, True)
        
        # Test 4 :
        polygon = create_cone(p2, p4, 1)
        answer = S.Polygon([(0, 0), (0, 1), (-1, 1), (-1, -0.5)])
        test_result = polygon.equals(answer)
        self.assertEqual(test_result, True)
        
        # Test 5 :
        polygon = create_cone(p6, p7, 2)
        answer = S.Polygon([(0, 0), (-1, 2), (-2, 2), (-2, -2), (-1, -2)])
        test_result = polygon.equals(answer)
        self.assertEqual(test_result, True)
        
        # Test 6 :
        polygon = create_cone(p8, p3, 2)
        answer = S.Polygon([(0, 0), (2, -1), (2, 1)])
        test_result = polygon.equals(answer)
        self.assertEqual(test_result, True)
    
    def test_create_truncate_cone(self):
        tau = 2
        vmax = 10
        dmax = vmax * tau
        rA = rB = 4
        pA = S.Point(12, 6)
        pB = S.Point(0, 0)
        # To test this function we will assume that it is correct for at this point in time.
        center = S.Point(pB.x - pA.x, pB.y - pA.y)
        theta_c = argument(center)
        norm = distance(center, S.Point(0, 0))
        r = rA + rB
        if norm > 0:
            cos_theta = math.sqrt(norm ** 2 - r ** 2) / norm
            sin_theta = r / norm
            point1 = S.Point(norm * (math.cos(theta_c) * cos_theta + sin_theta * math.sin(theta_c)), norm * (math.sin(theta_c) * cos_theta - sin_theta * math.cos(theta_c)))
            point2 = S.Point(norm * (math.cos(theta_c) * cos_theta - sin_theta * math.sin(theta_c)), norm * (math.sin(theta_c) * cos_theta + sin_theta * math.cos(theta_c)))
        else:
            self.assertEqual(False, True)  # We crash
        # We compute the cone
        cone = create_cone(point1, point2, dmax)
        center = S.Point(center.x / tau, center.y / tau)
        # We truncate the cone
        radius = (rA + rB) / tau
        disk_plus = center.buffer(radius)
        disk_minus = S.Point(0, 0).buffer(math.sqrt(distance(center, S.Point(0, 0)) ** 2 - radius ** 2))
        answer = cone.difference(disk_minus)
        answer = answer.union(disk_plus)
        square = S.Polygon([(-dmax, -dmax), (dmax, -dmax), (dmax, dmax), (-dmax, dmax)])
        # We get the answer (i.e. what the current algorithm does when i'm writing this)
        answer = answer.intersection(square)
        # We get the result that the algorithm actualy gives
        result = create_truncate_cone(pA, rA, pB, rB, dmax, tau)[0]
        # We check if they are "equals"
        area1 = result.area
        area2 = answer.area
        area3 = result.intersection(answer).area
        self.assertEqual(area1, area3)
        self.assertEqual(area2, area3)
    
    def test_find_projection(self):
        p1 = (1, 0)
        p2 = (0, 1)
        p3 = (2, 1)
        p4 = (2, 1.5)
        p5 = (-1, 2)
        p6 = (2, -1)
        p7 = (0.5, 0.5)
        p8 = (-1, -1)
        # Test 1 :
        result = find_projection(p1, p2, p3)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 2 :
        result = find_projection(p1, p2, p4)
        answer = (0.75, 0.25)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 3 :
        result = find_projection(p1, p2, p5)
        answer = (0, 1)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 4 :
        result = find_projection(p1, p2, p6)
        answer = (1, 0)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 5 :
        result = find_projection(p1, p2, p7)
        answer = (0.5, 0.5)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 6 :
        result = find_projection(p1, p2, p8)
        answer = (0.5, 0.5)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])
        # Test 7 :
        result = find_projection(p3, p2, p8)
        answer = (0, 1)
        self.assertEqual(result[0], answer[0])
        self.assertEqual(result[1], answer[1])


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

"""
T = TestGeometricTools()
T.test_angle()
print("###")
T.test_create_cone()
T.test_create_truncate_cone()
T.test_find_projection()

tau = 1
vmax = 10
dmax = vmax * tau
rA = rB = 4
pA = S.Point(12,6)
pB = S.Point(0,0)
A = AffichePolygon()

print(distance(pA,pB))
poly = create_truncate_cone(pA, rA, pB, rB, dmax, tau)[0]
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
    plt.plot([point1.x,point2.x], [point1.y,point2.y], 'bo')
    norm2 = math.sqrt(norm ** 2 - r ** 2) / tau
    # Trigo !
    point1 = S.Point(norm2 * (math.cos(theta_c) * cos_theta + sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta - sin_theta * math.cos(theta_c)))
    point2 = S.Point(norm2 * (math.cos(theta_c) * cos_theta - sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta + sin_theta * math.cos(theta_c)))
    plt.plot([point1.x,point2.x], [point1.y,point2.y], 'yo')

A.plot_poly(poly, xrange = [-30, 30], yrange = [-30, 30])
A.plot_poly(center.buffer(r), xrange = [-30, 30], yrange = [-30, 30])
A.plot_poly(S.Point((pB.x -pA.x) /tau, (pB.y -pA.y) /tau).buffer(r/tau), xrange = [-30, 30], yrange = [-30, 30])

#
v_opt = (-7,-7)
u = find_closest(list(poly.exterior.coords), v_opt)
plt.plot([u.x,v_opt[0]], [u.y,v_opt[1]], 'go')
print(u.x, u.y)
plt.show()"""
