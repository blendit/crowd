import bpy
import os
import sys
import subprocess
import ast

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
#print("MYPATH = " + str(sys.path))
#print("\n\n\n")

# Get system's python path
proc = subprocess.Popen('python3 -c "import sys; print(sys.path)"', stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
paths = ast.literal_eval(out.decode("utf-8"))
sys.path += (paths)

from bpy.types import Menu, Panel
from bpy.props import *

from mathutils import *
from decimal import Decimal

import numpy as np
import shapely.geometry as S
import math
import pickle as pic
import blendit.GraphPLE as G
import blendit.classes as C
import blendit.geometric_tools as GT
import blendit.SimulationData as Sim




def initSceneProperties(scn):
    bpy.types.Scene.NumN = IntProperty(
        name="N",
        description="Total number of individuals")
    scn['NumN'] = 2
    bpy.types.Scene.Ind = IntProperty(
        name="i",
        description="Index of the individual")
    scn['Ind'] = 0
    bpy.types.Scene.InitX = FloatProperty(
        name="X",
        description="Initial position of the individual")
    scn['InitX'] = 0
    bpy.types.Scene.InitY = FloatProperty(
        name="Y",
        description="Initial position of the individual")
    scn['InitY'] = 0
    bpy.types.Scene.GoalX = FloatProperty(
        name="X",
        description="Goal of the individual")
    scn['GoalX'] = 0
    bpy.types.Scene.GoalY = FloatProperty(
        name="Y",
        description="Goal of the individual")
    scn['GoalY'] = 0
    bpy.types.Scene.SizeT = FloatProperty(
        name="T",
        description="Size exclusion zone around the individual, can be seen as the size of the individual",
        default= 1.0)
    scn['SizeT'] = 1
    bpy.types.Scene.VMax = FloatProperty(
        name="Max Speed",
        description="Maximum Speed of the individual",
        default=3)
    scn['VMax'] = 3
    bpy.types.Scene.VOpt = FloatProperty(
        name="Optimal Speed",
        description="Optimal Speed of the individual (the algorithm makes the difference between maximal and optimal speed)",
        default=2)
    scn['VOpt'] = 2
    bpy.types.Scene.SelectSk = StringProperty(
        name="Mesh",
        description="Select a mesh/skeleton for the individual (otherwise the individual will be a simple cube)",
        subtype='FILE_PATH')
    scn['SelectSk'] = "filename.py"
    bpy.types.Scene.SelectAnim = StringProperty(
        name="Animation",
        description="Select an animation for the individual (otherwise no animation)",
        subtype='FILE_PATH')
    scn['SelectAnim'] = "filename.py"
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


class ParamButtonsPanel(Panel):
    bl_category = 'Parameters'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        
        
#    @classmethod
#    def poll(cls, context):
#        scene = context.scene
#        return scene and (scene.render.engine in cls.COMPAT_ENGINES)


class File_Tools(ParamButtonsPanel, Panel):
    bl_label = "Select from file / Save"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'SelectString')
        layout.operator("crowd.select")
        layout.prop(scn, 'SaveString')
        layout.operator("crowd.save")


