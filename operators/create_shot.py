import bpy, os


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
                            )
from ..functions.file_functions import getNextShot, createDirectory, replaceContentInPythonScript, suppressExistingFile, linkExternalScenes
from ..functions.project_data_functions import getShotPattern, getScriptReplacementListShotCreation
from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
from ..functions.strip_functions import returnAvailablePositionStripChannel


class BPMCreateShot(bpy.types.Operator):
    """Create Shot from Timeline"""
    bl_idname = "bpm.create_shot"
    bl_label = "Create Shot"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_datas[0].edit_scene_keyword
        return context.window_manager.bpm_isproject and context.window_manager.bpm_isedit and keyword in context.scene.name

    def execute(self, context):
        winman = context.window_manager
        scn = context.scene
        
        if winman.bpm_debug: print(creating_shot_statement) #debug
        
        project_datas = winman.bpm_datas[0]
        next_shot_folder, next_shot_file, next_shot_number = getNextShot(project_datas, getShotPattern(project_datas), 1)

        # check timeline available space
        if winman.bpm_debug: print(checking_available_timeline_space_statement) #debug
        name = project_datas.shot_prefix + next_shot_number
        start = scn.frame_current
        duration = project_datas.default_shot_length
        sequencer = scn.sequence_editor
        channel = returnAvailablePositionStripChannel(start, duration, sequencer)

        # if no place to put the clip
        if channel == 0:
            # return no place to put the strip
            self.report({'WARNING'}, no_available_timeline_space_message)
            print(no_available_timeline_space_statement)
            return {'FINISHED'}

        # create shot dir
        createDirectory(next_shot_folder)
        if winman.bpm_debug: print(creating_shot_folder_statement + next_shot_folder) #debug

        # modify and copy python script
        replacement_list = getScriptReplacementListShotCreation(project_datas, next_shot_folder, next_shot_file, next_shot_number)
        
        temp_python_script = os.path.join(next_shot_folder, python_temp)
        if winman.bpm_debug: print(launching_command_statement + temp_python_script) #debug

        replaceContentInPythonScript(shot_setup_file, temp_python_script, replacement_list)
        if winman.bpm_debug: print(python_script_created_statement) #debug

        # launch the blend command
        command = buildBlenderCommandBackgroundPython(temp_python_script, "", "")
        if winman.bpm_debug: print(launching_command_statement + command) #debug

        launchCommand(command)

        # delete the python temp
        suppressExistingFile(temp_python_script)
        if winman.bpm_debug: print(deleted_file_statement + temp_python_script) #debug

        # link shot
        linkExternalScenes(next_shot_file)
        if winman.bpm_debug: print(scenes_linked_statement + next_shot_file) #debug

        # add it to timeline
        linked_strip = sequencer.sequences.new_scene(name=name, scene=bpy.data.scenes[name], channel=channel, frame_start=start)
        linked_strip.bpm_isshot = True
        sequencer.active_strip = linked_strip

        return {'FINISHED'}