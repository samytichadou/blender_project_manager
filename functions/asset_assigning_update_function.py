from . import project_data_functions as pjt_dta_fct
from . import json_functions as js_fct
from .. import global_variables as g_var


# save asset to json
def saveAssetToJson(self, context):
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug

    if winman.bpm_generalsettings.bypass_update_tag:
        #if debug: print(bypass_settings_update_statement) #debug
        return

    assets_json_file, asset_file_exist = pjt_dta_fct.getAssetFile(winman)
    asset_settings = winman.bpm_assetsettings
    
    datas = js_fct.read_json(assets_json_file)

    if debug: print(g_var.saving_to_json_statement) #debug

    # remove old asset settings
    n = 0
    for a in datas['assets']:
        if a['name'] == asset_settings.name:
            del datas['assets'][n]
            break
        n += 1
    
    # get new asset datas
    asset_datas = js_fct.createJsonDatasetFromProperties(asset_settings, ("is_thisassetfile", "comments"))

    # add collection and shader
    if asset_settings.asset_collection is not None:
        asset_datas['asset_collection'] = asset_settings.asset_collection.name
    if asset_settings.asset_material is not None:
        asset_datas['asset_material'] = asset_settings.asset_material.name
    if asset_settings.asset_world is not None:
        asset_datas['asset_world'] = asset_settings.asset_world.name
    if asset_settings.asset_nodegroup is not None:
        asset_datas['asset_nodegroup'] = asset_settings.asset_nodegroup.name

    datas['assets'].append(asset_datas)

    #create json
    js_fct.create_json_file(datas, assets_json_file)

    if debug: print(g_var.saved_to_json_statement) #debug


# update function for assigning asset through pointer
def updateAssetAssigning(self, context):
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug

    if winman.bpm_generalsettings.bypass_update_tag:
        #if debug: print(bypass_settings_update_statement) #debug
        return
    
    if self.asset_type == 'SHADER':
        asset = self.asset_material
    elif self.asset_type == 'NODEGROUP':
        asset = self.asset_nodegroup
    elif self.asset_type == 'WORLD':
        asset = self.asset_world
    else:
        asset = self.asset_collection

    if debug: print(g_var.cleared_old_asset_statement)

    # clear old assets
    pjt_dta_fct.clearOldAssetBpmIsasset()

    # set asset
    if asset is not None:
        asset.bpm_isasset = True
        if debug: print(g_var.set_asset_statement + asset.name)

    # save json
    saveAssetToJson(self, context)


# update function for changing asset type
def updateChangingAssetType(self, context):
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    debug = winman.bpm_projectdatas.debug

    if general_settings.bypass_update_tag:
        #if debug: print(bypass_settings_update_statement) #debug
        return
    
    general_settings.bypass_update_tag = True

    pjt_dta_fct.clearOldAssetBpmIsasset()

    if self.asset_type not in {'SHADER', 'WORLD', 'NODEGROUP'}:       
        self.asset_material = None
        self.asset_world = None
        self.asset_nodegroup = None
        asset = self.asset_collection
    elif self.asset_type == 'SHADER':
        self.asset_collection = None
        self.asset_world = None
        self.asset_nodegroup = None
        asset = self.asset_material
    elif self.asset_type == 'NODEGROUP':
        self.asset_collection = None
        self.asset_world = None
        self.asset_material = None
        asset = self.asset_nodegroup
    elif self.asset_type == 'WORLD':
        self.asset_collection = None
        self.asset_material = None
        self.asset_nodegroup = None
        asset = self.asset_world

    general_settings.bypass_update_tag = False

    if asset is not None:
        asset.bpm_isasset = True

    if debug: print(g_var.cleared_old_asset_statement)

    # save json
    saveAssetToJson(self, context)