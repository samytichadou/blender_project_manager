import bpy


from ..global_variables import creating_shot_statement, creating_shot_folder_statement
from ..functions.file_functions import getNextShot, createDirectory
from ..functions.project_data_functions import getShotPattern


class BPMCreateShot(bpy.types.Operator):
    """Create Shot from Timeline"""
    bl_idname = "bpm.create_shot"
    bl_label = "Create Shot"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject and context.window_manager.bpm_isedit

    def execute(self, context):
        winman = context.window_manager
        
        if winman.bpm_debug: print(creating_shot_statement) #debug
        
        project_datas = winman.bpm_datas[0]
        next_shot_folder, next_shot = getNextShot(project_datas.project_folder, getShotPattern(project_datas), project_datas.shot_digits)

        createDirectory(next_shot_folder)

        if winman.bpm_debug: print(creating_shot_folder_statement + next_shot_folder) #debug

        return {'FINISHED'}