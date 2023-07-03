import bpy
import os
import shutil
from bpy.app.handlers import persistent

from ..global_management import naming_convention as nc

def get_asset_workfile_pattern(asset_workfile_name, project_name):
    return f"asset_{project_name}_{asset_workfile_name}"

def get_asset_workfile_name(pattern, project_name):
    return pattern.split(f"{project_name}_")[1]

class BPM_PR_asset_list(bpy.types.PropertyGroup):
    asset_name : bpy.props.StringProperty()
    folderpath : bpy.props.StringProperty()
    last_version : bpy.props.IntProperty()
    # TODO Version enum for asset browser

class BPM_PR_project_assets(bpy.types.PropertyGroup):
    asset_list : bpy.props.CollectionProperty(
        type = BPM_PR_asset_list,
        )
    asset_index : bpy.props.IntProperty()

def get_project_asset_list():
    asset_props = bpy.context.window_manager.bpm_project_assets

    project_datas = bpy.context.window_manager["bpm_project_datas"]
    root_folder = project_datas["root_folder"]
    assets_folder = os.path.join(root_folder, nc.assets_folder)

    for f in os.listdir(assets_folder):
        path = os.path.join(assets_folder, f)
        if f != nc.asset_library_folder\
        and os.path.isdir(path):
            new = asset_props.asset_list.add()
            new.asset_name = get_asset_workfile_name(f, project_datas["project_name"])
            new.folderpath = path

def reload_asset_list():
    asset_props = bpy.context.window_manager.bpm_project_assets

    print("BPM --- Clearing asset list")
    asset_props.asset_list.clear()

    print("BPM --- Reloading asset list")
    get_project_asset_list()

class BPM_OT_reload_asset_list(bpy.types.Operator):
    bl_idname = "bpm.reload_asset_list"
    bl_label = "Reload BPM Asset List"
    bl_description = "Reload BPM asset list"

    @classmethod
    def poll(cls, context):
        # Check if bpm project
        try:
            bpy.context.window_manager["bpm_project_datas"]
            return True
        except KeyError:
            return False

    def execute(self, context):
        reload_asset_list()

        self.report({'INFO'}, "BPM Asset list refreshed")

        return {'FINISHED'}

class BPM_OT_remove_asset(bpy.types.Operator):
    bl_idname = "bpm.remove_asset"
    bl_label = "Remove BPM Asset"
    bl_description = "Remove BPM asset"

    @classmethod
    def poll(cls, context):
        # Check if bpm project
        try:
            bpy.context.window_manager["bpm_project_datas"]
        except KeyError:
            return False
        asset_props = context.window_manager.bpm_project_assets
        return asset_props.asset_index in range(len(asset_props.asset_list))

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Active asset will be removed")
        layout.label(text="This action is irreversible")
        layout.label(text="Are you sure ?")

    def execute(self, context):
        asset_props = context.window_manager.bpm_project_assets
        asset_list = asset_props.asset_list
        active_asset = asset_list[asset_props.asset_index]

        # Remove asset folder and content
        print("BPM --- Removing asset files : {active_asset.asset_name}")
        asset_folder = active_asset.folderpath
        shutil.rmtree(asset_folder)

        # TODO Remove asset library file

        # Remove asset from list
        print("BPM --- Removing asset from list : {active_asset.asset_name}")
        asset_list.remove(asset_props.asset_index)

        # Refresh UI
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "BPM Asset removed")

        return {'FINISHED'}

def is_asset_workfile_name_existing(name):
    asset_list = bpy.context.window_manager.bpm_project_assets.asset_list
    for asset in asset_list:
        if asset.asset_name == name:
            return True
    return False

class BPM_OT_create_asset(bpy.types.Operator):
    bl_idname = "bpm.create_asset"
    bl_label = "Create BPM Asset"
    bl_description = "Create BPM asset"

    asset_workfile_name : bpy.props.StringProperty(
        name = "Name",
        default = "New Asset",
        )
    # TODO Type system from project json

    @classmethod
    def poll(cls, context):
        # Check if bpm project
        try:
            bpy.context.window_manager["bpm_project_datas"]
            return True
        except KeyError:
            return False

    def invoke(self, context, event):
        reload_asset_list()
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "asset_workfile_name")
        if is_asset_workfile_name_existing(self.asset_workfile_name):
            icon = "ERROR"
        else:
            icon = "CHECKMARK"
        row.label(text="", icon=icon)

    def execute(self, context):
        reload_asset_list()

        # Check if asset name exists
        if is_asset_workfile_name_existing(self.name):
            self.report({'WARNING'}, "BPM Asset name already existing")
            return {'CANCELLED'}

        project_datas = context.window_manager["bpm_project_datas"]
        root_folder = project_datas["root_folder"]

        # Create asset folder
        asset_folder = os.path.join(root_folder, nc.assets_folder)
        asset_pattern = get_asset_workfile_pattern(self.asset_workfile_name, project_datas["project_name"])
        new_folder = os.path.join(asset_folder, asset_pattern)
        os.mkdir(new_folder)

        # Create empty file
        startup_folders = os.path.join(root_folder, nc.startups_folder)
        asset_base_filepath = os.path.join(startup_folders, nc.startup_asset)
        new_asset_filepath = os.path.join(new_folder, f"{asset_pattern}_v001.blend")
        shutil.copy(asset_base_filepath, new_asset_filepath)

        # TODO Create asset json

        # Reload asset list
        reload_asset_list()

        # Refresh UI
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "BPM Asset Created")

        return {'FINISHED'}

@persistent
def asset_list_handler(scene):
    # Check if bpm project
    try:
        bpy.context.window_manager["bpm_project_datas"]
    except KeyError:
        return

    reload_asset_list()


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_PR_asset_list)
    bpy.utils.register_class(BPM_PR_project_assets)
    bpy.types.WindowManager.bpm_project_assets = \
        bpy.props.PointerProperty(
            type = BPM_PR_project_assets,
            name="BPM Project Assets",
            )
    bpy.utils.register_class(BPM_OT_reload_asset_list)
    bpy.utils.register_class(BPM_OT_remove_asset)
    bpy.utils.register_class(BPM_OT_create_asset)

    bpy.app.handlers.load_post.append(asset_list_handler)

def unregister():
    bpy.utils.unregister_class(BPM_PR_asset_list)
    bpy.utils.unregister_class(BPM_PR_project_assets)
    del bpy.types.WindowManager.bpm_project_assets
    bpy.utils.unregister_class(BPM_OT_reload_asset_list)
    bpy.utils.unregister_class(BPM_OT_remove_asset)
    bpy.utils.unregister_class(BPM_OT_create_asset)

    bpy.app.handlers.load_post.remove(asset_list_handler)
