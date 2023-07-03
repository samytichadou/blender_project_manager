import bpy
import os
import json
import shutil
import random
from bpy.app.handlers import persistent

from .. import addon_prefs as ap
from . import user_authorization as ua
from . import naming_convention as nc
from .. import constants

def generate_random():
    return(str(random.randrange(0,99999)).zfill(5))

def return_global_preferences_folder():
    folder=bpy.path.abspath(
        ap.getAddonPreferences().preferences_folder
        )
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder

def return_global_project_file(name="bpm_projects.json"):
    return os.path.join(return_global_preferences_folder(), name)

def read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset

def write_json_file(datas, path) :
    with open(path, "w") as write_file :
        json.dump(datas, write_file, indent=4, sort_keys=False)

def return_global_project_datas():
    path = return_global_project_file()
    if os.path.isfile(path):
        return read_json(path)
    else:
        datas = {}
        datas["projects"] = []
        return datas

def add_project_dataset(
    project_name,
    root_folder,
    first_ep,
    last_ep,
    ):
    print("BPM --- Creating project dataset")

    dataset = {}
    dataset["name"] = generate_random()
    dataset["project_name"] = project_name
    dataset["root_folder"] = root_folder
    dataset["project_info_file"] = return_project_infos_filepath(root_folder, project_name)
    dataset["episodes"] = []

    # Episodes folders and base files
    for i in range(first_ep, last_ep+1):
        pattern = return_episode_edit_pattern(project_name, i)
        edit_folder = os.path.join(root_folder, pattern)
        ep = {
            "number" : i,
            "identifier" : get_episode_identifier(project_name, i),
            "edit_folder" : edit_folder,
            }
        dataset["episodes"].append(ep)

    global_datas = return_global_project_datas()
    global_datas["projects"].append(dataset)

    print("BPM --- Writing global json")
    write_json_file(global_datas, return_global_project_file())
    return dataset

def create_hierarchy_folders(project_name, root_folder, first_ep, last_ep):
    print("BPM --- Creating project hierarchy")

    os.makedirs(root_folder)

    asset_folder = os.path.join(root_folder, nc.assets_folder)
    os.mkdir(asset_folder)
    os.mkdir(os.path.join(asset_folder, nc.asset_library_folder))

    os.mkdir(os.path.join(root_folder, nc.shots_folder))
    os.mkdir(os.path.join(root_folder, nc.renders_folder))
    os.mkdir(os.path.join(root_folder, nc.plannings_folder))
    os.mkdir(os.path.join(root_folder, nc.storyboards_folder))
    os.mkdir(os.path.join(root_folder, nc.scripts_folder))
    os.mkdir(os.path.join(root_folder, nc.startups_folder))
    os.mkdir(os.path.join(root_folder, nc.resources_folder))
    os.mkdir(os.path.join(root_folder, nc.locks_folder))
    os.mkdir(os.path.join(root_folder, nc.users_folder))

    edit_folder = os.path.join(root_folder, nc.edits_folder)
    os.mkdir(edit_folder)

    # Episodes folders and base files
    for i in range(first_ep, last_ep+1):
        pattern = return_episode_edit_pattern(project_name, i)
        edit_folder = os.path.join(edit_folder, pattern)
        edit_file = os.path.join(edit_folder, f"{pattern}_v001.blend")
        os.mkdir(edit_folder)
        shutil.copy(constants.episode_base_filepath, edit_file)

    copy_startup_files(root_folder)

def copy_startup_files(root_folder):
    startup_folder = os.path.join(root_folder, nc.startups_folder)

    shutil.copy(constants.episode_base_filepath, startup_folder)
    shutil.copy(constants.asset_base_filepath, startup_folder)


# TODO clean episode function to get ep file

def get_episode_identifier(project_name, number):
    return f"{project_name}_ep{str(number).zfill(3)}"

def intialize_project_infos_datas(
    uuid,
    project_name,
    framerate,
    resolution_x,
    resolution_y,
    first_ep,
    last_ep,
    root_folder,
    ):
    datas = {
        "name" : uuid,
        "project_name" : project_name,
        "framerate" : framerate,
        "resolution_x" : resolution_x,
        "resolution_y" : resolution_y,
        "root_folder" : root_folder,
        }
    datas["episodes"] = []
    for i in range(first_ep, last_ep+1):
        pattern = return_episode_edit_pattern(project_name, i)
        edit_folder = os.path.join(root_folder, nc.edits_folder)
        ep_folder = os.path.join(edit_folder, pattern)
        edit_file = os.path.join(ep_folder, f"{pattern}_v001.blend")
        ep = {
            "number" : i,
            "identifier" : get_episode_identifier(project_name, i),
            "edit_file" : edit_file,
            }
        datas["episodes"].append(ep)
    return datas

def return_episode_edit_pattern(project_name, ep_number):
    return f"{nc.edits_folder}_{get_episode_identifier(project_name, ep_number)}"

def return_project_infos_filepath(folder, name, pattern = "_projectinfos.json"):
    return os.path.join(folder, f"{name}{pattern}")

def create_project_infos_file(datas):
    path = return_project_infos_filepath(datas["root_folder"], datas["project_name"])
    write_json_file(datas, path)

def first_ep_callback(self, context):
    if self.no_update:
        return
    if self.first_episode > self.last_episode:
        self.no_update = True
        self.last_episode = self.first_episode
        self.no_update = False

