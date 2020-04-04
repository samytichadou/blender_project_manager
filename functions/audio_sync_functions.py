import bpy


from .dataset_functions import setPropertiesFromJsonDataset
from .strip_functions import checkStripInTargetSpaceOnSequencer


# find a shot strip offset from the audio sync file
def findShotOffsetFromSyncFile(datas, shot_name, shot_start):
    for strip in datas['shot_strips']:
        if strip['name'] == shot_name:
            shot_strip_datas = strip
            offset = -strip['frame_start'] + shot_start
            return shot_strip_datas, offset
    return None, None


# load all non existing sound into the blend from audio sync file
def loadSoundsFromSyncFile(datas):
    sound_list = []

    for s in datas['sounds']:
        try:
            bpy.data.sounds[s['name']]
        except KeyError:
            sound_list.append(s['name'])
            sound = bpy.data.sounds.load(s['filepath'])
            setPropertiesFromJsonDataset(s, sound, False, ())

    return sound_list


# create sound strips from audio sync file in sequencer
def createSoundStripsFromSyncFile(datas, sequencer, shot_strip_datas, offset):
    sound_strip_list = []

    # get random filepath for strip creation
    fp = datas['sounds'][0]['filepath']

    for s in datas['sound_strips']:

        # check if strip overlaps
        overlap = checkStripInTargetSpaceOnSequencer(s['frame_final_start'], s['frame_final_end']-1, shot_strip_datas['frame_final_start'], shot_strip_datas['frame_final_end']-1)

        if overlap:
            sound_strip_list.append(s['name'])

            new_strip = sequencer.sequences.new_sound(s['name'], fp, s['channel'], s['frame_start'] + offset)
            new_strip.sound = bpy.data.sounds[s['sound']]

            new_strip.frame_final_start = s['frame_final_start'] + offset
            new_strip.frame_final_duration = s['frame_final_duration']
            
            setPropertiesFromJsonDataset(s, new_strip, False, ("frame", "animation"))

            new_strip.lock = True
    
    return sound_strip_list