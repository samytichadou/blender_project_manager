import bpy
import os

from .. import global_variables as g_var
from . import json_functions as js_fct
from . import file_functions as fl_fct
from . import dataset_functions as dtset_fct


# create task dataset
def create_task_dataset(name, time, file_filepath, type, id, completion_total):
    datas = {}
    datas["name"]               = name
    datas["creation_time"]      = time
    datas["type"]               = type
    datas["id"]                 = id
    datas["filepath"]           = file_filepath
    datas["completion"]         = 0
    datas["completion_total"]   = completion_total
    datas["pid"]                = 0
    datas["completed"]          = 0
    
    return datas

# return task folder
def return_task_folder():
    winman = bpy.data.window_managers[0]
    general_settings = winman.bpm_generalsettings
    datas_folder = os.path.join(general_settings.project_folder, g_var.datas_folder)
    return os.path.join(datas_folder, g_var.datas_tasks_folder)

# write pid
def write_pid_task(taskfile, pid):
    dataset = js_fct.read_json(taskfile)
    dataset["pid"] = pid
    js_fct.create_json_file(dataset, taskfile)

# reload tasks in list
def reload_task_list():
    winman = bpy.data.window_managers[0]
    debug = winman.bpm_projectdatas.debug
    task_collection = winman.bpm_tasklist
    task_folder = return_task_folder()

    task_collection.clear()

    for task_file in fl_fct.returnAllFilesInFolder(task_folder):
        newentry = task_collection.add()
        dataset = js_fct.read_json(os.path.join(task_folder, task_file))
        dtset_fct.setPropertiesFromJsonDataset(dataset, newentry, debug, ())

# check if renders finished
def tasks_render_finished():
    winman = bpy.data.window_managers[0]
    debug = winman.bpm_projectdatas.debug
    task_collection = winman.bpm_tasklist

    chk_render_unfinished = False
    for task in task_collection:
        if task.type == "render":
            if not task.completed:
                chk_render_unfinished = True

    return not chk_render_unfinished