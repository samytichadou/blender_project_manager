import bpy, os
from bpy.app.handlers import persistent


from .functions.project_data_functions import getProjectDataFile, createProjectDatas, getCustomFoldersFile, loadCustomFolders
from .global_variables import startup_statement, loaded_datas_statement, no_datas_statement, loaded_folders_statement


@persistent
def bpmStartupHandler(scene):
    winman = bpy.data.window_managers[0]
    if winman.bpm_debug: print(startup_statement) #debug

    #load project datas
    project_data_file = getProjectDataFile(winman)
    if project_data_file is not None:
        createProjectDatas(winman, project_data_file)
        if winman.bpm_debug: print(loaded_datas_statement) #debug

        #load project custom folders
        custom_folders_file = getCustomFoldersFile(winman)
        if custom_folders_file is not None:
            loadCustomFolders(winman, custom_folders_file)
            if winman.bpm_debug: print(loaded_folders_statement) #debug

    else:
        if winman.bpm_debug: print(no_datas_statement) #debug