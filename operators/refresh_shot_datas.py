import bpy
import os


from ..functions.project_data_functions import refreshTimelineShotDatas, loadJsonDataToDataset, getShotSettingsFileFromBlend
from ..functions.reload_comments_function import reload_comments
from ..global_variables import (
                                refreshing_timeline_shot_datas_statement,
                                refreshed_timeline_shot_datas_statement,
                                shot_loading_statement,
                                shot_loaded_statement,
                                missing_shot_file_message,
                                missing_shot_file_statement,
                            )


class BPM_OT_refresh_edit_datas(bpy.types.Operator):
    """Refresh timeline datas from edit"""
    bl_idname = "bpm.refresh_edit_datas"
    bl_label = "Refresh timeline datas"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name

    def execute(self, context):
        
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug

        if debug: print(refreshing_timeline_shot_datas_statement) #debug

        refreshTimelineShotDatas(context, context.scene.sequence_editor)

        if debug: print(refreshed_timeline_shot_datas_statement) #debug

        return {'FINISHED'}


# refresh shot datas func
def refresh_shot_datas(context):
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug
    general_settings = winman.bpm_generalsettings

    shot_json = getShotSettingsFileFromBlend()

    if shot_json is None:
        return False

    if debug: print(shot_loading_statement + shot_json) #debug

    # load json in props
    shot_settings = winman.bpm_shotsettings

    general_settings.bypass_update_tag = True
    loadJsonDataToDataset(winman, shot_settings, shot_json, ("shot_version"))
    general_settings.bypass_update_tag = False

    # refresh comments
    reload_comments(context, "shot", None)

    if debug: print(shot_loaded_statement) #debug

    return True


class BPM_OT_refresh_shot_datas(bpy.types.Operator):
    """Refresh shot datas from shot"""
    bl_idname = "bpm.refresh_shot_datas"
    bl_label = "Refresh shot datas"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type == 'SHOT':
                return True

    def execute(self, context):

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug

        if not refresh_shot_datas(context):
            self.report({'INFO'}, missing_shot_file_message)
            return {'FINISHED'}
    
        return {'FINISHED'}