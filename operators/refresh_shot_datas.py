import bpy
import os


class BPMRefreshShotDatasEdit(bpy.types.Operator):
    """Refresh shot datas from edit"""
    bl_idname = "bpm.refresh_shot_datas_edit"
    bl_label = "Refresh shot datas"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name

    def execute(self, context):
        # import statements and functions
        from ..functions.project_data_functions import refreshTimelineShotDatas
        from ..global_variables import (
                                    refreshing_timeline_shot_datas_statement,
                                    refreshed_timeline_shot_datas_statement,
                                )

        winman = context.window_manager
        debug = winman.bpm_generalsettings.debug

        if debug: print(refreshing_timeline_shot_datas_statement) #debug

        refreshTimelineShotDatas(winman, context.scene.sequence_editor)

        if debug: print(refreshed_timeline_shot_datas_statement) #debug

        return {'FINISHED'}


class BPMRefreshShotDatasShot(bpy.types.Operator):
    """Refresh shot datas from shot"""
    bl_idname = "bpm.refresh_shot_datas_shot"
    bl_label = "Refresh shot datas"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type == 'SHOT':
                return True

    def execute(self, context):
        # import statements and functions
        from ..functions.project_data_functions import loadJsonDataToDataset, getShotSettingsFileFromBlend
        from ..global_variables import (
                                    shot_loading_statement,
                                    shot_loaded_statement,
                                    missing_shot_file_message,
                                    missing_shot_file_statement,
                                )

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        shot_json = getShotSettingsFileFromBlend()

        if shot_json is None:
            self.report({'INFO'}, missing_shot_file_message)
            if general_settings.debug: print(missing_shot_file_statement) #debug
            return {'FINISHED'}
    
        if general_settings.debug: print(shot_loading_statement + shot_json) #debug

        # load json in props
        shot_settings = winman.bpm_shotsettings

        general_settings.bypass_update_tag = True
        loadJsonDataToDataset(winman, shot_settings, shot_json, ())
        general_settings.bypass_update_tag = False

        if general_settings.debug: print(shot_loaded_statement) #debug

        return {'FINISHED'}


    