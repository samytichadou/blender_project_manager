import bpy
import os
import shutil


from ..global_variables import (
                            old_folder,
                            starting_empty_recycle_bin_statement,
                            emptying_folder_statement,
                            folder_emptied_statement,
                            empty_recycle_bin_completed_statement,
                        )

from ..functions.file_functions import deleteFolderContent


class BPMEmptyRecycleBin(bpy.types.Operator):
    """Empty project recycle bin"""
    bl_idname = "bpm.empty_recycle_bin"
    bl_label = "Empty recycle bin"
    bl_options = {'REGISTER'}

    wiki_page = "test"

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_datas[0].edit_scene_keyword
        if context.window_manager.bpm_isproject and context.window_manager.bpm_filetype == 'EDIT':
            if keyword in context.scene.name:
                return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Continue ?")

    def execute(self, context):
        winman = context.window_manager

        if winman.bpm_debug: print(starting_empty_recycle_bin_statement) #debug

        # get folders to empty
        old_folder_path = os.path.join(winman.bpm_projectfolder, old_folder)
        for filename in os.listdir(old_folder_path):

            filepath = os.path.join(old_folder_path, filename)
            if os.path.isdir(filepath):

                if winman.bpm_debug: print(emptying_folder_statement + filepath) #debug

                # empty folders
                deleteFolderContent(filepath)

                if winman.bpm_debug: print(folder_emptied_statement) #debug

        if winman.bpm_debug: print(empty_recycle_bin_completed_statement) #debug
        
        return {'FINISHED'}