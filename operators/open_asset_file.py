import bpy
import os
import subprocess


class BPM_OT_open_asset_file(bpy.types.Operator):
    """Open asset file"""
    bl_idname = "bpm.open_asset_file"
    bl_label = "Open asset file"
    bl_options = {'REGISTER'}

    new_blender_instance : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        idx = general_settings.asset_list_index
        if idx < len(winman.bpm_assets):
            if idx >= 0:
                return general_settings.is_project and not winman.bpm_assets[idx].is_thisassetfile

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
        debug = winman.bpm_projectdatas.debug
        asset_list = winman.bpm_assets
        asset_name = asset_list[general_settings.asset_list_index].name

        if debug: print(importing_asset_statement + asset_name) #debug

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
        if self.new_blender_instance:
            subprocess.Popen([bpy.app.binary_path, specific_asset_filepath])
        else:
            bpy.ops.wm.open_mainfile(filepath=specific_asset_filepath)
        
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_open_asset_file)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_open_asset_file)