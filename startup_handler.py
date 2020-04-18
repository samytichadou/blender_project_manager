import bpy, os
from bpy.app.handlers import persistent


from .functions.project_data_functions import (
                                            getProjectDataFile, 
                                            loadJsonDataToDataset, 
                                            getCustomFoldersFile, 
                                            loadJsonInCollection, 
                                            chekIfBpmProject, 
                                            getAssetFile,
                                            getRenderSettingsFile,
                                            findUnusedLibraries,
                                            getShotSettingsFileFromBlend,
                                            refreshTimelineShotDatas,
                                            getAssetDatasFromJson,
                                            setAssetCollectionFromJsonDataset,
                                        )
from .functions.dataset_functions import setPropertiesFromJsonDataset
from .global_variables import (
                            startup_statement, 
                            loaded_datas_statement, 
                            no_datas_statement, 
                            folders_loading_statement, 
                            loaded_folders_statement, 
                            loaded_project_folder,
                            assets_loading_statement,
                            assets_loaded_statement,
                            render_settings_loading_statement,
                            render_settings_loaded_statement,
                            missing_render_file_statement,
                            library_cleared_statement,
                            checking_unused_libraries_statement,
                            shot_loading_statement,
                            shot_loaded_statement,
                            missing_shot_file_statement,
                            refreshing_timeline_shot_datas_statement,
                            refreshed_timeline_shot_datas_statement,
                            assets_settings_loading_statement,
                            assets_settings_loaded_statement,
                            asset_missing_in_list_statement,
                        )
from .vse_extra_ui import enableSequencerCallback, disableSequencerCallback
from .functions.utils_functions import clearLibraryUsers
from .functions.audio_sync_functions import syncAudioShot
from .functions.file_functions import getBlendName


### HANDLER ###
@persistent
def bpmStartupHandler(scene):
    winman = bpy.data.window_managers[0]

    general_settings = winman.bpm_generalsettings

    if general_settings.debug: print(startup_statement) #debug

    #load project datas
    project_data_file, project_folder = getProjectDataFile(winman)
    if project_data_file is not None:
        if chekIfBpmProject(winman, project_data_file):
            loadJsonDataToDataset(winman, winman.bpm_projectdatas, project_data_file, ())
            if general_settings.debug: print(loaded_datas_statement) #debug
            general_settings.project_folder = project_folder
            if general_settings.debug: print(loaded_project_folder + project_folder) #debug


            ### common loading ###

            # load project custom folders
            custom_folders_file, is_folder_file = getCustomFoldersFile(winman)
            if is_folder_file:
                if general_settings.debug: print(folders_loading_statement + custom_folders_file) #debug
                custom_folders_coll = winman.bpm_customfolders
                loadJsonInCollection(winman, custom_folders_file, custom_folders_coll, 'folders')
                if general_settings.debug: print(loaded_folders_statement) #debug

            # load available assets
            asset_file, asset_file_exist = getAssetFile(winman)
            if asset_file_exist:
                if general_settings.debug: print(assets_loading_statement + asset_file) #debug
                asset_coll = winman.bpm_assets
                asset_datas = loadJsonInCollection(winman, asset_file, asset_coll, 'assets')
                if general_settings.debug: print(assets_loaded_statement) #debug

                # load asset file settings
                if general_settings.file_type == 'ASSET':

                    # set this blend file asset
                    blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
                    try:
                        asset_coll[blend_name].is_thisassetfile = True
                    except KeyError:
                        if general_settings.debug: print(asset_missing_in_list_statement) #debug

                    asset_settings = winman.bpm_assetsettings
                    specific_asset_datas = getAssetDatasFromJson(asset_datas)

                    if specific_asset_datas is not None:
                        if general_settings.debug: print(assets_settings_loading_statement) #debug

                        general_settings.bypass_update_tag = True
                        
                        setPropertiesFromJsonDataset(specific_asset_datas, asset_settings, general_settings.debug, ('asset_collection', 'asset_material'))
                        setAssetCollectionFromJsonDataset(asset_settings, specific_asset_datas, general_settings.debug)
                        
                        general_settings.bypass_update_tag = False

                        if general_settings.debug: print(assets_settings_loaded_statement) #debug

                    # asset does not exist in list error
                    else:
                        if general_settings.debug: print(asset_missing_in_list_statement) #debug


            if general_settings.file_type in {'EDIT', 'SHOT'}:

                # load render settings
                render_filepath, render_file_exist = getRenderSettingsFile(winman)
                if render_file_exist:
                    if general_settings.debug: print(render_settings_loading_statement + render_filepath) #debug
                    render_settings = winman.bpm_rendersettings
                    loadJsonInCollection(winman, render_filepath, render_settings, 'render_settings')
                    if general_settings.debug: print(render_settings_loaded_statement) #debug

                # no render file error
                else:
                    if general_settings.debug: print(missing_render_file_statement) #debug
                

            ### specific loading ###

            # load edit settings
            if general_settings.file_type == 'EDIT':
                
                # refresh timeline shots strips datas
                if general_settings.debug: print(refreshing_timeline_shot_datas_statement) #debug

                refreshTimelineShotDatas(winman, bpy.context.scene.sequence_editor)

                if general_settings.debug: print(refreshed_timeline_shot_datas_statement) #debug

            # load shot settings
            elif general_settings.file_type == 'SHOT':
                shot_json = getShotSettingsFileFromBlend()
                if shot_json is not None:
                    if general_settings.debug: print(shot_loading_statement + shot_json) #debug
                    # load json in props
                    shot_settings = winman.bpm_shotsettings

                    general_settings.bypass_update_tag = True
                    loadJsonDataToDataset(winman, shot_settings, shot_json, ())
                    general_settings.bypass_update_tag = False

                    if general_settings.debug: print(shot_loaded_statement) #debug

                    # synchronize audio if needed
                    if shot_settings.auto_audio_sync:
                        syncAudioShot(general_settings.debug, project_folder, bpy.context.scene)

                # no json error
                else: 
                    if general_settings.debug: print(missing_shot_file_statement) #debug

            # load asset settings
            elif general_settings.file_type == 'ASSET':
                asset_settings = winman.bpm_assetsettings
                asset_settings.name = getBlendName()

        else:
            if general_settings.debug: print(no_datas_statement) #debug

    else:
        if general_settings.debug: print(no_datas_statement) #debug
        
    if general_settings.is_project and general_settings.file_type == 'EDIT':
        # load ui if needed
        enableSequencerCallback()

        # # check for unused libraries and clear them
        # if general_settings.debug: print(checking_unused_libraries_statement) #debug

        # for lib in findUnusedLibraries():
        #     clearLibraryUsers(lib)
        #     if general_settings.debug: print(library_cleared_statement + lib.name) #debug

    else:
        # unload ui if needed
       disableSequencerCallback()