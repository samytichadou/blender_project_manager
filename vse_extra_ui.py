import bpy
import gpu
import blf
import bgl
from gpu_extras.batch import batch_for_shader
#from bgl import glEnable, glDisable, GL_BLEND


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

# get strip rectangle
def getStripRectangle(strip):
    x1 = strip.frame_final_start
    x2 = strip.frame_final_end
    y1 = strip.channel
    y2 = y1 + 1
    return [x1, y1, x2, y2]

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
    m_display = scn.bpm_displaymarkers
    mn_display = scn.bpm_displaymarkernames
    
    if not scn.bpm_extraui: return

    sequencer = scn.sequence_editor
    region = context.region

    # compute dpi_fac on every draw dynamically
    dpi_fac = getDpiFactorFromContext(context)

    # setup markers
    vertices_m = ()
    indices_m = ()
    color_m = (1, 1, 1, 1)

    id_m = 0
    text_size = int(12 * dpi_fac)
    blf.color(id_m, *color_m)
    blf.size(id_m, text_size, context.preferences.system.dpi)
    marker_texts = []

    # setup extras
    vertices_e = ()
    indices_e = ()
    color_e = (0.5, 0.5, 0.5, 0.5)

    # iterate through strips
    bgl.glEnable(bgl.GL_BLEND) # enable transparency

    n_m = 0
    n_e = 0

    ### COMPUTE TIMELINE ###
    for strip in sequencer.sequences_all:

        if strip.type in {'SCENE'}:

            # bpm shot
            if strip.bpm_isshot:

                x1, y1, x2, y2 = getStripRectangle(strip)
                v1 = region.view2d.view_to_region(x1, y1, clip=False)
                v2 = region.view2d.view_to_region(x2, y1, clip=False)
                v3 = region.view2d.view_to_region(x1, y2, clip=False)
                v4 = region.view2d.view_to_region(x2, y2, clip=False)
                vertices_e += (v1, v2, v3, v4)
                indices_e += ((n_e, n_e + 1, n_e + 2), (n_e + 2, n_e + 1, n_e + 3))
                n_e += 4

                if strip.scene:

                    # markers
                    if m_display != 'NONE' :
                        if (m_display == 'SELECTED' and strip.select) \
                        or (m_display == 'PERSTRIP' and strip.bpm_displaymarkers) \
                        or (m_display == 'ALL'):
                            for m in getMarkerFrameFromShotStrip(strip):
                                coord = getMarkerCoordinates(m[1], strip.channel, region, dpi_fac)
                                vertices_m += coord[0]
                                indices_m += ((n_m, n_m + 1, n_m + 2),)
                                n_m += 3   
                                # markers text
                                if (mn_display == "ALL") \
                                or (mn_display == "CURRENT" and scn.frame_current == m[1]):
                                    marker_texts.append((coord[1], m[0]))
    
    ### DRAW SHADERS ###

    #glBlendFunc(GL_DST_ALPHA, GL_ONE)
    
    #extras
    BPM_extra_shaders = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_extra_batch = batch_for_shader(BPM_extra_shaders, 'TRIS', {"pos": vertices_e}, indices=indices_e)
    BPM_extra_shaders.bind()
    BPM_extra_shaders.uniform_float("color", color_e)
    #BMP_extra_batch.draw(BPM_extra_shaders,)

    # markers
    BPM_marker_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_marker_batch = batch_for_shader(BPM_marker_shader, 'TRIS', {"pos": vertices_m}, indices=indices_m)
    BPM_marker_shader.bind()
    BPM_marker_shader.uniform_float("color", color_m)
    BMP_marker_batch.draw(BPM_marker_shader,)

    # draw marker texts
    for t in marker_texts:
        drawText(t[0], t[1])

    bgl.glDisable(bgl.GL_BLEND)

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