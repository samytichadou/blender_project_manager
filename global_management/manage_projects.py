import bpy
import os
import json
import shutil
import random
from bpy.app.handlers import persistent

from .. import addon_prefs as ap
from . import user_authorization as ua

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

def add_project_dataset(project_name, root_folder):
    print("BPM --- Creating project dataset")

    dataset = {}
    dataset["name"] = generate_random()
    dataset["project_name"] = project_name
    dataset["folder"] = root_folder

    global_datas = return_global_project_datas()
    global_datas["projects"].append(dataset)

    print("BPM --- Writing global json")
    write_json_file(global_datas, return_global_project_file())
    return global_datas

def create_hierarchy_folders(project_name, root_folder):
    print("BPM --- Creating project hierarchy")

    os.makedirs(root_folder)

    os.mkdir(os.path.join(root_folder, "assets"))
    os.mkdir(os.path.join(root_folder, "shots"))
    os.mkdir(os.path.join(root_folder, "renders"))
    os.mkdir(os.path.join(root_folder, "plannings"))
    os.mkdir(os.path.join(root_folder, "storyboards"))
    os.mkdir(os.path.join(root_folder, "edits"))
    os.mkdir(os.path.join(root_folder, "startups"))
    os.mkdir(os.path.join(root_folder, "resources"))
    os.mkdir(os.path.join(root_folder, "locks"))

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
    resolution : bpy.props.IntVectorProperty(
        name = "Resolution",
        size = 2,
        default = (1920,1080),
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
        global_projects = context.window_manager.bpm_global_projects
        layout = self.layout
        layout.prop(self, "framerate")
        layout.prop(self, "resolution")
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
        create_hierarchy_folders(project_name, root_folder)

        # Create json
        add_project_dataset(project_name, root_folder)

        # Refresh project list
        reload_global_projects()

        return {'FINISHED'}


def reload_global_projects():
    print("BPM --- Refreshing global project list")

    props = bpy.context.window_manager.bpm_global_projects
    props.clear()
    dataset = return_global_project_datas()
    for proj in dataset["projects"]:
        new = props.add()
        new.name = proj["name"]
        new.folder = proj["folder"]
        new.project_name = proj["project_name"]

@persistent
def global_project_load_handler(scene):
    reload_global_projects()

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

    @classmethod
    def poll(cls, context):
        return ua.compare_athcode(
            ua.patt_project_creation,
            ap.getAddonPreferences().athcode
            )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        global_projects = context.window_manager.bpm_global_projects
        layout = self.layout
        layout.label(
            text = f"Removing {global_projects[self.name].project_name}",
            icon = "ERROR",
            )
        layout.label(text = global_projects[self.name].folder)
        layout.prop(self, "remove_folder")
        layout.label(text = "Are you sure ?")

    def execute(self, context):
        global_projects = context.window_manager.bpm_global_projects

        # Remove project from json
        datas = return_global_project_datas()
        for p in datas["projects"]:
            if p["name"] == self.name:
                datas["projects"].remove(p)
                break
        print("BPM --- Writing global json")
        write_json_file(datas, return_global_project_file())

        if self.remove_folder:
            shutil.rmtree(global_projects[self.name].folder)

        self.report({'INFO'}, f"{global_projects[self.name].project_name} Removed")

        index = global_projects.find(self.name)
        global_projects.remove(index)

        # Refresh
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


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
