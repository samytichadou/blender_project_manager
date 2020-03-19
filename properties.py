import bpy


# project settings
class ProjectSettings(bpy.types.PropertyGroup) :
    name : bpy.props.StringProperty(name = "Project Name", default = "Project Name")
    project_prefix : bpy.props.StringProperty(name = "Project Prefix", default = "Project Prefix")
    framerate : bpy.props.IntProperty(name = "Project Framerate", default = 25)
    resolution_x : bpy.props.IntProperty(name = "Resolution X", default = 1920)
    resolution_y : bpy.props.IntProperty(name = "Resolution Y", default = 1080)
    project_folder : bpy.props.StringProperty(name = "Project Folder", default = "")
    edit_file_pattern : bpy.props.StringProperty(name = "Edit File Pattern", default = "")
    edit_scene_keyword : bpy.props.StringProperty(name = "Edit Scene Keyword", default = "")
    shot_prefix : bpy.props.StringProperty(name = "Shot Prefix", default = "S")
    shot_digits : bpy.props.IntProperty(name = "Shot Digits", default = 3)
    shot_version_suffix : bpy.props.StringProperty(name = "Shot Version Suffix", default = "v")
    shot_version_digits : bpy.props.IntProperty(name = "Shot Version Digits", default = 3)
    shot_start_frame : bpy.props.IntProperty(name = "Shot Start Frame", default = 100)
    default_shot_length : bpy.props.IntProperty(name = "Default Shot Length", default = 100)

# custom project folders
class CustomFolders(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    #name : bpy.props.StringProperty(name = "Project Name")
    filepath : bpy.props.StringProperty(name = "Filepath")