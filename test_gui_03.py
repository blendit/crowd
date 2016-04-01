import bpy
from bpy.props import *

S = [
    (3, 0, 0),
    (0, 3, 0),
    (0, 3, 1),
    (2, -1, 1),
    (0, 1, 0),
    (2, 2, 0),
]

#
#     Store prooerties in the active set
#
def initSceneProperties(scn):
    bpy.types.Scene.MyX = FloatProperty(
        name = "X",
        default= 0.)
    scn['MyX'] = 0
    bpy.types.Scene.MyY = FloatProperty(
        name = "Y",
        description = "Enter a float")
    scn['MyY'] = 0
    bpy.types.Scene.MyZ = FloatProperty(
        name = "Z",
        description = "Enter a float")
    scn['MyZ'] = 0
    bpy.types.Scene.MyInt = IntProperty(
        name = "Iterations",
        description = "Enter a integer")
    scn['MyZ'] = 3
    bpy.types.Scene.MyString = StringProperty(
        name = "File",
        description = "Enter an input file")
    scn['MyString'] = "filename.py"
    return

initSceneProperties(bpy.context.scene)

#   tools panel
class ToolsPanel(bpy.types.Panel):
    bl_category = "SCC"
    bl_label = "Super Cool Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        layout=self.layout
        scn=context.scene
        layout.prop(scn, 'MyX')
        layout.prop(scn, 'MyY')
        layout.prop(scn, 'MyZ')
        layout.prop(scn, 'MyInt')
        layout.prop(scn, 'MyString')
        layout.operator("path.execute")

#    fancy button
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "path.execute"
    bl_label = "MakePath"
    def execute(self, context):
        scn = bpy.context.scene
        print(scn['MyX'])
        x = 0.
        y = 0.
        z = 0.
        iterations = 3
        P=(x,y,z)
        bpy.ops.curve.primitive_bezier_curve_add(view_align=False, enter_editmode=True, location=(x+ 1, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.curve.select_all()
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.delete()
        bpy.ops.curve.de_select_last()
        for i in range(iterations):
            if i >= len(S):
                print("too long")
                break
            print(i)
            P=(x + S[i][0] ,y + S[i][1], z + S[i][2])
            bpy.ops.curve.vertex_add(location=P)
        return{'FINISHED'}

#
#   registration
bpy.utils.register_module(__name__)
