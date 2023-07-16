import bpy
import os
import shutil
from datetime import datetime

from . import asset_workfile_management as awm
from ..global_management import naming_convention as nc
from ..global_management import manage_projects as mp
from ..global_management import user_authorization as ua
from .. import addon_prefs as ap

def get_datetime():
    now = datetime.now() # current date and time
    return now.strftime("%Y%m%d_%H%M%S")

def get_current_file_assets():
    asset_list = []
    with bpy.data.libraries.load(bpy.data.filepath, assets_only=True) as (file_contents, _):
        # Iterate through type
        for t in dir(file_contents):
            datas = getattr(file_contents, t)
            for name in datas:
                asset_list.append(getattr(bpy.data, t)[name])
    return asset_list

def get_publish_pattern(asset_name, project_name):
    return f"assetpublish_{project_name}_{asset_name}"

def get_new_publish_datas(version, publish_filename, comment=""):
    new_publish_version = {}
    new_publish_version["version_number"] = version
    new_publish_version["workfile_from"] = os.path.basename(bpy.data.filepath)
    new_publish_version["publish_from"] = publish_filename
    new_publish_version["author"] = ap.getAddonPreferences().logged_user
    new_publish_version["datetime"] = get_datetime()
    new_publish_version["comment"] = comment
    return new_publish_version

class BPM_OT_publish_asset(bpy.types.Operator):
    bl_idname = "bpm.publish_asset"
    bl_label = "Publish BPM Asset"
    bl_description = "Publish BPM asset"

    comment : bpy.props.StringProperty(
        name = "Comment",
        )

    @classmethod
    def poll(cls, context):
        # Check if bpm asset file
        try:
            wm = context.window_manager
            wm["bpm_project_datas"]
            if wm["bpm_file_datas"]["file_type"] != "asset":
                return False
        except KeyError:
            return False
        # Check for authorisation
        return ua.compare_athcode(
            ua.patt_asset_modification,
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        if not get_current_file_assets():
            self.report({'WARNING'}, "No asset in this file")
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "comment")

    def execute(self, context):
        project_datas = context.window_manager["bpm_project_datas"]

        # Get asset datablocks
        print("BPM --- Collecting asset datas")
        data_blocks = get_current_file_assets()

        # Save asset library
        asset_folder_path = os.path.dirname(bpy.data.filepath)
        asset_folder = os.path.basename(asset_folder_path)
        asset_name = awm.get_asset_workfile_name(asset_folder, project_datas["project_name"])

        assets_folder = os.path.join(project_datas["root_folder"], nc.assets_folder)
        asset_lib_folder = os.path.join(assets_folder, nc.asset_library_folder)
        old_asset_lib_folder = os.path.join(assets_folder, nc.old_asset_library_folder)

        json_filepath = os.path.join(asset_folder_path, f"{asset_folder}.json")
        asset_datas = mp.read_json(json_filepath)
        last_version = asset_datas["last_published_version"]
        new_version = last_version + 1
        publish_pattern = get_publish_pattern(asset_name, project_datas["project_name"])
        publish_filename = f"{publish_pattern}_v{str(new_version).zfill(3)}.blend"

        lib_path = os.path.join(asset_lib_folder, publish_filename)

        # Save asset informations in assets for asset browser usage
        print("BPM --- Saving dataset in assets")
        new_publish_dataset = get_new_publish_datas(
            new_version,
            publish_filename,
            self.comment,
            )
        for data in data_blocks:
            data["bpm_asset_datas"] = new_publish_dataset

        # Old previous publish
        print("BPM --- Saving previous publish asset file if needed")
        old_publish_filename = f"{publish_pattern}_v{str(last_version).zfill(3)}.blend"
        old_publish_filepath = os.path.join(asset_lib_folder, old_publish_filename)
        if os.path.isfile(old_publish_filepath):
            shutil.copy(old_publish_filepath, old_asset_lib_folder)
            os.remove(old_publish_filepath)

        # Write new library
        print("BPM --- Writing new asset library")
        bpy.data.libraries.write(lib_path, set(data_blocks))

        # Update asset json
        print("BPM --- Updating asset json")
        asset_datas["last_published_version"] = new_version
        asset_datas["published_versions"].append(new_publish_dataset)

        mp.write_json_file(asset_datas, json_filepath)

        # Bump version
        print("BPM --- Bumping workfile version")
        filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        lgt = len(filename)
        test_name = filename[:-3]
        test_version = filename[lgt-3:]

        if test_version.isdigit():
            bump_version = str(int(test_version)+1).zfill(3)
            new_filename = f"{test_name}{bump_version}.blend"
            new_filepath = os.path.join(asset_folder_path, new_filename)
            bpy.ops.wm.save_as_mainfile(filepath=new_filepath)

        self.report({'INFO'}, "BPM Asset Published")

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_publish_asset)

def unregister():
    bpy.utils.unregister_class(BPM_OT_publish_asset)
