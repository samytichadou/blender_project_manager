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
                            render_folder,
                            render_file,
                            missing_shot_file_statement,
                            setting_prop_statement,
                        )
from .json_functions import read_json
from .file_functions import absolutePath, getBlendName
from .dataset_functions import setPropertiesFromJsonDataset
from .strip_functions import returnShotStrips, getListSequencerShots
from .reload_comments_function import reload_comments


# get project data file
def getProjectDataFile():
    if bpy.data.is_saved:
        # edit file
        parent_folder = os.path.dirname(bpy.data.filepath)
        subparent_folder = os.path.dirname(parent_folder)
        subsubparent_folder = os.path.dirname(subparent_folder)
        edit_project_data_file = os.path.join(parent_folder, file_project)
        shot_asset_project_data_file = os.path.join(subsubparent_folder, file_project)

        # edit file
        if os.path.isfile(edit_project_data_file):
            return edit_project_data_file, parent_folder, 'EDIT'

        # shot or asset file
        elif os.path.isfile(shot_asset_project_data_file):
            if os.path.basename(subparent_folder) == asset_folder:
                return shot_asset_project_data_file, subsubparent_folder, 'ASSET'
            elif os.path.basename(subparent_folder) == shot_folder:
                return shot_asset_project_data_file, subsubparent_folder, 'SHOT'

        else:
            return None, None, None
    else:
        return None, None, None


# check if project name match json project
def chekIfBpmProject(winman, project_data_file, file_type):
    general_settings = winman.bpm_generalsettings
    dataset = read_json(project_data_file)
    blend_name = os.path.splitext(os.path.basename(absolutePath(bpy.data.filepath)))[0]

    # edit
    if file_type == 'EDIT':
        pattern = dataset['edit_file_pattern']
        if pattern == blend_name:
            return True
        elif pattern in blend_name:
            try:
                int(blend_name.split(pattern)[1])                
                return True
            except (ValueError, IndexError):
                return False

    # shot
    elif file_type == 'SHOT':
        prefix = dataset['project_prefix']
        if not prefix.endswith("_"):
            prefix += "_"
        pattern1 = prefix + dataset['shot_prefix']
        pattern2 = "_" + dataset['version_suffix']
        if pattern1 in blend_name and pattern2 in blend_name:
            general_settings.is_project = True
            return True

    # asset
    elif file_type == 'ASSET':
        general_settings.is_project = True
        return True

    return False


# load json to dataset
def loadJsonDataToDataset(winman, dataset, json_file, avoid_list):
    debug = winman.bpm_projectdatas.debug
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


# get render settings file
def getRenderSettingsFile(winman):
    project_folder = winman.bpm_generalsettings.project_folder
    render_folder_path = os.path.join(project_folder, render_folder)
    render_filepath = os.path.join(render_folder_path, render_file)
    if os.path.isfile(render_filepath):
        return render_filepath, True
    else:
        return render_filepath, False


# load json in collection
def loadJsonInCollection(winman, json_file, collection, json_coll_name):
    # remove existing in collection
    collection.clear()
    debug = winman.bpm_projectdatas.debug
    dataset = read_json(json_file)
    for f in dataset[json_coll_name]:
        new = collection.add()
        setPropertiesFromJsonDataset(f, new, False, ())

    return dataset


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
def refreshTimelineShotDatas(context, sequencer):
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug
    general_settings = winman.bpm_generalsettings
    avoid_list = ('is_shot', 'shot_version', 'not_last_version', 'is_working')

    general_settings.bypass_update_tag = True
    # iterate through timeline strips
    for strip in returnShotStrips(sequencer):
        # get json path
        shot_folder = os.path.dirname(absolutePath(strip.bpm_shotsettings.shot_filepath))
        shot_json = os.path.join(shot_folder, shot_file)

        # set json datas
        if os.path.isfile(shot_json):
            loadJsonDataToDataset(winman, strip.bpm_shotsettings, shot_json, avoid_list)
        else:
            if debug: print(missing_shot_file_statement + " for " + strip.name) #debug

        # load comments
        reload_comments(context, "edit_shot", strip)

    # refresh edit comments
    reload_comments(context, "edit", None)

    general_settings.bypass_update_tag = False


# get specific asset datas from json
def getAssetDatasFromJson(asset_datas):
    name = getBlendName()
    for a in asset_datas['assets']:
        if name == a['name']:
            return a


# clear old asset bpm_isasset
def clearOldAssetBpmIsasset():
    for i in bpy.data.collections:
        i.bpm_isasset = False
    for i in bpy.data.materials:
        i.bpm_isasset = False
    for i in bpy.data.worlds:
        i.bpm_isasset = False


# set asset col from specific json dataset
def setAssetCollectionFromJsonDataset(datasetout, specific_asset_datas, debug):
    # clear old asset bpm_isasset
    clearOldAssetBpmIsasset()

    # shader
    if specific_asset_datas['asset_type'] == "SHADER":
        prop = 'asset_material'
        for m in bpy.data.materials:
            if m.name == specific_asset_datas[prop]:
                datasetout.asset_material = m
                m.bpm_isasset = True
                if debug: print(setting_prop_statement + prop) #debug
                return

    # world
    elif specific_asset_datas['asset_type'] == "WORLD":
        prop = 'asset_world'
        for w in bpy.data.worlds:
            if w.name == specific_asset_datas[prop]:
                datasetout.asset_world = w
                w.bpm_isasset = True
                if debug: print(setting_prop_statement + prop) #debug
                return

    # collections
    else:
        prop = 'asset_collection'
        for c in bpy.data.collections:
            if c.name == specific_asset_datas[prop]:
                datasetout.asset_collection = c
                c.bpm_isasset = True
                if debug: print(setting_prop_statement + prop) #debug
                return


# get shot task deadline, return identifier, value
def getShotTaskDeadline(shotsettings):
    state = shotsettings.shot_state.lower()
    for p in shotsettings.bl_rna.properties:
        if state + "_deadline" == p.identifier:
            return p.identifier, getattr(shotsettings, p.identifier)
    return None, "None"


# get shot task complete, return identifier, value
def getShotTaskComplete(shotsettings):
    state = shotsettings.shot_state.lower()
    for p in shotsettings.bl_rna.properties:
        if state + "_done" == p.identifier:
            return p.identifier, getattr(shotsettings, p.identifier)
    return None, None


# return render file extension from render settings
def returnRenderExtensionFromSettings(render_settings):
    extension = ""
    if render_settings.is_file_format == "OPEN_EXR" and render_settings.rd_use_file_extension:
        extension = '.exr'

    return extension