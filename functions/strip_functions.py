import bpy


# return strip duration
def returnStripStartEnd(strip):
    start = strip.frame_start + strip.frame_offset_start
    end = start + strip.frame_final_duration - 1
    return start, end

# check if strip is in target timing on the timeline
def checkStripInTargetSpaceOnSequencer(start, end, target_start, target_end):
    print("start -------- " + str(start))
    print("target_start - " + str(target_start))
    print("end ---------- " + str(end))
    print("target_end---- " + str(target_end))
    if target_start >= start and target_start <= end:
        print("sit1")
        return True
    elif target_end >= start and target_end <= end:
        print("sit2")
        return True
    elif start >= target_start and end <= target_end:
        print("sit3")
        return True
    else:
        print("sit0")
        return False

# returne available position for a strip
def returnAvailablePositionStripChannel(start, duration, sequencer):
    unavailable_channels = []
    strip_end = start + duration

    for s in sequencer.sequences_all:
        s_start, s_end = returnStripStartEnd(s)
        print()
        print(s.name)
        is_overlapping = checkStripInTargetSpaceOnSequencer(s_start, s_end, start, strip_end)
        if is_overlapping:
            if s.channel not in unavailable_channels:
                unavailable_channels.append(s.channel)

    print(unavailable_channels)
    for i in range (1,32):
        if i not in unavailable_channels:
            print(i)
            return i

    return 1