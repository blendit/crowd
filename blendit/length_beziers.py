import os
import sys
import subprocess
import ast
import random

script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(script_dir)

# Get system's python path
proc = subprocess.Popen('python3 -c "import sys; print(sys.path)"', stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
paths = ast.literal_eval(out.decode("utf-8"))
sys.path += (paths)


import bpy
from mathutils import *
from decimal import Decimal

# bla
import numpy as np
import shapely.geometry as S
import math

import blendit.GraphPLE as G
import blendit.classes as C
import blendit.geometric_tools as GT


# information concerning the points
class point_info:
    def __init__(point, recurrence, location):
        # point.rec > 1 means that an objects spends (point.rec - 1) time intervals being stationary in that point before moving on
        point.rec = recurrence
        point.loc = location
        # length of the segment of the path starting at this point
        point.length = 0
        # evaluation time of the keyframe that will be inserted to represent this point
        point.eval_time = 0
        

# information concerning the path
class path_info:
    def __init__(path, name, data_name, total_length, points):
        # blender attribute two names (object.name and object.data.name) to the curve
        path.name = name
        path.d_name = data_name
        # length of the path
        path.l = total_length
        # an array of the point_info objects representing the points of the path
        path.p = points


# Computing lenght of a path
def cubic(p, t):
    # Cubic bezier value:
    # Input: Four points p defining a bezier curve and a parameter t
    # Output: Coordinates of a point parameterd by t on the curve
    
    return p[0] * (1.0 - t) ** 3.0 + 3.0 * p[1] * t * (1.0 - t) ** 2.0 + 3.0 * p[2] * (t ** 2.0) * (1.0 - t) + p[3] * t ** 3.0


def getbezpoints(spl, mt, seg=0):
    # Gets a bezier segment's control points on global coordinates
    
    points = spl.bezier_points
    p0 = mt * points[seg].co
    p1 = mt * points[seg].handle_right
    p2 = mt * points[seg + 1].handle_left
    p3 = mt * points[seg + 1].co
    return p0, p1, p2, p3


def seg_lengths(obj, points):
    # Computes distances between the consecutive points of the curve
    # Every segment is divided into prec number of linear intervals whose lengths are added to obtain the length of the segment
    # PREC is set manually
    
    prec = 10000
    inc = 1 / prec

    spl = None
    mw = obj.matrix_world
    if obj.data.splines.active is None:
        if len(obj.data.splines) > 0:
            spl = obj.data.splines[0]
    else:
        spl = obj.data.splines.active

    if spl is None:
        return False
            
    # Working Part
    
    if spl.type == "BEZIER":
        total_length = 0.0
        
        for seg in range(0, len(points) - 1):
            segment_length = 0.0
            p = getbezpoints(spl, mw, seg)
            for i in range(0, prec):
                t1 = i * inc
                t2 = (i + 1) * inc
                a = cubic(p, t1)
                b = cubic(p, t2)
                r = (b - a).magnitude
                segment_length = segment_length + r
            total_length = total_length + segment_length
            points[seg].length = segment_length
    else:
        print("THIS SHOULD BE BEZIER CURVE!")
        return False
    return total_length, seg_lengths


def create_path(points):
    # Creates a curve form an array of point_info objects representing the path and outputs names of the curve
    # At the end an active object is a curve in an object mode

    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, location=(points[0].loc[0] - 1, points[0].loc[1], points[0].loc[2]))
    
    bpy.ops.curve.select_all()
    bpy.ops.curve.de_select_last()

    for i in range(len(points) - 1):
        bpy.ops.curve.vertex_add(location=points[i + 1].loc)

    bpy.ops.curve.select_all()
    bpy.ops.curve.de_select_first()
    bpy.ops.curve.delete()

    bpy.ops.object.editmode_toggle()
    
    return [bpy.context.active_object.name, bpy.context.active_object.data.name]


def get_paths(paths):
    # Generates curves from the output of "crowd program" and outputs their names, total lengths and the lengths of their segments
    
    paths_info = []
    for path in paths:
        points = get_points(path)
        [path_name, path_data_name] = create_path(points)
        [total_length, lengths_of_segments] = seg_lengths(bpy.context.active_object, points)
        paths_info.append(path_info(path_name, path_data_name, total_length, points))
    return paths_info


def evaluation_times(path, duration, length, prec=0, approx=False):
    # Computes evaluation times that will be used in the animation of an object
    # However if prec is set to an integer n>0, then eval_time
    # is multiplied by 10**n and rounded to integer. Later duration of the frames is modified
    # in such a way that a greater number of frames would correspond to the same timelapse
    # This might be interesting if dt or the timelapse between two points is smaller than duration of the frame
  
    n = len(path)
    for i in range(1, n):
        path[i].eval_time = path[i - 1].eval_time + path[i - 1].length * duration / length
        # print(path[i].eval_time)
        # Decimal(path[i - 1].length * duration / length)
        if (prec != 0 or approx):
            path[i].eval_time = round(path[i].eval_time, 0)
        # print(path[i].eval_time)
    return


