import bpy


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

# return available position for a strip
def returnAvailablePositionStripChannel(start, duration, sequencer):
    unavailable_channels = []
    strip_end = start + duration

    # get unavailable channels
    for s in sequencer.sequences_all:
        s_start = s.frame_final_start
        s_end = s.frame_final_end - 1
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