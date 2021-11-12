import bpy
import os
import atexit
from bpy.app.handlers import persistent


from .functions import project_data_functions as proj_fct
from . import global_variables as g_var
from . import vse_extra_ui as vse_ui
from . import dopesheet_extra_ui as dsht_ui
from .functions.audio_sync_functions import syncAudioShot
from .functions import lock_file_functions as lck_fl_fct
from .functions.date_functions import getDateString
from .functions.reload_comments_function import reload_comments
from .functions import load_asset_settings as ld_ast_stg
from .functions.load_project_custom_folder import load_custom_folders
from .functions.check_addon_version_functions import check_addon_version
from .timer_function import bpmTimerFunction
from .addon_prefs import getAddonPreferences


### HANDLER ###
@persistent
def bpmStartupHandler(scene):
    winman = bpy.data.window_managers[0]

    general_settings = winman.bpm_generalsettings

    print(g_var.startup_statement)

    #load project datas
    project_data_file, project_folder, file_type = proj_fct.getProjectDataFile()
    if project_data_file is not None:

        if proj_fct.chekIfBpmProject(winman, project_data_file, file_type):
            
            ### bpm project ###

            general_settings.is_project = True
            general_settings.file_type = file_type

            proj_fct.loadJsonDataToDataset(winman, winman.bpm_projectdatas, project_data_file, ())

            debug = winman.bpm_projectdatas.debug

            if debug: print(g_var.loaded_datas_statement) #debug
            general_settings.project_folder = project_folder
            if debug: print(g_var.loaded_project_folder + project_folder) #debug

            # set date
            general_settings.today_date = getDateString()
            if debug: print(g_var.date_set_statement) #debug

            prefs = getAddonPreferences()

            # lock file system
            if prefs.use_lock_file_system:
                # check for lock file
                lock_filepath = lck_fl_fct.getLockFilepath()
                if os.path.isfile(lock_filepath):
                    if debug: print(g_var.locked_file_statement) #debug
                    # set already opened prop
                    general_settings.blend_already_opened = True
                
                # setup lock file
                lock_filepath = lck_fl_fct.setupLockFile()
                if debug: print(g_var.created_lock_file_statement) #debug
                
                if debug: print(g_var.registering_exit_function_statement) #debug
                atexit.register(lck_fl_fct.deleteLockFileExit, lock_filepath)

            # setup timer if needed
            if prefs.use_timer_refresh:
                bpy.app.timers.register(bpmTimerFunction)
                if debug: print(g_var.timer_function_added_statement) #debug


            ### common loading ###

            # load project custom folders
            load_custom_folders(winman)

            # load available assets
            ld_ast_stg.reload_asset_library(winman)

            if general_settings.file_type in {'EDIT', 'SHOT'}:

                # load render settings
                render_filepath, render_file_exist = proj_fct.getRenderSettingsFile(winman)
                if render_file_exist:
                    if debug: print(g_var.render_settings_loading_statement + render_filepath) #debug
                    render_settings = winman.bpm_rendersettings
                    proj_fct.loadJsonInCollection(winman, render_filepath, render_settings, 'render_settings')
                    if debug: print(g_var.render_settings_loaded_statement) #debug

                # no render file error
                else:
                    if debug: print(g_var.missing_render_file_statement) #debug
                

            ### specific loading ###

            # load edit settings
            if general_settings.file_type == 'EDIT':
                
                sequencer = bpy.context.scene.sequence_editor

                # refresh timeline shots strips datas
                if debug: print(g_var.refreshing_timeline_shot_datas_statement) #debug               
                proj_fct.refreshTimelineShotDatas(bpy.context, sequencer)
                if debug: print(g_var.refreshed_timeline_shot_datas_statement) #debug

                # load edit comments
                reload_comments(bpy.context, "edit", None)

            # load shot settings
            elif general_settings.file_type == 'SHOT':
                shot_json = proj_fct.getShotSettingsFileFromBlend()
                if shot_json is not None:
                    if debug: print(g_var.shot_loading_statement + shot_json) #debug
                    # load json in props
                    shot_settings = winman.bpm_shotsettings

                    general_settings.bypass_update_tag = True
                    proj_fct.loadJsonDataToDataset(winman, shot_settings, shot_json, ())
                    shot_settings.shot_filepath = bpy.path.relpath(bpy.data.filepath)
                    general_settings.bypass_update_tag = False

                    # load version number
                    shot_settings.shot_version_file = proj_fct.find_file_version(bpy.data.filepath, winman)
                    
                    if debug: print(g_var.shot_loaded_statement) #debug

                    # synchronize audio if needed
                    if shot_settings.auto_audio_sync:
                        syncAudioShot(debug, project_folder, bpy.context.scene)

                # no json error
                else: 
                    if debug: print(g_var.missing_shot_file_statement) #debug

                # load shot comments
                reload_comments(bpy.context, "shot", None)

            # load asset settings
            elif general_settings.file_type == 'ASSET':

                ld_ast_stg.reload_asset_setings(winman)


            # check for addon new version
            check_addon_version(winman)

        else:
            print(g_var.no_datas_statement)

    else:
        print(g_var.no_datas_statement)
    
    # ui callback
    # load ui if needed
    if general_settings.is_project:
        if general_settings.file_type == 'EDIT':
            dsht_ui.disable_dope_sheet_ui_callback()
            vse_ui.enableSequencerUICallback()
        elif general_settings.file_type in {"SHOT", "ASSET"}:
            vse_ui.disableSequencerUICallback()
            dsht_ui.enable_dope_sheet_ui_callback()
    #unload ui if needed
    else:
        vse_ui.disableSequencerUICallback()
        dsht_ui.disable_dope_sheet_ui_callback()


### REGISTER ---

def register():
    bpy.app.handlers.load_post.append(bpmStartupHandler)
    
def unregister():
    bpy.app.handlers.load_post.remove(bpmStartupHandler)