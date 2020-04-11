import bpy
import os


class BPMSynchronizeAudioEdit(bpy.types.Operator):
    """Synchronize audio edit file for shots"""
    bl_idname = "bpm.synchronize_audio_edit"
    bl_label = "Synchronize audio edit"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name

    def execute(self, context):
        # import statements and functions
        from ..functions.audio_sync_functions import syncAudioEdit

        general_settings = context.window_manager.bpm_generalsettings

        syncAudioEdit(general_settings.debug, general_settings.project_folder, context.scene)
        
        return {'FINISHED'}