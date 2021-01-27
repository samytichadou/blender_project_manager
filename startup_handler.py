import bpy, os, atexit
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
                                            find_file_version,
                                        )
from .functions.dataset_functions import setPropertiesFromJsonDataset
from .global_variables import (
                            startup_statement, 
                            loaded_datas_statement, 
                            no_datas_statement, 
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
                            refreshing_timeline_shot_display_mode,
                            refreshed_timeline_shot_display_mode,
                            assets_settings_loading_statement,
                            assets_settings_loaded_statement,
                            asset_missing_in_list_statement,
                            created_lock_file_statement,
                            locked_file_statement,
                            timer_function_added_statement,
                            timer_function_removed_statement,
                            date_set_statement,
                            registering_exit_function_statement,
                        )
from .vse_extra_ui import enableSequencerUICallback, disableSequencerUICallback
from .dopesheet_extra_ui import enable_dope_sheet_ui_callback, disable_dope_sheet_ui_callback
from .functions.audio_sync_functions import syncAudioShot
from .functions.file_functions import getBlendName
from .functions.lock_file_functions import setupLockFile, getLockFilepath, deleteLockFileExit
from .functions.date_functions import getDateString
from .functions.reload_comments_function import reload_comments
from .functions.load_asset_settings import reload_asset_library, reload_asset_setings
from .functions.load_project_custom_folder import load_custom_folders
from .functions.check_addon_version_functions import check_addon_version
from .timer_function import bpmTimerFunction
from .addon_prefs import getAddonPreferences


### HANDLER ###
@persistent
def bpmStartupHandler(scene):
    winman = bpy.data.window_managers[0]

    general_settings = winman.bpm_generalsettings

    print(startup_statement)

    #load project datas
    project_data_file, project_folder, file_type = getProjectDataFile()
    if project_data_file is not None:

        if chekIfBpmProject(winman, project_data_file, file_type):
            
            ### bpm project ###

            general_settings.is_project = True
            general_settings.file_type = file_type

            loadJsonDataToDataset(winman, winman.bpm_projectdatas, project_data_file, ())

            debug = winman.bpm_projectdatas.debug

            if debug: print(loaded_datas_statement) #debug
            general_settings.project_folder = project_folder
            if debug: print(loaded_project_folder + project_folder) #debug

            # set date
            general_settings.today_date = getDateString()
            if debug: print(date_set_statement) #debug

            prefs = getAddonPreferences()

            # lock file system
            if prefs.use_lock_file_system:
                # check for lock file
                lock_filepath = getLockFilepath()
                if os.path.isfile(lock_filepath):
                    if debug: print(locked_file_statement) #debug
                    # set already opened prop
                    general_settings.blend_already_opened = True
                
                # setup lock file
                lock_filepath = setupLockFile()
                if debug: print(created_lock_file_statement) #debug
                
                if debug: print(registering_exit_function_statement) #debug
                atexit.register(deleteLockFileExit, lock_filepath)

            # setup timer if needed
            if prefs.use_timer_refresh:
                bpy.app.timers.register(bpmTimerFunction)
                if debug: print(timer_function_added_statement) #debug


            ### common loading ###

            # load project custom folders
            load_custom_folders(winman)

            # load available assets
            reload_asset_library(winman)

            if general_settings.file_type in {'EDIT', 'SHOT'}:

                # load render settings
                render_filepath, render_file_exist = getRenderSettingsFile(winman)
                if render_file_exist:
                    if debug: print(render_settings_loading_statement + render_filepath) #debug
                    render_settings = winman.bpm_rendersettings
                    loadJsonInCollection(winman, render_filepath, render_settings, 'render_settings')
                    if debug: print(render_settings_loaded_statement) #debug

                # no render file error
                else:
                    if debug: print(missing_render_file_statement) #debug
                

            ### specific loading ###

            # load edit settings
            if general_settings.file_type == 'EDIT':
                
                sequencer = bpy.context.scene.sequence_editor

                # refresh timeline shots strips datas
                if debug: print(refreshing_timeline_shot_datas_statement) #debug               
                refreshTimelineShotDatas(bpy.context, sequencer)
                if debug: print(refreshed_timeline_shot_datas_statement) #debug

                # load edit comments
                reload_comments(bpy.context, "edit", None)

            # load shot settings
            elif general_settings.file_type == 'SHOT':
                shot_json = getShotSettingsFileFromBlend()
                if shot_json is not None:
                    if debug: print(shot_loading_statement + shot_json) #debug
                    # load json in props
                    shot_settings = winman.bpm_shotsettings

                    general_settings.bypass_update_tag = True
                    loadJsonDataToDataset(winman, shot_settings, shot_json, ())
                    shot_settings.shot_filepath = bpy.path.relpath(bpy.data.filepath)
                    general_settings.bypass_update_tag = False

                    # load version number
                    shot_settings.shot_version_file = find_file_version(bpy.data.filepath, winman)
                    
                    if debug: print(shot_loaded_statement) #debug

                    # synchronize audio if needed
                    if shot_settings.auto_audio_sync:
                        syncAudioShot(debug, project_folder, bpy.context.scene)

                # no json error
                else: 
                    if debug: print(missing_shot_file_statement) #debug

                # load shot comments
                reload_comments(bpy.context, "shot", None)

            # load asset settings
            elif general_settings.file_type == 'ASSET':

                reload_asset_setings(winman)


            # check for addon new version
            check_addon_version(winman)

        else:
            print(no_datas_statement)

    else:
        print(no_datas_statement)
    
    # ui callback
    # load ui if needed
    if general_settings.is_project:
        if general_settings.file_type == 'EDIT':
            disable_dope_sheet_ui_callback()
            enableSequencerUICallback()
        elif general_settings.file_type in {"SHOT", "ASSET"}:
            disableSequencerUICallback()
            enable_dope_sheet_ui_callback()
    #unload ui if needed
    else:
        disableSequencerUICallback()
        disable_dope_sheet_ui_callback()

    