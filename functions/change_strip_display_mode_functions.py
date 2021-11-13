import bpy
import os
import shutil

from . import file_functions as fl_fct
from .utils_functions import clearDataUsers
from .strip_functions import getListSequencerShots
from .dataset_functions import setPropertiesFromDataset
from .project_data_functions import returnRenderExtensionFromSettings
from .reload_comments_function import reload_comments
from .. import global_variables as g_var                        


# fill with missing images
def completeRenderMissingImages(render_filepath, extension, start_frame, end_frame, debug):

    render_folderpath = os.path.dirname(render_filepath)

    # create folder if needed
    if not os.path.isdir(render_folderpath):
        os.makedirs(render_folderpath, exist_ok=True)

    frame_list = fl_fct.returnAllFilesInFolder(render_folderpath)
    shot_frames = []

    # no image rendered
    if len(frame_list) == 0:
        
        if debug: print(g_var.shot_display_no_render_images_statement) #debug

        for i in range(start_frame, end_frame + 1):

            image_filepath = render_filepath + str(i).zfill(5) + extension
            shutil.copy(g_var.missing_file_image, image_filepath)
            shot_frames.append(os.path.basename(image_filepath))

    # image rendered
    else:

        if debug: print(g_var.shot_display_render_images_statement) #debug

        frames_to_create = []

        for i in range(start_frame, end_frame + 1):
            image_filepath = render_filepath + str(i).zfill(5) + extension
            image_file = os.path.basename(image_filepath)
            shot_frames.append(image_file)

            if image_file not in frame_list:
                frames_to_create.append(image_file)

        for f in frame_list:
            if f not in shot_frames:
                fl_fct.suppressExistingFile(os.path.join(render_folderpath, f))
                pass
                
        for f in frames_to_create:
            image_filepath = os.path.join(render_folderpath, f)
            shutil.copy(g_var.missing_file_image, image_filepath)

    return shot_frames


# update shot strip to image sequence
def updateStripToImageSequence(strip, sequencer, sequence_folder, winman):
    debug = winman.bpm_projectdatas.debug

    # get settings
    name = strip.name
    final_start = strip.frame_final_start
    final_duration = strip.frame_final_duration

    shot_settings = strip.bpm_shotsettings

    start_frame = shot_settings.shot_frame_start
    end_frame = shot_settings.shot_frame_end

    render_filepath = fl_fct.returnRenderFilePathFromShot(fl_fct.absolutePath(shot_settings.shot_filepath), winman, shot_settings.shot_timeline_display)

    extension = returnRenderExtensionFromSettings(winman.bpm_rendersettings[shot_settings.shot_timeline_display])

    frames = completeRenderMissingImages(render_filepath, extension, start_frame, end_frame, debug)
    
    first = os.path.join(sequence_folder, frames[0])

    # copy strip
    new_strip = bpy.context.scene.sequence_editor.sequences.new_image(
        filepath    = first,
        name        = "temp_name",
        channel     = strip.channel,
        frame_start = strip.frame_start,
    )

    if debug: print(g_var.created_strip_statement + strip.name) #debug

    if debug: print(g_var.setting_strip_properties_statement) #debug

    # remove first image already used
    frames.remove(frames[0])
    # get all images
    for f in frames:
        new_strip.elements.append(f)

    # set bpm shot props
    setPropertiesFromDataset(strip.bpm_shotsettings, new_strip.bpm_shotsettings, winman)

    # delete previous strip

    lib = None
    if strip.type == 'SCENE':
        lib = strip.scene.library

    bpy.context.scene.sequence_editor.sequences.remove(strip)

    # remove libraries
    if lib is not None:

        # check if old library is still used
        lib_used = getListSequencerShots(sequencer)[1]

        if lib not in lib_used:
            if debug: print(g_var.library_cleared_statement + lib.filepath) #debug

            clearDataUsers(lib)
            bpy.data.orphans_purge()

    # set frame offset
    new_strip.frame_final_start = final_start
    new_strip.frame_final_duration = final_duration

    # correct name dupe
    new_strip.name = name

    return new_strip


# update shot strip to scene
def updateStripToScene(strip, winman):
    debug = winman.bpm_projectdatas.debug

    # get settings
    name = strip.name
    final_start = strip.frame_final_start
    final_duration = strip.frame_final_duration

    # link new scene
    shot_path = fl_fct.absolutePath(strip.bpm_shotsettings.shot_filepath)
    fl_fct.linkExternalScenes(shot_path)
    if debug: print(g_var.scenes_linked_statement + shot_path) #debug

    # link strip to new scene
    scene_to_link = None
    for s in bpy.data.scenes:
        if s.library:
            if fl_fct.absolutePath(s.library.filepath) == shot_path:
                if s.name == strip.name:
                    scene_to_link = s
                    break
    # error message if scene not found
    if scene_to_link is None:
        if debug: print(g_var.scene_not_found_statement + strip.name) #debug
        return

    # copy strip
    new_strip = bpy.context.scene.sequence_editor.sequences.new_scene(
        scene       = scene_to_link,
        name        = "temp_name",
        channel     = strip.channel,
        frame_start = strip.frame_start,
    )

    if debug: print(g_var.created_strip_statement + strip.name) #debug

    if debug: print(g_var.setting_strip_properties_statement) #debug

    # set bpm shot props
    setPropertiesFromDataset(strip.bpm_shotsettings, new_strip.bpm_shotsettings, winman)

    # delete previous strip
    bpy.context.scene.sequence_editor.sequences.remove(strip)
    
    # set frame offset
    new_strip.frame_final_start = final_start
    new_strip.frame_final_duration = final_duration

    # correct name dupe
    new_strip.name = name

    return new_strip


# update function for shot display mode
def updateShotDisplayMode(self, context):
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    debug = winman.bpm_projectdatas.debug
    sequencer = context.scene.sequence_editor
    active = sequencer.active_strip

    if general_settings.bypass_update_tag:
        #if debug: print(bypass_settings_update_statement) #debug
        return

    general_settings.bypass_update_tag = True

    display_mode = self.shot_timeline_display

    if debug: print(g_var.setting_strip_display_mode_statement + display_mode) #debug

    # open gl
    if display_mode == '00_openGL':
        if active.type != 'SCENE':
            new_strip = updateStripToScene(active, winman)

    else:
        shot_filepath = fl_fct.absolutePath(active.bpm_shotsettings.shot_filepath)
        shot_draft, shot_render, shot_final = fl_fct.returnRenderFolderFromStrip(shot_filepath, winman.bpm_generalsettings.project_folder)
        # draft
        if display_mode == g_var.render_draft_folder:
            shot_render_folder = shot_draft
        elif display_mode == g_var.render_render_folder:
            shot_render_folder = shot_render
        elif display_mode == g_var.render_final_folder:
            shot_render_folder = shot_final
        
        new_strip = updateStripToImageSequence(active, sequencer, shot_render_folder, winman)

    sequencer.active_strip = new_strip

    # reload comments
    reload_comments(context, "edit_shot", new_strip)

    general_settings.bypass_update_tag = False