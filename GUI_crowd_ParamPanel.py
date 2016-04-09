import bpy
from bpy.types import Menu, Panel
from bpy.props import *

S = []
Index = 0


def initSceneProperties(scn):
    bpy.types.Scene.NumC = IntProperty(
        name="NumC",
        description="Number of individuals")
    scn['NumC']=2
    bpy.types.Scene.Ind = IntProperty(
        name="Ind",
        description="Index of the individual")
    scn['Ind']=0
    bpy.types.Scene.PosX = FloatProperty(
        name="PosX",
        description="position of the origin")
    scn['PosX'] = 0
    bpy.types.Scene.PosY = FloatProperty(
        name="PosY",
        description="position of the origin")
    scn['PosY'] = 0
    bpy.types.Scene.ObjX = FloatProperty(
        name="ObjX",
        description="position of the goal")
    scn['ObjX'] = 0
    bpy.types.Scene.ObjY = FloatProperty(
        name="ObjY",
        description="position of the goal")
    scn['ObjY'] = 0
    bpy.types.Scene.SizeT = FloatProperty(
        name="SizeT",
        description="Size of the individual")
    scn['SizeT'] = 1
    bpy.types.Scene.VMax = FloatProperty(
        name="Max Speed",
        description="Maximum Speed of the individual")
    scn['VMax'] = 1
    bpy.types.Scene.VOpt = FloatProperty(
        name="Optimal Speed",
        description="Optimal Speed of the individual")
    scn['VOpt'] = 1
    bpy.types.Scene.SelectSk = StringProperty(
        name="Armature",
        description="Select a skeleton for the individual",
        subtype='FILE_PATH')
    scn['SelectSk'] = "filename.py"
    bpy.types.Scene.SelectAnim = StringProperty(
        name="Animation",
        description="Select an animation for the individual",
        subtype='FILE_PATH')
    scn['SelectAnim'] = "filename.py"
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

class ParamButtonsPanel(Panel):
    bl_category = 'Parameters'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 


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
        layout.prop(scn, 'NumC', text="N")
        
        layout.label(text="Initial Position:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'PosX', text="X")
        row.prop(scn, 'PosY', text="Y")

        layout.label(text="Goal:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'ObjX', text="X")
        row.prop(scn, 'ObjY', text="Y")

        layout.label(text="Size of exclusion zone:")
        layout.prop(scn, 'SizeT', text="T")

        layout.label(text="Speed of individual")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'VMax', text="Max")
        row.prop(scn, 'VOpt', text="Opt")
        
        layout.prop(scn, 'SelectSk', text="Mesh")
        layout.prop(scn, 'SelectAnim', text="Animation")

        layout.label(text="Generate default crowd")
        layout.operator("crowd.default")

        

        

        
        
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
        row.prop(scn, 'PosX', text="X")
        row.prop(scn, 'PosY', text="Y")

        layout.label(text="Goal:")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'ObjX', text="X")
        row.prop(scn, 'ObjY', text="Y")

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
        
        

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.select"
    bl_label = "Set input as crowd"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    
    
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.save"
    bl_label = "Save crowd"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    
            
class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.default"
    bl_label = "Default"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    

class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "crowd.indiv"
    bl_label = "Set Specific"

    def execute(self, context):
        scn = bpy.context.scene
        view = bpy.context.space_data
        return{'FINISHED'}
    


    

bpy.utils.register_module(__name__)
