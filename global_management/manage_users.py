import bpy
import base64
import os
from bpy.app.handlers import persistent

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
        "name"                   : "admin",
        "password"               : encode("admin"),
        "ath_user_create"        : 1,
        "ath_user_modify"        : 1,
        "ath_project_create"     : 1,
        "ath_project_modify"     : 1,
        "ath_episode_create"     : 1,
        "ath_episode_modify"     : 1,
        "ath_shot_create"        : 1,
        "ath_shot_modify"        : 1,
        "ath_storyboard_create"  : 1,
        "ath_storyboard_modify"  : 1,
        "ath_render_create"      : 1,
        "ath_render_modify"      : 1,
        "ath_compositing_create" : 1,
        "ath_compositing_modify" : 1,
        "ath_asset_create"       : 1,
        "ath_asset_modify"       : 1,
        "ath_planning_create"    : 1,
        "ath_planning_modify"    : 1,
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

        prop_prefs.logged_user = prop_prefs.athcode = ""

        self.report({'INFO'}, "User Logged Out")

        # Refresh
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


class BPM_OT_create_user(bpy.types.Operator, ua.BPM_user_authorizations):
    bl_idname = "bpm.create_user"
    bl_label = "Create User"
    bl_description = "Create new BPM user"
    bl_options = {"INTERNAL", "UNDO"}

    name : bpy.props.StringProperty(
        name = "Name",
        )
    password : bpy.props.StringProperty(
        name = "Password",
        subtype = "PASSWORD",
        )
    password_confirm : bpy.props.StringProperty(
        name = "Confirm",
        subtype = "PASSWORD",
        )
    datas = None

    @classmethod
    def poll(cls, context):
        return ua.compare_athcode(
            ua.patt_user_creation,
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        self.datas = return_users_datas()
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)

        row = col.row()
        row.prop(self, "name")
        icon = "CHECKMARK"
        for user in self.datas["users"]:
            if self.name == user["name"]:
                icon = "ERROR"
                break
        if not self.name:
            icon = "ERROR"
        row.label(text = "", icon = icon,)

        row = col.row()
        row.prop(self, "password")
        icon = "ERROR"
        if self.password:
            icon = "CHECKMARK"
        row.label(text = "", icon = icon)

        row = col.row()
        row.prop(self, "password_confirm")
        icon = "ERROR"
        if self.password and self.password == self.password_confirm:
            icon = "CHECKMARK"
        row.label(text = "", icon = icon)

        box = layout.box()
        box.label(text = "User Authorizations")
        col = box.column(align = True)
        idx = 0
        for p in ua.ath_list:
            if (idx % 2) == 0:
                row = col.row()
            row.prop(self, p)
            idx += 1

    def execute(self, context):
        # Check for name availability
        if not self.name:
            self.report({'WARNING'}, "Name is mandatory")
            return {'FINISHED'}
        for user in self.datas["users"]:
            if self.name == user["name"]:
                self.report({'WARNING'}, "Name not available")
                return {'FINISHED'}

        # Check for password
        if not self.password or self.password != self.password_confirm:
            self.report({'WARNING'}, "Invalid password")
            return {'FINISHED'}

        # Create dataset
        user_datas = {}
        user_datas["name"] = self.name
        user_datas["password"] = encode(self.password)
        for p in ua.ath_list:
            user_datas[p] = int(getattr(self, p))

        # Write dataset
        self.datas["users"].append(user_datas)
        print("BPM --- Writing users json")
        mp.write_json_file(self.datas, return_users_file())

        self.name = self.password = self.password_confirm = ""

        self.report({'INFO'}, f"User {self.name} Added")

        return {'FINISHED'}


def user_callback(scene, context):
    items = []
    datas = return_users_datas()
    for user in datas["users"]:
        items.append((user["name"], user["name"], ""))
    return items

