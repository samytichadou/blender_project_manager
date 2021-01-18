import bpy


from ..global_variables import completed_render_statement, launching_command_statement

def renderShotEndFunction(shot_strip, debug):
    if debug: print(completed_render_statement + shot_strip.name) #debug
    shot_strip.bpm_shotsettings.is_working = False
    bpy.ops.sequencer.refresh_all()


class BPMRenderShotEdit(bpy.types.Operator):
    """Render shot from edit"""
    bl_idname = "bpm.render_shot_edit"
    bl_label = "Render shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        if context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor.active_strip:
                    if context.scene.sequence_editor:
                        active = context.scene.sequence_editor.active_strip
                        if active.type in {'SCENE', 'IMAGE'}:
                            if not active.lock:
                                try:
                                    if active.bpm_shotsettings.is_shot and not active.bpm_shotsettings.is_working:
                                        return True
                                except AttributeError:
                                    return False

    def execute(self, context):
        from ..functions.file_functions import absolutePath
        from ..functions.command_line_functions import buildBlenderCommandBackgroundRender
        from ..functions.threading_functions import launchSeparateThread

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug

        active_strip = context.scene.sequence_editor.active_strip

        shot_settings = active_strip.bpm_shotsettings

        shot_filepath = absolutePath(shot_settings.shot_filepath)

        #set rendering
        shot_settings.is_working = True

        #build command
        command = buildBlenderCommandBackgroundRender(shot_filepath)

        #launch command
        if debug: print(launching_command_statement + command) #debug
        launchSeparateThread([command, debug, renderShotEndFunction, active_strip, debug])

        #store render pid

        #refresh sequencer
        bpy.ops.sequencer.refresh_all()
        
        return {'FINISHED'}