# get_paths function takes list of paths defined
# by their points as an input (list of lists of points)
# it generates paths in blender and outputs a list
# paths_info which stores for every path its name in blender,
# total length and a list of lengths of its segments
# now paths can be accesed through their names

import bpy
from mathutils import *

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

def seg_lengths(obj):
    
    prec = 10000
    inc = 1 / prec

    # Testing part
    if obj.type != "CURVE":
        print("THIS SHOULD BE CURVE!")
        return False
        
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
        seg_lengths = []
               
        points = spl.bezier_points
        nsegs = len(points) - 1
        
        for seg in range(0, nsegs):
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
            seg_lengths.append(segment_length)
    else:
        print("THIS SHOULD BE BEZIER CURVE!")
        return False
    return total_length, seg_lengths

# Creates a path given its points and outputs paths name
# At the an active object is a curve in an object mode


def create_path(points):

    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, location=(points[0][0] - 1, points[0][1], points[0][2]))
    
    bpy.ops.curve.select_all()
    bpy.ops.curve.de_select_last()

    for i in range(len(points) - 1):
        bpy.ops.curve.vertex_add(location=points[i + 1])

    bpy.ops.curve.select_all()
    bpy.ops.curve.de_select_first()
    bpy.ops.curve.delete()

    bpy.ops.object.editmode_toggle()
    path_name = bpy.context.active_object.name
    
    return path_name

# Creates paths and outputs their names, lengths and lengths of their segments


def get_paths(paths):
    paths_info = []
    
    for points in paths:
        path_name = create_path(points)
        [total_length, lengths_of_segments] = seg_lengths(bpy.context.active_object)
        paths_info.append([path_name, total_length, lengths_of_segments, points[0]])
        print(points[0])
         
    return paths_info

paths_info = get_paths([[[0, 0, 1], [5, 0, 1], [5, 0, 5], [0, 0, 5]], [[-2, 0, -2], [-3, 0, -13]], [[-1, -2, -1], [0, -10, 0]]])

# we print names and lengths of the paths


scn = bpy.context.scene
scn.frame_start = 0
scn.frame_end = 250

for i in range(len(paths_info)):
    path = bpy.data.curves[paths_info[i][0]]
    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
    bpy.context.object.constraints["Follow Path"].target = bpy.data.objects[paths_info[i][0]]

    path.eval_time = 0
    path.keyframe_insert('eval_time', frame=0)
            
    path.eval_time = 100
    path.keyframe_insert('eval_time', frame=251)
