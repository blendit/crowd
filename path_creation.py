# creating a simple path that starts on point *initial* and points are taken from list *S*
initial = (0, 1, 0)
S = [
    (1, 1, 0),
    (1, 2, 0),
    (1, 3, 0),
    (2, 3, 0)
]

bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False, enter_editmode=True, location=(initial[0] + 2, initial[1], initial[2]), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

bpy.ops.curve.select_all()

for i in range(1, 5):
    bpy.ops.curve.de_select_last()
    bpy.ops.curve.delete()

bpy.ops.curve.de_select_last()

for x in S:
    print(x)
    bpy.ops.curve.vertex_add(location=x)
