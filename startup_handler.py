import bpy, os
from bpy.app.handlers import persistent


from .functions.project_data_functions import (
                                            getProjectDataFile, 
                                            loadJsonDataToDataset, 
                                            getCustomFoldersFile, 
                                            loadJsonInCollection, 
                                            chekIfBpmProject, 
                                            getAssetFile,
                                            findUnusedLibraries,
                                            getShotSettingsFileFromBlend,
                                        )
from .global_variables import (
                            startup_statement, 
                            loaded_datas_statement, 
                            no_datas_statement, 
                            folders_loading_statement, 
                            loaded_folders_statement, 
                            loaded_project_folder,
                            assets_loading_statement,
                            assets_loaded_statement,
                            library_cleared_statement,
                            checking_unused_libraries_statement,
                            shot_loading_statement,
                            shot_loaded_statement,
                            missing_shot_file_statement,
                        )
from .vse_extra_ui import enableSequencerCallback, disableSequencerCallback
from .functions.utils_functions import clearLibraryUsers


### HANDLER ###
@persistent
def bpmStartupHandler(scene):
    winman = bpy.data.window_managers[0]

    general_settings = winman.bpm_generalsettings

    if winman.bpm_generalsettings.debug: print(startup_statement) #debug

    #load project datas
    project_data_file, project_folder = getProjectDataFile(winman)
    if project_data_file is not None:

        if chekIfBpmProject(winman, project_data_file):
            loadJsonDataToDataset(winman, winman.bpm_projectdatas, project_data_file, ())
            if winman.bpm_generalsettings.debug: print(loaded_datas_statement) #debug
            general_settings.project_folder = project_folder
            if winman.bpm_generalsettings.debug: print(loaded_project_folder + project_folder) #debug

            # load project custom folders
            custom_folders_file, is_folder_file = getCustomFoldersFile(winman)
            if is_folder_file:
                if winman.bpm_generalsettings.debug: print(folders_loading_statement + custom_folders_file) #debug
                custom_folders_coll = winman.bpm_customfolders
                loadJsonInCollection(winman, custom_folders_file, custom_folders_coll, 'folders')
                if winman.bpm_generalsettings.debug: print(loaded_folders_statement) #debug

            # load available assets
            asset_file, is_asset_file = getAssetFile(winman)
            if is_asset_file:
                if winman.bpm_generalsettings.debug: print(assets_loading_statement + asset_file) #debug
                asset_coll = winman.bpm_assets
                loadJsonInCollection(winman, asset_file, asset_coll, 'assets')
                if winman.bpm_generalsettings.debug: print(assets_loaded_statement) #debug

            # load shot settings
            if general_settings.file_type == 'SHOT':
                shot_json = getShotSettingsFileFromBlend()
                if shot_json is not None:
                    if winman.bpm_generalsettings.debug: print(shot_loading_statement + shot_json) #debug
                    # load json in props
                    shot_settings = winman.bpm_shotsettings
                    loadJsonDataToDataset(winman, shot_settings, shot_json, ())
                    if winman.bpm_generalsettings.debug: print(shot_loaded_statement) #debug


                    # synchronize audio if needed

                # no json error
                else: 
                    if winman.bpm_generalsettings.debug: print(missing_shot_file_statement) #debug

        else:
            if winman.bpm_generalsettings.debug: print(no_datas_statement) #debug

    else:
        if winman.bpm_generalsettings.debug: print(no_datas_statement) #debug
        
    if general_settings.is_project and general_settings.file_type == 'EDIT':
        # load ui if needed
        enableSequencerCallback()

        # # check for unused libraries and clear them
        # if winman.bpm_generalsettings.debug: print(checking_unused_libraries_statement) #debug

        # for lib in findUnusedLibraries():
        #     clearLibraryUsers(lib)
        #     if winman.bpm_generalsettings.debug: print(library_cleared_statement + lib.name) #debug

    else:
        # unload ui if needed
       disableSequencerCallback()