import bpy, os


from ..global_variables import file_project, loading_statement, currently_loading_statement, folders_loading_statement, custom_folders_file
from .json_functions import read_json


# get project data file
def getProjectDataFile(winman):
    if bpy.data.is_saved:
        # edit file
        parent_folder = os.path.dirname(bpy.data.filepath)
        subparent_folder = os.path.dirname(parent_folder)
        edit_project_data_file = os.path.join(parent_folder, file_project)
        shot_project_data_file = os.path.join(subparent_folder, file_project)
        if os.path.isfile(edit_project_data_file):
            winman.bpm_isproject = True
            winman.bpm_isedit = True
            return edit_project_data_file
        elif os.path.isfile(shot_project_data_file):
            winman.bpm_isproject = True
            winman.bpm_isedit = False
            return shot_project_data_file

# load datas
def createProjectDatas(winman, project_data_file):
    if winman.bpm_debug: print(loading_statement + project_data_file) #debug

    datas = winman.bpm_datas.add()
    dataset = read_json(project_data_file)

    # set datas
    datas.name = dataset["name"]
    datas.framerate = dataset["framerate"]
    datas.project_folder = dataset["project_folder"]
    datas.edit_file = dataset["edit_file"]

# get custom folders file
def getCustomFoldersFile(winman):
    if winman.bpm_isedit:
        parent_folder = os.path.dirname(bpy.data.filepath)
    else:
        parent_folder = os.path.dirname(os.path.dirname(bpy.data.filepath))
    folders_file = os.path.join(parent_folder, custom_folders_file)
    if os.path.isfile(folders_file):
        return folders_file

# load custom folders
def loadCustomFolders(winman, folders_file):
    if winman.bpm_debug: print(folders_loading_statement + folders_file) #debug

    folders_coll = winman.bpm_folders
    dataset = read_json(folders_file)
    for f in dataset["folders"]:
        folder = folders_coll.add()
        folder.name = f['name']
        folder.filepath = f['filepath']