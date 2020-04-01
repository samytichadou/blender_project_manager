import bpy, os


from ..global_variables import (
                            file_project, 
                            loading_statement, 
                            currently_loading_statement, 
                            folders_loading_statement, 
                            custom_folders_file, 
                            bpm_statement,
                            asset_folder,
                            asset_file,
                        )
from .json_functions import read_json
from .file_functions import absolutePath
from .dataset_functions import setPropertiesFromJsonDataset


# get project data file
def getProjectDataFile(winman):
    if bpy.data.is_saved:
        # edit file
        parent_folder = os.path.dirname(bpy.data.filepath)
        subparent_folder = os.path.dirname(parent_folder)
        subsubparent_folder = os.path.dirname(subparent_folder)
        edit_project_data_file = os.path.join(parent_folder, file_project)
        shot_project_data_file = os.path.join(subsubparent_folder, file_project)

        # edit file
        if os.path.isfile(edit_project_data_file):
            #winman.bpm_isproject = True
            winman.bpm_filetype = 'EDIT'
            return edit_project_data_file, parent_folder

        # shot file
        elif os.path.isfile(shot_project_data_file):
            #winman.bpm_isproject = True
            winman.bpm_filetype = 'SHOT'
            return shot_project_data_file, subsubparent_folder

        else:
            return None, None
    else:
        return None, None    


# check if project name match json project
def chekIfBpmProject(winman, project_data_file):
    dataset = read_json(project_data_file)
    blend_name = os.path.splitext(os.path.basename(absolutePath(bpy.data.filepath)))[0]
    # edit
    if winman.bpm_filetype == 'EDIT':
        pattern = dataset['edit_file_pattern']
        # print(pattern)
        # print(blend_name)
        if pattern == blend_name:
            winman.bpm_isproject = True
            return True
        elif pattern in blend_name:
            try:
                int(blend_name.split(pattern)[1])
                winman.bpm_isproject = True
                return True
            except (ValueError, IndexError):
                return False
    # shot
    elif winman.bpm_filetype == 'SHOT':
        pattern1 = dataset['project_prefix'] + "_" + dataset['shot_prefix']
        pattern2 = "_" + dataset['shot_version_suffix']
        if pattern1 in blend_name and pattern2 in blend_name:
            winman.bpm_isproject = True
            return True
    return False


# load datas
def createProjectDatas(winman, project_data_file):
    if winman.bpm_debug: print(loading_statement + project_data_file) #debug

    datas = winman.bpm_datas.add()
    dataset = read_json(project_data_file)

    # set datas
    setPropertiesFromJsonDataset(dataset, datas, winman)

    return datas


# get custom folders file
def getCustomFoldersFile(winman):
    project_folder = winman.bpm_projectfolder
    folders_file = os.path.join(project_folder, custom_folders_file)
    if os.path.isfile(folders_file):
        return folders_file, True
    else:
        return folders_file, False


# get asset file
def getAssetFile(winman):
    project_folder = winman.bpm_projectfolder
    asset_folder_path = os.path.join(project_folder, asset_folder)
    asset_file_path = os.path.join(asset_folder_path, asset_file)
    if os.path.isfile(asset_file_path):
        return asset_file_path, True
    else:
        return asset_file_path, False


# load json in collection
def loadJsonInCollection(winman, json_file, collection, json_coll_name):
    dataset = read_json(json_file)
    for f in dataset[json_coll_name]:
        new = collection.add()
        setPropertiesFromJsonDataset(f, new, winman)


# get shot pattern
def getShotPattern(project_datas):
    prefix = project_datas.project_prefix
    if not project_datas.project_prefix.endswith("_"):
        prefix += "_"
    prefix += project_datas.shot_prefix
    return prefix


# get shot replacement list for python script for shot creation
def getScriptReplacementListShotCreation(project_datas, next_shot_folder, next_shot_file, next_shot_number):
    replacement_list = []
    replacement_list.append(['|bpm_statement', bpm_statement])
    replacement_list.append(['|filepath', next_shot_file])
    replacement_list.append(['|scene_name', project_datas.shot_prefix + next_shot_number])
    replacement_list.append(['|frame_start', project_datas.shot_start_frame])
    replacement_list.append(['|frame_end', project_datas.shot_start_frame + project_datas.default_shot_length])
    replacement_list.append(['|framerate', project_datas.framerate])
    replacement_list.append(['|resolution_x', project_datas.resolution_x])
    replacement_list.append(['|resolution_y', project_datas.resolution_y])

    return replacement_list


# get shot arguments list for python script
def getArgumentForPythonScript(argument_list):
    arguments = ""
    for a in argument_list:
        arguments += str(a)
        arguments += " ### "
    return arguments


# get all available shots list
def getAvailableShotsList(shot_folder, project_prefix):
    shot_list = []
    for filename in os.listdir(shot_folder):
        filepath = os.path.join(shot_folder, filename)
        if os.path.isdir(filepath):
            if project_prefix in filename:
                shot_list.append(filename.split(project_prefix)[1])
    return shot_list


# find lib from shot name
def findLibFromShot(shot_name):
    for l in bpy.data.libraries:
        if shot_name in l.name:
            lib = l
            break
    return lib


# find unused lib
def findUnusedLibraries():
    lib_list = []
    from .strip_functions import getListSequencerShots
    for scn in bpy.data.scenes:
        sequencer = scn.sequence_editor
        used_lib_list = getListSequencerShots(sequencer)[1]
        for lib in bpy.data.libraries:
            if lib not in used_lib_list:
                lib_list.append(lib)
    return lib_list