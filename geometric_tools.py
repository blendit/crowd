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


def find_closest_to_optimal(vopt, obj1, center, angle):
    """Find the point of the polygone obj1 (authorised speeds) at angle that is the closest to vopt"""
    xopt = math.cos(angle)
    yopt = math.sin(angle)
    p_opt = S.Point(xopt, yopt)
    if intersection_not_empty(obj1, p_opt):
        return p_opt
    else:
        line = S.LineString([(p_opt.x, p_opt.y), (center.x, center.y)])
        obj1_ext = obj1.exterior
        return line.intersection(obj1_ext)


def dist_theta(vopt, obj1, center, angle, tau, indiv, p_goal):
    """Find the energy used if the individual goes in the direction theta"""
    p_ind = find_closest_to_optimal(vopt, obj1, center, angle)
    vind = math.sqrt(p_ind.x * p_ind.x + p_ind.y * p_ind.y)
    dist = vind * tau
    xnew = center.x + dist * math.cos(angle)
    ynew = center.y + dist * math.sin(angle)
    L = math.sqrt((xnew - p_goal.x) * (xnew - p_goal.x) + (ynew - p_goal.y) * (ynew - p_goal.y))  # Result of A*
    energy = tau * (indiv.es + indiv.ew * vind * vind) + 2 * L * math.sqrt(indiv.es * indiv.ew)
    return energy


def best_angle(vopt, obj1, center, tau, dtheta, indiv):
    """Find the best angle and the speed vector corresponding"""
    act_ang = 0
    min_energy = dist_theta(vopt, obj1, center, act_ang, tau, indiv)
    best_ang = 0
    while (ang < 2 * math.pi):  # If angles are not in degree
        act_ang += dtheta
        energy = dist_theta(vopt, obj1, center, act_ang, tau, indiv)
        if energy < min_energy:
            min_energy = energy
            best_ang = act_ang
    v = find_closest_to_optimal(vopt, obj1, center, best_angle):
    return (best_ang, v)
