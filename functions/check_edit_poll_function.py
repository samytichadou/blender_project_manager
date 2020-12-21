def check_edit_poll_function(context):

    is_bpm_edit = False
    is_bpm_strip = False
    active_strip = None

    if context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT':
        if context.window_manager.bpm_projectdatas.edit_scene_keyword in context.scene.name:
            if context.scene.sequence_editor:
                is_bpm_edit = True
                if context.scene.sequence_editor.active_strip:
                    active_strip = context.scene.sequence_editor.active_strip
                    try:
                        if active_strip.bpm_shotsettings.is_shot:
                            is_bpm_strip = True
                    except AttributeError:
                        pass

    return (is_bpm_edit, is_bpm_strip, active_strip)