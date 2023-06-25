import bpy
import base64
import os
from bpy.app.handlers import persistent

from .. import addon_prefs as ap
from . import manage_projects as mp
from . import user_authorization as ua
from . import naming_convention as nc
from ..project_management import project_users as pu

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

def login_check_athcode(name, password, datas):
    for user in datas["users"]:
        if user["name"] == name:
            if user["password"] == password:
                return ua.get_athcode_from_dict(user)
    return None

def login(name, password):
    datas = return_users_datas()
    prop_prefs = ap.getAddon().preferences
    athcode = login_check_athcode(name, encode(password), datas)
    if athcode is not None:
        prop_prefs.logged_user = name
        prop_prefs.athcode = athcode
        print(f"BPM --- {name} Logged in")
        # Reset user fields
        print("BPM --- Cleaning temporaries user fields")
        prop_prefs.user_temp = prop_prefs.password_temp = ""
        return True

    print(f"BPM --- Invalid Username/Password")
    return False

def logout():
    prop_prefs = ap.getAddon().preferences
    prop_prefs.logged_user = prop_prefs.athcode = ""
    print("BPM --- User Logged Out")

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

        if login(prefs.user_temp, prefs.password_temp):
            # Reload project user authorizations
            pu.update_project_user_authorizations()
            self.report({'INFO'}, f"{prefs.user_temp} Logged")
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
        logout()
        self.report({'INFO'}, "User Logged Out")

        # Refresh
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


def draw_create_username_password(container, self, datas):
    col = container.column(align = True)
    row = col.row()
    row.prop(self, "name")
    icon = "CHECKMARK"
    for user in datas["users"]:
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

def draw_user_authorization_list(container, self, ath_list):
    box = container.box()
    box.label(text = "User Authorizations")
    col = box.column(align = True)
    idx = 0
    for p in ath_list:
        if (idx % 2) == 0:
            row = col.row()
        row.prop(self, p)
        idx += 1

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
        draw_create_username_password(layout, self, self.datas)
        draw_user_authorization_list(layout, self, ua.ath_list)

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
        items = user_callback,
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
                datas["users"].remove(user)
                self.user = datas["users"][0]["name"]
                chk_user = True
                break

        if not chk_user:
            self.report({'WARNING'}, "Invalid User selection")
            return {'FINISHED'}

        # Log out if needed
        prop_prefs = ap.getAddon().preferences
        if prop_prefs.logged_user == old_name:
            logout()
            for area in context.screen.areas:
                area.tag_redraw()
        print("BPM --- Writing users json")
        mp.write_json_file(datas, return_users_file())

        self.report({'INFO'}, f"User {old_name} Removed")

        return {'FINISHED'}

def modify_user_callback(self, context):
    print("BPM --- Updating user infos")
    datas = return_users_datas()
    for user in datas["users"]:
        if self.user == user["name"]:
            for k in user:
                if k.startswith("ath_"):
                    setattr(self, k, user[k])
            break

