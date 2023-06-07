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
            return project
    return None

@persistent
def project_detect_handler(scene):
    print("BPM --- Detecting project file")
    project_datas = get_project_from_filepath()
    if project_datas is None:
        print("BPM --- Not a project file")
        return
    project_props = bpy.context.window_manager.bpm_current_project
    project_props.name = project_datas["name"]
    project_props.project_name = project_datas["project_name"]
    project_props.project_folder = project_datas["root_folder"]
    print(f"BPM --- Current project : {project_props.project_name}")

class BPM_PR_current_project(bpy.types.PropertyGroup):
    project_name: bpy.props.StringProperty()
    project_folder: bpy.props.StringProperty()

### REGISTER ---
def register():
    bpy.utils.register_class(BPM_PR_current_project)
    bpy.types.WindowManager.bpm_current_project=\
        bpy.props.PointerProperty(type=BPM_PR_current_project)
    bpy.app.handlers.load_post.append(project_detect_handler)
def unregister():
    bpy.utils.unregister_class(BPM_PR_current_project)
    del bpy.types.WindowManager.bpm_current_project
    bpy.app.handlers.load_post.remove(project_detect_handler)
