import bpy , gpu
import blf
from gpu_extras.batch import batch_for_shader
import bgl
from bgl import glEnable, glDisable, GL_BLEND


from .functions.strip_functions import getMarkerFrameFromShotStrip


def draw_callback_px():
    scn = bpy.context.scene
    sequencer = scn.sequence_editor
    region = bpy.context.region
    frame = scn.frame_current

    if not scn.bpm_displaymarkers : return()
    for strip in sequencer.sequences_all:
        if strip.bpm_isshot and strip.scene:
            for m in getMarkerFrameFromShotStrip(strip):
                x, y = region.view2d.view_to_region(m[1] - 0.5, strip.channel, clip=False)
                x2, y2 = region.view2d.view_to_region(m[1] + 0.5, strip.channel + 0.25, clip=False)
                x3, y2 = region.view2d.view_to_region(m[1], strip.channel + 0.25, clip=False)
                
                vertices = ( (x, y), (x2, y), (x3, y2))
                BPM_marker_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
                BMP_marker_batch = batch_for_shader(BPM_marker_shader, 'TRIS', {"pos": vertices})
                BPM_marker_shader.bind()
                BPM_marker_shader.uniform_float("color", (1, 1, 1, 1))
                BMP_marker_batch.draw(BPM_marker_shader)