import bpy
from bpy.types import Menu, Panel
from bpy.props import *

import os
import sys
import subprocess
import ast

script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(script_dir)

# Get system's python path
proc = subprocess.Popen('python3 -c "import sys; print(sys.path)"', stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
paths = ast.literal_eval(out.decode("utf-8"))
sys.path += (paths)

import blendit/SimulationData.py as Sim
import pickle as pic

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
        min=0,
        max=100)
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
        layout.label(text="Origin Position:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'PosX')
        row.prop(scn, 'PosY')
        layout.operator("env.origin")
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

        
class Generate_Tools (ToolsButtonsPanel, Panel):
    bl_label = "Generate Map"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.operator("env.generate")
        

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.select"
    bl_label = "Set input as configuration"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        ic = open(SelectString,"rb")
        Sim.graph = pic.load(ic)
        ic.close()
        return{'FINISHED'}
    
    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.save"
    bl_label = "Save configuration"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        oc = open(SaveString, "wb")
        pic.dump(Sim.graph, oc)
        oc.close()
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
        Sim.OriginX = PosX
        Sim.OriginY = PosY
        return{'FINISHED'}
    

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.size"
    bl_label = "Set map size"

    def execute(self, context):
        scn = bpy.context.scene
        Sim.MinX = MinX
        Sim.MaxX = MaxX
        Sim.MinY = MinY
        Sim.MaxY = MaxY
        return{'FINISHED'}

    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.grid"
    bl_label = "Set Grid size"

    def execute(self, context):
        scn = bpy.context.scene
        coefficient = 5 - (GridP/20)
        Sim.Grid = Sim.MinGrid*(10**coefficient)
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "env.generate"
    bl_label = "Generate"

    def execute(self, context):
        scn = bpy.context.scene
        Sim.renew_graph()
        return{'FINISHED'}


bpy.utils.register_module(__name__)
