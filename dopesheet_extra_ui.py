import bpy
import bgl


from .vse_extra_ui import (
                        initializeExternalFontId,
                        unloadExternalFontId,
                        comments_font,
                        getDpiFactorFromContext,
                        drawShader,
                        )
from .global_variables import (
                        font_file,
                        add_dopesheet_extra_ui_statement,
                        remove_dopesheet_extra_ui_statement,
                            )


# get comments coordinates
def getCommentsCoordinates(frame, region, dpi_fac):
    m_width = 6
    m_height = 9
    t_pos_x = 3
    t_pos_y = 7
    x, y =region.view2d.view_to_region(frame, 0, clip=False)
    y = 13 * dpi_fac
    v1 = (x - m_width * dpi_fac, y)
    v2 = (x + m_width * dpi_fac, y)
    v3 = (x, y + m_height * dpi_fac)
    v4 = (x + t_pos_x, y + t_pos_y)
    return ((v1, v2, v3), v4)


# draw function
def draw_bpm_dope_sheet_comments_callback_px():
    context = bpy.context
    winman = context.window_manager

    general_settings = winman.bpm_generalsettings
    scene_settings = context.scene.bpm_scenesettings

    if general_settings.file_type == "SHOT":
        settings = winman.bpm_shotsettings
    elif general_settings.file_type == "ASSET":
        settings = winman.bpm_assetsettings
    if not scene_settings.extra_ui:
        return

    region = context.region
    dpi_fac = getDpiFactorFromContext(context)

    comments = settings.comments

    # setup timeline comments
    vertices_tc = ()
    indices_tc = ()
    n_tc = 0
    color_tc = scene_settings.color_shot_comments

    bgl.glEnable(bgl.GL_BLEND) # enable transparency

    # iterate through comments
    for c in comments:
        if c.frame_comment:
            coord = getCommentsCoordinates(c.frame, region, dpi_fac)

            vertices_tc += coord[0]
            indices_tc += ((n_tc, n_tc + 1, n_tc + 2),)
            n_tc += 3

    # timeline comments
    drawShader(vertices_tc, indices_tc, color_tc)

    bgl.glDisable(bgl.GL_BLEND) # disable transparency


#enable callback
cb_handle = []
def enable_dope_sheet_ui_callback():
    if cb_handle:
        return
    
    initializeExternalFontId(comments_font, font_file)

    # dopesheet
    cb_handle.append(bpy.types.SpaceDopeSheetEditor.draw_handler_add(
        draw_bpm_dope_sheet_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'))

    # graph editor
    cb_handle.append(bpy.types.SpaceGraphEditor.draw_handler_add(
        draw_bpm_dope_sheet_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'))

    # nla
    cb_handle.append(bpy.types.SpaceNLA.draw_handler_add(
        draw_bpm_dope_sheet_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'))

    # sequencer
    cb_handle.append(bpy.types.SpaceSequenceEditor.draw_handler_add(
        draw_bpm_dope_sheet_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'))

    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(add_dopesheet_extra_ui_statement)#debug


#disable callback
def disable_dope_sheet_ui_callback():
    if not cb_handle:
        return

    unloadExternalFontId(comments_font, font_file)

    # bpy.types.SpaceSequenceEditor.draw_handler_remove(cb_handle[0], 'WINDOW')

    for h in cb_handle:
        # dopesheet
        bpy.types.SpaceDopeSheetEditor.draw_handler_remove(h, 'WINDOW')
        # graph editor
        bpy.types.SpaceGraphEditor.draw_handler_remove(h, 'WINDOW')
        # nla
        bpy.types.SpaceNLA.draw_handler_remove(h, 'WINDOW')
        # sequencer
        bpy.types.SpaceSequenceEditor.draw_handler_remove(h, 'WINDOW')
    cb_handle.clear()

    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(remove_dopesheet_extra_ui_statement) #debug