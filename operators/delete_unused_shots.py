import bpy
import os
import shutil


from ..global_variables import (
                            shot_folder, 
                            old_folder,
                            used_shots_list_statement,
                            existing_shots_list_statement,
                            unused_shots_list_statement,
                            no_unused_shots_message,
                            no_unused_shots_statement,
                            starting_delete_shots_statement,
                            starting_delete_specific_shot_statement,
                            deleting_scene_statement,
                            starting_moving_folder,
                            moved_folder_statement,
                            starting_deleting_folder,
                            deleted_folder_statement,
                        )

from ..functions.project_data_functions import getAvailableShotsList
from ..functions.strip_functions import getListSequencerShots
from ..functions.utils_functions import listDifference


class BPMDeleteUnusedShots(bpy.types.Operator):
    """Delete shots in the project not present on the timeline"""
    bl_idname = "bpm.delete_unused_shots"
    bl_label = "Delete unused shots"
    #bl_options = {}

    shots_to_remove = []
    shot_folder_path = None
    project_prefix = None
    shot_prefix = None

    permanently_delete = bpy.props.BoolProperty(name = "Permanently delete")

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_datas[0].edit_scene_keyword
        if context.window_manager.bpm_isproject and context.window_manager.bpm_filetype == 'EDIT':
            if keyword in context.scene.name:
                return True

    def invoke(self, context, event):
        # reset permanently delete
        self.permanently_delete = False

        winman = context.window_manager

        project_datas = winman.bpm_datas[0]
        project_prefix = project_datas.project_prefix
        if not project_prefix.endswith("_"): project_prefix += "_"
        self.project_prefix = project_prefix
        self.shot_prefix = project_datas.shot_prefix

        self.shot_folder_path = os.path.join(winman.bpm_projectfolder, shot_folder)
        sequencer = context.scene.sequence_editor

        # get used shot
        timeline_shots = getListSequencerShots(sequencer)

        if winman.bpm_debug: print(used_shots_list_statement + str(timeline_shots)) #debug

        # get all existing shot
        existing_shots = getAvailableShotsList(self.shot_folder_path, self.project_prefix)

        if winman.bpm_debug: print(existing_shots_list_statement + str(existing_shots)) #debug

        # find difference
        self.shots_to_remove = listDifference(existing_shots, timeline_shots)

        if winman.bpm_debug: print(unused_shots_list_statement + str(self.shots_to_remove)) #debug

        if len(self.shots_to_remove) == 0:
            self.report({'INFO'}, no_unused_shots_message)
            if winman.bpm_debug: print(no_unused_shots_statement) #debug
            return {'FINISHED'}

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        for shot in self.shots_to_remove:
            layout.label(text = shot)
        layout.prop(self, 'permanently_delete')
        layout.label(text = "Continue ?")

    def execute(self, context):
        winman = context.window_manager

        if winman.bpm_debug: print(starting_delete_shots_statement) #debug

        # move shots
        for shot in self.shots_to_remove:
            
            if winman.bpm_debug: print(starting_delete_specific_shot_statement + shot) #debug

            # delete corresponding scene if exists
            for s in bpy.data.scenes:
                if s.name == shot:
                    if winman.bpm_debug: print(deleting_scene_statement + s.name) #debug

                    bpy.data.scenes.remove(s, do_unlink = True)
            
            shot_folder_name = self.project_prefix + shot
            folder = os.path.join(self.shot_folder_path, shot_folder_name)
            # move
            if not self.permanently_delete:
                old_shot_folder = os.path.join(winman.bpm_projectfolder, old_folder)
                if winman.bpm_debug: print(starting_moving_folder + shot_folder_name + " to " + old_shot_folder) #debug

                old_shot_path = os.path.join(old_shot_folder, shot_folder)
                shutil.move(folder, old_shot_path)

                if winman.bpm_debug: print(moved_folder_statement) #debug
            # delete
            else:
                if winman.bpm_debug: print(starting_deleting_folder + shot_folder_name) #debug
                shutil.rmtree(folder)
                if winman.bpm_debug: print(deleted_folder_statement) #debug
        
        return {'FINISHED'}