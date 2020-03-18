import bpy


# project settings
class ProjectSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    #name : bpy.props.StringProperty(name = "Project Name")
    framerate : bpy.props.IntProperty(name = "Project Framerate")
    project_folder : bpy.props.StringProperty(name = "Project Folder", subtype = 'DIR_PATH')
    edit_file : bpy.props.StringProperty(name = "Edit File")

# custom project folders
class CustomFolders(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    #name : bpy.props.StringProperty(name = "Project Name")
    filepath : bpy.props.StringProperty(name = "Filepath", subtype = 'DIR_PATH')