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
        from ..functions.file_functions import absolutePath
        from ..functions.json_functions import read_json
        from ..functions.strip_functions import deleteAllSequencerStrips, createSequencer
        from ..functions.audio_sync_functions import findShotOffsetFromSyncFile, loadSoundsFromSyncFile, createSoundStripsFromSyncFile, autoSyncAudioShot
        from ..global_variables import (
                                    sync_file_not_found_message,
                                    shot_not_used_message,
                                    shot_not_used_statement,
                                )

        general_settings = context.window_manager.bpm_generalsettings
        scn = context.scene
        debug = general_settings.debug

        state = autoSyncAudioShot(debug, general_settings.project_folder, scn)
        if state == 'SYNC_FILE_MISSING':
            self.report({'INFO'}, sync_file_not_found_message)
        elif state == 'SHOT_NOT_USED':
            self.report({'INFO'}, shot_not_used_message)

        return {'FINISHED'}