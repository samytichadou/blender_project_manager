import bpy
import os
import shutil


from ..functions.file_functions import absolutePath, linkExternalScenes
from ..functions.utils_functions import clearDataUsers
from ..functions.strip_functions import getListSequencerShots
from ..functions.check_file_poll_function import check_file_poll_function
from ..global_variables import (invalid_shot_version_message,
                                invalid_shot_version_statement,
                                already_loaded_shot_version_message,
                                already_loaded_shot_version_statement,
                                changing_shot_version_statement,
                                file_does_not_exist_message,
                                file_does_not_exist_statement,
                                deleting_scene_statement,
                                library_cleared_statement,
                                scenes_linked_statement,
                                linked_to_strip_statement,
                                scene_not_found_message,
                                scene_not_found_statement,
                            )


class BPM_OT_change_shot_version_edit(bpy.types.Operator):
    """Change version of active shot"""
    bl_idname = "bpm.change_shot_version_edit"
    bl_label = "Change shot version"
    bl_options = {'REGISTER'}

    version_number : bpy.props.IntProperty(name = "Version number", min = 1, default = 1)
    go_to_last_version : bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        is_bpm_project, bpm_filetype, bpm_active_strip = check_file_poll_function(context)
        if bpm_filetype == "EDIT" and bpm_active_strip:
            if not bpm_active_strip.lock:
                if not bpm_active_strip.bpm_shotsettings.is_working:
                    if not bpm_active_strip.bpm_shotsettings.is_rendering:
                        return True

    def invoke(self, context, event):
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings

        if self.go_to_last_version:
            self.version_number = shot_settings.shot_last_version
            self.go_to_last_version = False
            return self.execute(context)

        self.version_number = shot_settings.shot_version_used

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        current = shot_settings.shot_version_used
        last = shot_settings.shot_last_version

        layout = self.layout
        layout.label(text="Current : " + str(current))
        layout.label(text="Last : " + str(last))
        layout.prop(self, 'version_number')
        if self.version_number > last:
            layout.label(text="Not an existing version", icon = 'ERROR')
        elif self.version_number == current:
            layout.label(text="Already loaded version", icon = 'ERROR')

    def execute(self, context):

        # variables
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = winman.bpm_generalsettings
        active_strip = context.scene.sequence_editor.active_strip
        shot_settings = active_strip.bpm_shotsettings
        proj_datas = winman.bpm_projectdatas
        shot_name = active_strip.name

        # check for invalid shot version number or already loaded version
        if self.version_number > shot_settings.shot_last_version:
            self.report({'INFO'}, invalid_shot_version_message)
            if debug: print(invalid_shot_version_statement) #debug
            return {'FINISHED'}

        elif self.version_number == shot_settings.shot_version_used:
            self.report({'INFO'}, already_loaded_shot_version_message)
            if debug: print(already_loaded_shot_version_statement) #debug
            return {'FINISHED'}

        if debug: print(changing_shot_version_statement + str(self.version_number)) #debug

        # check if file exist
        old_version_shot_filepath = absolutePath(shot_settings.shot_filepath)
        shot_folder_path = os.path.dirname(old_version_shot_filepath)
        old_version_shot_file = os.path.basename(old_version_shot_filepath)
        old_version_shot_name = os.path.splitext(old_version_shot_file)[0]
        shot_pattern = old_version_shot_name[:-(proj_datas.version_digits)]
        target_shot_name = shot_pattern + str(self.version_number).zfill(proj_datas.version_digits)
        target_shot_path = os.path.join(shot_folder_path, target_shot_name + ".blend")

        if not os.path.isfile(target_shot_path):
            self.report({'INFO'}, file_does_not_exist_message + target_shot_path)
            if debug: print(file_does_not_exist_statement + target_shot_path) #debug
            return {'FINISHED'}
        
        # change version number
        shot_settings.shot_version_used = self.version_number

        # set new filepath
        shot_settings.shot_filepath = bpy.path.relpath(target_shot_path)

        ### deal with scene if scene strip ###
        if active_strip.type == 'SCENE':

            shot_scn = active_strip.scene
            shot_lib = shot_scn.library

            # link new scene
            linkExternalScenes(target_shot_path)
            if debug: print(scenes_linked_statement + target_shot_path) #debug

            # link strip to new scene
            scene_to_link = None
            for s in bpy.data.scenes:
                if s.library:
                    if absolutePath(s.library.filepath) == target_shot_path:
                        if s.name == shot_name:
                            scene_to_link = s
                            break
            if scene_to_link is not None:
                active_strip.scene = scene_to_link
                if debug: print(linked_to_strip_statement + target_shot_path) #debug

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