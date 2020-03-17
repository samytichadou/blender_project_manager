import bpy, os
from bpy.app.handlers import persistent


from .functions.project_data_functions import getProjectDataFile
from .global_variables import startup_statement, loaded_datas_statement, no_datas_statement


@persistent
def bpmStartupHandler(scene):
    winman = bpy.data.window_managers[0]
    if winman.bpm_debug: print(startup_statement) #debug

    project_data_file = getProjectDataFile(winman)
    if project_data_file is not None:
        #winman.bpm_isproject = True
        if winman.bpm_debug: print(loaded_datas_statement) #debug
    else:
        if winman.bpm_debug: print(no_datas_statement) #debug
        #winman.bpm_isproject = False