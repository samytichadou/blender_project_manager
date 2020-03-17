import bpy

class OpenShot(bpy.types.Operator):
    """Open Shot from Timeline"""
    bl_idname = "bpm.open_shot"
    bl_label = "Open Shot"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        if context.scene.sequence_editor.active_strip:
            active = context.scene.sequence_editor.active_strip
            if active.type == 'SCENE':
                if active.scene.library:
                    return True

    def execute(self, context):
        pass
        return {'FINISHED'}