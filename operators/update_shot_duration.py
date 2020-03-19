import bpy


from ..functions.strip_functions import returnSelectedStrips

class BPMCreateShot(bpy.types.Operator):
    """Create Shot from Timeline"""
    bl_idname = "bpm.create_shot"
    bl_label = "Create Shot"
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

        selected_strips = returnSelectedStrips(context.scene.sequence_editor):
        for strip in selected:
            # get duration
            duration = strip.frame_final_duration
            # get argument

            # build command
            # launch command
            pass

        return {'FINISHED'}