class BPM_OT_remove_user(bpy.types.Operator):
    bl_idname = "bpm.remove_user"
    bl_label = "Remove User"
    bl_description = "Remove BPM user"
    bl_options = {"INTERNAL", "UNDO"}

    user : bpy.props.EnumProperty(
        name = "User",
        items = user_callback
        )

    @classmethod
    def poll(cls, context):
        return ua.compare_athcode(
            ua.patt_user_creation,
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "user", text = "")
        layout.label(text = "Are you sure ?", icon = "ERROR")

    def execute(self, context):
        datas = return_users_datas()
        old_name = self.user

        chk_user = False
        for user in datas["users"]:
            if old_name == user["name"]:
                self.report({'WARNING'}, "Name not available")
                datas["users"].remove(user)
                self.user = datas["users"][0]["name"]
                chk_user = True
                break

        if not chk_user:
            self.report({'WARNING'}, "Invalid User name")
            return {'FINISHED'}

        # Log out if needed
        prop_prefs = ap.getAddon().preferences
        if prop_prefs.logged_user == old_name:
            print("BPM --- Log out removed user")
            prop_prefs.logged_user = prop_prefs.athcode = ""
            # Refresh
            for area in context.screen.areas:
                area.tag_redraw()
        print("BPM --- Writing users json")
        mp.write_json_file(datas, return_users_file())

        self.report({'INFO'}, f"User {old_name} Removed")

        return {'FINISHED'}


class BPM_OT_modify_user(bpy.types.Operator):
    bl_idname = "bpm.modify_user"
    bl_label = "Modify User"
    bl_description = "Modify BPM user"
    bl_options = {"INTERNAL", "UNDO"}

    user : bpy.props.EnumProperty(
        name = "User",
        items = user_callback
        )

    @classmethod
    def poll(cls, context):
        return ua.compare_athcode(
            ua.patt_user_modification,
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "user", text = "")
        layout.label(text = "Are you sure ?", icon = "ERROR")

    def execute(self, context):
        datas = return_users_datas()
        old_name = self.user

        chk_user = False
        for user in datas["users"]:
            if old_name == user["name"]:
                self.report({'WARNING'}, "Name not available")
                datas["users"].remove(user)
                self.user = datas["users"][0]["name"]
                chk_user = True
                break

        if not chk_user:
            self.report({'WARNING'}, "Invalid User name")
            return {'FINISHED'}

        # Log out if needed
        prop_prefs = ap.getAddon().preferences
        if prop_prefs.logged_user == old_name:
            print("BPM --- Log out removed user")
            prop_prefs.logged_user = prop_prefs.athcode = ""
            # Refresh
            for area in context.screen.areas:
                area.tag_redraw()
        print("BPM --- Writing users json")
        mp.write_json_file(datas, return_users_file())

        self.report({'INFO'}, f"User {old_name} Removed")

        return {'FINISHED'}

@persistent
def users_load_handler(scene):
    print("BPM --- Checking valid login")
    prop_prefs = ap.getAddon().preferences
    if not prop_prefs.logged_user:
        print("BPM --- Not logged")
        return
    datas = return_users_datas()
    for user in datas["users"]:
        if user["name"] == prop_prefs.logged_user:
            print("BPM --- Valid login found")
            return
    prop_prefs.logged_user = prop_prefs.athcode = ""
    print("BPM --- No valid login found, logged out")


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_user_login)
    bpy.utils.register_class(BPM_OT_user_logout)
    bpy.utils.register_class(BPM_OT_create_user)
    bpy.utils.register_class(BPM_OT_remove_user)
    bpy.app.handlers.load_post.append(users_load_handler)
def unregister():
    bpy.utils.unregister_class(BPM_OT_user_login)
    bpy.utils.unregister_class(BPM_OT_user_logout)
    bpy.utils.unregister_class(BPM_OT_create_user)
    bpy.utils.unregister_class(BPM_OT_remove_user)
    bpy.app.handlers.load_post.remove(users_load_handler)
