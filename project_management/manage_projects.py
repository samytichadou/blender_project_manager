import bpy
import os
import json
import shutil
from bpy.app.handlers import persistent

from ..addon_prefs import getAddonPreferences

def return_global_preferences_folder():
    folder=bpy.path.abspath(
        getAddonPreferences().preferences_folder
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
    dataset["name"] = project_name
    dataset["folder"] = root_folder

    global_datas = return_global_project_datas()
    global_datas["projects"].append(dataset)

    print("BPM --- Writing global json")
    write_json_file(global_datas, return_global_project_file())
    return global_datas

def create_hierarchy_folders(project_name, root_folder):
    print("BPM --- Creating project hierarchy")

    os.makedirs(root_folder)

    os.mkdir(os.path.join(root_folder, "users"))
    os.mkdir(os.path.join(root_folder, "assets"))
    os.mkdir(os.path.join(root_folder, "shots"))
    os.mkdir(os.path.join(root_folder, "renders"))
    os.mkdir(os.path.join(root_folder, "plannings"))
    os.mkdir(os.path.join(root_folder, "storyboards"))
    os.mkdir(os.path.join(root_folder, "edits"))
    os.mkdir(os.path.join(root_folder, "startups"))
    os.mkdir(os.path.join(root_folder, "resources"))
    os.mkdir(os.path.join(root_folder, "locks"))


class BPM_OT_create_project(bpy.types.Operator):
    bl_idname = "bpm.create_project"
    bl_label = "Create Project"
    bl_description = "Create a new BPM project"
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        prefs = getAddonPreferences()
        if prefs.new_project_name:
            return os.path.isdir(bpy.path.abspath(prefs.new_project_folder))

    def execute(self, context):
        prefs = getAddonPreferences()
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

    folder : bpy.props.StringProperty()
    remove_folder : bpy.props.BoolProperty(
        name = "Also remove project content",
        )
    project_index = None

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        global_projects = context.window_manager.bpm_global_projects
        for i, item in enumerate(global_projects, 0):
            if item.folder == self.folder:
                self.project_index = i
                break
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        global_projects = context.window_manager.bpm_global_projects
        layout = self.layout
        layout.label(
            text = f"Removing {global_projects[self.project_index].name}",
            icon = "ERROR",
            )
        layout.label(
            text = global_projects[self.project_index].folder,
            )
        layout.prop(
            self,
            "remove_folder",
            )
        layout.label(
            text = "Are you sure ?",
            )

    def execute(self, context):
        global_projects = context.window_manager.bpm_global_projects

        global_projects.remove(self.project_index)

        # Remove project from json

        if self.remove_folder:
            shutil.rmtree(self.folder)

        self.report({'INFO'}, f"{self.folder} Removed")

        # Refresh

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
