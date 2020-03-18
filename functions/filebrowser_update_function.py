import bpy


#update function for filebrowser custom path
def updateFilebrowserPath(self, context):
    winman = context.window_manager
    folders_coll = winman.bpm_folders
    
    area = context.area

    try:
        folder = folders_coll[winman.bpm_foldersindex]
        area.spaces[0].params.directory = str.encode(folder.filepath)
    except IndexError:
        pass