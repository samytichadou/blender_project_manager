from . import project_data_functions as pjt_dta_fct
from .. import global_variables as g_var


def load_custom_folders(winman):

    custom_folders_file, is_folder_file = pjt_dta_fct.getCustomFoldersFile(winman)
    debug = winman.bpm_projectdatas.debug
    custom_folders_coll = winman.bpm_customfolders

    if not is_folder_file:
        custom_folders_coll.clear()
        if debug: print(g_var.no_custom_folder_file_statement) #debug
        return

    general_settings = winman.bpm_generalsettings
    general_settings.bypass_update_tag = True
    
    pjt_dta_fct.loadJsonInCollection(winman, custom_folders_file, custom_folders_coll, 'folders')

    general_settings.bypass_update_tag = False

    if debug: print(g_var.loaded_folders_statement) #debug
