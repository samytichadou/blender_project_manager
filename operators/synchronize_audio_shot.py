import bpy
import os


class BPMSynchronizeAudioShot(bpy.types.Operator):
    """Synchronize audio edit file from edit"""
    bl_idname = "bpm.synchronize_audio_shot"
    bl_label = "Synchronize audio shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'SHOT'

    def execute(self, context):
        # import statements and functions
        from ..functions.file_functions import absolutePath
        from ..functions.json_functions import read_json
        from ..functions.dataset_functions import setPropertiesFromJsonDataset
        from ..functions.strip_functions import deleteAllSequencerStrips, checkStripInTargetSpaceOnSequencer
        from ..global_variables import (
                                    audio_sync_file,
                                )

        general_settings = context.window_manager.bpm_generalsettings
        sequencer = context.scene.sequence_editor
        debug = general_settings.debug

        if debug: print() #debug

        # get audio sync filepath
        filepath = absolutePath(os.path.join(general_settings.project_folder, audio_sync_file))
        scn = context.scene
        sequencer = scn.sequence_editor
        current_shot_strip = None
        offset = 0

        if not os.path.isfile(filepath):
            if debug: print("No synchronization file") #debug
            return {'FINISHED'}

        if debug: print("Synchronizing shot audio") #debug

        # create sequencer if none
        if sequencer is None:
            if debug: print("Creating sequencer")
            scn.sequence_editor_create()

        else:
            # delete existing strips
            if debug: print("Removing existing strips") #debug
            deleteAllSequencerStrips(sequencer)

        # get json datas
        if debug: print() #debug
        datas = read_json(filepath)

        # find shot offset
        for strip in datas['shot_strips']:
            if strip['name'] == scn.name: # TODO use blend name for startup
                current_shot_strip = strip
                offset = -strip['frame_start'] + scn.frame_start
                break

        # if shot strip not find in timeline
        if current_shot_strip is None:
            if debug: print("Shot not used in timeline") #debug
            return {'FINISHED'}

        # iterate through the strips
        # sounds
        for s in datas['sounds']:
            try:
                bpy.data.sounds[s['name']]
            except KeyError:
                if debug: print("Loading sound : " + s['name']) #debug

                sound = bpy.data.sounds.load(s['filepath'])
                setPropertiesFromJsonDataset(s, sound, debug, ())

        # get random filepath for strip creation
        fp = datas['sounds'][0]['filepath']

        # strips
        for s in datas['sound_strips']:

            # check if strip overlaps
            overlap = checkStripInTargetSpaceOnSequencer(s['frame_final_start'], s['frame_final_end']-1, current_shot_strip['frame_final_start'], current_shot_strip['frame_final_end']-1)

            if overlap:

                if debug: print("Creating strip : " + s['name']) #debug

                new_strip = sequencer.sequences.new_sound(s['name'], fp, s['channel'], s['frame_start'] + offset)
                new_strip.sound = bpy.data.sounds[s['sound']]

                new_strip.frame_final_start = s['frame_final_start'] + offset
                new_strip.frame_final_duration = s['frame_final_duration']
                
                setPropertiesFromJsonDataset(s, new_strip, debug, ("frame", "animation"))

                new_strip.lock = True

        if debug: print('Audio synchronized') #debug
        
        return {'FINISHED'}