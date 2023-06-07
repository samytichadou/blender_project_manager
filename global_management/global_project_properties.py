import bpy

class BPM_PR_global_projects(bpy.types.PropertyGroup):
    project_name: bpy.props.StringProperty()
    project_folder: bpy.props.StringProperty()

### REGISTER ---
def register():
    bpy.utils.register_class(BPM_PR_global_projects)
    bpy.types.WindowManager.bpm_global_projects=\
        bpy.props.CollectionProperty(type=BPM_PR_global_projects)
def unregister():
    bpy.utils.unregister_class(BPM_PR_global_projects)
    del bpy.types.WindowManager.bpm_global_projects
