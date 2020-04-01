import bpy


from ..functions.file_functions import absolutePath, getLastVersion
from ..global_variables import back_to_edit_statement


class BPMBackToEdit(bpy.types.Operator):
    """Go Back to Edit Project"""
    bl_idname = "bpm.back_to_edit"
    bl_label = "Back to Edit"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_isproject and context.window_manager.bpm_filetype in {'SHOT', 'ASSET'}:
            return True

    def execute(self, context):
        winman = context.window_manager
        project_datas = winman.bpm_datas[0]
        filepath = getLastVersion(winman.bpm_projectfolder, project_datas.edit_file_pattern, ".blend")

        if winman.bpm_debug: print(back_to_edit_statement + filepath) #debug

        # save
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        # open
        bpy.ops.wm.open_mainfile(filepath=filepath)

        return {'FINISHED'}