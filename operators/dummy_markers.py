import bpy, os


from ..functions.strip_functions import getMarkerFrameFromShotStrip

# display project settings
class BpmDummy(bpy.types.Operator):
    """Create new Blender Project Manager Project"""
    bl_idname = "bpm.dummy"
    bl_label = "marker dummy"
            
    def execute(self, context):
        sequencer = bpy.context.scene.sequence_editor

        for strip in sequencer.sequences_all:
            if strip.bpm_isshot and strip.scene:
                markers = getMarkerFrameFromShotStrip(strip)
                for m in markers:
                    print(m)

        return {'FINISHED'}