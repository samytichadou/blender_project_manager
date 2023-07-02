import bpy
import os
from bpy.app.handlers import persistent

from ..global_management import naming_convention as nc

def remove_bpm_project_libraries(pattern = "bpm_", to_keep = None):
    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    idx = 0
    for lib in asset_libraries:
        # Look for pattern
        if pattern in lib.name:
            # Check if to_keep
            if to_keep is not None and lib.name == to_keep:
                continue
            bpy.ops.preferences.asset_library_remove(index=idx)
        idx += 1

def create_asset_library(name, directory):
    bpy.ops.preferences.asset_library_add(directory=directory)
    new_library = bpy.context.preferences.filepaths.asset_libraries[-1]
    new_library.name = name

def get_project_asset_library_folder():
    root_folder = bpy.context.window_manager["bpm_project_datas"]["root_folder"]
    assets_folder = os.path.join(root_folder, nc.assets_folder)
    return os.path.join(assets_folder, nc.asset_library_folder)

@persistent
def setup_asset_library_handler(scene):
    # Check if bpm project
    try:
        project_datas = bpy.context.window_manager["bpm_project_datas"]
    except KeyError:
        print("BPM --- Removing project asset library")
        remove_bpm_project_libraries()
        return

    print("BPM --- Removing old project asset libraries")
    remove_bpm_project_libraries()
    print("BPM --- Setting project asset library")
    project_name = project_datas["project_name"]
    create_asset_library(
        f"bpm_{project_name}",
        get_project_asset_library_folder(),
        )


### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(setup_asset_library_handler)
def unregister():
    bpy.app.handlers.load_post.remove(setup_asset_library_handler)
