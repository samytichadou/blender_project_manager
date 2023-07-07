import bpy
import os
from bpy.app.handlers import persistent

from ..global_management import naming_convention as nc
from ..global_management import user_authorization as ua
from ..global_management import manage_projects as mp
from ..global_management import manage_users as mu
from .. import addon_prefs as ap

def update_project_user_authorizations():
    prop_prefs = ap.getAddon().preferences

    # Check if user logged
    if not prop_prefs.logged_user:
        return False

    # Check if bpm project
    try:
        project_datas = bpy.context.window_manager["bpm_project_datas"]
    except KeyError:
        return False

    # Check if logged user is a project user
    user_folder = os.path.join(project_datas["root_folder"], nc.users_folder)
    for filename in os.listdir(user_folder):
        user = filename.split(".json")[0]
        if user == prop_prefs.logged_user:
            # Get project authorizations
            user_datas = mp.read_json(os.path.join(user_folder, filename))
            prop_prefs.athcode = ua.get_athcode_from_dict(user_datas)
            print(f"BPM --- User : {user} found for this project, settings authorizations")
            return True

    # If user not in this project, set authorizations
    print(f"BPM --- User : {prop_prefs.logged_user} not found for this project, settings authorizations")
    prop_prefs.athcode = "0000000000000000"
    return False

def remove_old_project_user():
    # Check if bpm project
    try:
        project_datas = bpy.context.window_manager["bpm_project_datas"]
    except KeyError:
        return False

    print("BPM --- Cleaning old project users")

    users_datas = mu.return_users_datas()
    project_users = mu.return_project_users(project_datas["name"])
    for user in project_users:
        # Check if global user exists
        chk_user = False
        for g_user in users_datas["users"]:
            if g_user["name"] == user:
                chk_user = True
                break
        if chk_user:
            continue

        filepath = mu.return_project_user_filepath(user)
        if filepath is not None:
            os.remove(filepath)
            print(f"BPM --- Old user : {user} removed")
    return True

@persistent
def project_users_load_handler(scene):
    update_project_user_authorizations()

@persistent
def project_users_cleaning_handler(scene):
    remove_old_project_user()

@persistent
def save_last_file_user_handler(scene):
    scn = bpy.context.scene
    user = ap.getAddonPreferences().logged_user
    if user:
        print("BPM --- Saving last user")
        scn["bpm_last_user"] = user

@persistent
def project_setup_last_user_handler(scene):
    # Check if bpm project
    bpm_project = True
    try:
        project_datas = bpy.context.window_manager["bpm_project_datas"]
    except KeyError:
        bpm_project = False

    # Look for existing handler
    for handler in bpy.app.handlers.save_pre:
        if "save_last_file_user_handler"==handler.__name__:
            if not bpm_project:
                print("BPM --- Removing save handler")
                bpy.app.handlers.save_pre.remove(save_last_file_user_handler)
            else:
                print("BPM --- Existing save handler found")
            return False

    # Setup save handler
    print("BPM --- Setting up save handler")
    bpy.app.handlers.save_pre.append(save_last_file_user_handler)

### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(project_users_cleaning_handler)
    bpy.app.handlers.load_post.append(project_users_load_handler)
    bpy.app.handlers.load_post.append(project_setup_last_user_handler)
def unregister():
    bpy.app.handlers.load_post.remove(project_users_cleaning_handler)
    bpy.app.handlers.load_post.remove(project_users_load_handler)
    bpy.app.handlers.load_post.remove(project_setup_last_user_handler)
