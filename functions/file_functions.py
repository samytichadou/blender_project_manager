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
def getNextShot(folder, pattern, shot_digits):
    shot_subdirs = []
    subdir = [f.path for f in os.scandir(folder) if f.is_dir()]
    path_pattern = os.path.join(folder, pattern)

    for s in subdir:
        if path_pattern in s:
            shot_number = int(s.split(path_pattern)[1])
            shot_subdirs.append([s, shot_number])

    shot_subdirs_sorted = sorted(shot_subdirs, key=lambda item: item[1], reverse=True)
    next_shot_number = str(shot_subdirs_sorted[0][1] + 1).zfill(shot_digits)
    next_shot = pattern + next_shot_number
    next_shot_folder = os.path.join(folder, next_shot)
    next_shot_file = os.path.join(next_shot_folder, next_shot + ".blend")

    return [next_shot_folder, next_shot_file, next_shot_number]

# create directory if doesn't exist
def createDirectory(dir_path):
    if os.path.isdir(dir_path) == False :
        os.makedirs(dir_path)

# replace content in py scripts with a list ([to_replace, replacement])
def replaceContentInPythonScript(python_script_in, python_script_out, replacement_list):
    python_code= open(python_script_in, 'r').read()

    for r in replacement_list:
        python_code = python_code.replace(r[0], r[1])

    with open(python_script_out, 'w') as file:
        file.write(python_code)