import bpy
import gpu
import blf
import bgl
from gpu_extras.batch import batch_for_shader


from .functions.strip_functions import returnShotStrips
from .global_variables import (
                            font_file, 
                            add_extra_ui_statement, 
                            remove_extra_ui_statement, 
                            load_font_statement, 
                            unload_font_statement,
                        )
from .functions.project_data_functions import getShotTaskDeadline, getShotTaskComplete


# compute dpi_fac on every blender startup
# dpi_fac = bpy.context.preferences.system.pixel_size * bpy.context.preferences.system.dpi / 72

# font id for makers
markers_font = {
    "font_id": 0,
}


# initialize fonts
def initializeExternalFontId(font_id, file_font):
    winman = bpy.context.window_manager
    if winman.bpm_generalsettings.debug: print(load_font_statement + file_font) #debug
    font_id["font_id"] = blf.load(file_font)


# unload external font
def unloadExternalFontId(font_id, file_font):
    winman = bpy.context.window_manager
    if winman.bpm_generalsettings.debug: print(unload_font_statement + file_font) #debug
    font_id["font_id"] = 0
    blf.unload(file_font)


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
    t_pos_x = 3
    t_pos_y = 7
    x, y =region.view2d.view_to_region(frame, channel + m_pos_y, clip=False)
    v1 = (x - m_width * dpi_fac, y)
    v2 = (x + m_width * dpi_fac, y)
    v3 = (x, y + m_height * dpi_fac)
    v4 = (x + t_pos_x, y + t_pos_y)
    return ((v1, v2, v3), v4)


# get strip rectangle
def getStripRectangle(strip):
    x_offset = 0.05
    y_offset = 0.05
    x1 = strip.frame_final_start
    x2 = strip.frame_final_end + x_offset
    y1 = strip.channel + y_offset
    y2 = strip.channel + 1 - y_offset
    return [x1, y1, x2, y2]


# get text bounding box
def getBoundingBoxCoordinates(pos, text, text_size, dpi_fac):
    step = text_size / 2 + 1
    width = len(text) * step * dpi_fac
    height = 9
    
    offs_x = 3
    offs_y = 3
    
    v1 = (pos[0] - offs_x, pos[1] - offs_y)
    v2 = (pos[0] + width + offs_x, pos[1] - offs_y)
    v3 = (pos[0] - offs_x, pos[1] + height + offs_y)
    v4 = (pos[0] + width + offs_x, pos[1] + height + offs_y)

    return (v1, v2, v3, v4)


# get warning zone of a strip
warning_square_size = 8

def getWarningZoneStrip(x, y):
    v1 = (x-warning_square_size, y-warning_square_size)
    v2 = (x, y-warning_square_size)
    v3 = (x-warning_square_size, y)
    v4 = (x, y)
    return (v1,v2,v3,v4)

def getSecondWarningZoneStrip(x, y):
    v1, v2, v3, v4 = getWarningZoneStrip(x - warning_square_size, y)
    return (v1,v2,v3,v4)

# get info zone of a strip
def getInfoZoneStrip(x, y):
    v1 = (x - warning_square_size, y)
    v2 = (x, y)
    v3 = (x - warning_square_size, y + warning_square_size)
    v4 = (x, y + warning_square_size)
    return (v1,v2,v3,v4)


# check if a strip has to be updated
def getStripNeedUpdate(strip):
    if strip.frame_start != strip.frame_final_start:
        return True
    elif (strip.frame_start + strip.frame_duration) != strip.frame_final_end:
        return True
    else:
        return False


# draw text
def drawText(location, text, f_id):
    blf.position(f_id, location[0], location[1], 0)   
    blf.draw(f_id, text)


# get dpi factor from context
def getDpiFactorFromContext(context):
    pixel_size = context.preferences.system.pixel_size
    dpi = context.preferences.system.dpi
    dpi_fac = pixel_size * dpi / 72
    return dpi_fac


# draw shader
def drawShader(vertices, indices, color):
    BPM_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    BMP_batch = batch_for_shader(BPM_shader, 'TRIS', {"pos": vertices}, indices=indices)
    BPM_shader.bind()
    BPM_shader.uniform_float("color", color)
    BMP_batch.draw(BPM_shader,)

   