class BPM_OT_modify_user(bpy.types.Operator, ua.BPM_user_authorizations):
    bl_idname = "bpm.modify_user"
    bl_label = "Modify User"
    bl_description = "Modify BPM user"
    bl_options = {"INTERNAL", "UNDO"}

    user : bpy.props.EnumProperty(
        name = "User",
        items = user_callback,
        update = modify_user_callback,
        )
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
            ua.patt_user_modification,
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        self.datas = return_users_datas()
        self.user = self.datas["users"][0]["name"]
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "user", text = "")
        layout.label(text = "Fill to change :")
        draw_create_username_password(layout, self, self.datas)
        draw_user_authorization_list(layout, self, ua.ath_list)

        layout.label(text = "Are you sure ?", icon = "ERROR")

    def execute(self, context):
        datas = return_users_datas()

        # Check user to modify
        chk_user = False
        for user in self.datas["users"]:
            if self.user == user["name"]:
                old_user = user
                old_name = user["name"]
                self.datas["users"].remove(user)
                chk_user = True
                break

        if not chk_user:
            self.report({'WARNING'}, "Invalid User selection")
            return {'FINISHED'}

        # Check new user name
        chk_new_name = False
        if self.name:
            chk_new_name = True
            for user in self.datas["users"]:
                if self.name == user["name"]:
                    self.report({'WARNING'}, "Name not available")
                    return {'FINISHED'}

        # Check new user password
        chk_new_password = False
        if self.password:
            chk_new_password = True
            if self.password != self.password_confirm:
                self.report({'WARNING'}, "Invalid password")
                return {'FINISHED'}

        # Build new dataset
        user_datas = {}
        if chk_new_name:
            user_datas["name"] = self.name
        else:
            user_datas["name"] = old_user["name"]
        if chk_new_password:
            user_datas["password"] = encode(self.password)
        else:
            user_datas["password"] = old_user["password"]
        for p in ua.ath_list:
            user_datas[p] = int(getattr(self, p))

        # Write dataset
        self.datas["users"].append(user_datas)
        print("BPM --- Writing users json")
        mp.write_json_file(self.datas, return_users_file())

        # Relog if needed
        prop_prefs = ap.getAddon().preferences
        if prop_prefs.logged_user == old_user["name"]:
            print("BPM --- Relog modified user")
            prop_prefs.logged_user = user_datas["name"]
            prop_prefs.athcode = ua.get_athcode_from_dict(user_datas)
            # Refresh
            for area in context.screen.areas:
                area.tag_redraw()

        self.user = datas["users"][0]["name"]
        self.name = self.password = self.password_confirm = ""
        self.report({'INFO'}, f"User {old_name} Modified")

        return {'FINISHED'}

def return_project_users(name):
    root_folder = None
    for project in bpy.context.window_manager["bpm_global_projects"]["projects"]:
        if project["name"] == name:
            root_folder = project["root_folder"]
            break
    if root_folder is not None:
        user_list = []
        user_folder = os.path.join(root_folder, nc.users_folder)
        for filename in os.listdir(user_folder):
            user_list.append(filename.split(".json")[0])
        return user_list

def return_project_users_folder(name):
    root_folder = None
    for project in bpy.context.window_manager["bpm_global_projects"]["projects"]:
        if project["name"] == name:
            root_folder = project["root_folder"]
            break
    if root_folder is not None:
        user_list = []
        user_folder = os.path.join(root_folder, nc.users_folder)
        return user_folder

def return_project_user_dataset(global_user):
    dataset = {}
    for k in global_user:
        if k.startswith("ath_"):
            dataset[k] = global_user[k]
    return dataset

class BPM_OT_add_remove_user_to_project(bpy.types.Operator, ua.BPM_user_authorizations):
    bl_idname = "bpm.add_remove_user_to_project"
    bl_label = "Add/Remove User"
    bl_description = "Add/Remove BPM user to selected project"
    bl_options = {"INTERNAL"}

    remove : bpy.props.BoolProperty(default=False)
    user_name : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return ua.compare_athcode(
            "x1x1xxxxxxxxxxxx",
            ap.getAddonPreferences().athcode
            )

    def execute(self, context):
        wm = context.window_manager

        global_users = []
        for user in wm["temporary_global_users"]:
            global_users.append(user)

        project_users = []
        for user in wm["temporary_project_users"]:
            project_users.append(user)

        if not self.remove:
            if self.user_name not in project_users:
                project_users.append(self.user_name)
        else:
            if self.user_name in project_users:
                project_users.remove(self.user_name)

        wm["temporary_project_users"] = project_users

        return {'FINISHED'}


