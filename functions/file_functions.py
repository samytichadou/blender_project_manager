import bpy
import os
import shutil


# absolute path
def absolutePath(path):
    apath = os.path.abspath(bpy.path.abspath(path))
    return apath


# get last version of file
def getLastVersion(folder, pattern, extension):
    # print("DEBUG --- folder : "+folder) #debug
    # print("DEBUG --- pattern : "+pattern) #debug

    corresponding_files = []
    for filename in os.listdir(folder):
        
        # print("DEBUG --- iterate filename : "+filename) #debug
        if pattern in filename and filename.endswith(extension):
            temp_name = os.path.splitext(filename)[0]
            temp_name_2 = temp_name.split(pattern)[1]
            try:
                version_number = int(temp_name_2)
            except ValueError:
                if len(temp_name_2) == 0:
                    version_number = 0
                else:
                    version_number = -1
            if version_number != -1:
                corresponding_files.append([filename, version_number])

    # print("DEBUG --- corresponding files : "+str(corresponding_files)) #debug
    corresponding_files_sorted = sorted(corresponding_files, key=lambda item: item[1], reverse=True)

    # print("DEBUG --- corresponding files sorted : "+str(corresponding_files_sorted)) #debug
    filepath = os.path.join(folder, corresponding_files_sorted[0][0])

    return filepath


# suppress existing file
def suppressExistingFile(filepath) :
    if os.path.isfile(filepath) :
        os.remove(filepath)


# delete folder content
def deleteFolderContent(folder):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        # folder
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
        else:
            os.remove(filepath)


# get next shot
def getNextShot(winman, project_datas, pattern, shot_version, shot_folder):
    shot_digits = project_datas.shot_digits
    version_suffix = project_datas.version_suffix
    version_digits = project_datas.version_digits

    version = ""
    if not pattern.endswith("_"):
        version += "_"
    version += version_suffix + str(shot_version).zfill(version_digits)

    shot_subdirs = []
    subdir = [f.path for f in os.scandir(shot_folder) if f.is_dir()]
    path_pattern = os.path.join(shot_folder, pattern)

    for s in subdir:
        if path_pattern in s:
            shot_number = int(s.split(path_pattern)[1])
            shot_subdirs.append([s, shot_number])

    if len(shot_subdirs) != 0:
        shot_subdirs_sorted = sorted(shot_subdirs, key=lambda item: item[1], reverse=True)
        next_shot_number = str(shot_subdirs_sorted[0][1] + 1).zfill(shot_digits)
    else:
        next_shot_number = str(1).zfill(shot_digits)
    next_shot = pattern + next_shot_number
    next_shot_folder = os.path.join(shot_folder, next_shot)
    next_shot_file = os.path.join(next_shot_folder, next_shot + version + ".blend")

    return [next_shot_folder, next_shot_file, next_shot_number]


# create directory if doesn't exist
def createDirectory(dir_path):
    if os.path.isdir(dir_path) == False :
        os.makedirs(dir_path)


# replace content in py scripts with a list ([to_replace, replacement])
def replaceContentInPythonScript(python_script_in, python_script_out, replacement_list):
    python_code= open(python_script_in, 'r').read()

    for r in replacement_list:
        if type(r[1]) is str:
            python_code = python_code.replace(r[0], 'r"' + r[1] + '"')
        else:
            python_code = python_code.replace(r[0], str(r[1]))

    with open(python_script_out, 'w') as file:
        file.write(python_code)


# link all scenes as libraries
def linkExternalScenes(filepath):
    try: #debug
        with bpy.data.libraries.load(filepath, link=True, relative=True) as (data_from, data_to):
            data_to.scenes = data_from.scenes
    except OSError as err: #debug
        print("OS error: {0}".format(err)) #debug


# create folder if doesn't exist
def createFolder(dir_path) :
    path = absolutePath(dir_path)
    if not os.path.isdir(path):
            os.makedirs(path)


# get blend name
def getBlendName():
    file_name = os.path.basename(bpy.data.filepath)
    name = os.path.splitext(file_name)[0]
    return name


# link asset libraries
def linkAssetLibrary(filepath, asset_type, debug):
    from .utils_functions import clearLibraryUsers
    from ..global_variables import(
                                library_cleared_statement,
                                asset_linked_statement,
                            )


    blend_name = os.path.basename(filepath)

    imported = []
    lib = bpy.data.libraries.load(filepath, link=True, relative=True)

    if asset_type != "SHADER":
        master_collection = bpy.context.scene.collection

        with lib as (data_from, data_to):
            data_to.collections = data_from.collections

        for new_coll in data_to.collections:
            if new_coll.bpm_isasset:

                if debug: print(asset_linked_statement + new_coll.name) #debug

                instance = bpy.data.objects.new(new_coll.name, None)
                instance.instance_type = 'COLLECTION'
                instance.instance_collection = new_coll
                master_collection.objects.link(instance)

                imported.append(instance)

    elif asset_type == "SHADER":
        with lib as (data_from, data_to):
            data_to.materials = data_from.materials

        for new_mat in data_to.materials:
            imported.append(new_mat)
            if not new_mat.bpm_isasset:
                bpy.data.materials.remove(bpy.data.materials[new_mat.name])
            else:
                if debug: print(asset_linked_statement + new_mat.name) #debug

    # remove lib if nothing imported
    if len(imported) == 0:

        clearLibraryUsers(bpy.data.libraries[blend_name])
        bpy.data.orphans_purge()

        if debug: print(library_cleared_statement + blend_name) #debug

        return False

    else:
        return True