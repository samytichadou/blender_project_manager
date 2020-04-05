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
        from ..functions.project_data_functions import loadJsonDataToDataset
        from ..global_variables import (
                                    shot_file,
                                )

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        scn = context.scene
        avoid_list = ('is_shot', 'shot_version', 'shot_last_version', 'not_last_version')

        general_settings.bypass_update_tag = True

        # iterate through timeline strips
        for strip in scn.sequence_editor.sequences_all:

            if strip.type in {'SCENE'}:
                shot_settings = strip.bpm_shotsettings

                if shot_settings.is_shot:

                    # get json path
                    shot_folder = os.path.dirname(strip.scene.library.filepath)
                    shot_json = os.path.join(shot_folder, shot_file)

                    # set json datas
                    if os.path.isfile(shot_json):
                        loadJsonDataToDataset(winman, shot_settings, shot_json, avoid_list)

        general_settings.bypass_update_tag = False

        return {'FINISHED'}