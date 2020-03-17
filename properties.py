import bpy


class ProjectSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    #name : bpy.props.StringProperty(name = "Project Name")
    framerate : bpy.props.IntProperty(name = "Project Framerate")
    project_folder : bpy.props.StringProperty(name = "Project Folder")
    edit_file : bpy.props.StringProperty(name = "Edit File")
    