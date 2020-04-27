import bpy
import os


from .dataset_functions import setPropertiesFromDataset


# get strip offsets
def getStripOffsets(strip):
    start_offset = strip.frame_final_start - strip.frame_start
    end_offset = strip.frame_final_end - (strip.frame_start + strip.frame_duration)
    return start_offset, end_offset


# get new timing of a shot strip
def getStripNewTiming(strip) :
    shot_settings = strip.bpm_shotsettings

    old_start = shot_settings.shot_frame_start
    old_end = shot_settings.shot_frame_end

    offset = strip.frame_offset_start - strip.frame_still_start
    start = old_start + offset
    end = old_end + strip.frame_still_end - strip.frame_offset_end

    return start, end


# check if strip is in target timing on the timeline, careful with end frame (-1)
def checkStripInTargetSpaceOnSequencer(start, end, target_start, target_end):
    if target_start >= start and target_start <= end:
        return True
    elif target_end >= start and target_end <= end:
        return True
    elif start >= target_start and end <= target_end:
        return True
    else:
        return False


# return available position for a strip
def returnAvailablePositionStripChannel(start, duration, sequencer):
    unavailable_channels = []
    strip_end = start + duration

    # get unavailable channels
    for s in sequencer.sequences_all:
        s_start = s.frame_final_start
        s_end   = s.frame_final_end - 1
        is_overlapping = checkStripInTargetSpaceOnSequencer(s_start, s_end, start, strip_end)
        if is_overlapping:
            if s.channel not in unavailable_channels:
                unavailable_channels.append(s.channel)

    # loop through channel
    for i in range (1,32):
        if i not in unavailable_channels:
            return i
    return 0


# return selected strips
def returnSelectedStrips(sequencer):
    selected_strips = []
    for strip in sequencer.sequences_all:
        if strip.select:
            selected_strips.append(strip)
    return selected_strips


# update shot strip start/end
def updateSceneStripOnTimeline(strip, winman):
    name = strip.name

    # copy strip
    new_strip = bpy.context.scene.sequence_editor.sequences.new_scene(
        scene       = strip.scene,
        name        = "temp_name",
        channel     = strip.channel,
        frame_start = strip.frame_final_start,
    )

    # set bpm shot props
    new_strip.bpm_shotsettings.shot_filepath = strip.bpm_shotsettings.shot_filepath
    setPropertiesFromDataset(strip.bpm_shotsettings, new_strip.bpm_shotsettings, winman)

    # delete previous strip
    bpy.context.scene.sequence_editor.sequences.remove(strip)

    # correct name dupe
    new_strip.name = name

    return new_strip


# get shot marker position
def getShotMarkerPosition(marker_frame, shot_strip, marker_scn):
    shot_frame = (marker_frame - shot_strip.frame_final_start) + marker_scn.frame_start
    return shot_frame


# get list of sequencer shots names and libs
def getListSequencerShots(sequencer):
    shot_list = []
    lib_list = []
    for s in sequencer.sequences_all:
        # get name
        try:
            if s.bpm_shotsettings.is_shot:
                shot_list.append(s.name)
        except AttributeError: pass
        # get lib
        try:
            if s.bpm_shotsettings.is_shot:
                lib_list.append(s.scene.library)
        except AttributeError: pass
    return shot_list, lib_list


# delete all strips
def deleteAllSequencerStrips(sequencer):
    for strip in sequencer.sequences_all:
        sequencer.sequences.remove(strip)


# create sequencer if none
def createSequencer(scene):
    if scene.sequence_editor is None:
        scene.sequence_editor_create()
        return True
    return False


# return all shot strips in sequencer
def returnShotStrips(sequencer):
    shot_list = []
    for strip in sequencer.sequences_all:
        if strip.type in {'SCENE', 'IMAGE'}:
            if strip.bpm_shotsettings.is_shot:
                shot_list.append(strip)
    return shot_list


# deselect all strips
def deselectAllStrips(sequencer):
    for strip in sequencer.sequences_all:
        if strip.select:
            strip.select = False


# update shot image sequence on timeline
def updateImageSequenceShot(strip, winman):
    from .change_strip_display_mode_functions import completeRenderMissingImages
    from .file_functions import absolutePath, returnRenderFilePathFromShot
    from .project_data_functions import returnRenderExtensionFromSettings, setPropertiesFromJsonDataset
    from ..global_variables import created_strip_statement, setting_strip_properties_statement
    from .json_functions import createJsonDatasetFromProperties

    debug = winman.bpm_generalsettings.debug

    # get settings
    name = strip.name
    channel = strip.channel
    strip_frame_start = strip.frame_final_start

    shot_settings = strip.bpm_shotsettings

    start_frame = shot_settings.shot_frame_start
    end_frame = shot_settings.shot_frame_end

    render_filepath = returnRenderFilePathFromShot(absolutePath(shot_settings.shot_filepath), winman, shot_settings.shot_timeline_display)

    sequence_folder = os.path.dirname(render_filepath)

    extension = returnRenderExtensionFromSettings(winman.bpm_rendersettings[shot_settings.shot_timeline_display])
    
    # get render image sequence
    frames = completeRenderMissingImages(render_filepath, extension, start_frame, end_frame, debug)
    
    first = os.path.join(sequence_folder, frames[0])

    # store shot settings
    shot_dataset = createJsonDatasetFromProperties(shot_settings, ())

    # delete previous strip
    bpy.context.scene.sequence_editor.sequences.remove(strip)

    # copy strip
    new_strip = bpy.context.scene.sequence_editor.sequences.new_image(
        filepath    = first,
        name        = "temp_name",
        channel     = channel,
        frame_start = strip_frame_start,
    )

    if debug: print(created_strip_statement + name) #debug

    if debug: print(setting_strip_properties_statement) #debug

    # remove first image already used
    frames.remove(frames[0])

    # get all images
    for f in frames:
        new_strip.elements.append(f)

    # set bpm shot props
    setPropertiesFromJsonDataset(shot_dataset, new_strip.bpm_shotsettings, debug, ())

    # correct name dupe
    new_strip.name = name

    return new_strip