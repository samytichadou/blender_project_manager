import bpy


from ..global_variables import (
    launching_command_statement,
    start_update_shot_statement,
    checking_update_shot_statement,
    updating_shot_statement,
    update_shot_new_start_end_statement,
    updated_shot_statement,
    no_update_needed_statement,
    update_shot_file,
    shot_update_impossible_message,
    shot_update_impossible_statement,
)
from ..functions.strip_functions import (
    returnSelectedStrips, 
    getStripOffsets, 
    getStripNewTiming, 
    updateStripOnTimeline,
)
from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
from ..functions.project_data_functions import getArgumentForPythonScript
from ..functions.file_functions import absolutePath
from ..functions.utils_functions import redrawAreas

class BPMUpdateShotDuration(bpy.types.Operator):
    """Update selected shots duration"""
    bl_idname = "bpm.update_shot_duration"
    bl_label = "Update Shots duration"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_datas[0].edit_scene_keyword
        if context.window_manager.bpm_isproject and context.window_manager.bpm_isedit and keyword in context.scene.name:
            if context.scene.sequence_editor.active_strip:
                active = context.scene.sequence_editor.active_strip
                try:
                    if active.bpm_isshot and active.scene.library:
                        return True
                except AttributeError:
                    pass

    def execute(self, context):
        winman = context.window_manager

        if winman.bpm_debug: print(start_update_shot_statement) #debug

        selected_strips = returnSelectedStrips(context.scene.sequence_editor)
        for strip in selected_strips:
            try:
                if strip.bpm_isshot and strip.scene.library:
                    if winman.bpm_debug: print(checking_update_shot_statement + strip.name) #debug
                    
                    strip_scene = strip.scene
                    new_start, new_end = getStripNewTiming(strip)

                    if new_start != strip_scene.frame_start or new_end != strip_scene.frame_end:
                        if winman.bpm_debug: print(updating_shot_statement) #debug
                        if winman.bpm_debug: print(update_shot_new_start_end_statement + str(new_start) + "-" + str(new_end)) #debug
                        # check if frame become negative and avoid it
                        if new_start < 0:
                            self.report({'WARNING'}, shot_update_impossible_message)
                            print(shot_update_impossible_statement)
                        else:
                            filepath = absolutePath(strip.scene.library.filepath)

                            arguments = getArgumentForPythonScript([new_start, new_end])

                            # build command
                            command = buildBlenderCommandBackgroundPython(update_shot_file, filepath, arguments)

                            if winman.bpm_debug: print(launching_command_statement + command) #debug

                            # launch command
                            launchCommand(command)

                            # update scene fram_start frame_end
                            strip_scene.frame_start = new_start
                            strip_scene.frame_end   = new_end

                            # update the strip
                            updateStripOnTimeline(strip)

                            if winman.bpm_debug: print(updated_shot_statement) #debug

                    elif winman.bpm_debug: print(no_update_needed_statement) #debug

            except AttributeError:
                pass
            
        # reload library

        return {'FINISHED'}