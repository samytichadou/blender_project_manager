import bpy
import os


from .project_data_functions import getAssetFile
from .json_functions import read_json, createJsonDatasetFromProperties, create_json_file
from .file_functions import getBlendName
from ..global_variables import (
                            bypass_shot_settings_update_statement,
                            cleared_old_asset_statement,
                            set_asset_statement,
                        )


# save asset to json
def saveAssetToJson(self, context):
    winman = context.window_manager
    assets_json_file = getAssetFile(winman)
    asset_settings = winman.bpm_assetsettings
    debug = winman.bpm_generalsettings.debug

    datas = read_json(assets_json_file)

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

    datas['assets'].append(asset_datas)

    #create json
    create_json_file(datas, assets_json_file)


# update function for assigning asset through pointer
def updateAssetAssigning(self, context):
    winman = context.window_manager
    debug = winman.bpm_generalsettings.debug

    if winman.bpm_generalsettings.bypass_update_tag:
        if debug: print(bypass_shot_settings_update_statement) #debug
        return
    
    if self.asset_type != 'SHADER':
        asset = self.asset_collection
    else:
        asset = self.asset_material

    if debug: print(cleared_old_asset_statement)

    # clear old assets
    for i in bpy.data.collections:
        i.bpm_isasset = False
    for i in bpy.data.materials:
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

    if self.asset_type != 'SHADER':
        self.asset_material = None
        to_clear = bpy.data.materials
    else:
        self.asset_collection = None
        to_clear = bpy.data.collections

    general_settings.bypass_update_tag = False

    # clear old assets
    for i in to_clear:
        i.bpm_isasset = False

    if debug: print(cleared_old_asset_statement)

    # save json
    saveAssetToJson(self, context)