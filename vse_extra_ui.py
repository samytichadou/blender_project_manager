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
from .functions.date_functions import formatDateFromYrMoDa, returnPriorDate
from .functions.reload_comments_function import get_shot_comment_frame


# compute dpi_fac on every blender startup
# dpi_fac = bpy.context.preferences.system.pixel_size * bpy.context.preferences.system.dpi / 72

# ui parameters 
warning_square_size = 8
strip_line_length = 0.075

# font id for makers
comments_font = {
    "font_id": 0,
}

# text size
text_size = 12

# initialize fonts
def initializeExternalFontId(font_id, file_font):
    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(load_font_statement + file_font) #debug
    font_id["font_id"] = blf.load(file_font)


# unload external font
def unloadExternalFontId(font_id, file_font):
    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(unload_font_statement + file_font) #debug
    font_id["font_id"] = 0
    blf.unload(file_font)


# get area width
def get_area_height(area):
    return area.height


# get comments frame
def getCommentFrameFromShotStrip(strip):
    comment_list = []
    shot_settings = strip.bpm_shotsettings
    for comment in shot_settings.comments:
        if comment.frame_comment:
            comment_frame = get_shot_comment_frame(comment.frame, strip)
            if comment_frame >= strip.frame_final_start and comment_frame < strip.frame_final_end:
                comment_list.append((comment.comment, comment_frame))
    return comment_list


# get timeline comments frame
def get_timeline_comments_list(context, region, dpi_fac):
    project_settings = context.window_manager.bpm_projectdatas
    comment_list = []

    for c in project_settings.comments:
        if c.frame_comment:
            comment_list.append((c.comment, get_timeline_comments_coordinates(c.frame, region, dpi_fac, get_area_height(context.area)), c.frame))

    return comment_list


# get timeline comments coordinates
def get_timeline_comments_coordinates(frame, region, dpi_fac, area_height):
    m_width = 6
    m_height = 9
    t_pos_x = 3
    t_pos_y = 7
    x, y =region.view2d.view_to_region(frame, 0, clip=False)
    y = 20 * dpi_fac
    v1 = (x - m_width * dpi_fac, y)
    v2 = (x + m_width * dpi_fac, y)
    v3 = (x, y + m_height * dpi_fac)
    v4 = (x + t_pos_x, y + t_pos_y)
    return ((v1, v2, v3), v4)


# get comments coordinates
def getCommentsCoordinates(frame, channel, region, dpi_fac):
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

