import bpy
from bpy.props import *

S = []
Index = 0


def initSceneProperties(scn):
    bpy.types.Scene.MyX = FloatProperty(
        name="X",
        description="Enter a float")
    scn['MyX'] = 0
    bpy.types.Scene.MyY = FloatProperty(
        name="Y",
        description="Enter a float")
    scn['MyY'] = 0
    bpy.types.Scene.MyZ = FloatProperty(
        name="Z",
        description="Enter a float")
    scn['MyZ'] = 0
    return

initSceneProperties(bpy.context.scene)

class ToolsPanel (bpy.types.Panel):
    bl_category = "Cursor"
    bl_label = "Cursor Utilities Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'MyX')
        layout.prop(scn, 'MyY')
        layout.prop(scn, 'MyZ')
        layout.operator("cursor.get")
        layout.operator("cursor.set")
        layout.operator("cursor.save")
        layout.operator("cursor.old")


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "cursor.get"
    bl_label = "Get Cursor Position"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        Pcursor = view.cursor_location
        bpy.context.scene.MyX = Pcursor[0]
        bpy.context.scene.MyY = Pcursor[1]
        bpy.context.scene.MyZ = Pcursor[2]
        return{'FINISHED'}

    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "cursor.set"
    bl_label = "Set Cursor Position"

    def execute(self, context):
        scn = bpy.context.scene
        scn.cursor_location = (scn.MyX, scn.MyY, scn.MyZ)
        return{'FINISHED'}

    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "cursor.save"
    bl_label = "Save Position"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        S.append((scn.MyX, scn.MyY, scn.MyZ))
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "cursor.old"
    bl_label = "Print Saved Positions"

    def execute(self, context):
        scn = bpy.context.scene
        print(S)
        return{'FINISHED'}

bpy.utils.register_module(__name__)
