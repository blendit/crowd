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


class point_info:
    def __init__(point, recurrence, location):
        point.rec = recurrence
        point.loc = location
        point.length = 0
        point.eval_time = 0
        

class path_info:
    def __init__(path, name, data_name, total_length, points):
        path.name = name
        path.d_name = data_name
        path.l = total_length
        path.p = points

# Computing a lenght of a path

# cubic bezier value
# Input four points p defining a curve and a parameter t
# Coordinates of a point parameterd by t on the curve


def cubic(p, t):
    return p[0] * (1.0 - t) ** 3.0 + 3.0 * p[1] * t * (1.0 - t) ** 2.0 + 3.0 * p[2] * (t ** 2.0) * (1.0 - t) + p[3] * t ** 3.0


# Gets a bezier segment's control points on global coordinates

def getbezpoints(spl, mt, seg=0):
    points = spl.bezier_points
    p0 = mt * points[seg].co
    p1 = mt * points[seg].handle_right
    p2 = mt * points[seg + 1].handle_left
    p3 = mt * points[seg + 1].co
    return p0, p1, p2, p3


# Computes segments lengths, precision can be chosen, this is the same precision
# for every segment


def seg_lengths(obj, points):
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

# Creates a path given its points and outputs paths name
# At the an active object is a curve in an object mode


def create_path(points):

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

# Creates paths and outputs their names, lengths and lengths of their segments


def get_paths(paths):
    
    paths_info = []
    for path in paths:
        points = get_points(path)
        [path_name, path_data_name] = create_path(points)
        [total_length, lengths_of_segments] = seg_lengths(bpy.context.active_object, points)
        paths_info.append(path_info(path_name, path_data_name, total_length, points))
    return paths_info


def evaluation_times(path, duration, length, prec):
    n = len(path)
    for i in range(1, n):
        path[i].eval_time = path[i - 1].eval_time + Decimal(path[i - 1].length * duration / length)
        path[i].eval_time = round(path[i].eval_time, prec)
    return


def get_points(path):
    points = []
    n = len(path)
    count = 1
    
    if n == 1:
        return [point(path[0], 1, 0)]
    
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


# crados
es = 2.23
ew = 1.26

ind1 = C.Individual(0, 0, 0, 3, 2, es, ew, 1, S.Point(40, 50))
ind2 = C.Individual(40, 50, 0, 3, 2, es, ew, 1, S.Point(0, 0))

graph = G.Graph(d=0.5, sizeX=100, sizeY=100, posX=0, posY=0)

cr = C.Crowd(graph, 1)
# minefield = [S.Polygon([(20,10), (20, 40), (30, 50), (20,10)])]
minefield = []
cr.add_indiv(ind1)
cr.add_indiv(ind2)

cr.animate(0.1, -1, minefield)

data = cr.to_list_of_point()

def main(data, dt, prec):
    paths_info = get_paths(data)
    n = len(data[0]) - 1
    duration = n * dt * 10 ** prec
    
    scn = bpy.context.scene
    scn.frame_start = 0
    scn.frame_end = duration

    bpy.context.scene.render.frame_map_old = 10**prec
    bpy.context.scene.render.frame_map_new = 1

    for path_info in paths_info:
        path = bpy.data.curves[path_info.d_name]
        path.path_duration = duration
        bpy.ops.mesh.primitive_cube_add(radius=0.5, view_align=False, enter_editmode=False, location=(0, 0, 0))
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        bpy.context.object.constraints["Follow Path"].target = bpy.data.objects[path_info.name]
    
        current_frame = 0
        
        evaluation_times(path_info.p, duration, path_info.l, prec)
    
        for i in range(0, len(path_info.p)):
            path.eval_time = (path_info.p[i].eval_time) * 10**prec
            # print([path.eval_time, current_frame])
            path.keyframe_insert('eval_time', frame=current_frame)
            if (path_info.p[i].rec != 1):
                current_frame += (path_info.p[i].rec - 1) * dt * 10**prec
                path.keyframe_insert('eval_time', frame=current_frame)
               
            current_frame += dt * 10 ** prec
           
main(data, 20, 0)