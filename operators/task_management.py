import bpy

from ..functions import task_functions as tsk_fct


# reload tasks
class BPM_OT_reload_tasks(bpy.types.Operator):
    """Reload all project tasks"""
    bl_idname = "bpm.reload_tasks"
    bl_label = "Reload Tasks"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
       
    def execute(self, context):
        # winman = context.window_manager
        # general_settings = context.window_manager.bpm_generalsettings
        # render_settings = winman.bpm_rendersettings
        # debug = winman.bpm_projectdatas.debug

        # if debug: print(g_var.saving_to_json_statement)

        tsk_fct.reload_task_list()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_reload_tasks)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_reload_tasks)