import bpy
import os

from ..functions import json_functions as js_fct
from .. import global_variables as g_var


# save render settings
class BPM_OT_save_render_settings_to_json(bpy.types.Operator):
    """Save Render Settings to json"""
    bl_idname = "bpm.save_render_settings_json"
    bl_label = "Save Project Settings"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project # and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Save Render Settings to json file ?")
        
    def execute(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        render_settings = winman.bpm_rendersettings
        debug = winman.bpm_projectdatas.debug

        if debug: print(g_var.saving_to_json_statement)

        render_folder_path = os.path.join(general_settings.project_folder, g_var.render_folder)
        render_filepath = os.path.join(render_folder_path, g_var.render_file)

        # format the json dataset
        json_render_dataset = js_fct.initializeAssetJsonDatas({"render_settings"})
        for r in render_settings:
            r_datas = js_fct.createJsonDatasetFromProperties(r, ())
            json_render_dataset['render_settings'].append(r_datas)

        # create json file
        js_fct.create_json_file(json_render_dataset, render_filepath)

        if debug: print(g_var.saved_to_json_statement)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_save_render_settings_to_json)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_save_render_settings_to_json)