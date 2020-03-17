import bpy


from ..functions.file_functions import absolutePath, getLastVersion
from ..global_variables import back_to_edit_statement

class BackToEdit(bpy.types.Operator):
    """Go Back to Edit Project"""
    bl_idname = "bpm.back_to_edit"
    bl_label = "Back to Edit"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_isproject and not context.window_manager.bpm_isedit:
            return True

    def execute(self, context):
        winman = context.window_manager
        project_datas = winman.bpm_datas[0]
        filepath = getLastVersion(project_datas.project_folder, project_datas.edit_file, ".blend")

        if winman.bpm_debug: print(back_to_edit_statement + filepath) #debug

        # save
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        # open
        bpy.ops.wm.open_mainfile(filepath=filepath)

        return {'FINISHED'}