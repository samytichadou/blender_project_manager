import bpy, os
from bpy.app.handlers import persistent


from .functions.project_data_functions import (
                                            getProjectDataFile, 
                                            createProjectDatas, 
                                            getCustomFoldersFile, 
                                            loadJsonInCollection, 
                                            chekIfBpmProject, 
                                            getAssetFile,
                                        )
from .global_variables import (
                            startup_statement, 
                            loaded_datas_statement, 
                            no_datas_statement, 
                            folders_loading_statement, 
                            loaded_folders_statement, 
                            loaded_project_folder,
                            assets_loading_statement,
                            assets_loaded_statement
                        )
from .vse_extra_ui import enableSequencerCallback, disableSequencerCallback


### HANDLER ###
@persistent
def bpmStartupHandler(scene):
    winman = bpy.data.window_managers[0]
    if winman.bpm_debug: print(startup_statement) #debug

    #load project datas
    project_data_file, project_folder = getProjectDataFile(winman)
    if project_data_file is not None:

        if chekIfBpmProject(winman, project_data_file):
            createProjectDatas(winman, project_data_file)
            if winman.bpm_debug: print(loaded_datas_statement) #debug
            winman.bpm_projectfolder = project_folder
            if winman.bpm_debug: print(loaded_project_folder + project_folder) #debug

            # load project custom folders
            custom_folders_file, is_folder_file = getCustomFoldersFile(winman)
            if is_folder_file:
                if winman.bpm_debug: print(folders_loading_statement + custom_folders_file) #debug
                custom_folders_coll = winman.bpm_folders
                loadJsonInCollection(winman, custom_folders_file, custom_folders_coll, 'folders')
                if winman.bpm_debug: print(loaded_folders_statement) #debug

            # load available assets
            asset_file, is_asset_file = getAssetFile(winman)
            if is_asset_file:
                if winman.bpm_debug: print(assets_loading_statement + asset_file) #debug
                asset_coll = winman.bpm_assets
                loadJsonInCollection(winman, asset_file, asset_coll, 'assets')
                if winman.bpm_debug: print(assets_loaded_statement) #debug

        else:
            if winman.bpm_debug: print(no_datas_statement) #debug

    else:
        if winman.bpm_debug: print(no_datas_statement) #debug
        
    #load ui if needed
    if winman.bpm_isproject and winman.bpm_filetype == 'EDIT':
        enableSequencerCallback()
        # check for unused libraries to clear
        
    else:
       disableSequencerCallback()