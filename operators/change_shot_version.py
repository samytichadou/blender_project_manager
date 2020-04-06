import bpy
import os
import shutil


class BPMBumpChangeShotVersionFromEdit(bpy.types.Operator):
    """Change version of active shot"""
    bl_idname = "bpm.change_shot_version_edit"
    bl_label = "Change shot version"
    bl_options = {'REGISTER'}

    version_number : bpy.props.IntProperty(name = "Version number", min = 1, default = 1)
    go_to_last_version : bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        if context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor:
                    if context.scene.sequence_editor.active_strip:
                        active = context.scene.sequence_editor.active_strip
                        if not active.lock:
                            try:
                                if active.bpm_shotsettings.is_shot and active.scene.library:
                                    if active.bpm_shotsettings.shot_last_version != 1:
                                        return True
                            except AttributeError:
                                pass

    def invoke(self, context, event):
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings

        if self.go_to_last_version:
            self.version_number = shot_settings.shot_last_version
            self.go_to_last_version = False
            return self.execute(context)

        self.version_number = shot_settings.shot_version

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        current = shot_settings.shot_version
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
        # import statements and functions
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
        from ..functions.file_functions import absolutePath, linkExternalScenes
        from ..functions.utils_functions import clearLibraryUsers
        from ..functions.strip_functions import getListSequencerShots

        # variables
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        active_strip = context.scene.sequence_editor.active_strip
        shot_settings = active_strip.bpm_shotsettings
        proj_datas = winman.bpm_projectdatas
        shot_scn = active_strip.scene
        shot_lib = shot_scn.library
        shot_name = shot_scn.name

        # check for invalid shot version number or already loaded version
        if self.version_number > shot_settings.shot_last_version:
            self.report({'INFO'}, invalid_shot_version_message)
            if general_settings.debug: print(invalid_shot_version_statement) #debug
            return {'FINISHED'}

        elif self.version_number == shot_settings.shot_version:
            self.report({'INFO'}, already_loaded_shot_version_message)
            if general_settings.debug: print(already_loaded_shot_version_statement) #debug
            return {'FINISHED'}

        if general_settings.debug: print(changing_shot_version_statement + str(self.version_number)) #debug

        # check if file exist
        old_version_shot_filepath = absolutePath(shot_lib.filepath)
        shot_folder_path = os.path.dirname(old_version_shot_filepath)
        old_version_shot_file = os.path.basename(old_version_shot_filepath)
        old_version_shot_name = os.path.splitext(old_version_shot_file)[0]
        shot_pattern = old_version_shot_name[:-(proj_datas.version_digits)]
        target_shot_name = shot_pattern + str(self.version_number).zfill(proj_datas.version_digits)
        target_shot_path = os.path.join(shot_folder_path, target_shot_name + ".blend")

        if not os.path.isfile(target_shot_path):
            self.report({'INFO'}, file_does_not_exist_message + target_shot_path)
            if general_settings.debug: print(file_does_not_exist_statement + target_shot_path) #debug
            return {'FINISHED'}
        
        # change version number and set warning if needed
        shot_settings.shot_version = self.version_number
        if self.version_number != shot_settings.shot_last_version:
            shot_settings.not_last_version = True
        else:
            shot_settings.not_last_version = False

        # link new scene
        linkExternalScenes(target_shot_path)
        if general_settings.debug: print(scenes_linked_statement + target_shot_path) #debug

        # link strip to new scene
        scene_to_link = None
        for s in bpy.data.scenes:
            if s.library:
                if s.library.filepath == target_shot_path:
                    if s.name == shot_name:
                        scene_to_link = s
                        break
        if scene_to_link is not None:
            active_strip.scene = scene_to_link
            if general_settings.debug: print(linked_to_strip_statement + target_shot_path) #debug
        # error message if scene not found
        else:
            self.report({'INFO'}, scene_not_found_message + shot_name)
            if general_settings.debug: print(scene_not_found_statement + shot_name) #debug
            return {'FINISHED'}

        # check if old library is still used
        lib_used = getListSequencerShots(context.scene.sequence_editor)[1]
        if shot_lib not in lib_used:

            # delete old scene
            if general_settings.debug: print(deleting_scene_statement + shot_name) #debug
            bpy.data.scenes.remove(shot_scn, do_unlink = True)

            # unlink old lib
            clearLibraryUsers(shot_lib)
            if general_settings.debug: print(library_cleared_statement + old_version_shot_filepath) #debug

        return {'FINISHED'}