import bpy

from ..functions import task_functions as tsk_fct
from ..addon_prefs import getAddonPreferences
from .. import global_variables as g_var
from ..functions import utils_functions as utl_fct

# render timer function
def bpm_render_timer():
    context = bpy.context
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug
    general_settings = winman.bpm_generalsettings

    prefs = getAddonPreferences()
    interval = prefs.render_timer_frequency

    if debug: print(g_var.render_timer_function_processing_statement) #debug

    tsk_fct.reload_task_list()
    
    # reload vse areas
    utl_fct.redrawAreas(context, 'SEQUENCE_EDITOR')

    if tsk_fct.tasks_render_finished():
        general_settings.is_rendering = False

    return interval

### REGISTER ---

# def register():
#     bpy.app.handlers.load_post.append(bpmStartupHandler)
    
def unregister():
    if bpy.app.timers.is_registered(bpm_render_timer):
        bpy.app.timers.unregister(bpm_render_timer)