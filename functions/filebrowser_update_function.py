import bpy


#update function for filebrowser custom path
def updateFilebrowserPath(self, context):
    winman = context.window_manager
    folders_coll = winman.bpm_folders
    general_settings = context.window_manager.bpm_generalsettings
    
    area = context.area

    try:
        folder = folders_coll[general_settings.custom_folders_index]
        area.spaces[0].params.directory = str.encode(folder.filepath)
    except IndexError:
        pass