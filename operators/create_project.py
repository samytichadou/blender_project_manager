import bpy
import os
import re


from ..functions.dataset_functions import returnDatasetProperties
from ..functions.file_functions import suppressExistingFile, absolutePath, createFolder
from ..functions.json_functions import createJsonDatasetFromProperties, create_json_file
from ..functions.utils_functions import redrawAreas

from ..global_variables import (
                            file_project,
                            saving_to_json_statement,
                            saved_to_json_statement,
                            new_project_name,
                            shot_folder,
                            asset_folder,
                            render_folder,
                            folder_created_statement,
                            old_folder,
                        )
from ..vse_extra_ui import enableSequencerCallback

# display project settings
class BpmCreateProject(bpy.types.Operator):
    """Create new Blender Project Manager Project"""
    bl_idname = "bpm.create_project"
    bl_label = "Create BPM Project"

    @classmethod
    def poll(cls, context):
        return not context.window_manager.bpm_isproject and bpy.data.is_saved
    
    def invoke(self, context, event):
        # create properties
        winman = context.window_manager
        if not winman.bpm_datas:
            winman.bpm_datas.add()
        datas = winman.bpm_datas

        # find project dir and project file
        project_dir = os.path.dirname(absolutePath(bpy.data.filepath))
        file_name = os.path.splitext(os.path.basename(absolutePath(bpy.data.filepath)))[0]
        
        # get edit file pattern without version numbers
        i = re.search(r'\d+$', file_name)
        if i is not None:
            edit_file_name = file_name[:-len(i.group())]
        else:
            edit_file_name = file_name

        # set specific project properties
        winman.bpm_projectfolder = project_dir
        datas.edit_file_pattern = edit_file_name
        datas.name = new_project_name

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        datas = context.window_manager.bpm_datas

        layout = self.layout
        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for p in returnDatasetProperties(datas):
            box = col1.box()
            box.label(text=p[0].name)
            box = col2.box()
            box.prop(datas, '%s' % p[0].identifier, text='')
        
    def execute(self, context):
        winman = context.window_manager
        datas = winman.bpm_datas

        if winman.bpm_debug: print(saving_to_json_statement) #debug

        project_folder = winman.bpm_projectfolder
        project_file = os.path.join(project_folder, file_project)

        # format the json dataset
        json_dataset = createJsonDatasetFromProperties(datas)
        # delete previous file
        suppressExistingFile(project_file)
        # create json file
        create_json_file(json_dataset, project_file)

        if winman.bpm_debug: print(saved_to_json_statement) #debug

        # set project as bpm edit project
        winman.bpm_isproject = True
        winman.bpm_filetype = 'EDIT'

        # create associated folder structure
        #shot
        shot_folder_path = os.path.join(project_folder, shot_folder)
        createFolder(shot_folder_path)
        if winman.bpm_debug: print(folder_created_statement + shot_folder_path) #debug

        #asset
        asset_folder_path = os.path.join(project_folder, asset_folder)
        createFolder(asset_folder_path)
        if winman.bpm_debug: print(folder_created_statement + asset_folder_path) #debug

        #render
        render_folder_path = os.path.join(project_folder, render_folder)
        createFolder(render_folder_path)
        if winman.bpm_debug: print(folder_created_statement + render_folder_path) #debug

        #old
        old_folder_path = os.path.join(project_folder, old_folder)

        #old shot
        old_shot_folder_path = os.path.join(old_folder_path, shot_folder)
        createFolder(old_shot_folder_path)
        if winman.bpm_debug: print(folder_created_statement + old_shot_folder_path) #debug

        #old asset
        old_asset_folder_path = os.path.join(old_folder_path, asset_folder)
        createFolder(old_asset_folder_path)
        if winman.bpm_debug: print(folder_created_statement + old_asset_folder_path) #debug

        #old render
        old_render_folder_path = os.path.join(old_folder_path, render_folder)
        createFolder(old_render_folder_path)
        if winman.bpm_debug: print(folder_created_statement + old_render_folder_path) #debug

        enableSequencerCallback()

        # reload vse areas
        redrawAreas(context, 'SEQUENCE_EDITOR')

        return {'FINISHED'}