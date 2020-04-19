import bpy
import os
import atexit
from bpy.app.handlers import persistent


from ..global_variables import lockfile_extension, deleted_lock_file_statement
from .file_functions import suppressExistingFile


# get lock filepath
def getLockFilepath():
    return os.path.splitext(bpy.data.filepath)[0] + lockfile_extension

# create lock file
def createLockFile():
    open(getLockFilepath(), 'a').close()

# delete lock file if existing
def deleteLockFile():
    lock_filepath = getLockFilepath()
    if suppressExistingFile(lock_filepath):
        return True
    else: 
        return False

# delete on exit
@atexit.register
def deleteLockFileExit():
    if deleteLockFile():
        print(deleted_lock_file_statement) #debug

# delete on load pre
@persistent
def deleteLockFileHandler(scene):
    if bpy.data.window_managers[0].bpm_generalsettings.is_project:
        if deleteLockFile():
            if bpy.data.window_managers[0].bpm_generalsettings.debug: print(deleted_lock_file_statement) #debug