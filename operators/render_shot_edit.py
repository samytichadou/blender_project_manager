import bpy
import os

from .. import global_variables as g_var
from ..functions import file_functions as fl_fct
from ..functions.command_line_functions import buildBlenderCommandBackgroundRender
from ..functions.threading_functions import launchSeparateThread
from ..functions.check_file_poll_function import check_file_poll_function
from ..functions import task_functions as tsk_fct
from ..functions.json_functions import create_json_file
from ..functions import date_functions as dt_fct


def renderShotEndFunction(shot_strip, debug):
    if debug: print(g_var.completed_render_statement + shot_strip.name) #debug
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

        shot_filepath = fl_fct.absolutePath(shot_settings.shot_filepath)

        #set rendering
        shot_settings.is_rendering = True

        #build command
        command = buildBlenderCommandBackgroundRender(shot_filepath)

        #create task file
        shot_name = fl_fct.get_filename_from_filepath(shot_filepath)[0]
        id = dt_fct.getDateTimeID()
        time = dt_fct.getDateTimeString()
        task_folder = tsk_fct.return_task_folder(winman)
        task_filepath = os.path.join(task_folder, shot_name + "_" + id + g_var.taskfile_extension)
        completion_total = shot_settings.shot_frame_end - shot_settings.shot_frame_start + 1

        task_datas = tsk_fct.create_task_dataset(shot_name, time, shot_filepath, "render", id, completion_total)
        create_json_file(task_datas, task_filepath)

        #launch command
        if debug: print(g_var.launching_command_statement + command) #debug
        launchSeparateThread([command, debug, task_filepath, renderShotEndFunction, active_strip, debug])

        #refresh sequencer
        bpy.ops.sequencer.refresh_all()
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_render_shot_edit)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_render_shot_edit)