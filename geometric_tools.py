import numpy as np
import shapely.geometry as S
import math


def intersection_not_empty(obj1, obj2):
    """Returns true if the intersection of the objects is empty, false otherwise"""
    intersection = obj1.intersection(obj2)
    if intersection.is_empty:
        return False
    else:
        return True


def find_closest_to_optimal(d, pA, pB):
    """Find the point(s) in [AB] whose distance to zero is the closest to d"""
    p0 = S.Point(0, 0)
    circle = p0.buffer(d).exterior
    line = S.LineString([(pA.x, pA.y), (pB.X, pB.y)])
    if intersection_not_empty(circle, line):
        return circle.intersection(line)
    else:
        # test if p0 is the point we want (special case)
        dist = circle.distance(line)
        circle_dist = circle.buffer(dist).exterior
        return circle_dist.intersection(line)


def find_closest_to_optimal(vopt, obj1, center, angle)
    """Find the point of the polygone obj1 at angle that is the closest to vopt"""
    xopt = math.cos(angle)
    yopt = math.sin(angle)
    Popt = S.Point(xopt, yopt)
    if intersection_not_empty(obj1, Popt):
        return Popt
    else:
        line = S.LineString([(Popt.x, Popt.y), (center.X, center.y)])
