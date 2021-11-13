import bpy

from ..functions.audio_sync_functions import syncAudioShot
from .. import global_variables as g_var                   


class BPM_OT_synchronize_audio_shot(bpy.types.Operator):
    """Synchronize audio edit file from edit"""
    bl_idname = "bpm.synchronize_audio_shot"
    bl_label = "Synchronize audio shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'SHOT'

    def execute(self, context):       
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = winman.bpm_projectdatas.debug

        state = syncAudioShot(debug, general_settings.project_folder, context.scene)
        if state == 'SYNC_FILE_MISSING':
            self.report({'INFO'}, g_var.sync_file_not_found_message)
        elif state == 'SHOT_NOT_USED':
            self.report({'INFO'}, g_var.shot_not_used_message)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_synchronize_audio_shot)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_synchronize_audio_shot)