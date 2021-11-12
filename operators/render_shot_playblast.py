import bpy


class BPM_OT_render_shot_playblast(bpy.types.Operator):
    """Find help on the wiki page"""
    bl_idname = "bpm.render_shot_playlast"
    bl_label = "Render playblast"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'SHOT'

    def execute(self, context):
        # import statements and functions
        from ..functions.set_render_shot_update_function import setRenderShot
        from ..global_variables import (
                                    render_playblast_folder,
                                    setting_playblast_statement,
                                    starting_playblast_statement,
                                    playing_playblast_statement,
                                    setting_usual_render_statement,
                                    completed_playblast_statement,
                                )

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = winman.bpm_generalsettings
        shot_settings = winman.bpm_shotsettings
        old_render_state = shot_settings.shot_render_state

        if debug: print(setting_playblast_statement) #debug
        
        # set render settings 
        setRenderShot(context, render_playblast_folder)
        
        # launch viewport render
        if debug: print(starting_playblast_statement) #debug
        bpy.ops.render.opengl(animation=True)

        # launch playback
        bpy.ops.render.play_rendered_anim()
        if debug: print(playing_playblast_statement) #debug

        # set old settings back
        if debug: print(setting_usual_render_statement) #debug
        general_settings.bypass_update_tag = True
        shot_settings.shot_render_state = old_render_state
        general_settings.bypass_update_tag = False

        if debug: print(completed_playblast_statement) #debug

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_render_shot_playblast)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_render_shot_playblast)