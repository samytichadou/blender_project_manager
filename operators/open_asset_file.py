import bpy
import os


class BPMOpenAssetFile(bpy.types.Operator):
    """Open asset file"""
    bl_idname = "bpm.open_asset_file"
    bl_label = "Open asset file"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        return winman.bpm_generalsettings.is_project and winman.bpm_generalsettings.asset_choose != "NONE"

    def execute(self, context):
        from ..global_variables import (
                                    importing_asset_statement,
                                    asset_not_existing_message,
                                    asset_not_existing_statement,
                                    asset_file_not_found_message,
                                    asset_file_not_found_statement,
                                    asset_folder,
                                )

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = general_settings.debug
        asset_name = general_settings.asset_choose
        asset_list = winman.bpm_assets

        if debug: print(importing_asset_statement + asset_name) #debug

        # check for asset in asset list
        try:
            asset_list[asset_name]
        except KeyError:
            self.report({'INFO'}, asset_not_existing_message + asset_name)
            if debug: print(asset_not_existing_statement + asset_name) #debug
            return {'FINISHED'}

        # asset filepath
        asset_folder_path = os.path.join(general_settings.project_folder, asset_folder)
        specific_asset_folder_path = os.path.join(asset_folder_path, asset_name)
        specific_asset_filepath = os.path.join(specific_asset_folder_path, asset_name + ".blend")

        # check for asset file
        if not os.path.isfile(specific_asset_filepath):
            self.report({'INFO'}, asset_file_not_found_message + asset_name)
            if debug: print(asset_file_not_found_statement + asset_name) #debug
            return {'FINISHED'}

        # save
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        # open
        bpy.ops.wm.open_mainfile(filepath=specific_asset_filepath)
        
        return {'FINISHED'}