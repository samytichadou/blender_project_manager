import bpy
import os


from .strip_functions import returnShotStrips
from .file_functions import counFilesInFolder

from ..properties import shot_render_state_items
from ..global_variables import (
                            render_folder, 
                            render_shots_folder, 
                            render_draft_folder, 
                            render_render_folder, 
                            render_final_folder,
                        )


# refresh shot strips timeline display mode available
def refreshShotStripsDisplay(winman, sequencer):

    print("start refreshing available shot strips display mode")

    general_settings = winman.bpm_generalsettings

    for s in returnShotStrips(sequencer):
        length = s.frame_duration
        shot_settings = s.bpm_shotsettings

        # get render folder
        shot_name = os.path.splitext(os.path.basename(s.scene.library.filepath))[0]

        render_folder_path = os.path.join(general_settings.project_folder, render_folder)
        render_shot_folder_path = os.path.join(render_folder_path, render_shots_folder)

        draft_folder_path = os.path.join(render_shot_folder_path, render_draft_folder)
        render_folder_path = os.path.join(render_shot_folder_path, render_render_folder)
        final_folder_path = os.path.join(render_shot_folder_path, render_final_folder)

        shot_draft_folder_path = os.path.join(draft_folder_path, shot_name)
        shot_render_folder_path = os.path.join(render_folder_path, shot_name)
        shot_final_folder_path = os.path.join(final_folder_path, shot_name)

        shot_settings.is_draft = False
        if os.path.isdir(shot_draft_folder_path):
            if counFilesInFolder(shot_draft_folder_path) == length:
                shot_settings.is_draft = True

        shot_settings.is_render = False
        if os.path.isdir(shot_render_folder_path):
            if counFilesInFolder(shot_render_folder_path) == length:
                shot_settings.is_render = True

        shot_settings.is_final = False
        if os.path.isdir(shot_final_folder_path):
            if counFilesInFolder(shot_final_folder_path) == length:
                shot_settings.is_final = True