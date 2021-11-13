import bpy
import os

from .dataset_functions import setPropertiesFromJsonDataset
from . import strip_functions as str_fct
from . import json_functions as js_fct
from .file_functions import absolutePath
from .. import global_variables as g_var


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
        overlap = str_fct.checkStripInTargetSpaceOnSequencer(s['frame_final_start'], s['frame_final_end']-1, shot_strip_datas['frame_final_start'], shot_strip_datas['frame_final_end']-1)

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
def syncAudioShot(debug, project_folder, scene):

    audio_sync_json = os.path.join(project_folder, g_var.audio_sync_file)
    if not os.path.isfile(audio_sync_json):
        if debug: print(g_var.sync_file_not_found_statement) #debug
        return 'SYNC_FILE_MISSING'

    if debug: print(g_var.starting_shot_audio_sync_statement) #debug

    # create sequencer if none
    created_sequencer = str_fct.createSequencer(scene)
    if not created_sequencer:
        # delete existing strips
        if debug: print(g_var.cleaning_timeline_statement) #debug
        str_fct.deleteAllSequencerStrips(scene.sequence_editor)
    else:
        if debug: print(g_var.creating_sequencer_statement)

    # get json datas
    if debug: print(g_var.reading_json_statement + audio_sync_json) #debug
    datas = js_fct.read_json(audio_sync_json)

    # find shot offset
    current_shot_datas, offset = findShotOffsetFromSyncFile(datas, scene.name, scene.frame_start)

    # if shot strip not found in timeline
    if current_shot_datas is None:      
        if debug: print(g_var.shot_not_used_statement) #debug
        return 'SHOT_NOT_USED'

    # iterate through sounds and strips
    # load sounds
    sound_list = loadSoundsFromSyncFile(datas)
    if debug: print(g_var.loaded_sounds_statement + str(sound_list)) #debug

    # strips
    sound_strip_list = createSoundStripsFromSyncFile(datas, scene.sequence_editor, current_shot_datas, offset)
    if debug: print(g_var.created_sound_strips_statement + str(sound_strip_list)) #debug

    if debug: print(g_var.shot_audio_synced_statement) #debug

    return 'FINISHED'

# sync audio edit function
def syncAudioEdit(debug, project_folder, scene):

    if debug: print(g_var.starting_audio_sync_file_statement) #debug


    # get audio sync filepath
    filepath = os.path.join(project_folder, g_var.audio_sync_file)
    sequencer = scene.sequence_editor

    # init json datas
    if debug: print(g_var.initialize_json_statement + filepath) #debug

    datas = js_fct.initializeAssetJsonDatas({'sounds', 'sound_strips', 'shot_strips'})

    sound_list = []

    # iterate through strips
    for strip in sequencer.sequences_all:

        if strip.type == 'SOUND':

            if debug: print(g_var.adding_dataset_to_json + strip.name) #debug
            
            # sound datas
            sound = strip.sound
            if sound not in sound_list:
                sound_list.append(sound)
                sound_datas = js_fct.createJsonDatasetFromProperties(sound, ())
                sound_datas['filepath'] = absolutePath(sound.filepath)
                datas['sounds'].append(sound_datas)

            # strip datas
            strip_datas = js_fct.createJsonDatasetFromProperties(strip, ())
            strip_datas['sound'] = sound.name    
            datas['sound_strips'].append(strip_datas)

        else:
            # shot datas
            try:
                if strip.bpm_shotsettings.is_shot:
                    shot_datas = js_fct.createJsonDatasetFromProperties(strip, ())
                    datas['shot_strips'].append(shot_datas)

            except AttributeError:
                pass
    
    if debug: print(g_var.saving_to_json_statement) #debug

    js_fct.create_json_file(datas, filepath)

    if debug: print(g_var.saved_to_json_statement) #debug

    if debug: print(g_var.audio_sync_file_created_statement) #debug

    return 'FINISHED'