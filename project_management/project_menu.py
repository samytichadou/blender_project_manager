import bpy
import os

from ..addon_prefs import getAddonPreferences

def poll_bpm_project(context):
    try:
        context.window_manager["bpm_project_datas"]
        return True
    except KeyError:
        return False

def bpm_project_topbar(self, context):
    if not poll_bpm_project(context):
        return
    if context.region.alignment == 'RIGHT':
        layout=self.layout
        project_name = context.window_manager["bpm_project_datas"]["project_name"]
        layout.menu(
            "BPM_MT_project_menu",
            text = f" {project_name}",
            icon = "FREEZE",
            )

class BPM_MT_project_menu(bpy.types.Menu):
    bl_label = "BPMP Project"
    bl_idname = "BPM_MT_project_menu"

    @classmethod
    def poll(cls, context):
        return poll_bpm_project(context)

    def draw(self, context):
        project_datas = context.window_manager["bpm_project_datas"]

        layout = self.layout

        layout.label(
            text = getAddonPreferences().logged_user,
            icon = "USER",
            )

        layout.separator()

        layout.label(text = "Lock Files") # Placeholder

        layout.separator()

        layout.label(text = "Create Episode(s)") # Placeholder
        layout.label(text = "Remove Episode(s)") # Placeholder

        layout.separator()

        op = layout.operator("bpm.manage_project_users")
        op.project_name = project_datas["name"]
        layout.operator("bpm.modify_project_user")

        layout.separator()

        layout.label(text = "Modify Project") # Placeholder

        try:
            last_user = context.scene["bpm_last_user"]
            layout.separator()
            layout.label(text = f"Last save : {last_user}")
        except KeyError:
            pass


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_MT_project_menu)
    bpy.types.TOPBAR_HT_upper_bar.prepend(bpm_project_topbar)

def unregister():
    bpy.utils.unregister_class(BPM_MT_project_menu)
    bpy.types.TOPBAR_HT_upper_bar.remove(bpm_project_topbar)
