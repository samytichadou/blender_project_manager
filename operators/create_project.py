import bpy
import os
import shutil
import re


# display project settings
class BpmCreateProject(bpy.types.Operator):
    """Create new Blender Project Manager Project"""
    bl_idname = "bpm.create_project"
    bl_label = "Create BPM Project"

    @classmethod
    def poll(cls, context):
        return not context.window_manager.bpm_generalsettings.is_project and bpy.data.is_saved
    
    def invoke(self, context, event):
        from ..functions.file_functions import absolutePath

        # create properties
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        if not winman.bpm_projectdatas:
            winman.bpm_projectdatas.add()
        datas = winman.bpm_projectdatas

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
        general_settings.project_folder = project_dir
        datas.edit_file_pattern = edit_file_name
        datas.name = edit_file_name
        datas.project_prefix = edit_file_name

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        from ..functions.dataset_functions import returnDatasetProperties
        datas = context.window_manager.bpm_projectdatas

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
        # import statements and functions
        from ..functions.file_functions import absolutePath, createFolder
        from ..functions.json_functions import createJsonDatasetFromProperties, create_json_file, initializeAssetJsonDatas
        from ..functions.utils_functions import redrawAreas
        from ..global_variables import (
                                    file_project,
                                    saving_to_json_statement,
                                    saved_to_json_statement,
                                    shot_folder,
                                    asset_folder,
                                    render_folder,
                                    ressources_folder,
                                    old_folder,
                                    folder_created_statement,
                                    render_shots_folder,
                                    render_dailies_folder,
                                    render_draft_folder,
                                    render_render_folder,
                                    render_final_folder,
                                    render_draft_folder,
                                    render_render_folder,
                                    render_final_folder,
                                    render_playblast_folder,
                                    render_file,
                                    startup_files_folder,
                                    base_startup_filepath,
                                    shot_startup_file,
                                    asset_startup_file,
                                )
        from ..vse_extra_ui import enableSequencerCallback

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        render_settings = winman.bpm_rendersettings
        datas = winman.bpm_projectdatas

        if winman.bpm_generalsettings.debug: print(saving_to_json_statement) #debug

        project_folder = general_settings.project_folder
        project_file = os.path.join(project_folder, file_project)

        # format the project datas json dataset
        json_dataset = createJsonDatasetFromProperties(datas, ())

        # create json file
        create_json_file(json_dataset, project_file)
        if winman.bpm_generalsettings.debug: print(saved_to_json_statement) #debug

        # set project as bpm edit project
        general_settings.is_project = True
        general_settings.file_type = 'EDIT'

        # set scene
        scn = bpy.context.scene
        scn.render.fps = datas.framerate
        scn.render.resolution_x = datas.resolution_x
        scn.render.resolution_y = datas.resolution_y

        # create associated folder structure
        #shot
        shot_folder_path = os.path.join(project_folder, shot_folder)
        createFolder(shot_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + shot_folder_path) #debug

        #asset
        asset_folder_path = os.path.join(project_folder, asset_folder)
        createFolder(asset_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + asset_folder_path) #debug

        #render
        render_folder_path = os.path.join(project_folder, render_folder)
        createFolder(render_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_folder_path) #debug

        #shot render
        render_shot_folder_path = os.path.join(render_folder_path, render_shots_folder)
        createFolder(render_shot_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_shot_folder_path) #debug

        #draft shot render
        render_shot_draft_folder_path = os.path.join(render_shot_folder_path, render_draft_folder)
        createFolder(render_shot_draft_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_shot_draft_folder_path) #debug

        #render shot render
        render_shot_render_folder_path = os.path.join(render_shot_folder_path, render_render_folder)
        createFolder(render_shot_render_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_shot_render_folder_path) #debug

        #final shot render
        render_shot_final_folder_path = os.path.join(render_shot_folder_path, render_final_folder)
        createFolder(render_shot_final_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_shot_final_folder_path) #debug

        #playblast shot render
        render_playblast_folder_path = os.path.join(render_shot_folder_path, render_playblast_folder)
        createFolder(render_playblast_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_playblast_folder_path) #debug

        #dailies render
        render_dailies_folder_path = os.path.join(render_folder_path, render_dailies_folder)
        createFolder(render_dailies_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_dailies_folder_path) #debug

        #draft dailies render
        render_dailies_draft_folder_path = os.path.join(render_dailies_folder_path, render_draft_folder)
        createFolder(render_dailies_draft_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_dailies_draft_folder_path) #debug

        #render dailies render
        render_dailies_render_folder_path = os.path.join(render_dailies_folder_path, render_render_folder)
        createFolder(render_dailies_render_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_dailies_render_folder_path) #debug

        #final dailies render
        render_dailies_final_folder_path = os.path.join(render_dailies_folder_path, render_final_folder)
        createFolder(render_dailies_final_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + render_dailies_final_folder_path) #debug

        #ressources
        ressources_folder_path = os.path.join(project_folder, ressources_folder)
        createFolder(ressources_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + ressources_folder_path) #debug

        #startup files folder
        project_startup_files_folder = os.path.join(ressources_folder_path, startup_files_folder)
        createFolder(project_startup_files_folder)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + project_startup_files_folder) #debug

        #old
        old_folder_path = os.path.join(project_folder, old_folder)

        #old shot
        old_shot_folder_path = os.path.join(old_folder_path, shot_folder)
        createFolder(old_shot_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + old_shot_folder_path) #debug

        #old asset
        old_asset_folder_path = os.path.join(old_folder_path, asset_folder)
        createFolder(old_asset_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + old_asset_folder_path) #debug

        #old render
        old_render_folder_path = os.path.join(old_folder_path, render_folder)
        createFolder(old_render_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + old_render_folder_path) #debug

        #old ressources
        old_ressources_folder_path = os.path.join(old_folder_path, ressources_folder)
        createFolder(old_ressources_folder_path)
        if winman.bpm_generalsettings.debug: print(folder_created_statement + old_ressources_folder_path) #debug


        # copy startup files

        #shot startup file
        shot_startup = os.path.join(project_startup_files_folder, shot_startup_file)
        shutil.copy(base_startup_filepath, shot_startup)

        #asset startup file
        asset_startup = os.path.join(project_startup_files_folder, asset_startup_file)
        shutil.copy(base_startup_filepath, asset_startup)


        # create render settings
        #playblast
        new_render = render_settings.add()
        new_render.name = render_playblast_folder

        new_render.is_file_format = 'FFMPEG'
        #draft
        new_render = render_settings.add()
        new_render.name = render_draft_folder
        #render
        new_render = render_settings.add()
        new_render.name = render_render_folder
        #final
        new_render = render_settings.add()
        new_render.name = render_final_folder


        # save render settings as json 
        json_render_dataset = initializeAssetJsonDatas({"render_settings"})
        for r in render_settings:
            r_datas = createJsonDatasetFromProperties(r, ())
            json_render_dataset['render_settings'].append(r_datas)

        # create json file
        if winman.bpm_generalsettings.debug: print(saving_to_json_statement) #debug

        render_filepath = os.path.join(render_folder_path, render_file)
        create_json_file(json_render_dataset, render_filepath)

        if winman.bpm_generalsettings.debug: print(saved_to_json_statement) #debug

        
        # add extra ui
        enableSequencerCallback()

        # reload vse areas
        redrawAreas(context, 'SEQUENCE_EDITOR')

        return {'FINISHED'}