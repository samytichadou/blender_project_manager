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
        from ..functions.strip_functions import deleteAllSequencerStrips, createSequencer
        from ..functions.audio_sync_functions import findShotOffsetFromSyncFile, loadSoundsFromSyncFile, createSoundStripsFromSyncFile
        from ..global_variables import (
                                    audio_sync_file,
                                    sync_file_not_found_statement,
                                    starting_shot_audio_sync_statement,
                                    creating_sequencer_statement,
                                    cleaning_timeline_statement,
                                    shot_not_used_message,
                                    shot_not_used_statement,
                                    loaded_sounds_statement,
                                    created_sound_strips_statement,
                                    shot_audio_synced_statement,
                                    reading_json_statement,
                                )

        general_settings = context.window_manager.bpm_generalsettings
        sequencer = context.scene.sequence_editor
        debug = general_settings.debug

        if debug: print() #debug

        # get audio sync filepath
        filepath = absolutePath(os.path.join(general_settings.project_folder, audio_sync_file))
        scn = context.scene
        sequencer = scn.sequence_editor

        if not os.path.isfile(filepath):
            if debug: print(sync_file_not_found_statement) #debug
            return {'FINISHED'}

        if debug: print(starting_shot_audio_sync_statement) #debug

        # create sequencer if none
        created_sequencer = createSequencer(scn)
        if not created_sequencer:
            # delete existing strips
            if debug: print(cleaning_timeline_statement) #debug
            deleteAllSequencerStrips(sequencer)
        else:
            if debug: print(creating_sequencer_statement)

        # get json datas
        if debug: print(reading_json_statement + filepath) #debug
        datas = read_json(filepath)

        # find shot offset
        current_shot_datas, offset = findShotOffsetFromSyncFile(datas, scn.name, scn.frame_start)

        # if shot strip not find in timeline
        if current_shot_datas is None:
            self.report({'INFO'}, shot_not_used_message)
            if debug: print(shot_not_used_statement) #debug
            return {'FINISHED'}

        # iterate through sounds and strips
        # load sounds
        sound_list = loadSoundsFromSyncFile(datas)
        if debug: print(loaded_sounds_statement + str(sound_list)) #debug

        # strips
        sound_strip_list = createSoundStripsFromSyncFile(datas, sequencer, current_shot_datas, offset)
        if debug: print(created_sound_strips_statement + str(sound_strip_list)) #debug

        if debug: print(shot_audio_synced_statement) #debug
        
        return {'FINISHED'}