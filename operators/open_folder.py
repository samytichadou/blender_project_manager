import bpy
import os

from ..functions.utils_functions import openFolderInExplorer
from ..functions import file_functions as fl_fct
from .. import global_variables as g_var
from ..functions.check_file_poll_function import check_file_poll_function


# opening function
def openFolderFilebrowserOption(folder_path, filebrowser, context, debug):        
    if os.path.isdir(folder_path):

        if debug: print(g_var.opening_folder_statement + folder_path) #debug

        if filebrowser:
            area = context.area
            area.spaces[0].params.directory = str.encode(folder_path)

        else:
            openFolderInExplorer(folder_path)

    else:
        if debug: print(g_var.no_folder_statement + folder_path) #debug


# shot folder
class BPM_OT_open_shot_folder(bpy.types.Operator):
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
            folder_path = os.path.dirname(fl_fct.absolutePath(shot_settings.shot_filepath))

        elif general_settings.file_type == 'SHOT':
            folder_path = os.path.dirname(bpy.data.filepath)

        # open if available        
        openFolderFilebrowserOption(folder_path, self.filebrowser, context, debug)

        return {'FINISHED'}


# shot render folder
class BPM_OT_open_shot_render_folder(bpy.types.Operator):
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
            shot_filepath = fl_fct.absolutePath(shot_settings.shot_filepath)
            render_state = shot_settings.shot_render_state

        elif general_settings.file_type == 'SHOT':
            shot_filepath = bpy.data.filepath
            render_state = winman.bpm_shotsettings.shot_render_state

        folder_path = os.path.dirname(fl_fct.returnRenderFilePathFromShot(shot_filepath, winman, render_state))

        # open if available        
        openFolderFilebrowserOption(folder_path, self.filebrowser, context, debug)

        return {'FINISHED'}


# general folders
class BPM_OT_open_project_folder(bpy.types.Operator):
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
            folder_path = os.path.join(general_settings.project_folder, g_var.render_folder)

        elif self.folder == "Asset":
            folder_path = os.path.join(general_settings.project_folder, g_var.asset_folder)

        elif self.folder == "Shot":
            folder_path = os.path.join(general_settings.project_folder, g_var.shot_folder)

        elif self.folder == "Ressources":
            folder_path = os.path.join(general_settings.project_folder, g_var.ressources_folder)

        elif self.folder == "Project":
            folder_path = general_settings.project_folder

        elif self.folder == "Datas":
            folder_path = os.path.join(general_settings.project_folder, g_var.datas_folder)

        elif self.folder == "Playblast":
            render_shot_folderpath = os.path.join(os.path.join(general_settings.project_folder, g_var.render_folder), g_var.render_shots_folder)
            folder_path = os.path.join(render_shot_folderpath, g_var.render_playblast_folder)

        # open if available  
        openFolderFilebrowserOption(folder_path, self.filebrowser, context, debug)

        return {'FINISHED'}


# custom folders
class BPM_OT_open_custom_folder(bpy.types.Operator):
    """Open project custom folder"""
    bl_idname = "bpm.open_custom_folder"
    bl_label = "Open Custom Folder"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        if general_settings.is_project:
            custom_folders_coll = winman.bpm_customfolders
            return general_settings.custom_folders_index in range(0, len(custom_folders_coll))


    def execute(self, context):
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        
        general_settings = winman.bpm_generalsettings

        folder = winman.bpm_customfolders[general_settings.custom_folders_index]

        if not os.path.isdir(folder.filepath):
            self.report({'INFO'}, g_var.no_folder_statement + folder.filepath)
            return

        openFolderInExplorer(folder.filepath)

        if debug: print(g_var.opening_folder_statement + folder.filepath) #debug

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_open_shot_folder)
    bpy.utils.register_class(BPM_OT_open_shot_render_folder)
    bpy.utils.register_class(BPM_OT_open_project_folder)
    bpy.utils.register_class(BPM_OT_open_custom_folder)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_open_shot_folder)
    bpy.utils.unregister_class(BPM_OT_open_shot_render_folder)
    bpy.utils.unregister_class(BPM_OT_open_project_folder)
    bpy.utils.unregister_class(BPM_OT_open_custom_folder)