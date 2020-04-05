import bpy


class BPMBackToEdit(bpy.types.Operator):
    """Go Back to Edit Project"""
    bl_idname = "bpm.back_to_edit"
    bl_label = "Back to Edit"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type in {'SHOT', 'ASSET'}:
                return True

    def execute(self, context):
        # import statement and functions
        from ..functions.file_functions import absolutePath, getLastVersion
        from ..global_variables import back_to_edit_statement

        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        project_datas = winman.bpm_projectdatas
        filepath = getLastVersion(general_settings.project_folder, project_datas.edit_file_pattern, ".blend")

        if general_settings.debug: print(back_to_edit_statement + filepath) #debug

        # save
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        # open
        bpy.ops.wm.open_mainfile(filepath=filepath)

        return {'FINISHED'}