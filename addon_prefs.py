import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

def new_project_name_correction_callback(self, context):
    if self.no_update:
        return
    self.no_update = True
    name = self.new_project_name
    name = ''.join(e for e in name if e.isalnum() or e==" ")
    name = name.strip()
    name = name.replace(" ","_")
    self.new_project_name = name
    self.no_update = False

# addon preferences
class BPM_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    preferences_folder : bpy.props.StringProperty(
        name = "BPM preferences folder",
        default = os.path.join(os.path.join(bpy.utils.resource_path("USER"), "datafiles"), "bpm"),
        description = "Where BPM store global preferences",
        subtype = "DIR_PATH",
        )
    new_project_name : bpy.props.StringProperty(
        name = "New Project Name",
        default = "new_project",
        update = new_project_name_correction_callback,
        )
    new_project_folder : bpy.props.StringProperty(
        name = "New Project Folder",
        subtype = "DIR_PATH",
        )
    no_update : bpy.props.BoolProperty()

    def draw(self, context):
        layout = self.layout

        layout.prop(
            self,
            "preferences_folder",
            text = "Preference Folder",
            )
        layout.operator(
            "bpm.reload_global_projects",
            )

        # New Project
        box = layout.box()
        row = box.row()
        row.label(
            text = "New",
            )
        row.prop(
            self,
            "new_project_name",
            text = "",
            )
        row.prop(
            self,
            "new_project_folder",
            text = "",
            )
        row.operator(
            "bpm.create_project",
            text = "Create",
            )


# get addon preferences
def getAddonPreferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_PF_addon_prefs)
def unregister():
    bpy.utils.unregister_class(BPM_PF_addon_prefs)
