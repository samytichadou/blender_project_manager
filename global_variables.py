import bpy
import os

### STATEMENTS ###

# initial
bpm_statement = "Blender Project Manager --- "

opening_statement = bpm_statement + "Opening "
back_to_edit_statement = bpm_statement + "Opening editing eroject "
loaded_project_folder = bpm_statement + "Project folder loaded : "


# shot management statements
creating_shot_statement = bpm_statement + "Starting new shot creation"
creating_shot_folder_statement = bpm_statement + "Creating new shot folder : "
used_shots_list_statement = bpm_statement + "Shots used in edit : "
existing_shots_list_statement = bpm_statement + "Existing shots in project : "
unused_shots_list_statement = bpm_statement + "Unused shots : "
no_unused_shots_message = "No unused shots"
no_unused_shots_statement = bpm_statement + no_unused_shots_message
starting_delete_shots_statement = bpm_statement + "Starting shot(s) deletion"
starting_delete_specific_shot_statement = bpm_statement + "Starting to delete shot : "
deleting_scene_statement = bpm_statement + "Deleting scene : "
bumping_shot_statement = bpm_statement + "Bumping shot version"
changing_shot_version_statement = bpm_statement + "Changing shot version to version "
invalid_shot_version_message = "Not an existing shot version"
invalid_shot_version_statement = bpm_statement + invalid_shot_version_message
already_loaded_shot_version_message = "Already loaded shot version"
already_loaded_shot_version_statement = bpm_statement + already_loaded_shot_version_message
bypass_shot_settings_update_statement = bpm_statement + "Bypassing shot settings update"


# project datas statements
startup_statement = bpm_statement + "Looking for project datas"
loaded_datas_statement = bpm_statement + "Project datas loaded"
loaded_folders_statement = bpm_statement + "Project folders loaded"
no_datas_statement = bpm_statement + "Datas not found"
loading_statement = bpm_statement + "Datas found, loading from "
folders_loading_statement = bpm_statement + "Project folders found, loading from "
currently_loading_statement = bpm_statement + "Currently loading "

reading_json_statement = bpm_statement + "Reading datas from json file : "
initialize_json_statement = bpm_statement + "Initializing json : "

saving_to_json_statement = bpm_statement + "Saving to json"
saved_to_json_statement = bpm_statement + "Successfully saved to json"

adding_dataset_to_json = bpm_statement + "Adding dataset to json : "

setting_prop_statement = bpm_statement + "Setting property : "
setting_prop_error_statement = bpm_statement + "Unable to set property : "
prop_avoided_statement = bpm_statement + "Property avoided : "

library_cleared_statement = bpm_statement + "Cleaned library from user, reload file to delete it : "
checking_unused_libraries_statement = bpm_statement + "Checking unused libraries"

starting_empty_recycle_bin_statement = bpm_statement + "Emptying recycle bin"
empty_recycle_bin_completed_statement = bpm_statement + "Recycle bin successfully emptied"

scene_not_found_message = "Scene not found : "
scene_not_found_statement = bpm_statement + scene_not_found_message

starting_audio_sync_file_statement = bpm_statement + "Starting creation of audio sync file"
audio_sync_file_created_statement = bpm_statement + "Audio synchronization file successfully created"

starting_shot_audio_sync_statement = bpm_statement + "Audio synchronization started"
shot_audio_synced_statement = bpm_statement + "Shot audio successfully synchronized"
sync_file_not_found_message = "Audio synchronization file not found"
sync_file_not_found_statement = bpm_statement + sync_file_not_found_message

render_settings_loading_statement = bpm_statement + "Render settings loading from : "
render_settings_loaded_statement = bpm_statement + "Render settings successfully loaded"
missing_render_file_statement = bpm_statement + "Render settings file missing"

setting_render_statement = bpm_statement + "Setting render"
render_set_statement = bpm_statement + "Render set"


# python scripts statement
creating_python_script_statement = bpm_statement + "Creating python script : "
python_script_created_statement = bpm_statement + "Python script successfully created"
launching_command_statement = bpm_statement + "Launching command : "


# files operation statements
deleted_file_statement = bpm_statement + "File successfully deleted : "
scenes_linked_statement = bpm_statement + "Scenes linked from : "
folder_created_statement = bpm_statement + "Folder created : "
starting_moving_folder = bpm_statement + "Moving folder : "
moved_folder_statement = bpm_statement + "Folder successfully moved"
starting_deleting_folder = bpm_statement + "Deleting folder : "
deleted_folder_statement = bpm_statement + "Folder successfully deleted"
emptying_folder_statement = bpm_statement + "Emptying folder : "
folder_emptied_statement = bpm_statement + "Folder successfully emptied"
copying_file_statement = bpm_statement + "Copying file from : "
file_does_not_exist_message = "File does not exist : "
file_does_not_exist_statement = bpm_statement + file_does_not_exist_message


