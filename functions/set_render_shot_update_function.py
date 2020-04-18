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


def setRenderShot(context):

    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    shot_render_state = winman.bpm_shotsettings.shot_render_state
    debug = general_settings.debug
    render_settings = winman.bpm_rendersettings[shot_render_state]
    scn = context.scene
    render = scn.render

    if debug: print(setting_render_statement) #debug

    # get render folder
    shot_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    render_folder_path = os.path.join(general_settings.project_folder, render_folder)
    render_shot_folder_path = os.path.join(render_folder_path, render_shots_folder)
    spec_render_folder_path = os.path.join(render_shot_folder_path, shot_render_state)

    shot_folder_path = os.path.join(spec_render_folder_path, shot_name)
    output_filepath = os.path.join(shot_folder_path, shot_name + "_#####")

    # set render

    #filepath
    render.filepath = bpy.path.relpath(output_filepath)

    #props
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
                if debug: print(setting_prop_statement + identif) #debug
                setattr(dataset, identif, getattr(render_settings, p.identifier))
            except (KeyError, AttributeError, TypeError):
                if debug: print(setting_prop_error_statement + identif) #debug
                pass

    if debug: print(render_set_statement) #debug