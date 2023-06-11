import bpy

from ..addon_prefs import getAddonPreferences

def bpm_project_topbar(self, context):
    try:
        datas = context.window_manager["bpm_project_datas"]
    except KeyError:
        return
    if context.region.alignment == 'RIGHT':
        layout=self.layout
        project_name = datas["project_name"]
        layout.menu(
            "BPM_MT_project_menu",
            text = f" {project_name}",
            icon = "FREEZE",
            )

class BPM_MT_project_menu(bpy.types.Menu):
    bl_label = "BPMP Project"
    bl_idname = "BPM_MT_project_menu"

    def draw(self, context):
        layout = self.layout
        layout.label(
            text = getAddonPreferences().logged_user,
            icon = "USER",
            )
        layout.separator()

### REGISTER ---
def register():
    bpy.utils.register_class(BPM_MT_project_menu)
    bpy.types.TOPBAR_HT_upper_bar.prepend(bpm_project_topbar)

def unregister():
    bpy.utils.unregister_class(BPM_MT_project_menu)
    bpy.types.TOPBAR_HT_upper_bar.remove(bpm_project_topbar)
