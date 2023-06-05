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

        # Available Projects
        box = layout.box()
        row = box.row()
        row.label(
            text = "Available Pojects"
            )
        row.operator(
            "bpm.reload_global_projects",
            text = "",
            icon = "FILE_REFRESH",
            )
        global_projects = context.window_manager.bpm_global_projects
        if global_projects:
            col = box.column(align = True)
            for p in context.window_manager.bpm_global_projects:
                # TODO better spacing
                row = col.row()
                row.label(text = p.project_name)
                row.label(text = p.folder)
                op = row.operator(
                    "bpm.remove_global_project",
                    text = "",
                    icon = "X",
                    )
                op.name = p.name

        # New Project
        box = layout.box()
        box.label(
            text = "New Project",
            )
        row = box.row()
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
