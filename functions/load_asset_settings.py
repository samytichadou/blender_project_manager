import bpy


from .file_functions import getBlendName
from .dataset_functions import setPropertiesFromJsonDataset
from .json_functions import read_json
from .project_data_functions import getAssetFile, getAssetDatasFromJson, setAssetCollectionFromJsonDataset, loadJsonInCollection
from .reload_comments_function import reload_comments
from ..global_variables import (
                            assets_loading_statement,
                            assets_loaded_statement,
                            no_asset_json_file_statement,
                            asset_missing_in_list_statement,
                            assets_settings_loading_statement,
                            assets_settings_loaded_statement,
                            )


def reload_asset_library(winman):

    asset_coll = winman.bpm_assets
    debug = winman.bpm_projectdatas.debug

    asset_file, asset_file_exist = getAssetFile(winman)
    if asset_file_exist:
        if debug: print(assets_loading_statement + asset_file) #debug
        asset_coll = winman.bpm_assets
        loadJsonInCollection(winman, asset_file, asset_coll, 'assets')
        if debug: print(assets_loaded_statement) #debug

    else: 
        if debug: print(no_asset_json_file_statement) #debug


def reload_asset_setings(winman):

    asset_coll = winman.bpm_assets
    debug = winman.bpm_projectdatas.debug
    general_settings = winman.bpm_generalsettings

    # set name of current asset
    asset_settings = winman.bpm_assetsettings
    asset_settings.name = getBlendName()

    asset_file, asset_file_exist = getAssetFile(winman)
    if asset_file_exist:
        if debug: print(assets_loading_statement + asset_file) #debug
        asset_coll = winman.bpm_assets
        asset_datas = read_json(asset_file)
    else:

        return

    # set this blend file asset
    try:
        asset_coll[asset_settings.name].is_thisassetfile = True
    except KeyError:
        if debug: print(asset_missing_in_list_statement) #debug

    asset_settings = winman.bpm_assetsettings
    specific_asset_datas = getAssetDatasFromJson(asset_datas)

    if specific_asset_datas is not None:
        if debug: print(assets_settings_loading_statement) #debug

        general_settings.bypass_update_tag = True
        
        setPropertiesFromJsonDataset(specific_asset_datas, asset_settings, debug, ('asset_collection', 'asset_material'))
        setAssetCollectionFromJsonDataset(asset_settings, specific_asset_datas, debug)
        
        general_settings.bypass_update_tag = False

        if debug: print(assets_settings_loaded_statement) #debug

    # asset does not exist in list error
    else:
        if debug: print(asset_missing_in_list_statement) #debug

    # load asset comments
    reload_comments(bpy.context, "asset", None)