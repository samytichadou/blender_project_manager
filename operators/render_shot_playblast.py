import bpy


class BPMRenderShotPlayblast(bpy.types.Operator):
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
        from ..global_variables import render_playblast_folder

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        shot_settings = winman.bpm_shotsettings
        old_render_state = shot_settings.shot_render_state

        pass

        return {'FINISHED'}