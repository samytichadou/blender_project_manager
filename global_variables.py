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


# project datas statements
startup_statement = bpm_statement + "Looking for project datas"
loaded_datas_statement = bpm_statement + "Project datas loaded"
loaded_folders_statement = bpm_statement + "Project folders loaded"
no_custom_folder_file_statement = bpm_statement + "No custom project folder file found"
no_datas_statement = bpm_statement + "Datas not found"
loading_statement = bpm_statement + "Datas found, loading from "
currently_loading_statement = bpm_statement + "Currently loading "

custom_folder_not_selected_message = "Custom folder not selected"
unable_to_move_custom_folder_message = "Unable to move custom folder in this direction"
custom_folder_not_found_statement = bpm_statement + "Custom folder path not found"

custom_folder_added_statement = bpm_statement + "Custom folder added"
custom_folder_moved_statement = bpm_statement + "Custom folder moved"

reading_json_statement = bpm_statement + "Reading datas from json file : "
initialize_json_statement = bpm_statement + "Initializing json : "

saving_to_json_statement = bpm_statement + "Saving to json"
saved_to_json_statement = bpm_statement + "Successfully saved to json"

adding_dataset_to_json = bpm_statement + "Adding dataset to json : "

setting_prop_statement = bpm_statement + "Setting properties from "
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

setting_playblast_statement = bpm_statement + "Setting playblast render"
starting_playblast_statement = bpm_statement + "Starting playblast render"
playing_playblast_statement = bpm_statement + "Playing playblast render"
setting_usual_render_statement = bpm_statement + "Setting usual render back"
completed_playblast_statement = bpm_statement + "Playblast successfully rendered"

completed_render_statement = bpm_statement + "Render completed : "

strip_already_working_statement = bpm_statement + "Avoiding strip, already working : "

date_set_statement = bpm_statement + "Current date set"

bypass_settings_update_statement = bpm_statement + "Bypassing shot settings update"


# deadlines statements
shot_deadlines_modification_statement = bpm_statement + "Starting shot(s) deadlines modification"
deadlines_modified_statement = bpm_statement + "Deadlines modified for "


# python scripts statements
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

opening_folder_statement = bpm_statement + "Opening folder : "
no_folder_statement = bpm_statement + "Folder does not exist : "


# lock system
created_lock_file_statement = bpm_statement + "Lock file created"
deleted_lock_file_statement = bpm_statement + "Lock file deleted"
locked_file_statement = bpm_statement + "Project already opened, proceed with caution"
starting_clear_user_statement = bpm_statement + "Starting clear lock file user"
clearing_user_statement = bpm_statement + "Clearing lock file user : "


# timer statements
timer_function_added_statement = bpm_statement + "Timer function added"
timer_function_updated_statement = bpm_statement + "Timer function updated"
timer_function_removed_statement = bpm_statement + "Timer function removed"
timer_function_processing_statement = bpm_statement + "Timer function processing"


# thread statements
thread_start_statement = bpm_statement + "Starting new thread"
thread_end_statement = bpm_statement + "Thread ended"
thread_end_function_statement = bpm_statement + "Starting thread end function"
thread_error_statement = bpm_statement + "Error in thread, aborted"


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
created_strip_statement = bpm_statement + "Created strip : "
setting_strip_properties_statement = bpm_statement + "Setting strip properties"
setting_strip_display_mode_statement = bpm_statement + "Setting strip display to : "

refreshing_timeline_shot_datas_statement = bpm_statement + "Refreshing timeline shots datas from files"
refreshed_timeline_shot_datas_statement = bpm_statement + "Timeline shots datas refreshed"

refreshing_timeline_shot_display_mode = bpm_statement + "Refreshing timeline shots available display mode"
refreshed_timeline_shot_display_mode = bpm_statement + "Timeline shots available display mode refreshed"

no_active_shot_message = "No active shot"
no_active_shot_statement = bpm_statement + no_active_shot_message

lock_strip_message = "Locked strip"
lock_strip_statement = bpm_statement + lock_strip_message


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

shot_display_no_render_images_statement = bpm_statement + "No rendered images found, filling"
shot_display_render_images_statement = bpm_statement + "Rendered images found, deleting and filling"


# comment statements
start_edit_comment_statement = bpm_statement + "Starting editing comment"
editing_comment_statement = bpm_statement + "Editing comment : "
edited_comment_statement = bpm_statement + "Comment successfully edited"
removed_comment_statement = bpm_statement + "Comment successfully removed"
comment_file_updated_statement = bpm_statement + "Comment file updated"
loading_comments_statement = bpm_statement + "Loading comments"
no_comment_file_statement = bpm_statement + "Comment file not found : "
comment_reloaded_statement = bpm_statement + "Comments successfully reloaded"
getting_edit_comments_statement = bpm_statement + "Getting edit comments"
getting_shot_comments_statement = bpm_statement + "Getting shot comments"
getting_asset_comments_statement = bpm_statement + "Getting asset comments"
searching_comment_statement = bpm_statement + "Searching comment"
no_more_comments_message = "No more comments to jump to in this direction"


# extra ui statements
add_sequencer_extra_ui_statement = bpm_statement + "Sequencer UI handler added"
remove_sequencer_extra_ui_statement = bpm_statement + "Sequencer UI handler removed"
load_font_statement = bpm_statement + "External font loaded : "
unload_font_statement = bpm_statement + "External font unloaded : "
add_dopesheet_extra_ui_statement = bpm_statement + "Dope sheet handler added"
remove_shot_asset_extra_ui_statement = bpm_statement + "Dope sheet UI handler removed"


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
no_asset_json_file_statement = bpm_statement + "No existing asset json file"


# help statements
opening_web_page_statement = bpm_statement + "Opening web page : "


### FILES AND PATHS ###

file_project = "project_data.json"
asset_file = "project_assets.json"
custom_folders_file = "project_custom_folders.json"
audio_sync_file = "project_audio_sync.json"
shot_file = "shot_settings.json"
render_file = "render_settings.json"
comment_file = "comments.json"

python_temp = "python_temp.py"

script_file = os.path.realpath(__file__)
setup_script_folder = os.path.join(os.path.dirname(script_file), "setup_blend_scripts")
shot_setup_file = os.path.join(setup_script_folder, "shot_setup_command.py")
update_shot_file = os.path.join(setup_script_folder, "update_shot_command.py")
#add_modify_marker_file = os.path.join(setup_script_folder, "add_modify_marker_command.py")

ressources_folder = os.path.join(os.path.dirname(script_file), "ressources")
font_file = os.path.join(ressources_folder, "JetBrainsMono-Regular.ttf")

base_startup_filepath = os.path.join(ressources_folder, "blank.blend")

missing_file_image = os.path.join(ressources_folder, "missing_file_placeholder.exr")

#new_project_name = "Project_name"

asset_folder = "01_assets"
shot_folder = "02_shots"
render_folder = "03_renders"
render_shots_folder = "01_shots"
render_dailies_folder = "02_dailies"
render_playblast_folder = "00_playblast"
render_draft_folder = "01_draft"
render_render_folder = "02_render"
render_final_folder = "03_final"
ressources_folder = "04_ressources"
old_folder = "zz_old"

asset_ressources_folder = "00_asset_ressources"

startup_files_folder = "01_startup_files"
shot_startup_file = "blank_shot.blend"
asset_startup_file = "blank_asset.blend"

lockfile_extension = ".lck"
tempfile_extension = ".tmp"


### WEB ###

wiki_url = "https://github.com/samytichadou/blender_project_manager/wiki/"