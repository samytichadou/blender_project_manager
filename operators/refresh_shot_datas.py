import bpy
import os


class BPMRefreshShotDatasEdit(bpy.types.Operator):
    """Refresh shot datas from edit"""
    bl_idname = "bpm.refresh_shot_datas_edit"
    bl_label = "Refresh shot datas"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # import statements and functions
        from ..functions.json_functions import read_json
        from ..functions.project_data_functions import loadJsonDataToDataset, refreshTimelineShotDatas
        from ..functions.strip_functions import returnShotStrips
        from ..global_variables import (
                                    refreshing_timeline_shot_datas_statement,
                                    refreshed_timeline_shot_datas_statement,
                                    shot_file,
                                )

        winman = context.window_manager
        debug = winman.bpm_generalsettings.debug

        if debug: print(refreshing_timeline_shot_datas_statement) #debug

        refreshTimelineShotDatas(winman, context.scene.sequence_editor)

        if debug: print(refreshed_timeline_shot_datas_statement) #debug

        return {'FINISHED'}