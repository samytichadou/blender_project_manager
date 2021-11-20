import bpy

from ..functions.check_file_poll_function import check_file_poll_function
from ..functions import project_data_functions
from . import gui_classes

### drawing functions ###

# help function
def draw_wiki_help(container, wikipage):
    container.operator('bpm.open_wiki_page', text="", icon='QUESTION').wiki_page = wikipage

# draw operator and help function
def draw_operator_and_help(container, operator_bl_idname, icon, wikipage):
    row = container.row(align=True)
    if icon != '':
        row.operator(operator_bl_idname, icon = icon)
    else:
        row.operator(operator_bl_idname)
    row.operator('bpm.open_wiki_page', text="", icon='QUESTION').wiki_page = wikipage

# draw open folders panel
def draw_open_folders_menu(container, filebrowser):

    col = container.column(align=True)

    for f in ('Datas', 'Project', 'Asset', 'Shot', 'Render', 'Ressources', 'Playblast'):
        op = col.operator('bpm.open_project_folder', text = f)
        op.folder = f
        op.filebrowser = filebrowser

    col.operator('bpm.open_shot_folder', text='Active Shot').filebrowser=filebrowser
    
    col.operator('bpm.open_shot_render_folder', text='Active Render').filebrowser=filebrowser

# draw next previous comment panel
def draw_next_previous_comment(container):

    row = container.row(align = True)

    op = row.operator("bpm.goto_next_previous_comment", text = "", icon = "TRIA_LEFT")
    op.next = False
    
    op = row.operator("bpm.goto_next_previous_comment", text = "", icon = "TRIA_RIGHT")
    op.next = True

    row.label(text = "Comments")

# draw shot comments ui
def draw_shot_comments_ui(container, scene_settings):

    container.prop(scene_settings, 'color_shot_comments', text="Color")

    row = container.row()
    row.label(text = "Names")
    row.prop(scene_settings, 'display_shot_comments_names', text = "")

    row = container.row()
    row.prop(scene_settings, 'display_shot_comments_boxes', text = "Name Boxes")
    row.prop(scene_settings, 'color_shot_comments_boxes', text="")

    container.prop(scene_settings, 'display_shot_comments_text_limit')

    #container.prop(scene_settings, "test_prop")

# sequencer shot comment function 
def draw_comment(container, comments, c_type, context):

    row = container.row(align=True)
    op = row.operator("bpm.add_comment", text="Add")
    op.comment_type = c_type
    op2 = row.operator("bpm.reload_comments", text = "", icon = "FILE_REFRESH")
    op2.comment_type = c_type
    #row.separator()
    draw_wiki_help(row, "Comments")

    bigcol = container.column(align=True)

    for c in comments:
        box = bigcol.box()
        col = box.column(align=True)   

        row = col.row(align=True)
        if c.hide:
            icon = "DISCLOSURE_TRI_RIGHT"
        else:
            icon = "DISCLOSURE_TRI_DOWN"
        row.prop(c, "hide", text="", icon=icon, emboss=False)

        row.label(text=c.author + " - " + c.time)

        if c.frame_comment:
            if c_type == "edit_shot":
                target_frame = c.timeline_frame
            else:
                target_frame = c.frame
            if context.scene.frame_current == target_frame:
                icon = "MARKER_HLT"
            else:
                icon = "MARKER"
            
            op = row.operator("bpm.goto_comment", text = "", icon = icon, emboss = False)
            op.frame = target_frame

        if c.edit_time:
            icon = "OUTLINER_DATA_GP_LAYER"
        else:
            icon = "GREASEPENCIL"
        idx = comments.find(c.name)
        op = row.operator("bpm.modify_comment", text="", icon=icon, emboss = False)
        op.index = idx
        op.comment_type = c_type
        op = row.operator("bpm.remove_comment", text="", icon="X", emboss = False)
        op.index = idx
        op.comment_type = c_type

        if not c.hide:
            for line in split_string_on_spaces(c.comment, 25):
                col.label(text=line)
            if c.frame_comment or c.edit_time:
                if c.frame_comment:
                    col.label(text="Frame : " + str(c.frame))
                    if c_type == "edit_shot":
                        col.label(text="Timeline Frame : " + str(c.timeline_frame))
                if c.edit_time:
                    col.label(text="Edited on " + c.edit_time)
                    
# draw all props for debug
def draw_debug(container, dataset):

    box = container.box()
    box.label(text = str(dataset.bl_rna.identifier) + ' - Be careful', icon='ERROR')

    for p in dataset.bl_rna.properties:
        if not p.is_readonly and p.identifier != 'name':
            row = container.row()
            row.prop(dataset, '%s' % p.identifier)

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

    draw_operator_and_help(container, 'bpm.create_asset', '', 'Asset-Management')

    container.prop(general_settings, 'panel_asset_display', text="Display")

    container.template_list("BPM_UL_Asset_UI_List", "", winman, "bpm_assets", general_settings, "asset_list_index", rows = 3)

    row = container.row(align=True)
    row.operator("bpm.open_asset_file", icon = "FILE_FOLDER").new_blender_instance = False
    row.operator("bpm.open_asset_file", text = "", icon = "BLENDER").new_blender_instance = True
    draw_wiki_help(row, "Asset-Management")

