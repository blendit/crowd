import bpy
from bpy.types import Menu, Panel
from bpy.props import *

from mathutils import *
from decimal import Decimal

import numpy as np
import shapely.geometry as S
import math

import blendit.GraphPLE as G
import blendit.classes as C
import blendit.geometric_tools as GT

import os
import sys
import subprocess
import ast

script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(script_dir)

# Get system's python path
proc = subprocess.Popen('python3 path.py', stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
paths = ast.literal_eval(out.decode("utf-8"))
sys.path += (paths)

S = []
Index = 0


def initSceneProperties(scn):
    bpy.types.Scene.DeltaT = FloatProperty(
        name="dt",
        description="Time quantum for the simulation")
    scn['DeltaT'] = 1.0
    bpy.types.Scene.Theta = FloatProperty(
        name="d\N{GREEK CAPITAL LETTER THETA}",
        description="Angle quantum for the simulation")
    scn['Theta'] = 1.0
    bpy.types.Scene.NumF = IntProperty(
        name="N",
        description="Number of frames to compute")
    scn['NumF'] = 1
    bpy.types.Scene.CountF = IntProperty(
        name="Count",
        description="Number of frames computed")
    scn['CountF'] = 0
    bpy.types.Scene.SelectSaveFile = StringProperty(
        name="File",
        description="Enter a file",
        subtype='FILE_PATH')
    scn['SelectSaveFile'] = "filename.py"
    return

initSceneProperties(bpy.context.scene)


class SimulButtonsPanel(Panel):
    bl_category = 'Simulation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
#    @classmethod
#    def poll(cls, context):
#        scene = context.scene
#        return scene and (scene.render.engine in cls.COMPAT_ENGINES)


class Time_Tools(SimulButtonsPanel, Panel):
    bl_label = "Parameters"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="Time Quantum:")
        layout.prop(scn, 'DeltaT', text="dt")
        layout.label(text="Angle Quantum:")
        layout.prop(scn, 'Theta', text="d\N{GREEK CAPITAL LETTER THETA}")


class Offline_Computation_Tools (SimulButtonsPanel, Panel):
    bl_label = "Offline computation"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="Number of frames")
        layout.prop(scn, 'NumF', text="N")
        layout.operator("simul.offline")
        layout.operator("simul.set_offline")


#class Online_Computation_Tools (SimulButtonsPanel, Panel):
#    bl_label = "Online computation"
#
#    def draw(self, context):
#        layout = self.layout
#        scn = context.scene
#        layout.operator("simul.online_start")
#        layout.prop(scn, "CountF", text="Counter")
#        layout.operator("simul.online_stop")
#
#
class Save_Tools(SimulButtonsPanel, Panel):
    bl_label = "Save"
#    COMPAT_ENGINES = {'BLENDER_RENDER'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'SelectSaveFile')
        layout.operator("simul.save")
        

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "simul.offline"
    bl_label = "Compute next N frames"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "simul.set_offline"
    bl_label = "Load simulation"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "simul.online_start"
    bl_label = "Start Computation"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "simul.online_stop"
    bl_label = "Stop computation"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "simul.save"
    bl_label = "Save"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}


bpy.utils.register_module(__name__)
