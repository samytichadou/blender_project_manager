import os

from .project_data_functions import getCustomFoldersFile
from .json_functions import createJsonDatasetFromProperties, create_json_file
from ..global_variables import saved_to_json_statement


def update_custom_folder_file(winman):

    debug = winman.bpm_projectdatas.debug
    custom_folders_coll = winman.bpm_customfolders

    custom_folders_file, is_folder_file = getCustomFoldersFile(winman)

    datas = {}
    datas["folders"] = []

    for c in custom_folders_coll:
        datas["folders"].append(createJsonDatasetFromProperties(c, ()))

    create_json_file(datas, custom_folders_file)

    if debug: print(saved_to_json_statement) #debug


# update function used when changing custom folder name
def update_custom_folder_file_from_name(self, context):

    winman = context.window_manager

    if winman.bpm_generalsettings.bypass_update_tag:
        return

    update_custom_folder_file(winman)