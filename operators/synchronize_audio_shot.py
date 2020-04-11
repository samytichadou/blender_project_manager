import bpy
import os


class BPMSynchronizeAudioShot(bpy.types.Operator):
    """Synchronize audio edit file from edit"""
    bl_idname = "bpm.synchronize_audio_shot"
    bl_label = "Synchronize audio shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'SHOT'

    def execute(self, context):
        # import statements and functions
        from ..functions.audio_sync_functions import syncAudioShot
        from ..global_variables import (
                                    sync_file_not_found_message,
                                    shot_not_used_message,
                                )

        general_settings = context.window_manager.bpm_generalsettings

        state = syncAudioShot(general_settings.debug, general_settings.project_folder, context.scene)
        if state == 'SYNC_FILE_MISSING':
            self.report({'INFO'}, sync_file_not_found_message)
        elif state == 'SHOT_NOT_USED':
            self.report({'INFO'}, shot_not_used_message)

        return {'FINISHED'}