# draw shot tracking
def draw_shot_tracking_shot_file(container, winman):

    shot_settings = winman.bpm_shotsettings

    row = container.row(align=True)
    row.prop(shot_settings, 'shot_state', text="")
    if shot_settings.shot_state != "FINISHED":
        row.prop(shot_settings, project_data_functions.getShotTaskComplete(shot_settings)[0], text="")
    draw_wiki_help(row, 'Shot-Datas')

    row = container.row(align=True)
    row.label(text = "Deadline : " + project_data_functions.getShotTaskDeadline(shot_settings)[1], icon = 'TIME')
    row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='GREASEPENCIL').behavior = 'active_strip'
    draw_wiki_help(row, 'Shot-Task-System')

    draw_operator_and_help(container, 'bpm.refresh_shot_datas', '', 'Shot-Datas')

    draw_operator_and_help(container, 'bpm.synchronize_audio_shot', '', 'Shot-Audio-Synchronization')

    row = container.row(align=True)
    row.prop(shot_settings, 'auto_audio_sync')
    draw_wiki_help(row, 'Shot-Audio-Synchronization')

    row = container.row(align=True)
    row.prop(shot_settings, 'shot_render_state', text = "Render")
    draw_wiki_help(row, 'Render-Settings')

# draw shot version
def draw_shot_version_shot_file(container, winman):

    shot_settings = winman.bpm_shotsettings

    container.label(text = "version " + str(shot_settings.shot_version_file) + "/" + str(shot_settings.shot_last_version))

    container.label(text = "used in edit " + str(shot_settings.shot_version_used) + "/" + str(shot_settings.shot_last_version))
    
    draw_operator_and_help(container, "bpm.bump_shot_version_shot", "", "Shot-Version-Management")

# draw shot render
def draw_shot_render_shot_file(container):
    
    draw_operator_and_help(container, 'bpm.render_shot_playlast', '', 'Render-Settings')

# draw debug for assets
def draw_debug_asset(container, dataset):

    draw_debug(container, dataset)

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