def last_ep_callback(self, context):
    if self.first_episode > self.last_episode:
        self.no_update = True
        self.first_episode = self.last_episode
        self.no_update = False


class BPM_OT_create_project(bpy.types.Operator):
    bl_idname = "bpm.create_project"
    bl_label = "Create Project"
    bl_description = "Create a new BPM project"
    bl_options = {"INTERNAL", "UNDO"}

    framerate : bpy.props.IntProperty(
        name = "Framerate",
        default = 25,
        min = 1,
        max = 240,
        )
    resolution_x : bpy.props.IntProperty(
        name = "Resolution X",
        default = 1920,
        min = 1,
        )
    resolution_y : bpy.props.IntProperty(
        name = "Resolution Y",
        default = 1080,
        min = 1,
        )
    first_episode : bpy.props.IntProperty(
        name = "First Episode",
        default = 1,
        min = 0,
        update = first_ep_callback,
        )
    last_episode : bpy.props.IntProperty(
        name = "Last Episode",
        default = 1,
        min = 0,
        update = last_ep_callback,
        )
    no_update : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        if not ua.compare_athcode(
            ua.patt_project_creation,
            ap.getAddonPreferences().athcode,
            ):
            return False
        prefs = ap.getAddonPreferences()
        if prefs.new_project_name:
            path = bpy.path.abspath(prefs.new_project_folder)
            if os.path.isdir(path):
                return not os.path.isdir(os.path.join(path, prefs.new_project_name))

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "framerate")
        layout.prop(self, "resolution_x")
        layout.prop(self, "resolution_y")
        layout.prop(self, "first_episode")
        layout.prop(self, "last_episode")

    def execute(self, context):
        prefs = ap.getAddonPreferences()
        base_folder = bpy.path.abspath(prefs.new_project_folder)
        project_name = prefs.new_project_name
        root_folder = os.path.join(base_folder, project_name)

        if os.path.isdir(root_folder):
            self.report({'WARNING'}, "Project Folder already exists")
            return {'CANCELLED'}

        # Create hierarchy
        create_hierarchy_folders(
            project_name,
            root_folder,
            self.first_episode,
            self.last_episode,
            )

        # Add project to global json
        project_datas = add_project_dataset(
            project_name,
            root_folder,
            self.first_episode,
            self.last_episode,
            )

        # Create project info file
        datas = intialize_project_infos_datas(
            project_datas["name"],
            project_name,
            self.framerate,
            self.resolution_x,
            self.resolution_y,
            self.first_episode,
            self.last_episode,
            root_folder,
            )
        create_project_infos_file(datas)

        # Refresh project list
        reload_global_projects()

        # Refresh
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


def reload_global_projects():
    # TODO reload episode lists from projects
    print("BPM --- Refreshing global project list")

    dataset = return_global_project_datas()
    bpy.context.window_manager["bpm_global_projects"] = dataset

class BPM_OT_reload_global_projects(bpy.types.Operator):
    bl_idname = "bpm.reload_global_projects"
    bl_label = "Reload BPM Projects"
    bl_description = "Reload BPM Project list"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return os.path.isfile(return_global_project_file())

    def execute(self, context):
        reload_global_projects()

        self.report({'INFO'}, "BPM Project list refreshed")

        return {'FINISHED'}


class BPM_OT_remove_global_project(bpy.types.Operator):
    bl_idname = "bpm.remove_global_project"
    bl_label = "Remove BPM Project"
    bl_description = "Remove selected BPM project"
    bl_options = {"INTERNAL"}

    name : bpy.props.StringProperty()
    remove_folder : bpy.props.BoolProperty(
        name = "Also remove project content",
        )
    project_datas = None

    @classmethod
    def poll(cls, context):
        return ua.compare_athcode(
            ua.patt_project_creation,
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        for project in context.window_manager["bpm_global_projects"]["projects"]:
            if project["name"] == self.name:
                self.project_datas = project
                break
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        project_name = self.project_datas["project_name"]
        root_folder = self.project_datas["root_folder"]

        layout = self.layout
        layout.label(
            text = f"Removing {project_name}",
            icon = "ERROR",
            )
        layout.label(text = root_folder)
        layout.prop(self, "remove_folder")
        layout.label(text = "Are you sure ?")

    def execute(self, context):
        # Remove project from json
        datas = return_global_project_datas()
        for p in datas["projects"]:
            if p["name"] == self.name:
                datas["projects"].remove(p)
                break
        print("BPM --- Writing global json")
        write_json_file(datas, return_global_project_file())

        if self.remove_folder:
            if os.path.isdir(self.project_datas["root_folder"]):
                print("BPM --- Removing project content")
                shutil.rmtree(self.project_datas["root_folder"])
            else:
                print("BPM --- No project content to remove")

        project_name = self.project_datas["project_name"]
        self.report({'INFO'}, f"{project_name} Removed")

        context.window_manager["bpm_global_projects"] = datas

        # Refresh
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


@persistent
def global_project_load_handler(scene):
    reload_global_projects()

### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_create_project)
    bpy.utils.register_class(BPM_OT_reload_global_projects)
    bpy.utils.register_class(BPM_OT_remove_global_project)
    bpy.app.handlers.load_post.append(global_project_load_handler)
def unregister():
    bpy.utils.unregister_class(BPM_OT_create_project)
    bpy.utils.unregister_class(BPM_OT_reload_global_projects)
    bpy.utils.unregister_class(BPM_OT_remove_global_project)
    bpy.app.handlers.load_post.remove(global_project_load_handler)
