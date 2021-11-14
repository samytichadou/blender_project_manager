import bpy
import os

from .. import global_variables as g_var
from . import json_functions as js_fct
from .set_render_shot_update_function import setRenderShot
from .file_functions import absolutePath


#update function for shot settings props general
def updateShotSettingsProperties(self, context):
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    debug = winman.bpm_projectdatas.debug

    if general_settings.bypass_update_tag:
        #if debug: print(bypass_settings_update_statement) #debug
        return

    # create the json file
    if debug: print(g_var.saving_to_json_statement) #debug

    if general_settings.file_type == 'EDIT':
        shot_folder = os.path.dirname(absolutePath(self.shot_filepath))
    else:
        shot_folder = os.path.dirname(bpy.data.filepath)
    
    shot_json = os.path.join(shot_folder, g_var.shot_file)

    # format the json dataset
    json_dataset = js_fct.createJsonDatasetFromProperties(self, ("shot_timeline_display", "shot_filepath", "shot_version_file"))
    # create json file
    js_fct.create_json_file(json_dataset, shot_json)

    if debug: print(g_var.saved_to_json_statement) #debug


#update function for shot render state prop
def updateShotRenderState(self, context):
    # save json
    updateShotSettingsProperties(self, context)
    # set render settings
    setRenderShot(context, context.window_manager.bpm_shotsettings.shot_render_state)
    