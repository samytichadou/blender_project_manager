import bpy
import os


from ..global_variables import (
                            render_folder,
                            render_shots_folder,
                            setting_prop_statement,
                            setting_prop_error_statement,
                            setting_render_statement,
                            render_set_statement,
                        )
from .file_functions import returnRenderFilePathFromShot


def setRenderShot(context, shot_render_state):

    winman = context.window_manager
    #shot_render_state = winman.bpm_shotsettings.shot_render_state
    debug = winman.bpm_projectdatas.debug
    render_settings = winman.bpm_rendersettings[shot_render_state]
    scn = context.scene
    render = scn.render

    if debug: print(setting_render_statement) #debug

    # get render folder
    output_filepath = returnRenderFilePathFromShot(bpy.data.filepath, winman, shot_render_state)

    if render_settings.is_file_format != 'FFMPEG':
        output_filepath += "#####"

    # set render

    #filepath
    render.filepath = bpy.path.relpath(output_filepath)

    #props
    if debug: print(setting_prop_statement + "render settings") #debug
    for p in render_settings.bl_rna.properties:
        if not p.is_readonly and p.identifier != 'name':
            # set dataset
            identif = p.identifier[3:]
            # render
            if "rd_" in p.identifier:
                dataset = render
            # image settings
            elif "is_" in p.identifier:
                dataset = render.image_settings
            # cycles
            elif "cy_" in p.identifier:
                dataset = scn.cycles
            # eevee
            elif "ee_" in p.identifier:
                dataset = scn.eevee
            # ffmpeg
            elif "ff_" in p.identifier:
                dataset = render.ffmpeg

            # set props
            try:
                setattr(dataset, identif, getattr(render_settings, p.identifier))
            except (KeyError, AttributeError, TypeError):
                if debug: print(setting_prop_error_statement + identif) #debug
                pass

    if debug: print(render_set_statement) #debug