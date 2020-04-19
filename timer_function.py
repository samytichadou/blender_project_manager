import bpy


from .global_variables import timer_function_processing_statement
from .functions.utils_functions import getCurrentPID
from .functions.lock_file_functions import getLockFilepath
from .functions.json_functions import read_json

def bpmTimerFunction():
    winman = bpy.context.window_manager
    general_settings = winman.bpm_generalsettings

    if general_settings.debug: print(timer_function_processing_statement) #debug

    # check for opened blend
    pid = getCurrentPID()
    lock_filepath = getLockFilepath()
    datas = read_json(lock_filepath)

    chk_free = True

    for o in datas['opened']:

        if o['pid'] != pid:
            general_settings.blend_already_opened = True
            chk_free = False
            break
    
    if chk_free:
        general_settings.blend_already_opened = False

    return 60.0