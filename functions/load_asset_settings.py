import bpy

from .file_functions import getBlendName
from .dataset_functions import setPropertiesFromJsonDataset
from .json_functions import read_json
from . import project_data_functions as pjt_dta_fct
from .reload_comments_function import reload_comments
from .. import global_variables as g_var


def reload_asset_library(winman):

    asset_coll = winman.bpm_assets
    debug = winman.bpm_projectdatas.debug

    asset_file, asset_file_exist = pjt_dta_fct.getAssetFile(winman)
    if asset_file_exist:
        if debug: print(g_var.assets_loading_statement + asset_file) #debug
        asset_coll = winman.bpm_assets
        pjt_dta_fct.loadJsonInCollection(winman, asset_file, asset_coll, 'assets')
        if debug: print(g_var.assets_loaded_statement) #debug

    else: 
        if debug: print(g_var.no_asset_json_file_statement) #debug


def reload_asset_setings(winman):

    asset_coll = winman.bpm_assets
    debug = winman.bpm_projectdatas.debug
    general_settings = winman.bpm_generalsettings

    # set name of current asset
    asset_settings = winman.bpm_assetsettings
    asset_settings.name = getBlendName()

    asset_file, asset_file_exist = pjt_dta_fct.getAssetFile(winman)
    if asset_file_exist:
        if debug: print(g_var.assets_loading_statement + asset_file) #debug
        asset_coll = winman.bpm_assets
        asset_datas = read_json(asset_file)
    else:

        return

    # set this blend file asset
    try:
        asset_coll[asset_settings.name].is_thisassetfile = True
    except KeyError:
        if debug: print(g_var.asset_missing_in_list_statement) #debug

    asset_settings = winman.bpm_assetsettings
    specific_asset_datas = pjt_dta_fct.getAssetDatasFromJson(asset_datas)

    if specific_asset_datas is not None:
        if debug: print(g_var.assets_settings_loading_statement) #debug

        general_settings.bypass_update_tag = True
        
        setPropertiesFromJsonDataset(specific_asset_datas, asset_settings, debug, ('asset_collection', 'asset_material'))
        pjt_dta_fct.setAssetCollectionFromJsonDataset(asset_settings, specific_asset_datas, debug)
        
        general_settings.bypass_update_tag = False

        if debug: print(g_var.assets_settings_loaded_statement) #debug

    # asset does not exist in list error
    else:
        if debug: print(g_var.asset_missing_in_list_statement) #debug

    # load asset comments
    reload_comments(bpy.context, "asset", None)
