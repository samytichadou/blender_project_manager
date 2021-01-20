import bpy
import os


from ..global_variables import custom_folder_not_found_statement


#update function for filebrowser custom path
def updateFilebrowserPath(self, context):
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug
    folders_coll = winman.bpm_customfolders
    general_settings = context.window_manager.bpm_generalsettings

    if general_settings.bypass_update_tag or len(folders_coll) == 0:
        return

    idx = general_settings.custom_folders_index

    if idx in range(0, len(folders_coll)):
        folder = folders_coll[general_settings.custom_folders_index]
        context.area.spaces[0].params.directory = str.encode(folder.filepath)

        if not os.path.isdir(folder.filepath):
            if debug: print(custom_folder_not_found_statement) #debug