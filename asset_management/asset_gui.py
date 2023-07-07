import bpy

from bpy_extras import (
    asset_utils,
)

from . import asset_management as am

class BPM_UL_asset_workfiles(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text = item.asset_name)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text = item.asset_name)

class BPM_PT_asset_workfiles(asset_utils.AssetBrowserPanel, bpy.types.Panel):
    bl_region_type = 'TOOL_PROPS'
    bl_label = "BPM Asset Workfiles"

    @classmethod
    def poll(cls, context):
        # Check if bpm project
        try:
            bpy.context.window_manager["bpm_project_datas"]
            return True
        except KeyError:
            return False

    def draw(self, context):
        asset_props = context.window_manager.bpm_project_assets

        layout = self.layout

        row = layout.row()
        row.template_list(
            "BPM_UL_asset_workfiles",
            "",
            asset_props,
            "asset_list",
            asset_props,
            "asset_index",
            rows = 5,
            )

        col = row.column(align=True)
        col.operator("bpm.reload_asset_list", icon='FILE_REFRESH', text="")
        col.separator()
        col.operator("bpm.create_asset", text="", icon="ADD")
        col.operator("bpm.remove_asset", text="", icon="REMOVE")
        col.separator()
        op = col.operator("bpm.open_blend", text="", icon="BLENDER")
        if asset_props.asset_index in range(len(asset_props.asset_list)):
            active = asset_props.asset_list[asset_props.asset_index]
            op.folderpath = active.folderpath
            op.pattern = am.get_asset_workfile_pattern(
                            active.name,
                            context.window_manager["bpm_project_datas"]["project_name"],
                            )
            row = layout.row()
            row.label(text = active.type)
            row.label(text = f"v{active.last_workfile_version}")
            if active.description:
                text=active.description
            else:
                text="No description"
            layout.label(text=text, icon="INFO")


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_UL_asset_workfiles)
    bpy.utils.register_class(BPM_PT_asset_workfiles)
def unregister():
    bpy.utils.unregister_class(BPM_UL_asset_workfiles)
    bpy.utils.unregister_class(BPM_PT_asset_workfiles)
