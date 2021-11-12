import bpy
import os
import shutil

from .. import global_variables as g_var
from ..functions import json_functions as js_fct
from ..functions.project_data_functions import getAssetFile
from ..functions.file_functions import createDirectory


class BPM_OT_create_asset(bpy.types.Operator):
    """Create new asset"""
    bl_idname = "bpm.create_asset"
    bl_label = "Create asset"
    bl_options = {'REGISTER'}

    from ..properties import asset_state_items, asset_type_items

    name : bpy.props.StringProperty(name = "Asset name", default="Asset name")
    asset_type : bpy.props.EnumProperty(name = "Asset type", items = asset_type_items, default = 'CHARACTER')
    asset_state : bpy.props.EnumProperty(name = "Asset state", items = asset_state_items, default = 'CONCEPT')

    @classmethod
    def poll(cls, context):
            return context.window_manager.bpm_generalsettings.is_project

    def invoke(self, context, event):
        winman = context.window_manager
        display_asset_type = winman.bpm_generalsettings.panel_asset_display
        if display_asset_type != "ALL":
            self.asset_type = display_asset_type
        return winman.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        # name
        layout.prop(self, 'name')
        # type
        layout.prop(self, 'asset_type')
        # state
        layout.prop(self, 'asset_state')

    def execute(self, context):
        

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = winman.bpm_generalsettings
        asset_collection = winman.bpm_assets

        if debug: print(g_var.creating_asset_statement + self.name) #debug

        # get json file path
        asset_file_path, asset_file_exist = getAssetFile(winman)

        # check json file if existing and get datas

        if asset_file_exist:

            if debug: print(g_var.reading_json_statement + asset_file_path) #debug

            datas = js_fct.(asset_file_path)

            for asset in datas['assets']:

                if asset['name']==self.name:

                    # error message because dupe name
                    self.report({'INFO'}, g_var.dupe_asset_name_message)
                    if debug: print(g_var.dupe_asset_name_statement) #debug

                    return {'FINISHED'}

        else:

            if debug: print(g_var.initialize_json_statement + asset_file_path) #debug

            datas = js_fct.({"assets"})

        # create asset datas
        asset_prop = asset_collection.add()

        # set the asset datas
        asset_prop.name = self.name
        asset_prop.asset_type = self.asset_type
        asset_prop.asset_state = self.asset_state

        # format new asset datas
        asset_datas_json = js_fct.(asset_prop, ("is_thisassetfile"))

        # add the new asset
        datas['assets'].append(asset_datas_json)

        # write json
        if debug: print(g_var.saving_to_json_statement) #debug

        js_fct.(datas, asset_file_path)

        if debug: print(g_var.saved_to_json_statement) #debug
        
        # create the folder
        asset_folder_path = os.path.join(general_settings.project_folder, g_var.asset_folder)
        new_asset_folder_path = os.path.join(asset_folder_path, self.name)
        createDirectory(new_asset_folder_path)
        
        new_asset_file_path = os.path.join(new_asset_folder_path, self.name + ".blend")

        if debug: print(g_var.asset_file_creation_statement + new_asset_file_path) #debug    

        # create ressources folder
        ressources_folder_path = os.path.join(new_asset_folder_path, g_var.asset_ressources_folder)
        createDirectory(ressources_folder_path)

        # create asset blend
        ressources_folder = os.path.join(general_settings.project_folder, ressources_folder)
        startup_folder = os.path.join(ressources_folder, g_var.startup_files_folder)
        asset_startup_filepath = os.path.join(startup_folder, g_var.asset_startup_file)
        shutil.copy(asset_startup_filepath, new_asset_file_path)

        if debug: print(g_var.copying_file_statement + asset_startup_filepath) #debug

        # select asset if available
        if general_settings.panel_asset_display in {'ALL', self.asset_type}:
            for idx, asset in enumerate(asset_collection):
                if asset.name == self.name:
                    general_settings.asset_list_index = idx
                    break

        if debug: print(g_var.asset_created_statement + self.name) #debug

        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_create_asset)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_create_asset)