# get todo zone of a strip
def getTodoZoneStrip(x, y):
    v1 = (x, y - warning_square_size)
    v2 = (x + warning_square_size, y- warning_square_size)
    v3 = (x, y)
    v4 = (x + warning_square_size, y)
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

   
# ui draw strip callback
def draw_bpm_sequencer_strip_callback_px():
    context = bpy.context

    scn = context.scene
    scene_settings = scn.bpm_scenesettings

    date = context.window_manager.bpm_generalsettings.today_date
    preview_date = formatDateFromYrMoDa(scene_settings.shot_deadline_preview_yr, scene_settings.shot_deadline_preview_mn, scene_settings.shot_deadline_preview_da)

    c_display = scene_settings.display_shot_comments
    c_n_display = scene_settings.display_shot_comments_names
    
    if not scene_settings.extra_ui: return

    sequencer = scn.sequence_editor
    region = context.region

    # compute dpi_fac on every draw dynamically
    dpi = context.preferences.system.dpi
    dpi_fac = getDpiFactorFromContext(context)

    # setup comments
    vertices_m = ()
    indices_m = ()
    color_m = scene_settings.color_shot_comments
    n_m = 0

    # setup comments text
    id_m = comments_font["font_id"]
    blf.color(id_m, *color_m)
    blf.size(id_m, text_size, dpi)
    comments_texts = []

    # setup comments bounding box
    vertices_m_bb = ()
    indices_m_bb = ()
    color_m_bb = scene_settings.color_shot_comments_boxes
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

    #working strips
    vertices_e_ws = ()
    indices_e_ws = ()
    n_e_ws = 0
    color_e_ws = scene_settings.color_strip_working

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

        display_todo = False

        display_need_update = False             

        x1, y1, x2, y2 = getStripRectangle(strip)

        v1 = region.view2d.view_to_region(x1, y1, clip=False)
        v2 = region.view2d.view_to_region(x2, y1, clip=False)
        v3 = region.view2d.view_to_region(x1, y2, clip=False)
        v4 = region.view2d.view_to_region(x2, y2, clip=False)

        # bpm todo shot
        if scene_settings.display_shot_todo != "NONE":

            shot_deadline = getShotTaskDeadline(strip.bpm_shotsettings)[1]

            if scene_settings.display_shot_todo ==  'TODAY':
                if shot_deadline == date:
                    display_todo = True

            elif scene_settings.display_shot_todo == 'UNTIL_TODAY':
                if shot_deadline == date or returnPriorDate(shot_deadline, date):
                    display_todo = True

            elif scene_settings.display_shot_todo == 'SPECIFIC_DATE':
                if shot_deadline == preview_date:
                    display_todo = True

            if display_todo:

                v1td, v2td, v3td, v4td = getTodoZoneStrip(*v3)

                vertices_e_td += (v1td, v2td, v3td, v4td)
                indices_e_td += ((n_e_td, n_e_td + 1, n_e_td + 2), (n_e_td + 2, n_e_td + 1, n_e_td + 3))
                n_e_td += 4

        # bpm shot
        if scene_settings.display_shot_strip:
                
            y2s = y1 + strip_line_length

            v3s = region.view2d.view_to_region(x1, y2s, clip=False)
            v4s = region.view2d.view_to_region(x2, y2s, clip=False)

            vertices_e_s += (v1, v2, v3s, v4s)
            indices_e_s += ((n_e_s, n_e_s + 1, n_e_s + 2), (n_e_s + 2, n_e_s + 1, n_e_s + 3))
            n_e_s += 4

        # bpm shot state
        if scene_settings.display_shot_state:

            y1st = y1 + 0.5
            y2st = y1st + strip_line_length

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
            if getShotTaskComplete(strip.bpm_shotsettings)[1] and strip.bpm_shotsettings.shot_state != 'FINISHED':
                
                y1do = y1st - strip_line_length

                v1do = region.view2d.view_to_region(x1, y1do, clip=False)
                v2do = region.view2d.view_to_region(x2, y1do, clip=False)
                v3do = region.view2d.view_to_region(x1, y1st, clip=False)
                v4do = region.view2d.view_to_region(x2, y1st, clip=False)

                vertices_e_st_do += (v1do, v2do, v3do, v4do)
                indices_e_st_do += ((n_e_st_do, n_e_st_do + 1, n_e_st_do + 2), (n_e_st_do + 2, n_e_st_do + 1, n_e_st_do + 3))
                n_e_st_do += 4


        # bpm is working
        if scene_settings.display_working_warning:

            if strip.bpm_shotsettings.is_working:
               
                y1ws = y1 + strip_line_length
                y2ws = y1ws + strip_line_length

                v1ws = region.view2d.view_to_region(x1, y1ws, clip=False)
                v2ws = region.view2d.view_to_region(x2, y1ws, clip=False)
                v3ws = region.view2d.view_to_region(x1, y2ws, clip=False)
                v4ws = region.view2d.view_to_region(x2, y2ws, clip=False)

                vertices_e_ws += (v1ws, v2ws, v3ws, v4ws)
                indices_e_ws += ((n_e_ws, n_e_ws + 1, n_e_ws + 2), (n_e_ws + 2, n_e_ws + 1, n_e_ws + 3))
                n_e_ws += 4

        # bpm shot audio sync
        if scene_settings.display_audio_sync_warning:
            if not strip.bpm_shotsettings.auto_audio_sync:
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

        # comments
        if c_display != 'NONE' :
            if (c_display == 'SELECTED' and strip.select) \
            or (c_display == 'PERSTRIP' and strip.bpm_shotsettings.display_shot_comments) \
            or (c_display == 'ALL'):
                for m in getCommentFrameFromShotStrip(strip):
                    coord = getCommentsCoordinates(m[1], strip.channel, region, dpi_fac)
                    vertices_m += coord[0]
                    indices_m += ((n_m, n_m + 1, n_m + 2),)
                    n_m += 3   

                    # comments text
                    if (c_n_display in {"CURRENT_STRIPPED", "CURRENT_ENTIRE"} and scn.frame_current == m[1]) \
                    or (c_n_display in {"ALL_STRIPPED", "ALL_ENTIRE", "ALL_STRIPPED_CURRENT_ENTIRE"}) :

                        text = m[0]
                        if (c_n_display in {"CURRENT_STRIPPED", "ALL_STRIPPED"}) \
                        or (c_n_display == "ALL_STRIPPED_CURRENT_ENTIRE" and scn.frame_current != m[1]):
                            limit = scene_settings.display_shot_comments_text_limit
                            if len(text) > limit and limit != 0:
                                if limit > 4:
                                    text = text[0:limit - 3] + "..."
                                else:
                                    text = text[0:limit]
                        comments_texts.append((coord[1], text))

                        # comments box
                        if scene_settings.display_shot_comments_boxes:
                            vertices_m_bb += getBoundingBoxCoordinates(coord[1], text, text_size, dpi_fac)
                            indices_m_bb += ((n_m_bb, n_m_bb + 1, n_m_bb + 2), (n_m_bb + 2, n_m_bb + 1, n_m_bb + 3))
                            n_m_bb += 4
    

    ### DRAW SHADERS ###

    #bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE)

    #shot todo
    if scene_settings.display_shot_todo:
        drawShader(vertices_e_td, indices_e_td, color_e_td)
    
    #shot strips
    if scene_settings.display_shot_strip:
        drawShader(vertices_e_s, indices_e_s, color_e_s)

    #bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)

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

    #deadline preview
    if scene_settings.display_working_warning:
        drawShader(vertices_e_ws, indices_e_ws, color_e_ws)

    # audio sync info
    if scene_settings.display_audio_sync_warning:
        drawShader(vertices_e_au, indices_e_au, color_e_au)

    # update warning
    if scene_settings.display_shot_update_warning:
        drawShader(vertices_e_w, indices_e_w, color_e_w)

    # version warning
    if scene_settings.display_shot_version_warning:
        drawShader(vertices_e_v_w, indices_e_v_w, color_e_v_w)

    # comments
    if c_display != 'NONE' :

        # comments bounding boxes
        if c_n_display != "NONE" and scene_settings.display_shot_comments_boxes:
            drawShader(vertices_m_bb, indices_m_bb, color_m_bb)

        # comments
        drawShader(vertices_m, indices_m, color_m)

        # draw comments texts
        if c_n_display != "NONE":
            for t in comments_texts:
                drawText(t[0], t[1], id_m)

            bgl.glDisable(bgl.GL_BLEND)


