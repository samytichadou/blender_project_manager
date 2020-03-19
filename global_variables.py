import os

bpm_statement = "Blender Project Manager --- "

opening_statement = bpm_statement + "Opening "
back_to_edit_statement = bpm_statement + "Opening Editing Project "

creating_shot_statement = bpm_statement + "Starting new shot creation"
creating_shot_folder_statement = bpm_statement + "Creating New Shot Folder : "

startup_statement = bpm_statement + "Looking for Project Datas"
loaded_datas_statement = bpm_statement + "Project Datas loaded"
loaded_folders_statement = bpm_statement + "Project Folders loaded"
no_datas_statement = bpm_statement + "Project Datas not found"
loading_statement = bpm_statement + "Project Datas found, loading from "
folders_loading_statement = bpm_statement + "Project Folders found, loading from "
currently_loading_statement = bpm_statement + "Currently loading "

reading_json_statement = bpm_statement + "Reading Project Datas from json file"

saving_to_json_statement = bpm_statement + "Saving to json"
saved_to_json_statement = bpm_statement + "Successfully saved to json"

setting_prop_statement = bpm_statement + "Setting property : "
setting_prop_error_statement = bpm_statement + "Unable to set property : "

creating_python_script_statement = bpm_statement + "Creating Python script : "
python_script_created_statement = bpm_statement + "Python script successfully created"
launching_command_statement = bpm_statement + "Launching Command : "
deleted_file_statement = bpm_statement + "File successfully deleted : "
scenes_linked_statement = bpm_statement + "Scenes linked from : "
no_available_timeline_space_message = "No available space on timeline"
no_available_timeline_space_statement = bpm_statement + no_available_timeline_space_message
checking_available_timeline_space_statement = bpm_statement + "Checking on timeline for available space"

file_project = "project_data.json"
custom_folders_file = "project_custom_folders.json"
python_temp = "python_temp.py"

script_file = os.path.realpath(__file__)
setup_script_folder = os.path.join(os.path.dirname(script_file), "setup_blend_scripts")
shot_setup_file = os.path.join(setup_script_folder, "shot_setup.py")