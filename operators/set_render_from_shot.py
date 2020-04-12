import bpy
import os


from .display_modify_render_settings import renderSettingsListCallback


class BPMSetRenderShot(bpy.types.Operator):
    """Set render from shot"""
    bl_idname = "bpm.set_render_shot"
    bl_label = "Set render"
    bl_options = {'REGISTER'}

    render_settings : bpy.props.EnumProperty(name = "Render settings", items = renderSettingsListCallback)

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'SHOT'

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'render_settings', text='') 

    def execute(self, context):
        from ..functions.file_functions import createDirectory
        from ..global_variables import (
                                    render_folder,
                                    render_shots_folder,
                                )

        general_settings = context.window_manager.bpm_generalsettings

        # get render folder
        shot_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        render_folder_path = os.path.join(general_settings.project_folder, render_folder)
        render_shot_folder_path = os.path.join(render_folder_path, render_shots_folder)
        spec_render_folder_path = os.path.join(render_shot_folder_path, self.render_settings)

        shot_folder_path = os.path.join(spec_render_folder_path, shot_name)

        # create render folder if needed
        createDirectory(shot_folder_path)

        # set render

        return {'FINISHED'}