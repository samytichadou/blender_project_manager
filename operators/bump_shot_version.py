import bpy
import os
import shutil


from ..functions.file_functions import absolutePath


class BPMBumpShotVersionFromEdit(bpy.types.Operator):
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
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        if context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor:
                    if context.scene.sequence_editor.active_strip:
                        active = context.scene.sequence_editor.active_strip
                        if active.type in {'SCENE', 'IMAGE'}:
                            if not active.lock:
                                if active.bpm_shotsettings.is_shot:
                                    #if os.path.isfile(absolutePath(active.bpm_shotsettings.shot_filepath)):
                                    return True

    def invoke(self, context, event):
        self.file_to_copy = 'CURRENT'
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        if shot_settings.shot_version != shot_settings.shot_last_version:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Which version to bump from : ")
        layout.prop(self, 'file_to_copy', expand = True)

    def execute(self, context):
        # import statements and functions
        from ..global_variables import (bumping_shot_statement, 
                                    copying_file_statement,
                                    deleting_scene_statement,
                                    library_cleared_statement,
                                    scenes_linked_statement,
                                    linked_to_strip_statement,
                                    scene_not_found_message,
                                    scene_not_found_statement,
                                )
        from ..functions.utils_functions import clearDataUsers
        from ..functions.strip_functions import getListSequencerShots
        from ..functions.file_functions import linkExternalScenes, createShotRenderFolders

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        active_strip = context.scene.sequence_editor.active_strip
        shot_settings = active_strip.bpm_shotsettings
        proj_datas = winman.bpm_projectdatas

        shot_name = active_strip.name
       
        if general_settings.debug: print(bumping_shot_statement) #debug

        # bump version number
        shot_settings.shot_version = shot_settings.shot_last_version + 1

        # get new shot path
        old_version_shot_filepath = absolutePath(shot_settings.shot_filepath)
        shot_folder_path = os.path.dirname(old_version_shot_filepath)
        old_version_shot_file = os.path.basename(old_version_shot_filepath)
        old_version_shot_name = os.path.splitext(old_version_shot_file)[0]
        shot_pattern = old_version_shot_name[:-(proj_datas.version_digits)]
        new_shot_name = shot_pattern + str(shot_settings.shot_version).zfill(proj_datas.version_digits)
        new_shot_path = os.path.join(shot_folder_path, new_shot_name + ".blend")

        if self.file_to_copy == 'LAST':
            last_version_name = shot_pattern + str(shot_settings.shot_last_version).zfill(proj_datas.version_digits)
            old_version_shot_filepath = os.path.join(shot_folder_path, last_version_name + ".blend")

        # bump shot last version number and make it last version
        shot_settings.shot_last_version = shot_settings.shot_version
        shot_settings.not_last_version = False

        # copy the shot file
        if general_settings.debug: print(copying_file_statement + old_version_shot_filepath + " - to - " + new_shot_path) #debug
        shutil.copy(old_version_shot_filepath, new_shot_path)

        # set new shot filepath
        shot_settings.shot_filepath = bpy.path.relpath(new_shot_path)

        # create shot render folders
        createShotRenderFolders(new_shot_path, winman)

        ### deal with scene if scene strip ###
        if active_strip.type == 'SCENE':

            shot_scn = active_strip.scene
            shot_lib = shot_scn.library

            # link new scene
            linkExternalScenes(new_shot_path)
            if general_settings.debug: print(scenes_linked_statement + new_shot_path) #debug

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
                if general_settings.debug: print(linked_to_strip_statement + new_shot_path) #debug

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
                clearDataUsers(shot_lib)
                bpy.data.orphans_purge()
                if general_settings.debug: print(library_cleared_statement + old_version_shot_filepath) #debug

        ### deal with images if image strip ###
        elif active_strip.type == 'IMAGE':
            shot_settings.shot_timeline_display = shot_settings.shot_timeline_display

        return {'FINISHED'}