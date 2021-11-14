import os

from .. import global_variables as g_var
from . import json_functions as js_fct


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
    
    return datas


# return task folder
def return_task_folder(winman):
    general_settings = winman.bpm_generalsettings
    datas_folder = os.path.join(general_settings.project_folder, g_var.datas_folder)
    return os.path.join(datas_folder, g_var.datas_tasks_folder)


# write pid
def write_pid_task(taskfile, pid):
    dataset = js_fct.read_json(taskfile)
    dataset["pid"] = pid
    js_fct.create_json_file(dataset, taskfile)
