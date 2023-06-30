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
            print(f"BPM --- {user} found for this project, settings authorizations")
            return True

    # If user not in this project, set authorizations
    print(f"BPM --- {prop_prefs.logged_user} not found for this project, settings authorizations")
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

### REGISTER ---
def register():
    bpy.app.handlers.load_post.append(project_users_cleaning_handler)
    bpy.app.handlers.load_post.append(project_users_load_handler)
def unregister():
    bpy.app.handlers.load_post.remove(project_users_cleaning_handler)
    bpy.app.handlers.load_post.remove(project_users_load_handler)
