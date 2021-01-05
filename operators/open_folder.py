import bpy
import os


from ..functions.utils_functions import openFolderInExplorer
from ..functions.file_functions import absolutePath, returnRenderFilePathFromShot
from ..global_variables import (
                            opening_folder_statement,
                            no_folder_statement,
                            render_folder,
                            shot_folder,
                            asset_folder,
                            ressources_folder,
                            render_playblast_folder,
                            render_shots_folder,
                        )
from ..functions.check_file_poll_function import check_file_poll_function


# opening function
def openFolderFilebrowserOption(folder_path, filebrowser, context, debug):        
    if os.path.isdir(folder_path):

        if debug: print(opening_folder_statement + folder_path) #debug

        if filebrowser:
            area = context.area
            area.spaces[0].params.directory = str.encode(folder_path)

        else:
            openFolderInExplorer(folder_path)

    else:
        if debug: print(no_folder_statement + folder_path) #debug

# shot folder
class BPMOpenShotFolder(bpy.types.Operator):
    """Open Shot Folder"""
    bl_idname = "bpm.open_shot_folder"
    bl_label = "Open Shot Folder"
    bl_options = {'REGISTER'}

    filebrowser : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "SHOT":
            return True
        elif active is not None:
            return not active.lock

    def execute(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        debug = winman.bpm_projectdatas.debug

        folder_path = None

        # get shot settings and filepath 
        if general_settings.file_type == 'EDIT':
            shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
            folder_path = os.path.dirname(absolutePath(shot_settings.shot_filepath))

        elif general_settings.file_type == 'SHOT':
            folder_path = os.path.dirname(bpy.data.filepath)

        # open if available        
        openFolderFilebrowserOption(folder_path, self.filebrowser, context, debug)

        return {'FINISHED'}


# shot render folder
class BPMOpenShotRenderFolder(bpy.types.Operator):
    """Open Shot Render Folder"""
    bl_idname = "bpm.open_shot_render_folder"
    bl_label = "Open Shot Render Folder"
    bl_options = {'REGISTER'}

    filebrowser : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "SHOT":
            return True
        elif active is not None:
            return not active.lock

    def execute(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        debug = winman.bpm_projectdatas.debug

        folder_path = None

        # get shot settings and filepath 
        if general_settings.file_type == 'EDIT':
            shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
            shot_filepath = absolutePath(shot_settings.shot_filepath)
            render_state = shot_settings.shot_render_state

        elif general_settings.file_type == 'SHOT':
            shot_filepath = bpy.data.filepath
            render_state = winman.bpm_shotsettings.shot_render_state

        folder_path = os.path.dirname(returnRenderFilePathFromShot(shot_filepath, winman, render_state))

        # open if available        
        openFolderFilebrowserOption(folder_path, self.filebrowser, context, debug)

        return {'FINISHED'}


# general folders
class BPMOpenProjectFolder(bpy.types.Operator):
    """Open Project Folder"""
    bl_idname = "bpm.open_project_folder"
    bl_label = "Open Project Folder"
    bl_options = {'REGISTER', 'INTERNAL'}

    filebrowser : bpy.props.BoolProperty()
    folder : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project

    def execute(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        debug = winman.bpm_projectdatas.debug

        folder_path = None

        if self.folder == "Render":
            folder_path = os.path.join(general_settings.project_folder, render_folder)

        elif self.folder == "Asset":
            folder_path = os.path.join(general_settings.project_folder, asset_folder)

        elif self.folder == "Shot":
            folder_path = os.path.join(general_settings.project_folder, shot_folder)

        elif self.folder == "Ressources":
            folder_path = os.path.join(general_settings.project_folder, ressources_folder)

        elif self.folder == "Project":
            folder_path = general_settings.project_folder

        elif self.folder == "Playblast":
            render_shot_folderpath = os.path.join(os.path.join(general_settings.project_folder, render_folder), render_shots_folder)
            folder_path = os.path.join(render_shot_folderpath, render_playblast_folder)

        # open if available  
        openFolderFilebrowserOption(folder_path, self.filebrowser, context, debug)

        return {'FINISHED'}