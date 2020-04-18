import bpy
import os
import shutil


class BPMCreateShot(bpy.types.Operator):
    """Create Shot from Timeline"""
    bl_idname = "bpm.create_shot"
    bl_label = "Create Shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name

    def execute(self, context):
        # import statements and functions
        from ..global_variables import (creating_shot_statement, 
                                    creating_shot_folder_statement, 
                                    python_temp, 
                                    shot_setup_file, 
                                    launching_command_statement, 
                                    creating_python_script_statement,
                                    python_script_created_statement,
                                    deleted_file_statement,
                                    scenes_linked_statement,
                                    no_available_timeline_space_message,
                                    no_available_timeline_space_statement,
                                    checking_available_timeline_space_statement,
                                    shot_folder,
                                    shot_file,
                                    saving_to_json_statement,
                                    saved_to_json_statement,
                                    audio_sync_file,
                                    starting_shot_audio_sync_statement,
                                    ressources_folder,
                                    startup_files_folder,
                                    shot_startup_file,
                                    copying_file_statement
                                )
        from ..functions.file_functions import getNextShot, createDirectory, replaceContentInPythonScript, suppressExistingFile, linkExternalScenes, absolutePath
        from ..functions.project_data_functions import getShotPattern, getScriptReplacementListShotCreation
        from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
        from ..functions.strip_functions import returnAvailablePositionStripChannel, deselectAllStrips
        from ..functions.json_functions import createJsonDatasetFromProperties, create_json_file
        from ..functions.audio_sync_functions import syncAudioEdit


        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        scn = context.scene
        
        if general_settings.debug: print(creating_shot_statement) #debug
        
        project_datas = winman.bpm_projectdatas
        project_folder = general_settings.project_folder
        shot_folder_path = os.path.join(project_folder, shot_folder)
        next_shot_folder, next_shot_file, next_shot_number = getNextShot(winman, project_datas, getShotPattern(project_datas), 1, shot_folder_path)

        # check timeline available space
        if general_settings.debug: print(checking_available_timeline_space_statement) #debug
        name = project_datas.shot_prefix + next_shot_number
        start = scn.frame_current
        duration = project_datas.default_shot_length
        sequencer = scn.sequence_editor
        channel = returnAvailablePositionStripChannel(start, duration, sequencer)

        # if no place to put the clip
        if channel == 0:
            # return no place to put the strip
            self.report({'INFO'}, no_available_timeline_space_message)
            if general_settings.debug: print(no_available_timeline_space_statement) #debug
            return {'FINISHED'}

        # create shot dir
        createDirectory(next_shot_folder)
        if general_settings.debug: print(creating_shot_folder_statement + next_shot_folder) #debug

        # copy shot file
        ressources_folderpath = os.path.join(project_folder, ressources_folder)
        startup_folderpath = os.path.join(ressources_folderpath, startup_files_folder)
        shot_startup_filepath = os.path.join(startup_folderpath, shot_startup_file)
        shutil.copy(shot_startup_filepath, next_shot_file)

        if general_settings.debug: print(copying_file_statement + shot_startup_filepath) #debug

        # create the json file
        if general_settings.debug: print(saving_to_json_statement) #debug

        shot_json = os.path.join(next_shot_folder, shot_file)
        # format the json dataset
        json_dataset = createJsonDatasetFromProperties(winman.bpm_shotsettings)
        json_dataset['shot_folder'] = next_shot_folder
        # create json file
        create_json_file(json_dataset, shot_json)

        if general_settings.debug: print(saved_to_json_statement) #debug


        # modify and copy python script
        replacement_list = getScriptReplacementListShotCreation(project_datas, next_shot_folder, next_shot_file, next_shot_number)
        
        temp_python_script = os.path.join(next_shot_folder, python_temp)
        if general_settings.debug: print(creating_python_script_statement + temp_python_script) #debug

        replaceContentInPythonScript(shot_setup_file, temp_python_script, replacement_list)
        if general_settings.debug: print(python_script_created_statement) #debug

        # launch the blend command
        command = buildBlenderCommandBackgroundPython(temp_python_script, next_shot_file, "")
        if general_settings.debug: print(launching_command_statement + command) #debug

        launchCommand(command)

        # delete the python temp
        suppressExistingFile(temp_python_script)
        if general_settings.debug: print(deleted_file_statement + temp_python_script) #debug

        # link shot
        linkExternalScenes(next_shot_file)
        if general_settings.debug: print(scenes_linked_statement + next_shot_file) #debug

        # add it to timeline
        linked_strip = sequencer.sequences.new_scene(
            name=name, 
            scene=bpy.data.scenes[name], 
            channel=channel, 
            frame_start=start
            )
        linked_strip.bpm_shotsettings.is_shot = True
        linked_strip.bpm_shotsettings.shot_folder = next_shot_folder
        sequencer.active_strip = linked_strip

        # select created strip
        deselectAllStrips(sequencer)
        linked_strip.select = True

        # update audio sync if existing
        audio_sync_filepath = os.path.join(project_folder, audio_sync_file)
        if os.path.isfile(audio_sync_filepath):
            syncAudioEdit(general_settings.debug, general_settings.project_folder, scn)

        return {'FINISHED'}