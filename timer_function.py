import bpy

from .global_variables import timer_function_processing_statement
from .functions.utils_functions import getCurrentPID
from .functions.lock_file_functions import getLockFilepath
from .functions.json_functions import read_json
from .functions.project_data_functions import refreshTimelineShotDatas
from .functions import load_asset_settings as ld_ast_stg
from .functions.load_project_custom_folder import load_custom_folders
from .functions import audio_sync_functions as aud_sync_fct
from .operators.refresh_shot_datas import refresh_shot_datas
from .addon_prefs import getAddonPreferences


# check lock file
def check_lock_file(context):
    # check for opened blend
    pid = getCurrentPID()
    datas = read_json(getLockFilepath())
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings

    for o in datas['opened']:

        if o['pid'] != pid:
            if not general_settings.blend_already_opened:
                general_settings.blend_already_opened = True
            return
    
    # if not open
    general_settings.blend_already_opened = False

# timer function
def bpmTimerFunction():
    context = bpy.context
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug
    general_settings = winman.bpm_generalsettings

    prefs = getAddonPreferences()
    interval = prefs.timer_frequency

    if debug: print(timer_function_processing_statement) #debug

    ### lock system ###
    if prefs.use_lock_file_system:
        check_lock_file(context)

    # refresh datas
    if prefs.timer_datas_refresh:
        if general_settings.file_type == 'EDIT':
            refreshTimelineShotDatas(context, context.scene.sequence_editor)
        elif general_settings.file_type == 'SHOT':
            refresh_shot_datas(context)
        elif general_settings.file_type == 'ASSET':
            ld_ast_stg.reload_asset_setings(winman)

        # refresh asset library
        ld_ast_stg.reload_asset_library(winman)

    # refresh custom project folders
    if prefs.timer_custom_folders_refresh:
        load_custom_folders(winman)

    # syncrhonize audio
    if prefs.timer_audio_sync:
        if general_settings.file_type == 'EDIT':
            aud_sync_fct.syncAudioEdit(debug, general_settings.project_folder, context.scene)
        elif general_settings.file_type == 'SHOT':
            aud_sync_fct.syncAudioShot(debug, general_settings.project_folder, context.scene)

    return interval

### REGISTER ---

# def register():
#     bpy.app.handlers.load_post.append(bpmStartupHandler)
    
def unregister():
    if bpy.app.timers.is_registered(bpmTimerFunction):
        bpy.app.timers.unregister(bpmTimerFunction)