# ui draw callback
def drawBpmSequencerCallbackPx():
    context = bpy.context

    scn = context.scene
    scene_settings = scn.bpm_scenesettings
    date = context.window_manager.bpm_generalsettings.today_date
    m_display = scene_settings.display_markers
    mn_display = scene_settings.display_marker_names
    
    if not scene_settings.extra_ui: return

    sequencer = scn.sequence_editor
    region = context.region

    # compute dpi_fac on every draw dynamically
    dpi = context.preferences.system.dpi
    dpi_fac = getDpiFactorFromContext(context)

    # setup markers
    vertices_m = ()
    indices_m = ()
    #color_m = (1, 1, 1, 1)
    color_m = scene_settings.color_markers
    n_m = 0

    # setup markers text
    #text_size = int(12 * dpi_fac)
    id_m = markers_font["font_id"]
    text_size = 12
    blf.color(id_m, *color_m)
    blf.size(id_m, text_size, dpi)
    marker_texts = []

    # setup markers bounding box
    vertices_m_bb = ()
    indices_m_bb = ()
    #color_m_bb = (0, 0, 0, 0.5)
    color_m_bb = scene_settings.color_marker_boxes
    n_m_bb = 0

    # setup extras

    # bpm todo
    vertices_e_td = ()
    indices_e_td = ()
    color_e_td = scene_settings.color_shot_todo
    n_e_td = 0

    # bpm shots
    vertices_e_s = ()
    indices_e_s = ()
    color_e_s = scene_settings.color_shot_strip
    n_e_s = 0

    # bpm shots state
    #state_alpha = 1.0

    #storyboard
    vertices_e_st_st = ()
    indices_e_st_st = ()
    color_e_st_st = scene_settings.color_state_storyboard
    n_e_st_st = 0

    #layout
    vertices_e_st_la = ()
    indices_e_st_la = ()
    color_e_st_la = scene_settings.color_state_layout
    n_e_st_la = 0

    #animation
    vertices_e_st_an = ()
    indices_e_st_an = ()
    color_e_st_an = scene_settings.color_state_animation
    n_e_st_an = 0

    #lighting
    vertices_e_st_li = ()
    indices_e_st_li = ()
    color_e_st_li = scene_settings.color_state_lighting
    n_e_st_li = 0

    #rendering
    vertices_e_st_re = ()
    indices_e_st_re = ()
    color_e_st_re = scene_settings.color_state_rendering
    n_e_st_re = 0

    #compositing
    vertices_e_st_co = ()
    indices_e_st_co = ()
    color_e_st_co = scene_settings.color_state_compositing
    n_e_st_co = 0

    #finished
    vertices_e_st_fi = ()
    indices_e_st_fi = ()
    color_e_st_fi = scene_settings.color_state_finished
    n_e_st_fi = 0

    #done
    vertices_e_st_do = ()
    indices_e_st_do = ()
    n_e_st_do = 0

    # info shot audio sync
    vertices_e_au = ()
    indices_e_au = ()
    color_e_au = scene_settings.color_audio_sync
    n_e_au = 0

    # warning update bpm shots
    vertices_e_w = ()
    indices_e_w = ()
    color_e_w = scene_settings.color_update_warning
    n_e_w = 0

    # warning version bpm shots
    vertices_e_v_w = ()
    indices_e_v_w = ()
    color_e_v_w = scene_settings.color_version_warning
    n_e_v_w = 0

    # iterate through strips
    bgl.glEnable(bgl.GL_BLEND) # enable transparency

    ### COMPUTE TIMELINE ###
    for strip in returnShotStrips(sequencer):

        display_need_update = False
        display_todo = False                  

        x1, y1, x2, y2 = getStripRectangle(strip)

        v1 = region.view2d.view_to_region(x1, y1, clip=False)
        v2 = region.view2d.view_to_region(x2, y1, clip=False)
        v3 = region.view2d.view_to_region(x1, y2, clip=False)
        v4 = region.view2d.view_to_region(x2, y2, clip=False)

        # bpm todo shot
        if scene_settings.display_shot_todo:

            shot_deadline = getShotTaskDeadline(strip.bpm_shotsettings)[1]

            if date == shot_deadline:
                display_todo = True

                y1s = y1 + 0.6

                v1s = region.view2d.view_to_region(x1, y1s, clip=False)
                v2s = region.view2d.view_to_region(x2, y1s, clip=False)

                vertices_e_td += (v1s, v2s, v3, v4)
                indices_e_td += ((n_e_td, n_e_td + 1, n_e_td + 2), (n_e_td + 2, n_e_td + 1, n_e_td + 3))
                n_e_td += 4


        # bpm shot
        if scene_settings.display_shot_strip:
            
            if not display_todo:
                
                y1s = y1 + 0.6

                v1s = region.view2d.view_to_region(x1, y1s, clip=False)
                v2s = region.view2d.view_to_region(x2, y1s, clip=False)

                vertices_e_s += (v1s, v2s, v3, v4)
                indices_e_s += ((n_e_s, n_e_s + 1, n_e_s + 2), (n_e_s + 2, n_e_s + 1, n_e_s + 3))
                n_e_s += 4

        # bpm shot state
        if scene_settings.display_shot_state:

            display_state_done = False

            if getShotTaskComplete(strip.bpm_shotsettings)[1] and strip.bpm_shotsettings.shot_state != 'FINISHED':
                display_state_done = True
                y1st = y1 + 0.55

            else:
                y1st = y1 + 0.5
                
            y2st = y2 - 0.3

            v1st = region.view2d.view_to_region(x1, y1st, clip=False)
            v2st = region.view2d.view_to_region(x2, y1st, clip=False)
            v3st = region.view2d.view_to_region(x1, y2st, clip=False)
            v4st = region.view2d.view_to_region(x2, y2st, clip=False)

            if strip.bpm_shotsettings.shot_state == 'STORYBOARD':
                vertices_e_st_st += (v1st, v2st, v3st, v4st)
                indices_e_st_st += ((n_e_st_st, n_e_st_st + 1, n_e_st_st + 2), (n_e_st_st + 2, n_e_st_st + 1, n_e_st_st + 3))
                n_e_st_st += 4
            elif strip.bpm_shotsettings.shot_state == 'LAYOUT':
                vertices_e_st_la += (v1st, v2st, v3st, v4st)
                indices_e_st_la += ((n_e_st_la, n_e_st_la + 1, n_e_st_la + 2), (n_e_st_la + 2, n_e_st_la + 1, n_e_st_la + 3))
                n_e_st_la += 4
            elif strip.bpm_shotsettings.shot_state == 'ANIMATION':
                vertices_e_st_an += (v1st, v2st, v3st, v4st)
                indices_e_st_an += ((n_e_st_an, n_e_st_an + 1, n_e_st_an + 2), (n_e_st_an + 2, n_e_st_an + 1, n_e_st_an + 3))
                n_e_st_an += 4
            elif strip.bpm_shotsettings.shot_state == 'LIGHTING':
                vertices_e_st_li += (v1st, v2st, v3st, v4st)
                indices_e_st_li += ((n_e_st_li, n_e_st_li + 1, n_e_st_li + 2), (n_e_st_li + 2, n_e_st_li + 1, n_e_st_li + 3))
                n_e_st_li += 4
            elif strip.bpm_shotsettings.shot_state == 'RENDERING':
                vertices_e_st_re += (v1st, v2st, v3st, v4st)
                indices_e_st_re += ((n_e_st_re, n_e_st_re + 1, n_e_st_re + 2), (n_e_st_re + 2, n_e_st_re + 1, n_e_st_re + 3))
                n_e_st_re += 4
            elif strip.bpm_shotsettings.shot_state == 'COMPOSITING':
                vertices_e_st_co += (v1st, v2st, v3st, v4st)
                indices_e_st_co += ((n_e_st_co, n_e_st_co + 1, n_e_st_co + 2), (n_e_st_co + 2, n_e_st_co + 1, n_e_st_co + 3))
                n_e_st_co += 4
            elif strip.bpm_shotsettings.shot_state == 'FINISHED':
                vertices_e_st_fi += (v1st, v2st, v3st, v4st)
                indices_e_st_fi += ((n_e_st_fi, n_e_st_fi + 1, n_e_st_fi + 2), (n_e_st_fi + 2, n_e_st_fi + 1, n_e_st_fi + 3))
                n_e_st_fi += 4

            # bpm state done
            if display_state_done:
                
                y1do = y1st - 0.05

                v1do = region.view2d.view_to_region(x1, y1do, clip=False)
                v2do = region.view2d.view_to_region(x2, y1do, clip=False)
                v3do = region.view2d.view_to_region(x1, y1st, clip=False)
                v4do = region.view2d.view_to_region(x2, y1st, clip=False)

                vertices_e_st_do += (v1do, v2do, v3do, v4do)
                indices_e_st_do += ((n_e_st_do, n_e_st_do + 1, n_e_st_do + 2), (n_e_st_do + 2, n_e_st_do + 1, n_e_st_do + 3))
                n_e_st_do += 4


        # bpm shot audio sync
        if scene_settings.display_audio_sync:
            if strip.bpm_shotsettings.auto_audio_sync:
                vertices_e_au += getInfoZoneStrip(*v2)
                indices_e_au += ((n_e_au, n_e_au + 1, n_e_au + 2), (n_e_au + 2, n_e_au + 1, n_e_au + 3))
                n_e_au += 4
                
        # bpm need to update
        if scene_settings.display_shot_update_warning:
            if getStripNeedUpdate(strip):
                display_need_update = True
                vertices_e_w += getWarningZoneStrip(*v4)
                indices_e_w += ((n_e_w, n_e_w + 1, n_e_w + 2), (n_e_w + 2, n_e_w + 1, n_e_w + 3))
                n_e_w += 4

        # bpm not last version
        if scene_settings.display_shot_version_warning:
            if strip.bpm_shotsettings.not_last_version:
                if display_need_update:
                    vertices_e_v_w += getSecondWarningZoneStrip(*v4)
                    indices_e_v_w += ((n_e_v_w, n_e_v_w + 1, n_e_v_w + 2), (n_e_v_w + 2, n_e_v_w + 1, n_e_v_w + 3))
                    n_e_v_w += 4
                else:
                    vertices_e_v_w += getWarningZoneStrip(*v4)
                    indices_e_v_w += ((n_e_v_w, n_e_v_w + 1, n_e_v_w + 2), (n_e_v_w + 2, n_e_v_w + 1, n_e_v_w + 3))
                    n_e_v_w += 4

        if strip.scene:

            # markers
            if m_display != 'NONE' :
                if (m_display == 'SELECTED' and strip.select) \
                or (m_display == 'PERSTRIP' and strip.bpm_shotsettings.display_markers) \
                or (m_display == 'ALL'):
                    for m in getMarkerFrameFromShotStrip(strip):
                        coord = getMarkerCoordinates(m[1], strip.channel, region, dpi_fac)
                        vertices_m += coord[0]
                        indices_m += ((n_m, n_m + 1, n_m + 2),)
                        n_m += 3   

                        # markers text
                        if (mn_display == "ALL") \
                        or (mn_display == "CURRENT" and scn.frame_current == m[1]):
                            text = m[0]
                            limit = scene_settings.display_marker_text_limit
                            if len(text) > limit and limit != 0:
                                if limit > 4:
                                    text = text[0:limit - 3] + "..."
                                else:
                                    text = text[0:limit]
                            marker_texts.append((coord[1], text))

                            # marker box
                            if scene_settings.display_marker_boxes:
                                vertices_m_bb += getBoundingBoxCoordinates(coord[1], text, text_size, dpi_fac)
                                indices_m_bb += ((n_m_bb, n_m_bb + 1, n_m_bb + 2), (n_m_bb + 2, n_m_bb + 1, n_m_bb + 3))
                                n_m_bb += 4
    
    ### DRAW SHADERS ###

    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE)

    #shot todo
    if scene_settings.display_shot_todo:
        drawShader(vertices_e_td, indices_e_td, color_e_td)
    
    #shot strips
    if scene_settings.display_shot_strip:
        drawShader(vertices_e_s, indices_e_s, color_e_s)

    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)

    #shot state
    if scene_settings.display_shot_state:
        drawShader(vertices_e_st_st, indices_e_st_st, color_e_st_st)
        drawShader(vertices_e_st_la, indices_e_st_la, color_e_st_la)
        drawShader(vertices_e_st_an, indices_e_st_an, color_e_st_an)
        drawShader(vertices_e_st_li, indices_e_st_li, color_e_st_li)
        drawShader(vertices_e_st_re, indices_e_st_re, color_e_st_re)
        drawShader(vertices_e_st_co, indices_e_st_co, color_e_st_co)
        drawShader(vertices_e_st_fi, indices_e_st_fi, color_e_st_fi)

        drawShader(vertices_e_st_do, indices_e_st_do, color_e_st_fi)

    # audio sync info
    if scene_settings.display_audio_sync:
        drawShader(vertices_e_au, indices_e_au, color_e_au)

    # update warning
    if scene_settings.display_shot_update_warning:
        drawShader(vertices_e_w, indices_e_w, color_e_w)

    # version warning
    if scene_settings.display_shot_version_warning:
        drawShader(vertices_e_v_w, indices_e_v_w, color_e_v_w)

    # markers
    if m_display != 'NONE' :

        # markers bounding boxes
        if mn_display != "NONE" and scene_settings.display_marker_boxes:
            drawShader(vertices_m_bb, indices_m_bb, color_m_bb)

        # markers
        drawShader(vertices_m, indices_m, color_m)


        # draw marker texts
        if mn_display != "NONE":
            for t in marker_texts:
                drawText(t[0], t[1], id_m)

            bgl.glDisable(bgl.GL_BLEND)

#enable callback
cb_handle = []
def enableSequencerCallback():
    if cb_handle:
        return
    
    initializeExternalFontId(markers_font, font_file)

    cb_handle.append(bpy.types.SpaceSequenceEditor.draw_handler_add(
        drawBpmSequencerCallbackPx, (), 'WINDOW', 'POST_PIXEL'))

    winman = bpy.context.window_manager
    if winman.bpm_generalsettings.debug: print(add_extra_ui_statement)#debug

#disable callback
def disableSequencerCallback():
    if not cb_handle:
        return

    unloadExternalFontId(markers_font, font_file)

    bpy.types.SpaceSequenceEditor.draw_handler_remove(cb_handle[0], 'WINDOW')
    cb_handle.clear()

    winman = bpy.context.window_manager
    if winman.bpm_generalsettings.debug: print(remove_extra_ui_statement) #debug