class Default_Tools(ParamButtonsPanel, Panel):
    bl_label = "Set default settings"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="Size of the crowd:")
        layout.prop(scn, 'NumN', text="N")
        
        layout.label(text="Initial Position:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'DefaultInitX', text="X")
        row.prop(scn, 'DefaultInitY', text="Y")
        layout.operator("crowd.cursor_init")

        layout.label(text="Goal:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'DefaultGoalX', text="X")
        row.prop(scn, 'DefaultGoalY', text="Y")
        layout.operator("crowd.cursor_goal")

        layout.label(text="Size of exclusion zone:")
        layout.prop(scn, 'DefaultSize', text="T")

        layout.label(text="Speed of individual")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'DefaultVMax', text="Max")
        row.prop(scn, 'DefaultVOpt', text="Opt")
        
        layout.prop(scn, 'DefaultMesh', text="Mesh")
        layout.prop(scn, 'DefaultAnim', text="Animation")

        layout.label(text="Generate default crowd")
        layout.operator("crowd.default")


class Random_Tools(ParamButtonsPanel, Panel):
    bl_label = "Set random settings"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}



    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="Size of the crowd:")
        layout.prop(scn, 'NumN', text="N")
        
        layout.label(text="Initial X:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinInitX', text="Min")
        row.prop(scn, 'MaxInitX', text="Max")
        layout.label(text="Initial Y:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinInitY', text="Min")
        row.prop(scn, 'MaxInitY', text="Max")

        layout.label(text="Goal X:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinGoalX', text="Min")
        row.prop(scn, 'MaxGoalX', text="Max")
        layout.label(text="Goal Y:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinGoalY', text="Min")
        row.prop(scn, 'MaxGoalY', text="Max")

        layout.label(text="Size of exclusion zone:")
        layout.prop(scn, 'MinSize', text="Min")
        layout.prop(scn, 'MaxSize', text="Max")

        layout.label(text="Maximal speed of individual")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinVMax', text="v")
        row.prop(scn, 'MaxVMax', text="V")

        layout.label(text="Optimal speed of individual")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'MinVOpt', text="v")
        row.prop(scn, 'MaxVOpt', text="V")
        
        layout.prop(scn, 'RandomMesh', text="Mesh")
        layout.prop(scn, 'RandomAnim', text="Animation")

        layout.label(text="Generate random crowd")
        layout.operator("crowd.random")

        
class Specific_Tools(ParamButtonsPanel, Panel):
    bl_label = "Individual Settings"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="Select index of individual")
        layout.prop(scn, 'Ind', text="i")
        
        layout.label(text="Initial Position:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'InitX', text="X")
        row.prop(scn, 'InitY', text="Y")
        layout.operator("crowd.cursor_init")
        
        layout.label(text="Goal:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'GoalX', text="X")
        row.prop(scn, 'GoalY', text="Y")
        layout.operator("crowd.cursor_goal")

        layout.label(text="Size of exclusion zone:")
        layout.prop(scn, 'SizeT', text="T")

        layout.label(text="Speed of individual")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'VMax', text="Max")
        row.prop(scn, 'VOpt', text="Opt")
        
        layout.prop(scn, 'SelectSk', text="Mesh")
        layout.prop(scn, 'SelectAnim', text="Animation")

        layout.label(text="Change settings of individual i")
        layout.operator("crowd.indiv")

class Generation_Tools(ParamButtonsPanel, Panel):
    bl_label = "Generate the crowd"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.operator("crowd.generate")


class Example_Tools(ParamButtonsPanel,Panel):
    bl_label = "Example crowd"

    def draw(self,context):
        layout=self.layout
        scn = context.scene
        layout.operator("crowd.example")

        
        
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.select"
    bl_label = "Set input as crowd"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        input_file=open(scn.SelectString, "rb")
        S.imcr=pic.load(input_file)
        input_file.close()
        return{'FINISHED'}
    
    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.save"
    bl_label = "Save crowd"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        output_file=open(scn.SaveString, "wb")
        pic.dump(Sim.cr, output_file)
        output_file.close()
        return{'FINISHED'}
    
            
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.default"
    bl_label = "Default"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        for i in range(scn.NumN):
            Sim.Individuals.append(C.Individual(scn.DefaultInitX,
                                            scn.DefaultInitY,
                                            0,
                                            scn.DefaultVMax,
                                            scn.DefaultVOpt,
                                            Sim.es,
                                            Sim.ew,
                                            scn.DefaultSize,
                                            S.Point(scn.DefaultGoalX, scn.DefaultGoalY,0)))
        
        return{'FINISHED'}

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.random"
    bl_label = "Random"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        for i in range(scn.NumN):
            x = rand(scn.MinInitX, scn.MaxInitX)
            y = rand(scn.MinInitY, scn.MinInitY)
            z = 0
            vm = rand(scn.MinVMax, scn.MaxVMax)
            vo = rand(scn.MinVOpt, scn.MaxVOpt)
            es = Sim.es
            ew = Sim.ew
            t = rand(scn.MinSize, scn.MaxSize)
            gx = rand(scn.MinGoalX, scn.MaxGoalX)
            gy = rand(scn.MinGoalY, scn.MaxGoalY)
            gz = 0
            Sim.Individuals.append(C.Individual(x,y,z,vw,vo,es,ew,t,S.Point(gx,gy,gz)))
        
        return{'FINISHED'}
    

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.indiv"
    bl_label = "Set Specific"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        Sim.Individuals[scn.Ind]=C.Individual(scn.InitX,
                                    scn.InitY,
                                    0,
                                    scn.VMax,
                                    scn.VOpt,
                                    Sim.es,
                                    Sim.ew,
                                    scn.SizeT,
                                    S.Point(scn.GoalX, scn.GoalY, 0))
        scn.InitX = scn.DefaultInitX
        scn.InitY = scn.DefaultInitY
        scn.VMax = scn.DefaultVMax
        scn.VOpt = scn.DefaultVOpt
        scn.SizeT = scn.DefaultSize
        scn.GoalX = scn.DefaultGoalX
        scn.GoalY = scn.DefaultGoalY
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.cursor_init"
    bl_label = "From Cursor"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        Pcursor = view.cursor_location
        bpy.context.scene.InitX = Pcursor[0]
        bpy.context.scene.InitY = Pcursor[1]
        scn.cursor_location = (scn.InitX, scn.InitY, 0)
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.cursor_goal"
    bl_label = "From Cursor"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        Pcursor = view.cursor_location
        bpy.context.scene.GoalX = Pcursor[0]
        bpy.context.scene.GoalY = Pcursor[1]
        scn.cursor_location = (scn.GoalX, scn.GoalY, 0)
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.generate"
    bl_label = "Generate"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        Sim.reset_crowd(Sim.cr)
        for x in Sim.Individuals:
            Sim.cr.add_indiv(x)
            
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.example"
    bl_label = "Generate example"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        ind1 = C.Individual(0, 0, 0, 3, 2, Sim.es, Sim.ew, 1, S.Point(40, 50))
        ind2 = C.Individual(40, 50, 0, 3, 2, Sim.es, Sim.ew, 1, S.Point(0, 0))
        Sim.cr = C.Crowd(Sim.graph, 1)
        Sim.cr.add_indiv(ind1)
        Sim.cr.add_indiv(ind2)
            
        return{'FINISHED'}


    
    
    
bpy.utils.register_module(__name__)
