#blender text editor에 넣어서 사용
"""
2019-11-22
ydm
"""
import bpy
from os import path
import numpy as np

# message box
class MessageBoxOperator(bpy.types.Operator):
    bl_idname = "ui.show_message_box"
    bl_label = "Minimal Operator"

    def execute(self, context):
        #this is where I send the message
        self.report({'INFO'}, "This is a test")
        return {'FINISHED'}

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

# operator
class SaveToNumPy(bpy.types.Operator):
    bl_idname = 'mesh.save_to_numpy'
    bl_label = 'Save to NumPy'
    bl_options = {"REGISTER"}
 
    def execute(self, context):
        objs = bpy.context.selected_objects
        if context.scene.save_path_prop == '':
            ShowMessageBox('Save path is null', 'ERROR', 'ERROR')
            return {"FINISHED"}
        if len(objs) == 0:
            ShowMessageBox('Selected objects is zero', 'ERROR', 'ERROR')
            return {"FINISHED"}
        
        for obj in objs:
            try:
                frames = [f[0] for f in obj.animation_data.action.fcurves[0].keyframe_points.items()]

                labels = obj.pose.bones.keys()
                result = []
                for idx in frames:
                    bpy.context.scene.frame_set(idx)
                    frame_data = []
                    for bone in obj.pose.bones:
                        world_location = obj.matrix_world * bone.matrix * bone.location
                        frame_data.append(world_location)
                    result.append(frame_data)

                result = np.array(result)
                
                np.save(path.join(context.scene.save_path_prop, obj.name+'_label.npy'), labels)
                np.save(path.join(context.scene.save_path_prop, obj.name+'.npy'), result)
            except:
                ShowMessageBox('"' + obj.name + '" object process failed', 'ERROR', 'ERROR')
                
        return {"FINISHED"}
 
# panel
class panel1(bpy.types.Panel):
    bl_idname = "panel.numpy"
    bl_label = "numpy"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    # bl_category = "Tools"
    bl_category = "numpy"
 
    def draw(self, context):
        col = self.layout.column()
        col.prop(context.scene, 'save_path_prop')
        self.layout.operator("mesh.save_to_numpy", icon='MESH_CUBE', text="Save selected c3d")

def register() :
    bpy.types.Scene.save_path_prop = bpy.props.StringProperty \
        (
        name = 'Save Path',
        default = '',
        description = 'NumPy file save path',
        subtype = 'DIR_PATH'
        )
    bpy.utils.register_class(MessageBoxOperator)
    bpy.utils.register_class(SaveToNumPy)
    bpy.utils.register_class(panel1)
 
def unregister() :
    del bpy.types.Scene.save_path_prop
    bpy.utils.unregister_class(MessageBoxOperator)
    bpy.utils.unregister_class(SaveToNumPy)
    bpy.utils.unregister_class(panel1)
 
if __name__ == "__main__" :
    register()
#    unregister()