# ui draw timeline comments callback
def draw_bpm_sequencer_timeline_callback_px():

    context = bpy.context

    scn = context.scene
    scene_settings = scn.bpm_scenesettings
    
    if not scene_settings.extra_ui \
    or not scene_settings.display_timeline_comments:
        return

    bgl.glEnable(bgl.GL_BLEND)

    sequencer = scn.sequence_editor
    region = context.region

    t_display = scene_settings.display_timeline_comments_names

    # compute dpi_fac on every draw dynamically
    dpi = context.preferences.system.dpi
    dpi_fac = getDpiFactorFromContext(context)

    # setup timeline comments
    vertices_tc = ()
    indices_tc = ()
    n_tc = 0
    color_tc = scene_settings.color_timeline_comments

    # setup comments text
    id_m = comments_font["font_id"]
    blf.color(id_m, *color_tc)
    blf.size(id_m, text_size, dpi)
    comments_texts = []

    # setup timeline com bounding boxes
    vertices_c_bb =()
    indices_c_bb = ()
    n_c_bb = 0
    color_c_bb = scene_settings.color_timeline_comments_boxes

    # timeline comments
    for c in get_timeline_comments_list(context, region, dpi_fac):
        comment = c[0]
        frame = c[2]
        coord = c[1]
        vertices_tc += coord[0]
        indices_tc += ((n_tc, n_tc + 1, n_tc + 2),)
        n_tc += 3

        if (t_display in {"CURRENT_STRIPPED", "CURRENT_ENTIRE"} and scn.frame_current == frame) \
        or (t_display in {"ALL_STRIPPED", "ALL_ENTIRE", "ALL_STRIPPED_CURRENT_ENTIRE"}) :

            text = c[0]
            if (t_display in {"CURRENT_STRIPPED", "ALL_STRIPPED"}) \
            or (t_display == "ALL_STRIPPED_CURRENT_ENTIRE" and scn.frame_current != frame):
                limit = scene_settings.display_timeline_comments_text_limit
                if len(text) > limit and limit != 0:
                    if limit > 4:
                        text = text[0:limit - 3] + "..."
                    else:
                        text = text[0:limit]
            
            comments_texts.append((coord[1], text))

            # comments box
            if scene_settings.display_shot_comments_boxes:
                vertices_c_bb += getBoundingBoxCoordinates(coord[1], text, text_size, dpi_fac)
                indices_c_bb += ((n_c_bb, n_c_bb + 1, n_c_bb + 2), (n_c_bb + 2, n_c_bb + 1, n_c_bb + 3))
                n_c_bb += 4

    # comments bounding boxes
    if t_display != "NONE" and scene_settings.display_shot_comments_boxes:
        drawShader(vertices_c_bb, indices_c_bb, color_c_bb)

    # timeline comments
    drawShader(vertices_tc, indices_tc, color_tc)

    # draw comments texts
    if t_display != "NONE":

        for t in comments_texts:
            drawText(t[0], t[1], comments_font["font_id"])

    bgl.glDisable(bgl.GL_BLEND)


#enable callback
cb_handle = []
def enableSequencerCallback():
    if cb_handle:
        return
    
    initializeExternalFontId(comments_font, font_file)

    cb_handle.append(bpy.types.SpaceSequenceEditor.draw_handler_add(
        draw_bpm_sequencer_strip_callback_px, (), 'WINDOW', 'POST_PIXEL'))

    cb_handle.append(bpy.types.SpaceSequenceEditor.draw_handler_add(
        draw_bpm_sequencer_timeline_callback_px, (), 'WINDOW', 'POST_PIXEL'))

    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(add_extra_ui_statement)#debug

#disable callback
def disableSequencerCallback():
    if not cb_handle:
        return

    unloadExternalFontId(comments_font, font_file)

    # bpy.types.SpaceSequenceEditor.draw_handler_remove(cb_handle[0], 'WINDOW')

    for h in cb_handle:
        bpy.types.SpaceSequenceEditor.draw_handler_remove(h, 'WINDOW')
    cb_handle.clear()

    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(remove_extra_ui_statement) #debug