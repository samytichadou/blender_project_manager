import bpy
import os

from ..functions import json_functions as js_fct
from .. import global_variables as g_var


# save project settings
class BPM_OT_save_project_settings_to_json(bpy.types.Operator):
    """Save Project Settings to json"""
    bl_idname = "bpm.save_project_settings_json"
    bl_label = "Save Project Settings"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project # and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Save Project Settings to json file ?")
        
    def execute(self, context):     
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        datas = winman.bpm_projectdatas

        if general_settings.debug: print(g_var.saving_to_json_statement)

        project_file = os.path.join(general_settings.project_folder, g_var.file_project)

        # format the json dataset
        json_dataset = js_fct.createJsonDatasetFromProperties(datas, ("comments"))

        # create json file
        js_fct.create_json_file(json_dataset, project_file)

        if general_settings.debug: print(g_var.saved_to_json_statement)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_save_project_settings_to_json)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_save_project_settings_to_json)