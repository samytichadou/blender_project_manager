import bpy
import base64
import os

from .. import addon_prefs as ap
from . import manage_projects as mp
from . import user_authorization as ua

def encode(text):
    return str(base64.b64encode(text.encode("utf-8")), 'utf-8')

def decode(text):
    return base64.b64decode(text).decode("utf-8")

def return_users_file(name="bpm_users.json"):
    return os.path.join(mp.return_global_preferences_folder(), name)

def return_users_datas():
    path = return_users_file()
    if os.path.isfile(path):
        return mp.read_json(path)
    else:
        datas = init_admin_user()
        mp.write_json_file(datas, path)
        return datas

def init_admin_user():
    datas = {}
    datas["users"] = []
    user = {
        "name"                 : "admin",
        "password"             : encode("admin"),
        "ath_project_create"   : 1,
        "ath_project_modify"   : 1,
        "ath_episode_create"   : 1,
        "ath_episode_modify"   : 1,
        "ath_shot_create"      : 1,
        "ath_shot_modify"      : 1,
        "ath_storyboard_create": 1,
        "ath_storyboard_modify": 1,
        "ath_render_create"    : 1,
        "ath_render_modify"    : 1,
        "ath_asset_create"     : 1,
        "ath_asset_modify"     : 1,
        "ath_planning_create"  : 1,
        "ath_planning_modify"  : 1,
        }
    datas["users"].append(user)
    return datas


class BPM_OT_user_login(bpy.types.Operator):
    bl_idname = "bpm.user_login"
    bl_label = "Login"
    bl_description = "Log user"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        prefs = ap.getAddonPreferences()
        return prefs.user_temp and prefs.password_temp

    def execute(self, context):
        prefs = ap.getAddonPreferences()
        prop_prefs = ap.getAddon().preferences

        datas = return_users_datas()

        chk_user = False
        for user in datas["users"]:
            if user["name"] == prefs.user_temp:
                password = user["password"]
                print(password)
                if decode(str(password)) == prefs.password_temp:
                    prop_prefs.logged_user = prefs.user_temp
                    prop_prefs.athcode = ua.get_athcode_from_dict(user)
                    chk_user = True
                    break

        if chk_user:
            self.report({'INFO'}, f"{prefs.user_temp} Logged")
            # Reset user fields
            print("BPM --- Cleaning temporaries user fields")
            prop_prefs.user_temp = ""
            prop_prefs.password_temp = ""
        else:
            self.report({'WARNING'}, "Invalid Username/Password")

        # Refresh
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


class BPM_OT_user_logout(bpy.types.Operator):
    bl_idname = "bpm.user_logout"
    bl_label = "Logout"
    bl_description = "Logout user"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        prefs = ap.getAddonPreferences()
        return prefs.logged_user

    def execute(self, context):
        prop_prefs = ap.getAddon().preferences

        prop_prefs.logged_user = ""
        prop_prefs.athcode = ""

        self.report({'INFO'}, "User Logged Out")

        # Refresh
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_user_login)
    bpy.utils.register_class(BPM_OT_user_logout)
def unregister():
    bpy.utils.unregister_class(BPM_OT_user_login)
    bpy.utils.unregister_class(BPM_OT_user_logout)
