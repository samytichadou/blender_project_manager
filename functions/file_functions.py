import bpy, os


# absolute path
def absolutePath(path):
    apath = os.path.abspath(bpy.path.abspath(path))
    return apath

# get last version of file
def getLastVersion(folder, pattern, extension):
    corresponding_files = []
    for filename in os.listdir(folder):
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

    corresponding_files_sorted = sorted(corresponding_files, key=lambda item: item[1], reverse=True)
    filepath = os.path.join(folder, corresponding_files_sorted[0][0])

    return filepath

# suppress existing file
def suppressExistingFile(filepath) :
    if os.path.isfile(filepath) :
        os.remove(filepath)

# get next shot
def getNextShot(project_datas, pattern, shot_version):
    folder = project_datas.project_folder
    shot_digits = project_datas.shot_digits
    version_suffix = project_datas.shot_version_suffix
    version_digits = project_datas.shot_version_digits

    version = ""
    if not pattern.endswith("_"):
        version += "_"
    version += version_suffix + str(shot_version).zfill(version_digits)

    shot_subdirs = []
    subdir = [f.path for f in os.scandir(folder) if f.is_dir()]
    path_pattern = os.path.join(folder, pattern)

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
    next_shot_folder = os.path.join(folder, next_shot)
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
    try:
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            data_to.scenes = data_from.scenes
    except OSError as err:
        print("OS error: {0}".format(err))