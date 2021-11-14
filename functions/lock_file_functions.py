import bpy
import os

from bpy.app.handlers import persistent

from .. import global_variables as g_var
from .file_functions import suppressExistingFile
from . import utils_functions as utl_fct
from . import json_functions as js_fct


# update function when finding lock file
def update_function_already_opened(self, context):
    if self.blend_already_opened:
        bpy.ops.bpm.dialog_popups(
                            'INVOKE_DEFAULT',
                            operator = "bpm.show_open_blend_lock_file",
                            operator_icon = "ERROR",
                            )


# get lock filepath
def getLockFilepath():
    return os.path.splitext(bpy.data.filepath)[0] + g_var.lockfile_extension


# format json opened entry
def formatJsonOpenedEntry():
    json_dataset = {}
    json_dataset['hostname'] = utl_fct.getHostName()
    json_dataset['timestamp'] = utl_fct.getTimestamp()
    json_dataset['pid'] = utl_fct.getCurrentPID()
    return json_dataset


# create lock file
def setupLockFile():
    lock_filepath = getLockFilepath()

    if os.path.isfile(lock_filepath):
        datas = js_fct.read_json(lock_filepath)
    else:
        datas = js_fct.initializeAssetJsonDatas({'opened'})

    datas['opened'].append(formatJsonOpenedEntry())

    js_fct.create_json_file(datas, lock_filepath)

    return lock_filepath


# delete lock file if existing
def clearLockFile(lock_filepath):

    if os.path.isfile(lock_filepath):

        pid = utl_fct.getCurrentPID()
        datas = js_fct.read_json(lock_filepath)
        n = 0
        for o in datas['opened']:
            if o['pid'] == pid:
                del datas['opened'][n]
                break
            n += 1

        if len(datas['opened']) != 0:
            js_fct.create_json_file(datas, lock_filepath)
            return 'UPDATED'
        else:
            suppressExistingFile(lock_filepath)
            return 'DELETED'
    else:
        return 'NONE'


# delete on exit
def deleteLockFileExit(lock_filepath):
    if clearLockFile(lock_filepath) in {'UPDATED', 'DELETED'}:
        print(g_var.deleted_lock_file_statement) #debug

# delete on load pre
@persistent
def deleteLockFileHandler(scene):
    winman = bpy.data.window_managers[0]
    if winman.bpm_generalsettings.is_project:
        if clearLockFile(getLockFilepath()) in {'UPDATED', 'DELETED'}:
            if winman.bpm_projectdatas.debug: print(g_var.deleted_lock_file_statement) #debug
