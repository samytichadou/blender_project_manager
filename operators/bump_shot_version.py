import bpy
import os
import shutil


from ..global_variables import (creating_shot_statement, 
                            creating_shot_folder_statement, 
                            python_temp, 
                            shot_setup_file, 
                            launching_command_statement, 
                            creating_python_script_statement,
                            python_script_created_statement,
                            deleted_file_statement,
                            scenes_linked_statement,
                            no_available_timeline_space_message,
                            no_available_timeline_space_statement,
                            checking_available_timeline_space_statement,
                            shot_folder,
                        )
from ..functions.file_functions import absolutePath, linkExternalScenes
from ..functions.utils_functions import clearLibraryUsers

from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
from ..functions.strip_functions import returnAvailablePositionStripChannel


class BPMBumpShotVersionFromEdit(bpy.types.Operator):
    """Create a new version of active shot"""
    bl_idname = "bpm.bump_shot_version_edit"
    bl_label = "Bump shot version"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        if context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor.active_strip:
                    active = context.scene.sequence_editor.active_strip
                    if not active.lock:
                        try:
                            if active.bpm_shotsettings.is_shot and active.scene.library:
                                return True
                        except AttributeError:
                            pass

    def execute(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        active_strip = context.scene.sequence_editor.active_strip
        shot_settings = active_strip.bpm_shotsettings
        proj_datas = winman.bpm_projectdatas
        shot_scn = active_strip.scene
        shot_lib = shot_scn.library
        shot_name = shot_scn.name
        
        if general_settings.debug: print('Bumping shot version') #debug

        # bump version number
        shot_settings.shot_version += 1

        # get new shot path
        old_version_shot_filepath = absolutePath(shot_lib.filepath)
        shot_folder_path = os.path.dirname(old_version_shot_filepath)
        old_version_shot_file = os.path.basename(old_version_shot_filepath)
        old_version_shot_name = os.path.splitext(old_version_shot_file)[0]
        shot_pattern = old_version_shot_name[:-(proj_datas.shot_version_digits)]
        new_shot_name = shot_pattern + str(shot_settings.shot_version).zfill(proj_datas.shot_version_digits)
        new_shot_path = os.path.join(shot_folder_path, new_shot_name + ".blend")

        # copy the shot file
        if general_settings.debug: print('Duplicating shot to : ' + new_shot_name) #debug
        shutil.copy(old_version_shot_filepath, new_shot_path)

        # delete old scene
        if general_settings.debug: print('Deleting scene : ' + shot_name) #debug
        bpy.data.scenes.remove(shot_scn, do_unlink = True)

        # unlink old lib
        if general_settings.debug: print('Unlinking library : ' + old_version_shot_filepath) #debug
        clearLibraryUsers(shot_lib)

        # link new scene
        if general_settings.debug: print('Linking new scene from : ' + new_shot_path) #debug
        linkExternalScenes(new_shot_path)

        # link strip to new scene
        if general_settings.debug: print('Linking scene to strip : ' + shot_name) #debug
        active_strip.scene = bpy.data.scenes[shot_name]

        return {'FINISHED'}