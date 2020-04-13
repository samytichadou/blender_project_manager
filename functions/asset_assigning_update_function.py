import bpy
import os


from .project_data_functions import getAssetFile
from .json_functions import read_json, createJsonDatasetFromProperties, create_json_file
from .file_functions import getBlendName
from ..global_variables import (
                            bypass_shot_settings_update_statement,
                            cleared_old_asset_statement,
                            set_asset_statement,
                            saving_to_json_statement,
                            saved_to_json_statement,
                        )


# save asset to json
def saveAssetToJson(self, context):
    winman = context.window_manager
    debug = winman.bpm_generalsettings.debug

    if winman.bpm_generalsettings.bypass_update_tag:
        if debug: print(bypass_shot_settings_update_statement) #debug
        return

    assets_json_file, asset_file_exist = getAssetFile(winman)
    asset_settings = winman.bpm_assetsettings
    
    datas = read_json(assets_json_file)

    if debug: print(saving_to_json_statement) #debug

    # remove old asset settings
    n = 0
    for a in datas['assets']:
        if a['name'] == asset_settings.name:
            del datas['assets'][n]
            break
        n += 1
    
    # get new asset datas
    asset_datas = createJsonDatasetFromProperties(asset_settings)

    # add collection and shader
    if asset_settings.asset_collection is not None:
        asset_datas['asset_collection'] = asset_settings.asset_collection.name
    if asset_settings.asset_material is not None:
        asset_datas['asset_material'] = asset_settings.asset_material.name
    if asset_settings.asset_world is not None:
        asset_datas['asset_world'] = asset_settings.asset_world.name

    datas['assets'].append(asset_datas)

    #create json
    create_json_file(datas, assets_json_file)

    if debug: print(saved_to_json_statement) #debug


# update function for assigning asset through pointer
def updateAssetAssigning(self, context):
    winman = context.window_manager
    debug = winman.bpm_generalsettings.debug

    if winman.bpm_generalsettings.bypass_update_tag:
        if debug: print(bypass_shot_settings_update_statement) #debug
        return
    
    if self.asset_type not in {'SHADER', 'WORLD'}:
        asset = self.asset_collection
    elif self.asset_type == 'SHADER':
        asset = self.asset_material
    elif self.asset_type == 'WORLD':
        asset = self.asset_world

    if debug: print(cleared_old_asset_statement)

    # clear old assets
    for i in bpy.data.collections:
        i.bpm_isasset = False
    for i in bpy.data.materials:
        i.bpm_isasset = False
    for i in bpy.data.worlds:
        i.bpm_isasset = False

    # set asset
    if asset is not None:
        asset.bpm_isasset = True
        if debug: print(set_asset_statement + asset.name)

    # save json
    saveAssetToJson(self, context)


# update function for changing asset type
def updateChangingAssetType(self, context):
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    debug = general_settings.debug

    if general_settings.bypass_update_tag:
        if debug: print(bypass_shot_settings_update_statement) #debug
        return
    
    general_settings.bypass_update_tag = True

    if self.asset_type not in {'SHADER', 'WORLD'}:
        self.asset_material = None
        self.asset_world = None
        to_clear1 = bpy.data.materials
        to_clear2 = bpy.data.worlds
    elif self.asset_type == 'SHADER':
        self.asset_collection = None
        self.asset_world = None
        to_clear1 = bpy.data.collections
        to_clear2 = bpy.data.worlds
    elif self.asset_type == 'WORLD':
        self.asset_collection = None
        self.asset_material = None
        to_clear1 = bpy.data.collections
        to_clear2 = bpy.data.materials

    general_settings.bypass_update_tag = False

    # clear old assets
    for i in to_clear1:
        i.bpm_isasset = False
    for i in to_clear2:
        i.bpm_isasset = False

    if debug: print(cleared_old_asset_statement)

    # save json
    saveAssetToJson(self, context)