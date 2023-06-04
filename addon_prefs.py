import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

# addon preferences
class BPM_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    preferences_folder : bpy.props.StringProperty(
        name = "BPM preferences folder",
        default = os.path.join(os.path.join(bpy.utils.resource_path('USER'), "datafiles"), "bpm"),
        description = "Where BPM store global preferences",
        subtype = "DIR_PATH",
        )

    def draw(self, context):
        layout = self.layout
        layout.prop(
            self,
            "preferences_folder",
            text="Preference Folder",
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
