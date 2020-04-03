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
        from ..global_variables import (
                                    audio_sync_file,
                                )

        general_settings = context.window_manager.bpm_generalsettings
        sequencer = context.scene.sequence_editor

        if general_settings.debug: print() #debug

        # get audio sync filepath
        filepath = absolutePath(os.path.join(general_settings.project_folder, audio_sync_file))
        sequencer = context.scene.sequence_editor

        # create sequencer if none


        # delete existing strips
        if general_settings.debug: print() #debug


        # iterate through the strips
        if general_settings.debug: print() #debug
        datas = read_json(filepath)

        # sounds
        for s in datas['sounds']:
            try:
                bpy.data.sounds[s['name']]
            except KeyError:
                if general_settings.debug: print() #debug

                sound = bpy.data.sounds.load(s['filepath'])
                setPropertiesFromJsonDataset(s, sound)

        # get random filepath
        fp = datas['sounds'][0]['filepath']

        # strips
        for s in datas['strips']:

            if general_settings.debug: print() #debug

            new_strip = sequencer.sequences.new_sound(s['name'], fp, s['channel'], s['frame_start'])
            new_strip.sound = bpy.data.sounds[s['sound']]

            new_strip.frame_offset_start = s['frame_offset_start']
            new_strip.frame_offset_end = s['frame_offset_end']
            new_strip.frame_final_start = s['frame_final_start']
            new_strip.frame_final_duration = s['frame_final_duration']
            
            setPropertiesFromJsonDataset(s, new_strip, ("frame", "animation"))

        if general_settings.debug: print() #debug
        
        return {'FINISHED'}