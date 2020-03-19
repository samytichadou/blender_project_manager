import bpy


# return strip duration
def returnStripStartEnd(strip):
    start = strip.frame_start + strip.frame_offset_start
    end = start + strip.frame_final_duration - 1
    return start, end

# check if strip is in target timing on the timeline
def checkStripInTargetSpaceOnSequencer(start, end, target_start, target_end):
    if start <= target_start and end >= target_start:
        return True
    elif start <= target_start and end >= target_end:
        return True
    if start <= target_end and end >= target_end:
        return True
    else:
        return False

# returne available position for a strip
def returnAvailablePositionStripChannel(start, duration, sequencer):
    unavailable_channels = []
    strip_end = start + duration - 1

    for s in sequencer.sequences_all:
        s_start, s_end = returnStripStartEnd(s)
        if checkStripInTargetSpaceOnSequencer(s_start, s_end, start, strip_end):
            unavailable_channels.append(s.channel)

    for i in range (1,32):
        if i not in unavailable_channels:
            return i

    return 1