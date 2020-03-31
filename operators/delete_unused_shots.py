import bpy


class BPMDeleteUnusedShots(bpy.types.Operator):
    """Delete shots in the project not present on the timeline"""
    bl_idname = "bpm.delete_unused_shots"
    bl_label = "Delete unused shots"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_datas[0].edit_scene_keyword
        if context.window_manager.bpm_isproject and context.window_manager.bpm_filetype == 'EDIT':
            if keyword in context.scene.name:
                return True

    def execute(self, context):
        winman = context.window_manager
        
        return {'FINISHED'}