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
    next_shot = shot_subdirs_sorted[0][1] + 1
    next_shot_folder = os.path.join(folder, pattern + str(next_shot).zfill(shot_digits))
    
    return [next_shot_folder, next_shot]