class BPM_OT_manage_project_users(bpy.types.Operator, ua.BPM_user_authorizations):
    bl_idname = "bpm.manage_project_users"
    bl_label = "Manage Users"
    bl_description = "Manage BPM users for selected project"
    bl_options = {"INTERNAL", "UNDO"}

    project_name : bpy.props.StringProperty()
    global_users_datas = None

    @classmethod
    def poll(cls, context):
        return ua.compare_athcode(
            "x1x1xxxxxxxxxxxx",
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        wm = context.window_manager
        self.global_users_datas = return_users_datas()

        user_list = []
        for user in self.global_users_datas["users"]:
            user_list.append(user["name"])
        wm["temporary_global_users"] = user_list

        wm["temporary_project_users"] = return_project_users(self.project_name)

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        split = layout.split()
        col1 = split.column(align = True)
        col2 = split.column(align = True)

        box = col1.box()
        box.label(text = "Global Users")
        box = col2.box()
        box.label(text = "Project Users")

        box1 = col1.box()
        box2 = col2.box()

        # TODO use ui_list to allow authorizations change

        for user in wm["temporary_global_users"]:
            if user not in wm["temporary_project_users"]:
                row = box1.row()
                row.label(text = user)
                op = row.operator(
                    "bpm.add_remove_user_to_project",
                    text = "",
                    icon = "TRIA_RIGHT",
                    )
                op.remove = False
                op.user_name = user
        for user in wm["temporary_project_users"]:
            row = box2.row()
            #row.label(text = "", icon = "TRIA_LEFT")
            op = row.operator(
                "bpm.add_remove_user_to_project",
                text = "",
                icon = "TRIA_LEFT",
                )
            op.remove = True
            op.user_name = user
            row.label(text = user)

    def execute(self, context):
        wm = context.window_manager

        # Create or remove user file for project
        project_users = return_project_users(self.project_name)

        # Add missing project users
        for user in wm["temporary_project_users"]:
            if user not in project_users:
                # Create json
                filepath = os.path.join(
                    return_project_users_folder(self.project_name),
                    f"{user}.json",
                    )
                for u in self.global_users_datas["users"]:
                    if u["name"] == user:
                        global_user_datas = u
                        break
                user_dataset = return_project_user_dataset(global_user_datas)
                mp.write_json_file(user_dataset, filepath)
                print(f"BPM --- Added : {user} to project")

        # Remove project users
        for user in project_users:
            if user not in wm["temporary_project_users"]:
                # Remove json
                filepath = os.path.join(
                    return_project_users_folder(self.project_name),
                    f"{user}.json",
                    )
                os.remove(filepath)
                print(f"BPM --- Removed : {user} from project")

        # Remove temp datas
        del wm["temporary_global_users"]
        del wm["temporary_project_users"]

        # Reload project user authorizations
        pu.update_project_user_authorizations()

        self.report({'INFO'}, "Project Users Modified")

        return {'FINISHED'}

def refresh_login():
    print("BPM --- Checking valid login")
    prop_prefs = ap.getAddon().preferences
    if not prop_prefs.logged_user:
        print("BPM --- Not logged")
        return
    datas = return_users_datas()
    for user in datas["users"]:
        if user["name"] == prop_prefs.logged_user:
            print("BPM --- Valid login found")
            print("BPM --- Refresh authorizations")
            prop_prefs.athcode = ua.get_athcode_from_dict(user)
            return
    print("BPM --- No valid login found")
    logout()

@persistent
def users_load_handler(scene):
    refresh_login()


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_user_login)
    bpy.utils.register_class(BPM_OT_user_logout)
    bpy.utils.register_class(BPM_OT_create_user)
    bpy.utils.register_class(BPM_OT_remove_user)
    bpy.utils.register_class(BPM_OT_modify_user)
    bpy.utils.register_class(BPM_OT_add_remove_user_to_project)
    bpy.utils.register_class(BPM_OT_manage_project_users)
    bpy.app.handlers.load_post.append(users_load_handler)
def unregister():
    bpy.utils.unregister_class(BPM_OT_user_login)
    bpy.utils.unregister_class(BPM_OT_user_logout)
    bpy.utils.unregister_class(BPM_OT_create_user)
    bpy.utils.unregister_class(BPM_OT_remove_user)
    bpy.utils.unregister_class(BPM_OT_modify_user)
    bpy.utils.unregister_class(BPM_OT_add_remove_user_to_project)
    bpy.utils.unregister_class(BPM_OT_manage_project_users)
    bpy.app.handlers.load_post.remove(users_load_handler)
