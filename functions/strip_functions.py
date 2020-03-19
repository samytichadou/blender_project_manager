import bpy


# return strip duration
def returnStripStartEnd(strip):
    start = strip.frame_start + strip.frame_offset_start
    end = start + strip.frame_final_duration - 1
    return start, end

# check if strip is in target timing on the timeline
def checkStripInTargetSpaceOnSequencer(start, end, target_start, target_end):
    if target_start >= start and target_start <= end:
        return True
    elif target_end >= start and target_end <= end:
        return True
    elif start >= target_start and end <= target_end:
        return True
    else:
        return False

# returne available position for a strip
def returnAvailablePositionStripChannel(start, duration, sequencer):
    unavailable_channels = []
    strip_end = start + duration

    # get unavailable channels
    for s in sequencer.sequences_all:
        s_start, s_end = returnStripStartEnd(s)
        is_overlapping = checkStripInTargetSpaceOnSequencer(s_start, s_end, start, strip_end)
        if is_overlapping:
            if s.channel not in unavailable_channels:
                unavailable_channels.append(s.channel)

    # loop through channel
    for i in range (1,32):
        if i not in unavailable_channels:
            return i
    return 0