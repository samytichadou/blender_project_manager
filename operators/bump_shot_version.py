import bpy
import os
import shutil
import atexit


from ..functions.file_functions import absolutePath, linkExternalScenes, createShotRenderFolders
from ..functions.check_file_poll_function import check_file_poll_function
from ..global_variables import (bumping_shot_statement, 
                            copying_file_statement,
                            deleting_scene_statement,
                            library_cleared_statement,
                            scenes_linked_statement,
                            linked_to_strip_statement,
                            scene_not_found_message,
                            scene_not_found_statement,
                            locked_file_statement,
                            created_lock_file_statement,
                            registering_exit_function_statement,
                        )
from ..functions.utils_functions import clearDataUsers
from ..functions.strip_functions import getListSequencerShots
from ..functions.lock_file_functions import deleteLockFileExit, getLockFilepath, setupLockFile
from ..addon_prefs import getAddonPreferences


class BPM_OT_bump_shot_version_edit(bpy.types.Operator):
    """Create a new version of active shot"""
    bl_idname = "bpm.bump_shot_version_edit"
    bl_label = "Bump shot version"
    bl_options = {'REGISTER'}

    file_to_copy_items = [
        ('CURRENT', 'Current version', ""),
        ('LAST', 'Last version', ""),
        ]
    file_to_copy : bpy.props.EnumProperty(name = "Create from", items = file_to_copy_items, default = 'CURRENT')

    @classmethod
    def poll(cls, context):
        is_bpm_project, bpm_filetype, bpm_active_strip = check_file_poll_function(context)
        if bpm_filetype == "EDIT" and bpm_active_strip:
            if not bpm_active_strip.lock:
                if not bpm_active_strip.bpm_shotsettings.is_working:
                    if not bpm_active_strip.bpm_shotsettings.is_rendering:
                        return True

    def invoke(self, context, event):
        self.file_to_copy = 'CURRENT'
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        if shot_settings.shot_version_used != shot_settings.shot_last_version:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Which version to bump from : ")
        layout.prop(self, 'file_to_copy', expand = True)

    def execute(self, context):

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = winman.bpm_generalsettings
        active_strip = context.scene.sequence_editor.active_strip
        shot_settings = active_strip.bpm_shotsettings
        proj_datas = winman.bpm_projectdatas

        shot_name = active_strip.name
       
        if debug: print(bumping_shot_statement) #debug

        # bump version number
        shot_settings.shot_version_used = shot_settings.shot_last_version + 1

        # get new shot path
        old_version_shot_filepath = absolutePath(shot_settings.shot_filepath)
        shot_folder_path = os.path.dirname(old_version_shot_filepath)
        old_version_shot_file = os.path.basename(old_version_shot_filepath)
        old_version_shot_name = os.path.splitext(old_version_shot_file)[0]
        shot_pattern = old_version_shot_name[:-(proj_datas.version_digits)]
        new_shot_name = shot_pattern + str(shot_settings.shot_version_used).zfill(proj_datas.version_digits)
        new_shot_path = os.path.join(shot_folder_path, new_shot_name + ".blend")

        if self.file_to_copy == 'LAST':
            last_version_name = shot_pattern + str(shot_settings.shot_last_version).zfill(proj_datas.version_digits)
            old_version_shot_filepath = os.path.join(shot_folder_path, last_version_name + ".blend")

        # bump shot last version number and make it last version
        shot_settings.shot_last_version = shot_settings.shot_version_used

        # copy the shot file
        if debug: print(copying_file_statement + old_version_shot_filepath + " - to - " + new_shot_path) #debug
        shutil.copy(old_version_shot_filepath, new_shot_path)

        # set new shot filepath
        shot_settings.shot_filepath = bpy.path.relpath(new_shot_path)

        # create shot render folders
        #createShotRenderFolders(new_shot_path, winman)

        ### deal with scene if scene strip ###
        if active_strip.type == 'SCENE':

            shot_scn = active_strip.scene
            shot_lib = shot_scn.library

            # link new scene
            linkExternalScenes(new_shot_path)
            if debug: print(scenes_linked_statement + new_shot_path) #debug

            # link strip to new scene
            scene_to_link = None
            for s in bpy.data.scenes:
                if s.library:
                    if absolutePath(s.library.filepath) == new_shot_path:
                        if s.name == shot_name:
                            scene_to_link = s
                            break
            if scene_to_link is not None:
                active_strip.scene = scene_to_link
                if debug: print(linked_to_strip_statement + new_shot_path) #debug

            # error message if scene not found
            else:
                self.report({'INFO'}, scene_not_found_message + shot_name)
                if debug: print(scene_not_found_statement + shot_name) #debug
                return {'FINISHED'}


            # check if old library is still used
            lib_used = getListSequencerShots(context.scene.sequence_editor)[1]
            if shot_lib not in lib_used:

                # delete old scene
                if debug: print(deleting_scene_statement + shot_name) #debug
                bpy.data.scenes.remove(shot_scn, do_unlink = True)

                # unlink old lib
                clearDataUsers(shot_lib)
                bpy.data.orphans_purge()
                if debug: print(library_cleared_statement + old_version_shot_filepath) #debug

        ### deal with images if image strip ###
        elif active_strip.type == 'IMAGE':
            shot_settings.shot_timeline_display = shot_settings.shot_timeline_display

        return {'FINISHED'}


class BPM_OT_bump_shot_version_shot(bpy.types.Operator):
    """Create a new version of active shot"""
    bl_idname = "bpm.bump_shot_version_shot"
    bl_label = "Bump shot version"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        is_bpm_project, bpm_filetype, bpm_active_strip = check_file_poll_function(context)
        if bpm_filetype == "SHOT":
            return True


    def execute(self, context):

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        shot_settings = winman.bpm_shotsettings
        proj_datas = winman.bpm_projectdatas
        prefs = getAddonPreferences()

        if debug: print(bumping_shot_statement) #debug

        bpy.ops.wm.save_as_mainfile(filepath = bpy.data.filepath)

        # set data shot version
        shot_settings.shot_last_version += 1
        shot_settings.shot_version_file = shot_settings.shot_last_version

        # get new shot path
        old_version_shot_filepath = bpy.data.filepath
        shot_folder_path = os.path.dirname(old_version_shot_filepath)
        old_version_shot_file = os.path.basename(old_version_shot_filepath)
        old_version_shot_name = os.path.splitext(old_version_shot_file)[0]
        shot_pattern = old_version_shot_name[:-(proj_datas.version_digits)]
        new_shot_name = shot_pattern + str(shot_settings.shot_last_version).zfill(proj_datas.version_digits)
        new_shot_path = os.path.join(shot_folder_path, new_shot_name + ".blend")

        

        # delete lock file
        if prefs.use_lock_file_system:
            deleteLockFileExit(getLockFilepath())
            atexit.unregister(deleteLockFileExit)

        # copy the shot file
        if debug: print(copying_file_statement + old_version_shot_filepath + " - to - " + new_shot_path) #debug
        bpy.ops.wm.save_as_mainfile(filepath = new_shot_path)

        # update lock file
        if prefs.use_lock_file_system:
            if debug: print(locked_file_statement) #debug
                
            lock_filepath = setupLockFile()
            if debug: print(created_lock_file_statement) #debug

            atexit.register(deleteLockFileExit, lock_filepath)
            if debug: print(registering_exit_function_statement) #debug

        return {'FINISHED'}