import bpy
import os

from ..functions.check_file_poll_function import check_file_poll_function
from .. import global_variables as g_var
from ..functions.file_functions import deleteFolderContent


class BPM_OT_empty_recycle_bin(bpy.types.Operator):
    """Empty project recycle bin"""
    bl_idname = "bpm.empty_recycle_bin"
    bl_label = "Empty recycle bin"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        return project

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Continue ?")

    def execute(self, context):

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = context.window_manager.bpm_generalsettings

        if debug: print(g_var.starting_empty_recycle_bin_statement) #debug

        # get folders to empty
        old_folder_path = os.path.join(general_settings.project_folder, g_var.old_folder)
        for filename in os.listdir(old_folder_path):

            filepath = os.path.join(old_folder_path, filename)
            if os.path.isdir(filepath):

                if debug: print(g_var.emptying_folder_statement + filepath) #debug

                # empty folders
                deleteFolderContent(filepath)

                if debug: print(g_var.folder_emptied_statement) #debug

        if debug: print(g_var.empty_recycle_bin_completed_statement) #debug
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_empty_recycle_bin)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_empty_recycle_bin)