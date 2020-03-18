import bpy


# project settings
class ProjectSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    #name : bpy.props.StringProperty(name = "Project Name")
    project_prefix : bpy.props.StringProperty(name = "Project Prefix")
    framerate : bpy.props.IntProperty(name = "Project Framerate")
    resolution_x : bpy.props.IntProperty(name = "Resolution X")
    resolution_y : bpy.props.IntProperty(name = "Resolution Y")
    project_folder : bpy.props.StringProperty(name = "Project Folder")
    edit_file : bpy.props.StringProperty(name = "Edit File")
    shot_prefix : bpy.props.StringProperty(name = "Shot Prefix")
    shot_digits : bpy.props.IntProperty(name = "Shot Digits")
    shot_start_frame : bpy.props.IntProperty(name = "Shot Start Frame")
    default_shot_length : bpy.props.IntProperty(name = "Default Shot Length")

# custom project folders
class CustomFolders(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    #name : bpy.props.StringProperty(name = "Project Name")
    filepath : bpy.props.StringProperty(name = "Filepath")