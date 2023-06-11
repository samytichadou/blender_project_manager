import bpy
from bpy.app.handlers import persistent

from . import manage_projects as mp

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


### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(project_detect_handler)
def unregister():
    bpy.app.handlers.load_post.remove(project_detect_handler)
