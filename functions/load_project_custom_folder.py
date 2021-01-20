from .project_data_functions import getCustomFoldersFile, loadJsonInCollection
from ..global_variables import (
                            loaded_folders_statement,
                            no_custom_folder_file_statement,
                            )


def load_custom_folders(winman):

    custom_folders_file, is_folder_file = getCustomFoldersFile(winman)
    debug = winman.bpm_projectdatas.debug
    custom_folders_coll = winman.bpm_customfolders

    if not is_folder_file:
        custom_folders_coll.clear()
        if debug: print(no_custom_folder_file_statement) #debug
        return

    general_settings = winman.bpm_generalsettings
    general_settings.bypass_update_tag = True
    
    loadJsonInCollection(winman, custom_folders_file, custom_folders_coll, 'folders')

    general_settings.bypass_update_tag = False

    if debug: print(loaded_folders_statement) #debug