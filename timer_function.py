import bpy


from .global_variables import timer_function_processing_statement
from .functions.utils_functions import getCurrentPID
from .functions.lock_file_functions import getLockFilepath
from .functions.json_functions import read_json
from .functions.project_data_functions import refreshTimelineShotDatas
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

    # refresh timeline datas
    if prefs.timer_timeline_refresh:
        if general_settings.file_type == 'EDIT':
            refreshTimelineShotDatas(context, context.scene.sequence_editor)
        elif general_settings.file_type == 'SHOT':
            pass

    return interval