import bpy
import os
import shutil
import re

from .. import global_variables as g_var
from ..addon_prefs import getAddonPreferences
from ..functions import file_functions as fl_fct
from ..functions import json_functions as js_fct
from ..functions.utils_functions import redrawAreas
from ..timer_function import bpmTimerFunction
from ..vse_extra_ui import enableSequencerUICallback


# display project settings
class BPM_OT_create_project(bpy.types.Operator):
    """Create new Blender Project Manager Project"""
    bl_idname = "bpm.create_project"
    bl_label = "Create BPM Project"

    @classmethod
    def poll(cls, context):
        return not context.window_manager.bpm_generalsettings.is_project and bpy.data.is_saved
    
    def invoke(self, context, event):

        # create properties
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        if not winman.bpm_projectdatas:
            winman.bpm_projectdatas.add()
        datas = winman.bpm_projectdatas

        # find project dir and project file
        project_dir = os.path.dirname(fl_fct.absolutePath(bpy.data.filepath))
        file_name = os.path.splitext(os.path.basename(fl_fct.absolutePath(bpy.data.filepath)))[0]
        
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

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        render_settings = winman.bpm_rendersettings
        datas = winman.bpm_projectdatas
        debug = datas.debug

        if debug: print(g_var.saving_to_json_statement) #debug

        project_folder = general_settings.project_folder
        project_file = os.path.join(project_folder, g_var.file_project)

        # format the project datas json dataset
        json_dataset = js_fct.createJsonDatasetFromProperties(datas, ("comments"))

        # create json file
        js_fct.create_json_file(json_dataset, project_file)
        if debug: print(g_var.saved_to_json_statement) #debug

        # set project as bpm edit project
        general_settings.is_project = True
        general_settings.file_type = 'EDIT'

        # set scene
        scn = bpy.context.scene
        scn.render.fps = datas.framerate
        scn.render.resolution_x = datas.resolution_x
        scn.render.resolution_y = datas.resolution_y

        # create associated folder structure
        #datas
        datas_folder_path = os.path.join(project_folder, g_var.datas_folder)        
        fl_fct.createFolder(datas_folder_path)
        if debug: print(g_var.folder_created_statement + datas_folder_path) #debug

        #datas tasks
        datas_tasks_path = os.path.join(datas_folder_path, g_var.datas_tasks_folder)
        fl_fct.createFolder(datas_tasks_path)
        if debug: print(g_var.folder_created_statement + datas_tasks_path) #debug

        #shot
        shot_folder_path = os.path.join(project_folder, g_var.shot_folder)
        fl_fct.createFolder(shot_folder_path)
        if debug: print(g_var.folder_created_statement + shot_folder_path) #debug

        #asset
        asset_folder_path = os.path.join(project_folder, g_var.asset_folder)
        fl_fct.createFolder(asset_folder_path)
        if debug: print(g_var.folder_created_statement + asset_folder_path) #debug

        #render
        render_folder_path = os.path.join(project_folder, g_var.render_folder)
        fl_fct.createFolder(render_folder_path)
        if debug: print(g_var.folder_created_statement + render_folder_path) #debug

        #shot render
        render_shot_folder_path = os.path.join(render_folder_path, g_var.render_shots_folder)
        fl_fct.createFolder(render_shot_folder_path)
        if debug: print(g_var.folder_created_statement + render_shot_folder_path) #debug

        #draft shot render
        render_shot_draft_folder_path = os.path.join(render_shot_folder_path, g_var.render_draft_folder)
        fl_fct.createFolder(render_shot_draft_folder_path)
        if debug: print(g_var.folder_created_statement + render_shot_draft_folder_path) #debug

        #render shot render
        render_shot_render_folder_path = os.path.join(render_shot_folder_path, g_var.render_render_folder)
        fl_fct.createFolder(render_shot_render_folder_path)
        if debug: print(g_var.folder_created_statement + render_shot_render_folder_path) #debug

        #final shot render
        render_shot_final_folder_path = os.path.join(render_shot_folder_path, g_var.render_final_folder)
        fl_fct.createFolder(render_shot_final_folder_path)
        if debug: print(g_var.folder_created_statement + render_shot_final_folder_path) #debug

        #playblast shot render
        render_playblast_folder_path = os.path.join(render_shot_folder_path, g_var.render_playblast_folder)
        fl_fct.createFolder(render_playblast_folder_path)
        if debug: print(g_var.folder_created_statement + render_playblast_folder_path) #debug

        #dailies render
        render_dailies_folder_path = os.path.join(render_folder_path, g_var.render_dailies_folder)
        fl_fct.createFolder(render_dailies_folder_path)
        if debug: print(g_var.folder_created_statement + render_dailies_folder_path) #debug

        #draft dailies render
        render_dailies_draft_folder_path = os.path.join(render_dailies_folder_path, g_var.render_draft_folder)
        fl_fct.createFolder(render_dailies_draft_folder_path)
        if debug: print(g_var.folder_created_statement + render_dailies_draft_folder_path) #debug

        #render dailies render
        render_dailies_render_folder_path = os.path.join(render_dailies_folder_path, g_var.render_render_folder)
        fl_fct.createFolder(render_dailies_render_folder_path)
        if debug: print(g_var.folder_created_statement + render_dailies_render_folder_path) #debug

        #final dailies render
        render_dailies_final_folder_path = os.path.join(render_dailies_folder_path, g_var.render_final_folder)
        fl_fct.createFolder(render_dailies_final_folder_path)
        if debug: print(g_var.folder_created_statement + render_dailies_final_folder_path) #debug

        #ressources
        ressources_folder_path = os.path.join(project_folder, g_var.ressources_folder)
        fl_fct.createFolder(ressources_folder_path)
        if debug: print(g_var.folder_created_statement + ressources_folder_path) #debug

        #startup files folder
        project_startup_files_folder = os.path.join(ressources_folder_path, g_var.startup_files_folder)
        fl_fct.createFolder(project_startup_files_folder)
        if debug: print(g_var.folder_created_statement + project_startup_files_folder) #debug

        #old
        old_folder_path = os.path.join(project_folder, g_var.old_folder)

        #old shot
        old_shot_folder_path = os.path.join(old_folder_path, g_var.shot_folder)
        fl_fct.createFolder(old_shot_folder_path)
        if debug: print(g_var.folder_created_statement + old_shot_folder_path) #debug

        #old asset
        old_asset_folder_path = os.path.join(old_folder_path, g_var.asset_folder)
        fl_fct.createFolder(old_asset_folder_path)
        if debug: print(g_var.folder_created_statement + old_asset_folder_path) #debug

        #old render
        old_render_folder_path = os.path.join(old_folder_path, g_var.render_folder)
        fl_fct.createFolder(old_render_folder_path)
        if debug: print(g_var.folder_created_statement + old_render_folder_path) #debug

        #old ressources
        old_ressources_folder_path = os.path.join(old_folder_path, g_var.ressources_folder)
        fl_fct.createFolder(old_ressources_folder_path)
        if debug: print(g_var.folder_created_statement + old_ressources_folder_path) #debug


        # copy startup files

        #shot startup file
        shot_startup = os.path.join(project_startup_files_folder, g_var.shot_startup_file)
        shutil.copy(g_var.base_startup_filepath, shot_startup)

        #asset startup file
        asset_startup = os.path.join(project_startup_files_folder, g_var.asset_startup_file)
        shutil.copy(g_var.base_startup_filepath, asset_startup)


        # create render settings
        #playblast
        new_render = render_settings.add()
        new_render.name = g_var.render_playblast_folder

        new_render.is_file_format = 'FFMPEG'
        #draft
        new_render = render_settings.add()
        new_render.name = g_var.render_draft_folder
        #render
        new_render = render_settings.add()
        new_render.name = g_var.render_render_folder
        #final
        new_render = render_settings.add()
        new_render.name = g_var.render_final_folder


        # save render settings as json 
        json_render_dataset = js_fct.initializeAssetJsonDatas({"render_settings"})
        for r in render_settings:
            r_datas = js_fct.createJsonDatasetFromProperties(r, ())
            json_render_dataset['render_settings'].append(r_datas)

        # create json file
        if debug: print(g_var.saving_to_json_statement) #debug

        render_filepath = os.path.join(render_folder_path, g_var.render_file)
        js_fct.create_json_file(json_render_dataset, render_filepath)

        if debug: print(g_var.saved_to_json_statement) #debug

        
        # add extra ui
        enableSequencerUICallback()

        # reload vse areas
        redrawAreas(context, 'SEQUENCE_EDITOR')

        # add timer if needed
        if getAddonPreferences().use_timer_refresh:
            bpy.app.timers.register(bpmTimerFunction)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_create_project)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_create_project)