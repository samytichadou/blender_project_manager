import bpy


from ..global_variables import creating_shot_statement


class BPMCreateShot(bpy.types.Operator):
    """Create Shot from Timeline"""
    bl_idname = "bpm.create_shot"
    bl_label = "Create Shot"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject and context.window_manager.bpm_isedit

    def execute(self, context):
        winman = context.window_manager
        
        if winman.bpm_debug: print(creating_shot_statement) #debug

        return {'FINISHED'}