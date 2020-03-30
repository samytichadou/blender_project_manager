import bpy
import os


from ..properties import asset_state_items, asset_type_items
from ..global_variables import(
                        asset_folder,
                        asset_file,
                        reading_json_statement,
                        saving_to_json_statement,
                        saved_to_json_statement,
                        deleted_file_statement,
                        creating_asset_statement,
                        asset_created_statement,
                        dupe_asset_name_message,
                        dupe_asset_name_statement,
                        initialize_json_statement,
                        )
from ..functions.json_functions import read_json, createJsonDatasetFromProperties, create_json_file, initializeAssetJsonDatas
from ..functions.file_functions import suppressExistingFile
from ..functions.dataset_functions import setPropertiesFromDataset
from ..functions.project_data_functions import getAssetFile


class BPMCreateAsset(bpy.types.Operator):
    """Create new asset"""
    bl_idname = "bpm.create_asset"
    bl_label = "Create asset"
    #bl_options = {}


    name : bpy.props.StringProperty(name = "Asset name", default="Asset name")
    asset_type : bpy.props.EnumProperty(name = "Asset type", items = asset_type_items, default = 'CHARACTER')
    asset_state : bpy.props.EnumProperty(name = "Asset state", items = asset_state_items, default = 'CONCEPT')

    @classmethod
    def poll(cls, context):
            return context.window_manager.bpm_isproject

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
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
        asset_collection = winman.bpm_assets

        if winman.bpm_debug: print(creating_asset_statement + self.name) #debug

        # create asset blend and get the link TODO

        # create asset datas
        asset_prop = asset_collection.add()

        # set the asset datas
        asset_prop.name = self.name
        asset_prop.asset_type = self.asset_type
        asset_prop.asset_state = self.asset_state

        # get json file path
        asset_file_path, is_asset_file = getAssetFile(winman)

        # check json file if existing and get datas

        if is_asset_file:

            if winman.bpm_debug: print(reading_json_statement + asset_file_path) #debug

            datas = read_json(asset_file_path)

            for asset in datas['assets']:
                if asset['name']==self.name:
                    # error message because dupe name
                    self.report({'INFO'}, dupe_asset_name_message)
                    print(dupe_asset_name_statement)
                    return {'FINISHED'}

            # remove json
            suppressExistingFile(asset_file_path)
            if winman.bpm_debug: print(deleted_file_statement + asset_file_path) #debug
            

        else:

            if winman.bpm_debug: print(initialize_json_statement + asset_file_path) #debug

            datas = initializeAssetJsonDatas()

        # format new asset datas
        asset_datas_json = createJsonDatasetFromProperties(asset_prop)

        # add the new asset
        datas['assets'].append(asset_datas_json)

        # write json
        if winman.bpm_debug: print(saving_to_json_statement) #debug
        create_json_file(datas, asset_file_path)
        if winman.bpm_debug: print(saved_to_json_statement) #debug

        if winman.bpm_debug: print(asset_created_statement + self.name) #debug

        return {'FINISHED'}