# bpm function topbar back/open operators
def draw_topbar(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        general_settings = context.window_manager.bpm_generalsettings

        if general_settings.is_project:

            if general_settings.file_type in {'SHOT', 'ASSET'}:

                draw_operator_and_help(layout, 'bpm.back_to_edit', '', 'Open-Shot-and-Back-to-Edit')

            elif general_settings.file_type == 'EDIT':
                row = layout.row(align=True)
                row.operator("bpm.open_shot", icon = "FILE_FOLDER").new_blender_instance = False
                row.operator("bpm.open_shot", text = "", icon = "BLENDER").new_blender_instance = True
                draw_wiki_help(row, "Open-Shot-and-Back-to-Edit")

        # draw menu
        if general_settings.blend_already_opened or general_settings.update_needed:
            layout.menu('BPM_MT_topbar_menu', icon = "ERROR")
        else:
            layout.menu('BPM_MT_topbar_menu')


### EXTRAS ###

# topbar file menu
class BPM_MT_topbar_menu(bpy.types.Menu):
    bl_label = "BPM"
    bl_idname = "BPM_MT_topbar_menu"

    def draw(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout
      
        if not general_settings.is_project:
            layout.operator('bpm.create_project')
        
        else:
            project_data = winman.bpm_projectdatas
            layout.label(text = project_data.name)

            # opened blend
            if general_settings.blend_already_opened:
                layout.separator()
                layout.operator("bpm.show_open_blend_lock_file", icon = "ERROR")

            # addon update needed
            if general_settings.update_needed:
                layout.separator()
                op = layout.operator("wm.url_open", text = "New addon version available", icon = "URL")
                op.url = general_settings.update_download_url
                                

# filebrowser gui
class BPM_PT_FileBrowser_Panel(gui_classes.FilebrowserPanel):
    bl_label = "BPM"
    
    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project
    
    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        row = layout.row(align = True)
        row.menu('BPM_MT_OpenFolder_Filebrowser_Menu')
        draw_wiki_help(row, 'Project-Architecture')
        
        draw_custom_folder_template_list(layout, winman, True)


# open folder menu
class BPM_MT_OpenFolder_Explorer_Menu(bpy.types.Menu):
    bl_label = "Open Folders"

    def draw(self, context):
        layout = self.layout
        
        draw_open_folders_menu(layout, False)


# open folder menu
class BPM_MT_OpenFolder_Filebrowser_Menu(bpy.types.Menu):
    bl_label = "Open Folders"

    def draw(self, context):
        layout = self.layout
        
        draw_open_folders_menu(layout, True)


# right click sequencer general menu
class BPM_MT_RightClickSequencerEdit_Menu(bpy.types.Menu):
    bl_label = "BPM Edit"

    def draw(self, context):
        layout = self.layout

        layout.operator("bpm.create_shot")
        layout.operator("bpm.synchronize_audio_edit")
        layout.operator("bpm.refresh_edit_datas")
        layout.separator()
        layout.operator("bpm.goto_next_previous_comment", text = "Previous Comment").next = False
        layout.operator("bpm.goto_next_previous_comment", text = "Next Comment").next = True


# right click sequencer active shot menu
class BPM_MT_RightClickSequencerShot_Menu(bpy.types.Menu):
    bl_label = "BPM Active Shot"

    def draw(self, context):
        layout = self.layout
        
        layout.operator('bpm.open_shot')
        layout.operator('bpm.update_shot_duration')
        layout.operator('bpm.bump_shot_version_edit')
        layout.operator('bpm.render_shot_edit')


# right click sequencer menu
def drawRightClickSequencerMenu(self, context):

    general_settings = context.window_manager.bpm_generalsettings
    scn = context.scene

    if general_settings.is_project and general_settings.file_type == 'EDIT':

        layout = self.layout
        layout.menu('BPM_MT_RightClickSequencerEdit_Menu')

        if scn.sequence_editor.active_strip:
            active_strip = scn.sequence_editor.active_strip
            if active_strip.type in {'SCENE', 'IMAGE'}:
                if active_strip.bpm_shotsettings.is_shot:

                    layout.menu('BPM_MT_RightClickSequencerShot_Menu')

        layout.separator()


### REGISTER ---

classes = (
    #SEQUENCER
    BPM_PT_sequencer_panels_display_panel,
    BPM_PT_sequencer_management_panel,
    BPM_PT_sequencer_files_panel,
    BPM_PT_sequencer_management_debug_panel,
    BPM_PT_sequencer_edit_panel,
    BPM_PT_sequencer_edit_comment_panel,
    BPM_PT_sequencer_edit_ui_panel,
    BPM_PT_sequencer_edit_ui_shot_subpanel,
    BPM_PT_sequencer_edit_ui_shot_state_subpanel,
    BPM_PT_sequencer_edit_ui_shot_frame_comment_subpanel,
    BPM_PT_sequencer_edit_ui_timeline_frame_comment_subpanel,
    BPM_PT_sequencer_edit_ui_scheduling_subpanel,
    BPM_PT_sequencer_shot_tracking_panel,
    BPM_PT_sequencer_shot_version_panel,
    BPM_PT_sequencer_shot_comment_panel,
    BPM_PT_sequencer_shot_display_panel,
    BPM_PT_sequencer_shot_debug_panel,
    BPM_PT_sequencer_asset_library_panel,
    #VIEWPORT
    BPM_PT_viewport_panels_display_panel,
    BPM_PT_viewport_management_panel,
    BPM_PT_viewport_files_panel,
    BPM_PT_viewport_management_debug_panel,
    BPM_PT_viewport_shot_tracking_panel,
    BPM_PT_viewport_shot_version_panel,
    BPM_PT_viewport_shot_comment_panel,
    BPM_PT_viewport_shot_ui_comment_subpanel,
    BPM_PT_viewport_shot_render_panel,
    BPM_PT_viewport_shot_debug_panel,
    BPM_PT_viewport_asset_settings_panel,
    BPM_PT_viewport_asset_comment_panel,
    BPM_PT_viewport_asset_ui_comment_subpanel,
    BPM_PT_viewport_asset_library_panel,
    BPM_PT_viewport_asset_debug_panel,
    #NODETREE
    BPM_PT_nodetree_panels_display_panel,
    BPM_PT_nodetree_management_panel,
    BPM_PT_nodetree_files_panel,
    BPM_PT_nodetree_management_debug_panel,
    BPM_PT_nodetree_shot_tracking_panel,
    BPM_PT_nodetree_shot_version_panel,
    BPM_PT_nodetree_shot_comment_panel,
    BPM_PT_nodetree_shot_render_panel,
    BPM_PT_nodetree_shot_debug_panel,
    BPM_PT_nodetree_asset_settings_panel,
    BPM_PT_nodetree_asset_comment_panel,
    BPM_PT_nodetree_asset_library_panel,
    BPM_PT_nodetree_asset_debug_panel,
    #FILEBROSER
    BPM_PT_FileBrowser_Panel,
    #MENUS
    BPM_MT_topbar_menu,
    BPM_MT_OpenFolder_Explorer_Menu,
    BPM_MT_OpenFolder_Filebrowser_Menu,
    BPM_MT_RightClickSequencerEdit_Menu,
    BPM_MT_RightClickSequencerShot_Menu,
)

def register():
    for cls in classes :
        bpy.utils.register_class(cls)   

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.prepend(draw_topbar)
    bpy.types.SEQUENCER_MT_context_menu.prepend(drawRightClickSequencerMenu)

def unregister():
    for cls in reversed(classes) :
        bpy.utils.unregister_class(cls)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_topbar)
    bpy.types.SEQUENCER_MT_context_menu.remove(drawRightClickSequencerMenu)