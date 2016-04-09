import bpy
from bpy.types import Menu, Panel
from bpy.props import *

S = []
Index = 0


def initSceneProperties(scn):
    bpy.types.Scene.PosX = FloatProperty(
        name="X",
        description="position of the origin")
    scn['PosX'] = 0
    bpy.types.Scene.PosY = FloatProperty(
        name="Y",
        description="position of the origin")
    scn['PosY'] = 0
    bpy.types.Scene.MinX = FloatProperty(
        name="Min",
        description="Bound of the map")
    scn['MinX'] = -float("inf")
    bpy.types.Scene.MaxX = FloatProperty(
        name="Max",
        description="Bound of the map")
    scn['MaxX'] = float("inf")
    bpy.types.Scene.MinY = FloatProperty(
        name="Max",
        description="Bound of the map")
    scn['MinY'] = -float("inf")
    bpy.types.Scene.MaxY = FloatProperty(
        name="Max",
        description="Bound of the map")
    scn['MaxY'] = float("inf")
    bpy.types.Scene.GridP = FloatProperty(
        name="P",
        description="Grid precision",
        subtype='PERCENTAGE',
        min=1.03,
        max=99.96)
    scn['GridP'] = 0
    bpy.types.Scene.SelectString = StringProperty(
        name="Input",
        description="Enter an input file",
        subtype='FILE_PATH')
    scn['SelectString'] = "filename.py"
    bpy.types.Scene.SaveString = StringProperty(
        name="Output",
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
        layout.label(text="Initial Position:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'PosX')
        row.prop(scn, 'PosY')
        layout.operator("env.set")
        
        
class MapSize_Tools(ToolsButtonsPanel, Panel):
    bl_label = "Map Bounds"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="X bounds:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinX', text="Min")
        row.prop(scn, 'MaxX', text="Max")
        layout.label(text="Y bounds:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinY', text="Min")
        row.prop(scn, 'MaxY', text="Max")
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
    bl_label = "From cursor"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        Pcursor = view.cursor_location
        bpy.context.scene.PosX = Pcursor[0]
        bpy.context.scene.PosY = Pcursor[1]
        scn.cursor_location = (scn.PosX, scn.PosY, 0)
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
