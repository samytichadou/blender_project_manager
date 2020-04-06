import bpy, os


from ..global_variables import (
                            file_project, 
                            loading_statement, 
                            currently_loading_statement, 
                            folders_loading_statement, 
                            custom_folders_file, 
                            bpm_statement,
                            asset_folder,
                            shot_folder,
                            asset_file,
                            shot_file,
                        )
from .json_functions import read_json
from .file_functions import absolutePath
from .dataset_functions import setPropertiesFromJsonDataset
from .strip_functions import returnShotStrips, getListSequencerShots


# get project data file
def getProjectDataFile(winman):
    if bpy.data.is_saved:
        # edit file
        parent_folder = os.path.dirname(bpy.data.filepath)
        subparent_folder = os.path.dirname(parent_folder)
        subsubparent_folder = os.path.dirname(subparent_folder)
        edit_project_data_file = os.path.join(parent_folder, file_project)
        shot_asset_project_data_file = os.path.join(subsubparent_folder, file_project)

        # edit file
        if os.path.isfile(edit_project_data_file):
            winman.bpm_generalsettings.file_type = 'EDIT'
            return edit_project_data_file, parent_folder

        # shot or asset file
        elif os.path.isfile(shot_asset_project_data_file):
            if os.path.basename(subparent_folder) == asset_folder:
                winman.bpm_generalsettings.file_type = 'ASSET'
            elif os.path.basename(subparent_folder) == shot_folder:
                winman.bpm_generalsettings.file_type = 'SHOT'

            return shot_asset_project_data_file, subsubparent_folder

        else:
            return None, None
    else:
        return None, None


# check if project name match json project
def chekIfBpmProject(winman, project_data_file):
    general_settings = winman.bpm_generalsettings
    dataset = read_json(project_data_file)
    blend_name = os.path.splitext(os.path.basename(absolutePath(bpy.data.filepath)))[0]
    file_type = winman.bpm_generalsettings.file_type

    # edit
    if file_type == 'EDIT':
        pattern = dataset['edit_file_pattern']
        # print(pattern)
        # print(blend_name)
        if pattern == blend_name:
            general_settings.is_project = True
            return True
        elif pattern in blend_name:
            try:
                int(blend_name.split(pattern)[1])
                general_settings.is_project = True
                return True
            except (ValueError, IndexError):
                return False

    # shot
    elif file_type == 'SHOT':
        prefix = dataset['project_prefix']
        if not prefix.endswith("_"):
            prefix += "_"
        pattern1 = prefix + dataset['shot_prefix']
        pattern2 = "_" + dataset['shot_version_suffix']
        if pattern1 in blend_name and pattern2 in blend_name:
            general_settings.is_project = True
            return True

    # asset
    elif file_type == 'ASSET':
        general_settings.is_project = True
        return True

    return False


# load datas
def loadJsonDataToDataset(winman, dataset, json_file, avoid_list):
    debug = winman.bpm_generalsettings.debug
    if debug: print(loading_statement + json_file) #debug

    datasetin = read_json(json_file)

    # set datas
    setPropertiesFromJsonDataset(datasetin, dataset, False, (avoid_list))


# get custom folders file
def getCustomFoldersFile(winman):
    project_folder = winman.bpm_generalsettings.project_folder
    folders_file = os.path.join(project_folder, custom_folders_file)
    if os.path.isfile(folders_file):
        return folders_file, True
    else:
        return folders_file, False


# get asset file
def getAssetFile(winman):
    project_folder = winman.bpm_generalsettings.project_folder
    asset_folder_path = os.path.join(project_folder, asset_folder)
    asset_file_path = os.path.join(asset_folder_path, asset_file)
    if os.path.isfile(asset_file_path):
        return asset_file_path, True
    else:
        return asset_file_path, False


# load json in collection
def loadJsonInCollection(winman, json_file, collection, json_coll_name):
    debug = winman.bpm_generalsettings.debug
    dataset = read_json(json_file)
    for f in dataset[json_coll_name]:
        new = collection.add()
        setPropertiesFromJsonDataset(f, new, False, ())


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
            return lib


# find unused lib
def findUnusedLibraries():
    lib_list = []
    for scn in bpy.data.scenes:
        sequencer = scn.sequence_editor
        used_lib_list = getListSequencerShots(sequencer)[1]
        for lib in bpy.data.libraries:
            if lib not in used_lib_list:
                lib_list.append(lib)
    return lib_list


# get shot settings file
def getShotSettingsFileFromBlend():
    parent_folder = os.path.dirname(bpy.data.filepath)
    shot_json = os.path.join(parent_folder, shot_file)
    if os.path.isfile(shot_json):
        return shot_json


# refresh all shot strips in timeline from json shot files
def refreshTimelineShotDatas(winman, sequencer):
    general_settings = winman.bpm_generalsettings
    avoid_list = ('is_shot', 'shot_version', 'shot_last_version', 'not_last_version')

    general_settings.bypass_update_tag = True
    # iterate through timeline strips
    for strip in returnShotStrips(sequencer):

        # get json path
        shot_folder = os.path.dirname(strip.scene.library.filepath)
        shot_json = os.path.join(shot_folder, shot_file)

        # set json datas
        if os.path.isfile(shot_json):
            loadJsonDataToDataset(winman, strip.bpm_shotsettings, shot_json, avoid_list)
    general_settings.bypass_update_tag = False