import bpy


from ..global_variables import completed_render_statement, launching_command_statement
from ..functions.file_functions import absolutePath
from ..functions.command_line_functions import buildBlenderCommandBackgroundRender
from ..functions.threading_functions import launchSeparateThread
from ..functions.check_file_poll_function import check_file_poll_function


def renderShotEndFunction(shot_strip, debug):
    if debug: print(completed_render_statement + shot_strip.name) #debug
    shot_strip.bpm_shotsettings.is_rendering = False
    bpy.ops.sequencer.refresh_all()


class BPM_OT_render_shot_edit(bpy.types.Operator):
    """Render shot from edit"""
    bl_idname = "bpm.render_shot_edit"
    bl_label = "Render shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        is_bpm_project, bpm_filetype, bpm_active_strip = check_file_poll_function(context)
        if bpm_filetype == "EDIT" and bpm_active_strip:
            if not bpm_active_strip.lock:
                if not bpm_active_strip.bpm_shotsettings.is_working:
                    if not bpm_active_strip.bpm_shotsettings.is_rendering:
                        return True


    def execute(self, context):
        
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug

        active_strip = context.scene.sequence_editor.active_strip

        shot_settings = active_strip.bpm_shotsettings

        shot_filepath = absolutePath(shot_settings.shot_filepath)

        #set rendering
        shot_settings.is_rendering = True

        #build command
        command = buildBlenderCommandBackgroundRender(shot_filepath)

        #launch command
        if debug: print(launching_command_statement + command) #debug
        launchSeparateThread([command, debug, renderShotEndFunction, active_strip, debug])

        #store render pid

        #refresh sequencer
        bpy.ops.sequencer.refresh_all()
        
        return {'FINISHED'}