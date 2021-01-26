import bpy
import os


class BPM_OT_synchronize_audio_edit(bpy.types.Operator):
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

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = winman.bpm_projectdatas.debug

        syncAudioEdit(debug, general_settings.project_folder, context.scene)
        
        return {'FINISHED'}