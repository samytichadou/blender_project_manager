import bpy
import os
import json

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

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_create_project)
def unregister():
    bpy.utils.unregister_class(BPM_OT_create_project)
