import os

from .. import global_variables as gv

from .hash_functions import generate_hash
from .json_functions import read_json, create_json_file
from .date_functions import getDateTimeString, getDateTimeID

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
    datas_folder = os.path.join(general_settings.project_folder, gv.datas_folder)
    return os.path.join(datas_folder, gv.datas_tasks_folder)


# write pid
def write_pid_task(taskfile, pid):
    dataset = read_json(taskfile)
    dataset["pid"] = pid
    create_json_file(dataset, taskfile)
