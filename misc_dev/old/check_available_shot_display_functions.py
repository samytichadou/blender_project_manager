import bpy
import os


from .strip_functions import returnShotStrips
from .file_functions import returnRenderFolderFromStrip, absolutePath

from ..properties import shot_render_state_items
from ..global_variables import (
                            refreshing_timeline_shot_display_mode,
                            refreshed_timeline_shot_display_mode,
                            render_folder, 
                            render_shots_folder, 
                            render_draft_folder, 
                            render_render_folder, 
                            render_final_folder,
                        )


# refresh shot strips timeline display mode available
def refreshShotStripsDisplay(winman, sequencer):

    general_settings = winman.bpm_generalsettings
    debug = winman.bpm_projectdatas.debug

    if debug: print(refreshing_timeline_shot_display_mode) #debug

    for s in returnShotStrips(sequencer):
        shot_settings = s.bpm_shotsettings

        shot_filepath = absolutePath(s.bpm_shotsettings.shot_filepath)
        shot_draft, shot_render, shot_final = returnRenderFolderFromStrip(shot_filepath, general_settings.project_folder)

        shot_settings.is_draft = False
        if os.path.isdir(shot_draft):
            shot_settings.is_draft = True

        shot_settings.is_render = False
        if os.path.isdir(shot_render):
            shot_settings.is_render = True

        shot_settings.is_final = False
        if os.path.isdir(shot_final):
            shot_settings.is_final = True

    if debug: print(refreshed_timeline_shot_display_mode) #debug