import bpy, os

from .dataset_functions import setPropertiesFromJsonDataset
from .json_functions import read_json
from ..global_variables import (
                            comment_file,
                            loading_comments_statement,
                            editing_comment_statement,
                            no_comment_file_statement,
                            comment_reloaded_statement,
                        )



def return_commentcoll_folderpath(comment_type, context):
    winman = context.window_manager

    if comment_type == "edit_shot":
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        comment_collection = shot_settings.comments
        folder_path = os.path.dirname(bpy.path.abspath(shot_settings.shot_filepath))

    elif comment_type == "shot":
        shot_settings = winman.bpm_shotsettings
        comment_collection = shot_settings.comments
        folder_path = os.path.dirname(bpy.path.abspath(shot_settings.shot_filepath))

    elif comment_type == "edit":
        project_settings = winman.bpm_projectdatas
        comment_collection = project_settings.comments
        folder_path = os.path.dirname(bpy.data.filepath)

    elif comment_type == "asset":
        asset_settings = winman.bpm_assetsettings
        comment_collection = asset_settings.comments
        folder_path = os.path.dirname(bpy.data.filepath)

    return (comment_collection, folder_path)


def reload_comments(context, comment_type):
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    debug = winman.bpm_projectdatas.debug

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

    if debug: print(comment_reloaded_statement) #debug