def get_points(path):
    # Input: A list of lists of points in the space, every list of points represent a path. Every path has the same
    # number of points in it and an object will spend an equal amount of time between every two points of the path.
    # Two consecutive points in the path might be equal and we have to transform into the format where
    
    points = []
    n = len(path)
    count = 1
    
    if n == 1:
        return [point_info(1, path[0])]
    
    for i in range(n - 1):
        if path[i] == path[i + 1]:
            count = count + 1
        else:
            points.append(point_info(count, path[i]))
            count = 1
    
    if path[n - 1] == path[n - 2]:
        points.append(point_info(count, path[n - 1]))
    else:
        points.append(point_info(1, path[n - 1]))
    
    return points


def points_to_curves(data, dt, prec=0, approx=False, names=[]):
    # Input: data obtained from the crowd program defining the paths, dt timelapse between two points of the paths
    # prec = 0 and approximation = False, check function evaluation_times for the meaning of these variables
    # If names == [], then len(data) cubes will be created and they will follow the curves
    # Otherwise it is possible to add manually len(data) = m objects [obj_1, ..., obj_m] to the CENTER of the scene pass them with
    # names = [obj_1.name, ..., obj_m.name] and thus move them along the curves
    
    paths_info = get_paths(data)
    n = len(data[0]) - 1
    duration = n * dt * 10 ** prec
    
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = n * dt * 10 ** prec

    # Adjusts duration of the frame to precision
    bpy.context.scene.render.frame_map_old = 10**prec
    bpy.context.scene.render.frame_map_new = 1

    object = 0
    for path_info in paths_info:
        path = bpy.data.curves[path_info.d_name]
        path.path_duration = duration
        
        # Adds a cube and makes it follow the path
        if (names == []):
            bpy.ops.mesh.primitive_cylinder_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
        else:
            bpy.context.scene.objects.active = bpy.data.objects[names[object]]
            object += 1

        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        bpy.context.object.constraints["Follow Path"].target = bpy.data.objects[path_info.name]
        
        current_frame = 0
        evaluation_times(path_info.p, duration, path_info.l, prec, approx)
    
        # Sets the motion
        for i in range(0, len(path_info.p)):
            # print(path_info.p[i].eval_time)
            path.eval_time = (path_info.p[i].eval_time)
            path.keyframe_insert('eval_time', frame=current_frame)
            # print(path.eval_time)
            # print(current_frame)
            if (path_info.p[i].rec != 1):
                current_frame += (path_info.p[i].rec - 1) * dt * 10**prec
                path.keyframe_insert('eval_time', frame=current_frame)
                
            current_frame += dt * 10 ** prec


if __name__ == "__main__":
    # crados
    es = 2.23
    ew = 1.26

    graph = G.Graph(d=0.5, sizeX=100, sizeY=100, posX=0, posY=0)

    tau = 1
    cr = C.Crowd(graph, tau)

    Pos = S.Point(0, 0).buffer(0)
    Goal = S.Point(0, 0).buffer(0)
    taille = 30
    radius = 1.1
    random.seed()
    for i in range(20):
        p = S.Point(0, 0)
        while True:
            x = random.random() * taille
            y = random.random() * taille
            print("Pos : ", x, y)
            p = S.Point(x, y)
            if Pos.intersection(p.buffer(1)).is_empty or Pos.is_empty:
                break
        g = S.Point(0, 0)
        while True:
            x = random.random() * taille
            y = random.random() * taille
            print("Goal : ", x, y)
            g = S.Point(x, y)
            if Goal.intersection(g.buffer(1)).is_empty or Goal.is_empty:
                break
        """
        Pos = Pos.union(p.buffer(radius))
        Goal = Goal.union(g.buffer(radius))
        ind = C.Individual(p.x, p.y, 0, 3, 2, es, ew, radius, g)
        cr.add_indiv(ind)"""

    ind1 = C.Individual(0, 0, 0, 5, 2, es, ew, radius, S.Point(40, 40))
    ind2 = C.Individual(40, 40, 0, 5, 2, es, ew, radius, S.Point(0, 0))
    ind3 = C.Individual(40, 0, 0, 5, 2, es, ew, radius, S.Point(0, 40))
    ind4 = C.Individual(0, 40, 0, 5, 2, es, ew, radius, S.Point(40, 0))
    # ind5 = C.Individual(40, 50, 0, 5, 2, es, ew, 1, S.Point(0, 0))

    # minefield = [S.Polygon([(10, 0), (15, 0), (10, 15)])]
    # minefield = [S.Polygon([(7.5, 10), (10, 12.5), (12.5, 10), (10, 7.5)])]
    minefield = []
   
    cr.add_indiv(ind1)
    cr.add_indiv(ind2)
    cr.add_indiv(ind3)
    cr.add_indiv(ind4)

    # cr.add_indiv(ind5)
    N = 100
    cr.animate(0.05, N, minefield)

    data = cr.to_list_of_point()
    points_to_curves(data, 12)
