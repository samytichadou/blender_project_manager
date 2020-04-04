import bpy
import os


from ..global_variables import (
                            saving_to_json_statement,
                            saved_to_json_statement,
                            shot_file,
                        )
from .json_functions import create_json_file, createJsonDatasetFromProperties

#update function for filebrowser custom path
def updateShotSettingsStripsProperties(self, context):
    strip = context.scene.sequence_editor.active_strip
    debug = context.window_manager.bpm_generalsettings.debug

    # create the json file
    if debug: print(saving_to_json_statement) #debug
    parent_folder = os.path.dirname(strip.scene.library.filepath)
    shot_json = os.path.join(parent_folder, shot_file)

    # format the json dataset
    json_dataset = createJsonDatasetFromProperties(strip.bpm_shotsettings)
    # create json file
    create_json_file(json_dataset, shot_json)

    if debug: print(saved_to_json_statement) #debug