import bpy
import os


class BPMSynchronizeAudioEdit(bpy.types.Operator):
    """Synchronize audio edit file for shots"""
    bl_idname = "bpm.synchronize_audio_edit"
    bl_label = "Synchronize audio edit"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name

    def execute(self, context):
        # import statements and functions
        from ..functions.json_functions import createJsonDatasetFromProperties, initializeAssetJsonDatas, create_json_file
        from ..functions.file_functions import absolutePath
        from ..global_variables import (
                                    audio_sync_file,
                                    starting_audio_sync_file_statement,
                                    initialize_json_statement,
                                    adding_dataset_to_json,
                                    saving_to_json_statement,
                                    saved_to_json_statement,
                                    audio_sync_file_created_statement,
                                )

        general_settings = context.window_manager.bpm_generalsettings

        if general_settings.debug: print(starting_audio_sync_file_statement) #debug

        # get audio sync filepath
        filepath = absolutePath(os.path.join(general_settings.project_folder, audio_sync_file))
        sequencer = context.scene.sequence_editor

        # init json datas
        if general_settings.debug: print(initialize_json_statement + filepath) #debug

        datas = initializeAssetJsonDatas({'sounds', 'strips'})

        sound_list = []

        # iterate through strips
        for strip in sequencer.sequences_all:

            if strip.type == 'SOUND':

                if general_settings.debug: print(adding_dataset_to_json + strip.name) #debug
                
                # sound datas
                sound = strip.sound
                if sound not in sound_list:
                    sound_list.append(sound)
                    sound_datas = createJsonDatasetFromProperties(sound)
                    sound_datas['filepath'] = absolutePath(sound.filepath)
                    datas['sounds'].append(sound_datas)

                # strip datas
                strip_datas = createJsonDatasetFromProperties(strip)
                strip_datas['sound'] = sound.name    
                datas['strips'].append(strip_datas)
        
        if general_settings.debug: print(saving_to_json_statement) #debug

        create_json_file(datas, filepath)

        if general_settings.debug: print(saved_to_json_statement) #debug

        if general_settings.debug: print(audio_sync_file_created_statement) #debug
        
        return {'FINISHED'}