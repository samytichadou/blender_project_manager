import bpy
import os


class BPMImportAsset(bpy.types.Operator):
    """Import asset in shot"""
    bl_idname = "bpm.import_asset"
    bl_label = "Import asset"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        idx = general_settings.asset_list_index
        if idx < len(winman.bpm_assets):
            if idx >= 0:
                if general_settings.is_project:
                    return winman.bpm_generalsettings.file_type in {'SHOT', 'ASSET'} and not winman.bpm_assets[idx].is_thisassetfile

    def execute(self, context):
        from ..functions.file_functions import linkAssetLibrary
        from ..global_variables import (
                                    importing_asset_statement,
                                    asset_not_existing_message,
                                    asset_not_existing_statement,
                                    asset_file_not_found_message,
                                    asset_file_not_found_statement,
                                    asset_imported_statement,
                                    asset_folder,
                                )

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = general_settings.debug
        asset_list = winman.bpm_assets
        asset = asset_list[general_settings.asset_list_index]
        asset_name = asset_list[general_settings.asset_list_index].name


        asset_folder = os.path.join(general_settings.project_folder, asset_folder)

        if debug: print(importing_asset_statement + asset_name) #debug

        chosen_asset_folder = os.path.join(asset_folder, asset_name)
        chosen_asset_file = os.path.join(chosen_asset_folder, asset_name + ".blend")

        if not os.path.isfile(chosen_asset_file):
            self.report({'INFO'}, asset_file_not_found_message + chosen_asset_file)
            if debug: print(asset_file_not_found_statement + chosen_asset_file) #debug
            return {'FINISHED'} 
        
        # link asset
        if not linkAssetLibrary(chosen_asset_file, asset, debug):
            self.report({'INFO'}, asset_not_existing_message + asset_name)
            if debug: print(asset_not_existing_statement + asset_name) #debug

        else:

            if debug: print(asset_imported_statement) #debug
        
        return {'FINISHED'}