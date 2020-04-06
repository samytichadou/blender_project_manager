import bpy
import os


from ..global_variables import (
                            bypass_shot_settings_update_statement,
                            cleared_old_asset_statement,
                            set_asset_statement,
                        )


#update function for assigning asset through pointer
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


#update function for changing asset type
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