import bpy


from ..global_variables import update_shot_file
from ..functions.strip_functions import returnSelectedStrips, getStripOffsets
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
            selected_strips = returnSelectedStrips(context.scene.sequence_editor)
            if selected_strips:
                for strip in selected_strips:
                    if strip.type == 'SCENE':
                        if strip.scene:
                            if strip.scene.library:
                                return True

    def execute(self, context):
        winman = context.window_manager

        selected_strips = returnSelectedStrips(context.scene.sequence_editor)
        for strip in selected_strips:
            if strip.type == 'SCENE':
                if strip.scene:
                    if strip.scene.library:
                        filepath = absolutePath(strip.scene.library.filepath)
                        # get offsets
                        offsets = getStripOffsets(strip)
                        arguments = getArgumentForPythonScript(offsets)

                        # build command
                        command = buildBlenderCommandBackgroundPython(update_shot_file, filepath, arguments)
                        print(command)
                        # launch command
                        launchCommand(command)

                        # correct offsets
                        strip.frame_offset_start = strip.frame_still_start + offsets[0]
                        strip.frame_offset_end = strip.frame_still_end + offsets[1]
                        # slide clip content
            
        # reload library
        # redraw sequencer
        redrawAreas(context, 'SEQUENCE_EDITOR')

        return {'FINISHED'}