def check_file_poll_function(context):

    is_bpm_project = False
    bpm_filetype = None
    is_bpm_strip = False
    bpm_active_strip = None

    winman = context.window_manager
    general_settings = context.window_manager.bpm_generalsettings

    if general_settings.is_project:
        is_bpm_project = True
        bpm_filetype = general_settings.file_type 
        if general_settings.file_type == 'EDIT':
            if winman.bpm_projectdatas.edit_scene_keyword in context.scene.name:
                if context.scene.sequence_editor:
                    if context.scene.sequence_editor.active_strip:
                        active = context.scene.sequence_editor.active_strip
                        try:
                            if active.bpm_shotsettings.is_shot:
                                bpm_active_strip = active
                        except AttributeError:
                            pass

    return (is_bpm_project, bpm_filetype, bpm_active_strip)