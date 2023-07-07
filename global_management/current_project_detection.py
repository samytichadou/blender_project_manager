import bpy
import os
from bpy.app.handlers import persistent

from . import manage_projects as mp
from . import naming_convention as nc

def get_project_from_filepath():
    if not bpy.data.is_saved:
        return None
    filepath = bpy.path.abspath(bpy.data.filepath)
    # Get available project folders
    datas = mp.return_global_project_datas()
    for project in datas["projects"]:
        if project["root_folder"] in filepath:
            datas = mp.read_json(project["project_info_file"])
            return datas
    return None

@persistent
def project_detect_handler(scene):
    print("BPM --- Detecting project file")
    project_datas = get_project_from_filepath()
    if project_datas is None:
        print("BPM --- Not a project file")
        return

    bpy.context.window_manager["bpm_project_datas"] = project_datas
    name = project_datas["project_name"]
    print(f"BPM --- Current project : {name}")


def get_file_datas():
    # File not saved
    if not bpy.data.is_saved:
        return None

    file_datas = {}
    filepath = bpy.path.abspath(bpy.data.filepath)
    parent_folder = os.path.dirname(filepath)

    # TODO Get additional infos and types

    # Asset Library
    if nc.asset_library_folder in parent_folder:
        file_datas["file_type"] = "asset_library"

    # Asset
    elif nc.assets_folder in parent_folder:
        file_datas["file_type"] = "asset"
        # TODO Get asset informations (publish or workfiles, asset_name and type)

    # Edit
    elif nc.edits_folder in parent_folder:
        # Get infos from filename
        filename = os.path.splitext(os.path.basename(filepath))[0]
        project_name = bpy.context.window_manager["bpm_project_datas"]["project_name"]
        temp = filename.split(f"{project_name}_ep")[1]
        episode = int(temp.split("_v")[0])
        version = int(temp.split("_v")[1])
        # Store it
        file_datas["file_type"] = "edit"
        file_datas["episode"] = episode
        file_datas["version"] = version

    # Shot
    elif nc.shots_folder in parent_folder:
        file_datas["file_type"] = "shot"

    return file_datas

@persistent
def file_infos_handler(scene):
    # Check if bpm project
    try:
        bpy.context.window_manager["bpm_project_datas"]
    except KeyError:
        return

    print("BPM --- Getting file datas")
    file_datas = get_file_datas()
    if file_datas is not None:
        print(f"BPM --- Storing file datas : {file_datas}")
        bpy.context.window_manager["bpm_file_datas"] = file_datas


### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(project_detect_handler)
    bpy.app.handlers.load_post.append(file_infos_handler)
def unregister():
    bpy.app.handlers.load_post.remove(project_detect_handler)
    bpy.app.handlers.load_post.remove(file_infos_handler)
