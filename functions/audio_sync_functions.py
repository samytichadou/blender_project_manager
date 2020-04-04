import bpy
import os


from .dataset_functions import setPropertiesFromJsonDataset
from .strip_functions import checkStripInTargetSpaceOnSequencer, deleteAllSequencerStrips, createSequencer
from .json_functions import read_json
from ..global_variables import (
                            audio_sync_file, 
                            starting_shot_audio_sync_statement,
                            shot_audio_synced_statement,
                            sync_file_not_found_statement,
                            cleaning_timeline_statement,
                            creating_sequencer_statement,
                            reading_json_statement,
                            shot_not_used_statement,
                            loaded_sounds_statement,
                            created_sound_strips_statement,
                        )


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


# sync audio shot function for startup handler
def autoSyncAudioShot(debug, project_folder, scene):

    audio_sync_json = os.path.join(project_folder, audio_sync_file)
    if not os.path.isfile(audio_sync_json):
        if debug: print(sync_file_not_found_statement) #debug
        return 'SYNC_FILE_MISSING'

    if debug: print(starting_shot_audio_sync_statement) #debug

    # create sequencer if none
    created_sequencer = createSequencer(scene)
    if not created_sequencer:
        # delete existing strips
        if debug: print(cleaning_timeline_statement) #debug
        deleteAllSequencerStrips(scene.sequence_editor)
    else:
        if debug: print(creating_sequencer_statement)

    # get json datas
    if debug: print(reading_json_statement + audio_sync_json) #debug
    datas = read_json(audio_sync_json)

    # find shot offset
    current_shot_datas, offset = findShotOffsetFromSyncFile(datas, scene.name, scene.frame_start)

    # if shot strip not found in timeline
    if current_shot_datas is None:      
        if debug: print(shot_not_used_statement) #debug
        return 'SHOT_NOT_USED'

    # iterate through sounds and strips
    # load sounds
    sound_list = loadSoundsFromSyncFile(datas)
    if debug: print(loaded_sounds_statement + str(sound_list)) #debug

    # strips
    sound_strip_list = createSoundStripsFromSyncFile(datas, scene.sequence_editor, current_shot_datas, offset)
    if debug: print(created_sound_strips_statement + str(sound_strip_list)) #debug

    if debug: print(shot_audio_synced_statement) #debug

    return 'FINISHED'