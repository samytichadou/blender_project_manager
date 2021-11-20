import bpy

from . import gui_classes
from . import gui_common

### DRAW FCTS ###

# draw asset settings prop panel
def draw_asset_settings(container, asset_settings, general_settings):
    
    if asset_settings.asset_type == 'SHADER': target_prop = 'asset_material'
    elif asset_settings.asset_type == 'NODEGROUP': target_prop = 'asset_nodegroup'
    elif asset_settings.asset_type == 'WORLD': target_prop = 'asset_world'
    else: target_prop = 'asset_collection'

    container.prop(asset_settings, target_prop, text='')
    container.label(text = "Manually Update", icon = "INFO")

    col = container.column(align=True)

    col.prop(asset_settings, 'asset_type', text = "Type")
    col.prop(asset_settings, 'asset_state', text = "State")

# draw asset library
def draw_asset_library(container, winman):

    general_settings = winman.bpm_generalsettings

    gui_common.draw_operator_and_help(container, 'bpm.create_asset', '', 'Asset-Management')

    container.prop(general_settings, 'panel_asset_display', text="Display")

    container.template_list("BPM_UL_Asset_UI_List", "", winman, "bpm_assets", general_settings, "asset_list_index", rows = 3)

    row = container.row(align=True)
    row.operator("bpm.open_asset_file", icon = "FILE_FOLDER").new_blender_instance = False
    row.operator("bpm.open_asset_file", text = "", icon = "BLENDER").new_blender_instance = True
    gui_common.draw_wiki_help(row, "Asset-Management")

# draw debug for assets
def draw_debug_asset(container, dataset):

    gui_common.draw_debug(container, dataset)

    container.label(text = 'Debug', icon = 'ERROR')

    container.label(text = 'Collections', icon = 'GROUP')
    col = container.column(align=True)
    for i in bpy.data.collections:
        row = col.row(align=True)
        row.prop(i, 'bpm_isasset', text=i.name)

    container.label(text = 'Materials', icon = 'MATERIAL')
    col = container.column(align=True)
    for i in bpy.data.materials:
        row = col.row(align=True)
        row.prop(i, 'bpm_isasset', text=i.name)

    container.label(text = 'Nodegroups', icon = 'NODETREE')
    col = container.column(align=True)
    for i in bpy.data.node_groups:
        row = col.row(align=True)
        row.prop(i, 'bpm_isasset', text=i.name)

    container.label(text = 'Worlds', icon = 'WORLD')
    col = container.column(align=True)
    for i in bpy.data.worlds:
        row = col.row(align=True)
        row.prop(i, 'bpm_isasset', text=i.name)


### PANELS ###

### SEQUENCER PANELS ###

# sequencer asset library panel
class BPM_PT_sequencer_asset_library_panel(gui_classes.SequencerPanel_Assets):
    bl_label = "Asset Library"

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        draw_asset_library(layout, winman)

### VIEWPORT PANELS ###

# asset settings viewport panel
class BPM_PT_viewport_asset_settings_panel(gui_classes.ViewportPanel_Assets):
    bl_label = "Settings"

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        draw_asset_settings(layout, asset_settings, general_settings)

# asset library viewport panel
class BPM_PT_viewport_asset_library_panel(gui_classes.ViewportPanel_Assets_Library):
    bl_label = "Library"

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        draw_asset_library(layout, winman)

        layout.operator("bpm.import_asset", icon = "LINK_BLEND")

# asset comment viewport panel
class BPM_PT_viewport_asset_comment_panel(gui_classes.ViewportPanel_Assets):
    bl_label = "Comments"

    def draw(self, context):
        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        gui_common.draw_next_previous_comment(layout)

        gui_common.draw_comment(layout, asset_settings.comments, "asset", context)

# shot comment ui viewport subpanel
class BPM_PT_viewport_asset_ui_comment_subpanel(gui_classes.ViewportPanel_Assets):
    bl_label = ""
    bl_parent_id = "BPM_PT_viewport_asset_comment_panel"

    def draw_header(self, context):
        scn_settings = context.scene.bpm_scenesettings
        self.layout.label(text = "Comments UI")
        self.layout.prop(scn_settings, "extra_ui", text = "")

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

        gui_common.draw_shot_comments_ui(self.layout, scn_settings)

# asset settings debug viewport panel
class BPM_PT_viewport_asset_debug_panel(gui_classes.ViewportPanel_Assets_Debug):
    bl_label = "Debug"

    def draw(self, context):

        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        draw_debug_asset(layout, asset_settings)

### NODETREE PANELS ###

# asset settings nodetree panel
class BPM_PT_nodetree_asset_settings_panel(gui_classes.NodetreePanel_Assets):
    bl_label = "Settings"

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        draw_asset_settings(layout, asset_settings, general_settings)

# asset comment nodetree subpanel
class BPM_PT_nodetree_asset_comment_panel(gui_classes.NodetreePanel_Assets):
    bl_label = "Comments"

    def draw(self, context):
        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        gui_common.draw_next_previous_comment(layout)

        gui_common.draw_comment(layout, asset_settings.comments, "asset", context)

# asset library nodetree panel
class BPM_PT_nodetree_asset_library_panel(gui_classes.NodetreePanel_Assets_Library):
    bl_label = "Library"

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        draw_asset_library(layout, winman)

        if winman.bpm_generalsettings.file_type in {'SHOT', 'ASSET'}:
            layout.operator("bpm.import_asset", icon = "LINK_BLEND")

# asset settings nodetree debug subpanel
class BPM_PT_nodetree_asset_debug_panel(gui_classes.NodetreePanel_Assets_Debug):
    bl_label = "Debug"

    def draw(self, context):

        layout = self.layout

        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        draw_debug_asset(layout, asset_settings)


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_PT_sequencer_asset_library_panel)

    bpy.utils.register_class(BPM_PT_viewport_asset_settings_panel)
    bpy.utils.register_class(BPM_PT_viewport_asset_library_panel)
    bpy.utils.register_class(BPM_PT_viewport_asset_comment_panel)
    bpy.utils.register_class(BPM_PT_viewport_asset_ui_comment_subpanel)
    bpy.utils.register_class(BPM_PT_viewport_asset_debug_panel)

    bpy.utils.register_class(BPM_PT_nodetree_asset_settings_panel)
    bpy.utils.register_class(BPM_PT_nodetree_asset_comment_panel)
    bpy.utils.register_class(BPM_PT_nodetree_asset_library_panel)
    bpy.utils.register_class(BPM_PT_nodetree_asset_debug_panel)

def unregister():
    bpy.utils.unregister_class(BPM_PT_sequencer_asset_library_panel)

    bpy.utils.unregister_class(BPM_PT_viewport_asset_settings_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_asset_library_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_asset_comment_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_asset_ui_comment_subpanel)
    bpy.utils.unregister_class(BPM_PT_viewport_asset_debug_panel)

    bpy.utils.unregister_class(BPM_PT_nodetree_asset_settings_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_asset_comment_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_asset_library_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_asset_debug_panel)
