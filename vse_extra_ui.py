import bpy
import gpu
import blf
from gpu_extras.batch import batch_for_shader
from bgl import glEnable, glDisable, GL_BLEND


from .functions.utils_functions import redrawAreas


# compute dpi_fac on every blender startup
# dpi_fac = bpy.context.preferences.system.pixel_size * bpy.context.preferences.system.dpi / 72


# get link scene marker fram
def getMarkerFrameFromShotStrip(strip):
    marker_list = []
    frame_start = strip.frame_start
    scn = strip.scene
    for marker in scn.timeline_markers:
        marker_frame = (marker.frame - scn.frame_start) + frame_start
        if marker_frame >= strip.frame_final_start and marker_frame < strip.frame_final_end:
            marker_list.append((marker.name, marker_frame))
    return marker_list

# get marker coordinates
def getMarkerCoordinates(frame, channel, region, dpi_fac):
    m_width = 6
    m_height = 9
    m_pos_y = 0.035
    t_pos_x = 10
    t_pos_y = 7
    x, y =region.view2d.view_to_region(frame, channel + m_pos_y, clip=False)
    v1 = (x - m_width * dpi_fac, y)
    v2 = (x + m_width * dpi_fac, y)
    v3 = (x, y + m_height * dpi_fac)
    v4 = (x + t_pos_x, y + t_pos_y)
    return ((v1, v2, v3), v4)

# draw text
def drawText(location, text):
    blf.position(0, location[0], location[1], 0)   
    blf.draw(0, text)

# get dpi factor from context
def getDpiFactorFromContext(context):
    pixel_size = context.preferences.system.pixel_size
    dpi = context.preferences.system.dpi
    dpi_fac = pixel_size * dpi / 72
    return dpi_fac
   
# ui draw callback
def drawBpmSequencerCallbackPx():
    context = bpy.context

    scn = context.scene
    display = scn.bpm_displaymarkers
    
    if display == 'NONE' : return

    sequencer = scn.sequence_editor
    region = context.region

    # compute dpi_fac on every draw dynamically
    dpi_fac = getDpiFactorFromContext(context)

    color = (1, 1, 1, 1)
    text_size = int(10 * dpi_fac)
    blf.color(*color, 1)
    blf.size(0, text_size, context.preferences.system.dpi)
    
    vertices = ()

    glEnable(GL_BLEND) # enable transparency

    for strip in sequencer.sequences_all:
        if strip.bpm_isshot and strip.scene:
            if (display == 'SELECTED' and strip.select) \
            or (display == 'PERSTRIP' and strip.bpm_displaymarkers) \
            or (display == 'ALL'):
                for m in getMarkerFrameFromShotStrip(strip):
                    coord = getMarkerCoordinates(m[1], strip.channel, region, dpi_fac)
                    vertices += coord[0]
                    drawText(coord[1], m[0])

    BPM_marker_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_marker_batch = batch_for_shader(BPM_marker_shader, 'TRIS', {"pos": vertices})
    BPM_marker_shader.bind()
    BPM_marker_shader.uniform_float("color", color)
    BMP_marker_batch.draw(BPM_marker_shader)

    glDisable(GL_BLEND)

#enable callback
cb_handle = []
def enableSequencerCallback():
    if cb_handle:
        return
    cb_handle.append(bpy.types.SpaceSequenceEditor.draw_handler_add(
        drawBpmSequencerCallbackPx, (), 'WINDOW', 'POST_PIXEL'))
    print('add') #debug TODO statement system

#disable callback
def disableSequencerCallback():
    if not cb_handle:
        return
    bpy.types.SpaceSequenceEditor.draw_handler_remove(cb_handle[0], 'WINDOW')
    cb_handle.clear()
    print('remove') #debug TODO statement system