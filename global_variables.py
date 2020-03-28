import os

### STATEMENTS ###

# initial
bpm_statement = "Blender Project Manager --- "

opening_statement = bpm_statement + "Opening "
back_to_edit_statement = bpm_statement + "Opening editing eroject "
loaded_project_folder = bpm_statement + "Project folder loaded : "


# shot creation statements
creating_shot_statement = bpm_statement + "Starting new shot creation"
creating_shot_folder_statement = bpm_statement + "Creating new shot folder : "


# project datas statements
startup_statement = bpm_statement + "Looking for project datas"
loaded_datas_statement = bpm_statement + "Project datas loaded"
loaded_folders_statement = bpm_statement + "Project folders loaded"
no_datas_statement = bpm_statement + "Project datas not found"
loading_statement = bpm_statement + "Project datas found, loading from "
folders_loading_statement = bpm_statement + "Project folders found, loading from "
currently_loading_statement = bpm_statement + "Currently loading "

reading_json_statement = bpm_statement + "Reading project datas from json file"

saving_to_json_statement = bpm_statement + "Saving to json"
saved_to_json_statement = bpm_statement + "Successfully saved to json"

setting_prop_statement = bpm_statement + "Setting property : "
setting_prop_error_statement = bpm_statement + "Unable to set property : "


# python scripts statement
creating_python_script_statement = bpm_statement + "Creating python script : "
python_script_created_statement = bpm_statement + "Python script successfully created"
launching_command_statement = bpm_statement + "Launching command : "


# files operation statements
deleted_file_statement = bpm_statement + "File successfully deleted : "
scenes_linked_statement = bpm_statement + "Scenes linked from : "
folder_created_statement = bpm_statement + "Folder created : "


# timeline statements
no_available_timeline_space_message = "No available space on timeline"
no_available_timeline_space_statement = bpm_statement + no_available_timeline_space_message
checking_available_timeline_space_statement = bpm_statement + "Checking on timeline for available space"


# shot update statement
start_update_shot_statement = bpm_statement + "Starting update shot(s) from timeline"
checking_update_shot_statement  = bpm_statement + "Checking strip for needed update : "
updating_shot_statement = bpm_statement + "Update needed, starting"
update_shot_new_start_end_statement = bpm_statement + "Strip new start-end : "
updated_shot_statement = bpm_statement + "Strip successfully updated"
no_update_needed_statement = bpm_statement + "No update needed"
shot_update_impossible_message = "Impossible to update shot (negative shot start frame)"
shot_update_impossible_statement = bpm_statement + shot_update_impossible_message


# extra ui statements
add_extra_ui_statement = bpm_statement + "Sequencer UI handler added"
remove_extra_ui_statement = bpm_statement + "Sequencer UI handler removed"
load_font_statement = bpm_statement + "External font loaded : "


# asset statements
creating_asset_statement = bpm_statement + "Creating new asset : "
asset_created_statement = bpm_statement + "Asset successfully created : "
dupe_asset_name_message = "Asset name already exists"
dupe_asset_name_statement = bpm_statement + dupe_asset_name_message
assets_loading_statement = bpm_statement + "Loading assets from : "
assets_loaded_statement = bpm_statement + "Assets loaded"


### FILES ###

file_project = "project_data.json"
asset_file = "project_assets.json"
custom_folders_file = "project_custom_folders.json"
python_temp = "python_temp.py"

script_file = os.path.realpath(__file__)
setup_script_folder = os.path.join(os.path.dirname(script_file), "setup_blend_scripts")
shot_setup_file = os.path.join(setup_script_folder, "shot_setup.py")
update_shot_file = os.path.join(setup_script_folder, "update_shot.py")

ressources_folder = os.path.join(os.path.dirname(script_file), "ressources")
font_file = os.path.join(ressources_folder, "JetBrainsMono-Regular.ttf")

new_project_name = "Project_name"

shot_folder = "shots"
asset_folder = "assets"
render_folder = "renders"