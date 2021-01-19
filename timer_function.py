import bpy


from .global_variables import timer_function_processing_statement
from .functions.utils_functions import getCurrentPID
from .functions.lock_file_functions import getLockFilepath
from .functions.json_functions import read_json
from .functions.project_data_functions import refreshTimelineShotDatas
from .functions.load_asset_settings import reload_asset_library, reload_asset_setings
from .functions.load_project_custom_folder import load_custom_folders
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
            general_settings.blend_already_opened = True
            return
    
    # if not open
    general_settings.blend_already_opened = False


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
            reload_asset_setings(winman)

        # refresh asset library
        reload_asset_library(winman)

    # refresh custom project folders
    if prefs.timer_custom_folders_refresh:
        load_custom_folders(winman)

    return interval