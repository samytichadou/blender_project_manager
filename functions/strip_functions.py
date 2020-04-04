import bpy


# get strip offsets
def getStripOffsets(strip):
    start_offset    = strip.frame_final_start   - strip.frame_start
    end_offset      = strip.frame_final_end     - (strip.frame_start + strip.frame_duration)
    return start_offset, end_offset


# get new timing of a shot strip
def getStripNewTiming(strip) :
    strip_scene = strip.scene
    offset = strip.frame_offset_start - strip.frame_still_start
    start = strip_scene.frame_start + offset
    end = strip_scene.frame_end + strip.frame_still_end - strip.frame_offset_end

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
def updateStripOnTimeline(strip):
    # print("DEBUG --- frame_start : "+str(strip.frame_start))
    # copy strip
    new_strip = bpy.context.scene.sequence_editor.sequences.new_scene(
        scene       = strip.scene,
        name        = strip.name,
        channel     = strip.channel,
        frame_start = strip.frame_final_start,
    )
    # set it to bpm shot
    new_strip.bpm_shotsettings.is_shot = True
    # delete previous strip
    bpy.context.scene.sequence_editor.sequences.remove(strip)
    return new_strip


# get shot marker position
def getShotMarkerPosition(marker_frame, shot_strip, marker_scn):
    shot_frame = (marker_frame - shot_strip.frame_final_start) + marker_scn.frame_start
    return shot_frame


# get list of sequencer shot and libs
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