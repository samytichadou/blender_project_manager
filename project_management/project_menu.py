import bpy
import os

from ..addon_prefs import getAddonPreferences

# TODO Warning if not asset last version

def poll_bpm_project():
    try:
        bpy.context.window_manager["bpm_project_datas"]
        return True
    except KeyError:
        return False

def bpm_project_topbar(self, context):
    if not poll_bpm_project():
        return
    if context.region.alignment == 'RIGHT':
        layout=self.layout
        # TODO Back menu
        layout.operator("bpm.open_back_blend", text="", icon="LOOP_BACK")
        layout.menu(
            "BPM_MT_project_menu",
            text = "BPM",
            )

def draw_asset_entry(container):
    container.operator("bpm.publish_asset")
    container.separator()

class BPM_MT_project_menu(bpy.types.Menu):
    bl_label = "BPMP Project"
    bl_idname = "BPM_MT_project_menu"

    @classmethod
    def poll(cls, context):
        return poll_bpm_project()

    def draw(self, context):
        project_datas = context.window_manager["bpm_project_datas"]
        file_datas = context.window_manager["bpm_file_datas"]
        file_type = file_datas["file_type"]

        layout = self.layout

        layout.label(
            text = getAddonPreferences().logged_user,
            icon = "USER",
            )

        layout.separator()

        layout.label(text = project_datas["project_name"])

        layout.separator()

        layout.label(text = "Lock Files") # Placeholder
        # TODO Label current file

        layout.separator()

        if file_type == "asset": # TODO Only if authorization
            draw_asset_entry(layout)

        ### TODO Hide if not authorized users
        layout.separator()
        layout.label(text = "Create Episode(s)") # Placeholder
        layout.label(text = "Remove Episode(s)") # Placeholder

        layout.separator()

        op = layout.operator("bpm.manage_project_users")
        op.project_name = project_datas["name"]
        layout.operator("bpm.modify_project_user")

        layout.separator()

        layout.label(text = "Modify Project") # Placeholder
        ###

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
