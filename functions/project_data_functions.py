import bpy, os


from ..global_variables import file_project


# get project data file
def getProjectDataFile(winman):
    if bpy.data.is_saved:
        # edit file
        parent_folder = os.path.dirname(bpy.data.filepath)
        subparent_folder = os.path.dirname(parent_folder)
        edit_project_data_file = os.path.join(parent_folder, file_project)
        shot_project_data_file = os.path.join(subparent_folder, file_project)
        if os.path.isfile(edit_project_data_file):
            winman.bpm_isproject = True
            winman.bpm_isedit = True
            return edit_project_data_file
        elif os.path.isfile(shot_project_data_file):
            winman.bpm_isproject = True
            winman.bpm_isedit = False
            return shot_project_data_file