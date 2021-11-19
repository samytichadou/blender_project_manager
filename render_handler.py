import bpy
import os
from bpy.app.handlers import persistent

from .functions.file_functions import get_filename_from_filepath
from .functions.task_functions import return_task_folder
from .functions.json_functions import read_json, create_json_file

### HANDLER ###
@persistent
def bpm_render_handler(scene):

    winman = bpy.data.window_managers[0]
    general_settings = winman.bpm_generalsettings

    if general_settings.is_project:
        shot_name = get_filename_from_filepath(bpy.data.filepath)[0]

        for entry in os.scandir(return_task_folder()):
            if shot_name in entry.name and entry.is_file():
                dataset = read_json(entry.path)
                if os.getpid() == dataset["pid"]:
                    dataset["completion"] += 1
                    if dataset["completion_total"] == dataset["completion"]:
                        dataset["completed"] = 1
                    create_json_file(dataset, entry.path)
                    break


### REGISTER ---

def register():
    bpy.app.handlers.render_post.append(bpm_render_handler)

def unregister():
    bpy.app.handlers.render_post.remove(bpm_render_handler)