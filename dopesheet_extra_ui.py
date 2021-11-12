import bpy
import bgl
import blf

from . import vse_extra_ui as vse_ui
from . import global_variables as g_var


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
def draw_bpm_shot_asset_comments_callback_px():

    context = bpy.context
    winman = context.window_manager

    general_settings = winman.bpm_generalsettings
    scn = context.scene
    scene_settings = scn.bpm_scenesettings

    if general_settings.file_type == "SHOT":
        settings = winman.bpm_shotsettings
    elif general_settings.file_type == "ASSET":
        settings = winman.bpm_assetsettings
    if not scene_settings.extra_ui:
        return

    region = context.region
    dpi = context.preferences.system.dpi
    dpi_fac = vse_ui.getDpiFactorFromContext(context)

    comments = settings.comments

    c_display_mode = scene_settings.display_shot_comments_names

    # setup timeline comments
    vertices_tc = ()
    indices_tc = ()
    n_tc = 0
    color_tc = scene_settings.color_shot_comments

    # setup comments bounding box
    vertices_m_bb = ()
    indices_m_bb = ()
    n_m_bb = 0
    color_m_bb = scene_settings.color_shot_comments_boxes

    # setup comments text
    id_m = vse_ui.comments_font["font_id"]
    blf.color(id_m, *color_tc)
    blf.size(id_m, vse_ui.text_size, dpi)
    comments_texts = []

    # iterate through comments
    for c in comments:

        if c.frame_comment:

            coord = getCommentsCoordinates(c.frame, region, dpi_fac)

            vertices_tc += coord[0]
            indices_tc += ((n_tc, n_tc + 1, n_tc + 2),)
            n_tc += 3

            # comments text
            if (c_display_mode in {"CURRENT_STRIPPED", "CURRENT_ENTIRE"} and scn.frame_current == c.frame) \
            or (c_display_mode in {"ALL_STRIPPED", "ALL_ENTIRE", "ALL_STRIPPED_CURRENT_ENTIRE"}) :
                
                text = vse_ui.get_formatted_comment_text(c.comment, c.frame, c_display_mode, scn.frame_current, scene_settings.display_shot_comments_text_limit)

                comments_texts.append((coord[1], text))

                # comments box
                if scene_settings.display_shot_comments_boxes:
                    vertices_m_bb += vse_ui.getBoundingBoxCoordinates(coord[1], text, vse_ui.text_size, dpi_fac)
                    indices_m_bb += ((n_m_bb, n_m_bb + 1, n_m_bb + 2), (n_m_bb + 2, n_m_bb + 1, n_m_bb + 3))
                    n_m_bb += 4


    # actual drawing

    bgl.glEnable(bgl.GL_BLEND) # enable transparency

    # comments bounding boxes
    if c_display_mode != "NONE" and vertices_m_bb:
        vse_ui.drawShader(vertices_m_bb, indices_m_bb, color_m_bb)

    # timeline comments
    vse_ui.drawShader(vertices_tc, indices_tc, color_tc)

    # draw comments texts
    if c_display_mode != "NONE":
        for t in comments_texts:
            vse_ui.drawText(t[0], t[1], vse_ui.comments_font["font_id"])

    bgl.glDisable(bgl.GL_BLEND) # disable transparency


#enable callback
cb_handle = []
def enable_dope_sheet_ui_callback():
    if cb_handle:
        return
    
    vse_ui.initializeExternalFontId(vse_ui.comments_font, g_var.font_file)

    # dopesheet
    cb_handle.append((bpy.types.SpaceDopeSheetEditor.draw_handler_add(
        draw_bpm_shot_asset_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'), "dopesheet"))

    # graph editor
    cb_handle.append((bpy.types.SpaceGraphEditor.draw_handler_add(
        draw_bpm_shot_asset_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'), "graph"))

    # nla
    cb_handle.append((bpy.types.SpaceNLA.draw_handler_add(
        draw_bpm_shot_asset_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'), "nla"))

    # sequencer
    cb_handle.append((bpy.types.SpaceSequenceEditor.draw_handler_add(
        draw_bpm_shot_asset_comments_callback_px, (), 'WINDOW', 'POST_PIXEL'), "sequencer"))

    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(g_var.add_dopesheet_extra_ui_statement)#debug


#disable callback
def disable_dope_sheet_ui_callback():
    if not cb_handle:
        return

    vse_ui.unloadExternalFontId(vse_ui.comments_font, g_var.font_file)

    # bpy.types.SpaceSequenceEditor.draw_handler_remove(cb_handle[0], 'WINDOW')

    for h in cb_handle:
        # dopesheet
        if h[1] == "dopesheet":
            bpy.types.SpaceDopeSheetEditor.draw_handler_remove(h[0], 'WINDOW')
        # graph editor
        elif h[1] == "graph":
            bpy.types.SpaceGraphEditor.draw_handler_remove(h[0], 'WINDOW')
        # nla
        elif h[1] == "nla":
            bpy.types.SpaceNLA.draw_handler_remove(h[0], 'WINDOW')
        # sequencer
        elif h[1] == "sequencer":
            bpy.types.SpaceSequenceEditor.draw_handler_remove(h[0], 'WINDOW')
    cb_handle.clear()

    winman = bpy.context.window_manager
    debug = winman.bpm_projectdatas.debug
    if debug: print(g_var.remove_shot_asset_extra_ui_statement) #debug


### REGISTER ---

# def register():
#     pass

def unregister():
    disable_dope_sheet_ui_callback()