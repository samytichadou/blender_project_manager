import bpy
import os
import shutil


from ..functions.check_file_poll_function import check_file_poll_function
from ..global_variables import (
                            shot_folder, 
                            used_shots_list_statement,
                            existing_shots_list_statement,
                            unused_shots_list_statement,
                            no_unused_shots_message,
                            no_unused_shots_statement,
                            old_folder,
                            starting_delete_shots_statement,
                            starting_delete_specific_shot_statement,
                            deleting_scene_statement,
                            starting_moving_folder,
                            moved_folder_statement,
                            starting_deleting_folder,
                            deleted_folder_statement,
                        )
from ..functions.strip_functions import getListSequencerShots
from ..functions.project_data_functions import getAvailableShotsList, findLibFromShot
from ..functions.utils_functions import listDifference, clearDataUsers


class BPM_OT_delete_unused_shots(bpy.types.Operator):
    """Delete shots in the project not present on the timeline"""
    bl_idname = "bpm.delete_unused_shots"
    bl_label = "Delete unused shots"
    bl_options = {'REGISTER'}

    shots_to_remove = []
    shot_folder_path = None
    project_prefix = None
    shot_prefix = None

    permanently_delete : bpy.props.BoolProperty(name = "Permanently delete")

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        return file_type == "EDIT"

    def invoke(self, context, event):
  
        # reset permanently delete
        self.permanently_delete = False

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = context.window_manager.bpm_generalsettings

        project_datas = winman.bpm_projectdatas
        project_prefix = project_datas.project_prefix
        if not project_prefix.endswith("_"): project_prefix += "_"
        self.project_prefix = project_prefix
        self.shot_prefix = project_datas.shot_prefix

        self.shot_folder_path = os.path.join(general_settings.project_folder, shot_folder)
        sequencer = context.scene.sequence_editor

        # get used shot
        timeline_shots, used_libraries = getListSequencerShots(sequencer)

        if debug: print(used_shots_list_statement + str(timeline_shots)) #debug

        # get all existing shot
        existing_shots = getAvailableShotsList(self.shot_folder_path, self.project_prefix)

        if debug: print(existing_shots_list_statement + str(existing_shots)) #debug

        # find difference
        self.shots_to_remove = listDifference(existing_shots, timeline_shots)

        if debug: print(unused_shots_list_statement + str(self.shots_to_remove)) #debug

        if len(self.shots_to_remove) == 0:
            self.report({'INFO'}, no_unused_shots_message)
            if debug: print(no_unused_shots_statement) #debug
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
        debug = winman.bpm_projectdatas.debug
        general_settings = context.window_manager.bpm_generalsettings

        if debug: print(starting_delete_shots_statement) #debug

        # move shots
        for shot in self.shots_to_remove:
            
            if debug: print(starting_delete_specific_shot_statement + shot) #debug

            # delete corresponding scene if exists
            for s in bpy.data.scenes:
                if s.name == shot:
                    if debug: print(deleting_scene_statement + s.name) #debug

                    bpy.data.scenes.remove(s, do_unlink = True)
            
            shot_folder_name = self.project_prefix + shot
            folder = os.path.join(self.shot_folder_path, shot_folder_name)
            
            # move
            if not self.permanently_delete:
                old_shot_folder = os.path.join(general_settings.project_folder, old_folder)
                if debug: print(starting_moving_folder + shot_folder_name + " to " + old_shot_folder) #debug

                old_shot_path = os.path.join(old_shot_folder, shot_folder)
                temp_dir_path = os.path.join(old_shot_path, shot_folder_name)

                # check if existing and change name to copy
                if os.path.isdir(temp_dir_path):
                    v_number = 0
                    dir_path = temp_dir_path
                    while os.path.isdir(dir_path):
                        v_number += 1
                        dir_path = temp_dir_path + "_" + str(v_number)

                else:
                    dir_path = temp_dir_path

                shutil.move(folder, dir_path)

                if debug: print(moved_folder_statement) #debug

            # delete
            else:
                if debug: print(starting_deleting_folder + shot_folder_name) #debug
                shutil.rmtree(folder)
                if debug: print(deleted_folder_statement) #debug

            # remove libraries
            lib = findLibFromShot(shot_folder_name)
            if lib is not None:
                clearDataUsers(lib)
                bpy.data.orphans_purge()
        
        return {'FINISHED'}