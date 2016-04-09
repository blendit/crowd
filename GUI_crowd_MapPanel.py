import bpy
from bpy.types import Menu, Panel
from bpy.props import *

S = []
Index = 0


def initSceneProperties(scn):
    bpy.types.Scene.PosX = FloatProperty(
        name="PosX",
        description="position of the origin")
    scn['PosX'] = 0
    bpy.types.Scene.PosY = FloatProperty(
        name="PosY",
        description="position of the origin")
    scn['PosY'] = 0
    bpy.types.Scene.SizeX = FloatProperty(
        name="SizeX",
        description="Size of the map")
    scn['SizeX'] = 0
    bpy.types.Scene.SizeY = FloatProperty(
        name="SizeY",
        description="Size of the map")
    scn['SizeY'] = 0
    bpy.types.Scene.GridP = FloatProperty(
        name="GridP",
        description="Grid precision")
    scn['GridP'] = 0
    bpy.types.Scene.SelectString = StringProperty(
        name="SelectFile",
        description="Enter an input file",
        subtype='FILE_PATH')
    scn['SelectString'] = "filename.py"
    bpy.types.Scene.SaveString = StringProperty(
        name="SaveFile",
        description="Enter an output file",
        subtype='FILE_PATH')
    scn['SaveString'] = "filename.py"
    return

initSceneProperties(bpy.context.scene)


class ToolsButtonsPanel(Panel):
    bl_category = 'Map'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    
class InputFile_Tools(ToolsButtonsPanel, Panel):
    bl_label = "Input File"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'SelectString')
        layout.operator("env.select")
        layout.prop(scn, 'SaveString')
        layout.operator("env.save")

        
class MapOrigin_Tools(ToolsButtonsPanel, Panel):
    bl_label = "Map Origin"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.operator("env.origin")
        layout.prop(scn, 'PosX')
        layout.prop(scn, 'PosY')
        layout.operator("env.set")
        
        
class MapSize_Tools(ToolsButtonsPanel, Panel):
    bl_label = "Map Size"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'SizeX')
        layout.prop(scn, 'SizeY')
        layout.operator("env.size")

        
class GridSize_Tools (ToolsButtonsPanel, Panel):
    bl_label = "Grid Size"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'GridP')
        layout.operator("env.grid")
        

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.select"
    bl_label = "Set input as configuration"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    
    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.save"
    bl_label = "Save configuration"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    
            
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.origin"
    bl_label = "Get coordinates"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.set"
    bl_label = "Set map origin"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.size"
    bl_label = "Set map size"

    def execute(self, context):
        scn = bpy.context.scene
        return{'FINISHED'}

    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.grid"
    bl_label = "Set Grid size"

    def execute(self, context):
        scn = bpy.context.scene
        return{'FINISHED'}


bpy.utils.register_module(__name__)