# timeline statements
no_available_timeline_space_message = "No available space on timeline"
no_available_timeline_space_statement = bpm_statement + no_available_timeline_space_message
checking_available_timeline_space_statement = bpm_statement + "Checking on timeline for available space"
linked_to_strip_statement = bpm_statement + "Linking to strip : "
creating_sequencer_statement = bpm_statement + "Creating scene sequence editor"
cleaning_timeline_statement = bpm_statement + "Removing existing strips"
shot_not_used_message = "Shot not used in project timeline"
shot_not_used_statement = bpm_statement + shot_not_used_message
loaded_sounds_statement = bpm_statement + "Sounds loaded : "
created_sound_strips_statement = bpm_statement + "Created sound strips : "
refreshing_timeline_shot_datas_statement = bpm_statement + "Refreshing timeline shots datas from files"
refreshed_timeline_shot_datas_statement = bpm_statement + "Timeline shots datas refreshed"


# shot update statement
start_update_shot_statement = bpm_statement + "Starting update shot(s) from timeline"
checking_update_shot_statement  = bpm_statement + "Checking strip for needed update : "
updating_shot_statement = bpm_statement + "Update needed, starting"
update_shot_new_start_end_statement = bpm_statement + "Strip new start-end : "
updated_shot_statement = bpm_statement + "Strip successfully updated"
no_update_needed_statement = bpm_statement + "No update needed"
shot_update_impossible_message = "Impossible to update shot (negative shot start frame)"
shot_update_impossible_statement = bpm_statement + shot_update_impossible_message

shot_loading_statement = bpm_statement + "Loading shot settings from : "
shot_loaded_statement = bpm_statement + "Shot settings loaded"
missing_shot_file_message = "Shot settings file missing"
missing_shot_file_statement = bpm_statement + missing_shot_file_message


# marker statements
start_edit_shot_marker_statement = bpm_statement + "Starting editing shot marker"
editing_shot_marker_statement = bpm_statement + "Editing shot marker : "
edited_shot_marker_statement= bpm_statement + "Shot marker successfully edited"


# extra ui statements
add_extra_ui_statement = bpm_statement + "Sequencer UI handler added"
remove_extra_ui_statement = bpm_statement + "Sequencer UI handler removed"
load_font_statement = bpm_statement + "External font loaded : "
unload_font_statement = bpm_statement + "External font unloaded : "


# asset statements
creating_asset_statement = bpm_statement + "Creating new asset : "
asset_created_statement = bpm_statement + "Asset successfully created : "
dupe_asset_name_message = "Asset name already exists"
dupe_asset_name_statement = bpm_statement + dupe_asset_name_message
assets_loading_statement = bpm_statement + "Loading assets from : "
assets_loaded_statement = bpm_statement + "Assets loaded"
cleared_old_asset_statement = bpm_statement + "Old asset cleared"
set_asset_statement = bpm_statement + "Asset set to : "
importing_asset_statement = bpm_statement + "Importing asset : "
asset_not_existing_message = "Asset not existing : "
asset_not_existing_statement = bpm_statement + asset_not_existing_message
asset_file_not_found_message = "Asset file not found : "
asset_file_not_found_statement = bpm_statement + asset_file_not_found_message
asset_imported_statement = bpm_statement + "Asset successfully imported"
asset_linked_statement = bpm_statement + "Asset linked : "
asset_file_creation_statement = bpm_statement + "Asset file creation : "
assets_settings_loading_statement = bpm_statement + "Loading asset settings"
assets_settings_loaded_statement = bpm_statement + "Asset settings successfully loaded"
asset_missing_in_list_statement = bpm_statement + "Asset not found in project asset list"


# help statements
opening_web_page_statement = bpm_statement + "Opening web page : "


### FILES AND PATHS ###

file_project = "project_data.json"
asset_file = "project_assets.json"
custom_folders_file = "project_custom_folders.json"
audio_sync_file = "project_audio_sync.json"
shot_file = "shot_settings.json"
render_file = "render_settings.json"

python_temp = "python_temp.py"

script_file = os.path.realpath(__file__)
setup_script_folder = os.path.join(os.path.dirname(script_file), "setup_blend_scripts")
shot_setup_file = os.path.join(setup_script_folder, "shot_setup_command.py")
update_shot_file = os.path.join(setup_script_folder, "update_shot_command.py")
add_modify_marker_file = os.path.join(setup_script_folder, "add_modify_marker_command.py")

ressources_folder = os.path.join(os.path.dirname(script_file), "ressources")
font_file = os.path.join(ressources_folder, "JetBrainsMono-Regular.ttf")

base_startup_filepath = os.path.join(ressources_folder, "blank.blend")

new_project_name = "Project_name"

asset_folder = "01_assets"
shot_folder = "02_shots"
render_folder = "03_renders"
render_shots_folder = "01_shots"
render_dailies_folder = "02_dailies"
render_draft_folder = "01_draft"
render_render_folder = "02_render"
render_final_folder = "03_final"
ressources_folder = "04_ressources"
old_folder = "zz_old"

startup_files_folder = "01_startup_files"
shot_startup_file = "blank_shot.blend"
asset_startup_file = "blank_asset.blend"


### WEB ###

wiki_url = "https://github.com/samytichadou/blender_project_manager/wiki/"