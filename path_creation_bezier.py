# creating a simple BEZIER path that starts on point *initial* and points are taken from list *S*
# we switched to bezier curve for many reasons but the main one is that bezier curves are an interpolation of the given points (the path actually include the parameter points) when nurbs curves are an approximation of the given points (the path does not go through the parameter points)
initial = (0, 0, 0)
S = [
    (3, 0, 0),
    (3, 3, 0),
    (6, 3, 0),
    (8, 7, 0)
]

bpy.ops.curve.primitive_bezier_curve_add(view_align=False, enter_editmode=True, location=(initial[0] + 1, initial[1], initial[2]), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

bpy.ops.curve.select_all()
bpy.ops.curve.de_select_last()
bpy.ops.curve.delete()
bpy.ops.curve.de_select_last()

for x in S:
    print(x)
    bpy.ops.curve.vertex_add(location=x)
