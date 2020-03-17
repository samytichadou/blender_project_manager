import bpy


class ProjectSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    filepath : bpy.props.StringProperty(name = "File Path")
    missingfont : bpy.props.BoolProperty(name = "Missing Font", default = False)
    favorite : bpy.props.BoolProperty(name = "Favorite",
                                    default = False, 
                                    description = "Mark/Unmark as Favorite Font")
    subdirectory : bpy.props.StringProperty(name="Subdirectory")
    index : bpy.props.IntProperty()