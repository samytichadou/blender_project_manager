import bpy
import os
import shutil
import atexit

from bpy.app.handlers import persistent


from ..global_variables import lockfile_extension, deleted_lock_file_statement
from .file_functions import suppressExistingFile
from .utils_functions import getHostName, getTimestamp, getCurrentPID
from .json_functions import initializeAssetJsonDatas, read_json, create_json_file


# get lock filepath
def getLockFilepath():
    return os.path.splitext(bpy.data.filepath)[0] + lockfile_extension

# format json opened entry
def formatJsonOpenedEntry():
    json_dataset = {}
    json_dataset['hostname'] = getHostName()
    json_dataset['timestamp'] = getTimestamp()
    json_dataset['pid'] = getCurrentPID()
    return json_dataset

# create lock file
def setupLockFile():
    lock_filepath = getLockFilepath()

    if os.path.isfile(lock_filepath):
        datas = read_json(lock_filepath)
    else:
        datas = initializeAssetJsonDatas({'opened'})

    datas['opened'].append(formatJsonOpenedEntry())

    create_json_file(datas, lock_filepath)

# delete lock file if existing
def clearLockFile():
    lock_filepath = getLockFilepath()

    if os.path.isfile(lock_filepath):
        pid = getCurrentPID()
        datas = read_json(lock_filepath)
        n = 0
        for o in datas['opened']:
            if o['pid'] == pid:
                del datas['opened'][n]
                break
            n += 1

        if len(datas['opened']) != 0:
            create_json_file(datas, lock_filepath)
            return 'UPDATED'
        else:
            suppressExistingFile(lock_filepath)
            return 'DELETED'
    else:
        return 'NONE'

# delete on exit
@atexit.register
def deleteLockFileExit():
    if clearLockFile() in {'UPDATED', 'DELETED'}:
        print(deleted_lock_file_statement) #debug

# delete on load pre
@persistent
def deleteLockFileHandler(scene):
    if bpy.data.window_managers[0].bpm_generalsettings.is_project:
        if clearLockFile() in {'UPDATED', 'DELETED'}:
            if bpy.data.window_managers[0].bpm_projectdatas.debug: print(deleted_lock_file_statement) #debug