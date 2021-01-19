from .project_data_functions import getCustomFoldersFile, loadJsonInCollection
from ..global_variables import (
                            folders_loading_statement,
                            loaded_folders_statement,
                            no_custom_folder_file_statement,
                            )


def load_custom_folders(winman):

    custom_folders_file, is_folder_file = getCustomFoldersFile(winman)
    debug = winman.bpm_projectdatas.debug

    if not is_folder_file:
        if debug: print(no_custom_folder_file_statement) #debug
        return

    if debug: print(folders_loading_statement + custom_folders_file) #debug
    custom_folders_coll = winman.bpm_customfolders
    loadJsonInCollection(winman, custom_folders_file, custom_folders_coll, 'folders')
    if debug: print(loaded_folders_statement) #debug