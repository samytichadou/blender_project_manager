import bpy
import os

from .dataset_functions import setPropertiesFromJsonDataset
from .json_functions import read_json
from .. import global_variables as g_var


# get shot comment frame in timeline
def get_shot_comment_frame(comment_frame, strip):
    comment_frame = (comment_frame - strip.bpm_shotsettings.shot_frame_start) + strip.frame_start
    return comment_frame


def return_commentcoll_folderpath(comment_type, context, strip):
    winman = context.window_manager

    if comment_type == "edit_shot":
        if strip is not None:
            shot_settings = strip.bpm_shotsettings
            comment_collection = shot_settings.comments
            folder_path = os.path.dirname(bpy.path.abspath(shot_settings.shot_filepath))
        else:
            comment_collection = folder_path = None

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


def reload_comments(context, comment_type, strip):
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug

    if debug: print(g_var.loading_comments_statement) #debug

    comment_collection, folderpath = return_commentcoll_folderpath(comment_type, context, strip)

    comment_filepath = os.path.join(folderpath, g_var.comment_file)

    # get hide status
    hide_list = []
    for c in comment_collection:
        hide_list.append((c.name, c.hide))

    # empty comment collection
    comment_collection.clear()

    # check if file exists
    if not os.path.isfile(comment_filepath):
        if debug: print(g_var.no_comment_file_statement + comment_filepath) #debug
        return

    # set comments from json
    for c in read_json(comment_filepath)["comments"]:
        if debug: print(g_var.editing_comment_statement + c['name'])
        dataset_out = comment_collection.add()
        setPropertiesFromJsonDataset(c, dataset_out, debug, ())
    
    # set hide and timeline frame for shots
    for c in comment_collection:
        for oc in hide_list:
            if oc[0] == c.name:
                c.hide = oc[1]
                break
        if comment_type == "edit_shot":
            c.timeline_frame = get_shot_comment_frame(c.frame, strip)


    if debug: print(g_var.comment_reloaded_statement) #debug
