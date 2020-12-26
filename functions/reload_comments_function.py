import os

from .dataset_functions import setPropertiesFromJsonDataset
from .json_functions import read_json
from ..operators.comments_operators import return_commentcoll_folderpath
from ..global_variables import (
                            comment_file,
                            loading_comments_statement,
                            editing_comment_statement,
                            no_comment_file_statement,
                        )

def reload_comments(context, comment_type):
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    debug = general_settings.debug

    if debug: print(loading_comments_statement) #debug

    comment_collection, folderpath = return_commentcoll_folderpath(comment_type, context)

    comment_filepath = os.path.join(folderpath, comment_file)

    # empty comment collection
    comment_collection.clear()

    # check if file exists
    if not os.path.isfile(comment_filepath):
        if debug: print(no_comment_file_statement + comment_filepath) #debug
        return

    # set comments from json
    for c in read_json(comment_filepath)["comments"]:
        if debug: print(editing_comment_statement + c['name'])
        dataset_out = comment_collection.add()
        setPropertiesFromJsonDataset(c, dataset_out, debug, ())