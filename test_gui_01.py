import bpy
from bpy.props import *

#
#     Store prooerties in the active set
#
def initSceneProperties(scn):
    bpy.types.Scene.MyX = FloatProperty(
        name = "X",
        description = "Enter a float")
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
        name = "Integer",
        description = "Enter an integer")
    scn['MyInt'] = 3
    return

initSceneProperties(bpy.context.scene)

#   tools panel
class ToolsPanel(bpy.types.Panel):
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
        layout.operator("path.execute")

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "path.execute"
    bl_label = "MakePath"
    def execute(self, context):
        scn = context.scene
        return{'FINISHED'}

#
#   registration
bpy.utils.register_module(__name__)
