import bpy

from .properties import getAssetIcon
from .functions.project_data_functions import getShotTaskDeadline, getShotTaskComplete
from .functions.check_edit_poll_function import check_edit_poll_function

### drawing functions ###

# help function
def drawWikiHelp(container, wikipage):
    container.operator('bpm.open_wiki_page', text="", icon='QUESTION').wiki_page = wikipage


# draw operator and help function
def drawOperatorAndHelp(container, operator_bl_idname, icon, wikipage):
    row = container.row(align=True)
    if icon != '':
        row.operator(operator_bl_idname, icon = icon)
    else:
        row.operator(operator_bl_idname)
    row.operator('bpm.open_wiki_page', text="", icon='QUESTION').wiki_page = wikipage


# draw all props for debug
def drawDebugPanel(container, dataset):

    container.label(text = str(dataset.bl_rna.identifier) + ' - Be careful', icon='ERROR')
    for p in dataset.bl_rna.properties:
        if not p.is_readonly and p.identifier != 'name':
            row = container.row()
            row.prop(dataset, '%s' % p.identifier)


# draw debug for assets
def drawDebugAssetPanel(container, dataset):

    drawDebugPanel(container, dataset)

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


# draw already opened blend warning
def drawOpenedWarning(container, general_settings):
    if general_settings.blend_already_opened:
        drawOperatorAndHelp(container, 'bpm.show_open_blend_lock_file', 'ERROR', "Lock-File-System")
        #container.label(text="File already opened", icon='ERROR')


# draw open folders panel
def drawOpenFoldersPanel(container, filebrowser):

    col = container.column(align=True)

    for f in ('Project', 'Asset', 'Shot', 'Render', 'Ressources', 'Playblast'):
        op = col.operator('bpm.open_project_folder', text = f)
        op.folder = f
        op.filebrowser = filebrowser

    col.operator('bpm.open_shot_folder', text='Active Shot').filebrowser=filebrowser
    
    col.operator('bpm.open_shot_render_folder', text='Active Render').filebrowser=filebrowser


# split string on spaces
def split_string_on_spaces(string, char_limit):
    lines = []
    words = string.split()

    line = ""
    for w in words:
        if len(line) < char_limit:
            line += w + " "
        else:
            line = line[:-1]
            lines.append(line)
            line = w + " "

    if line not in lines:    
        lines.append(line)
        
    return lines


# sequencer shot comment function 
def comment_draw(container, comments, c_type):

    row = container.row(align=True)
    op = row.operator("bpm.add_comment")
    op.comment_type = c_type
    op2 = row.operator("bpm.reload_comment", text = "", icon = "FILE_REFRESH")
    op2.comment_type = c_type

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
        if c.edit_time:
            row.label(text="", icon="OUTLINER_DATA_GP_LAYER")
        idx = comments.find(c.name)
        op = row.operator("bpm.modify_comment", text="", icon="GREASEPENCIL")
        op.index = idx
        op.comment_type = c_type
        op = row.operator("bpm.remove_comment", text="", icon="X")
        op.index = idx
        op.comment_type = c_type

        if not c.hide:
            for line in split_string_on_spaces(c.comment, 25):
                col.label(text=line)
            if c.frame_comment or c.edit_time:
                col.separator()
                if c.frame_comment:
                    col.label(text="Frame : " + str(c.frame))
                if c.edit_time:
                    col.label(text="Edited on " + c.edit_time)


# draw asset settings prop panel
def drawPropertiesAssetPanel(container, asset_settings, general_settings):

    drawOpenedWarning(container, general_settings)
    
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
def drawAssetLibrary(container, winman):

    general_settings = winman.bpm_generalsettings

    container.operator("bpm.create_asset")

    container.prop(general_settings, 'panel_asset_display', text="Display")

    container.template_list("BPM_UL_Asset_UI_List", "", winman, "bpm_assets", general_settings, "asset_list_index", rows = 3)

    container.operator("bpm.open_asset_file", icon = "FILE_FOLDER")


# bpm function topbar back/open operators
def bpmTopbarFunction(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        general_settings = context.window_manager.bpm_generalsettings

        if general_settings.is_project:

            if general_settings.blend_already_opened:
                drawOpenedWarning(layout, general_settings)

            if general_settings.file_type in {'SHOT', 'ASSET'}:

                drawOperatorAndHelp(layout, 'bpm.back_to_edit', '', 'Open-Shot-and-Back-to-Edit')

            elif general_settings.file_type == 'EDIT':

                drawOperatorAndHelp(layout, 'bpm.open_shot', '', 'Open-Shot-and-Back-to-Edit')

        layout.menu('BPM_MT_topbar_menu')


# draw browse panel
def draw_browse_panel(container):

    row = container.row(align=True)
    row.menu('BPM_MT_OpenFolder_Explorer_Menu')
    drawWikiHelp(row, 'Project-Architecture')


### panel classes ###

# sequencer class
class SequencerPanel(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"

# viewport class
class ViewportPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"

# nodetree class
class NodetreePanel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "BPM"

# filebrowser class
class FilebrowserPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "BPM"


# sequencer management
class BPM_PT_sequencer_management_panel(SequencerPanel):
    bl_label = "Project"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'

    def draw(self, context):
        winman = context.window_manager
        project_data = context.window_manager.bpm_projectdatas
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        drawOpenedWarning(layout, general_settings)

        drawOperatorAndHelp(layout, 'bpm.create_shot', '', 'Create-Shot-Operator')

        drawOperatorAndHelp(layout, 'bpm.delete_unused_shots', '', 'Delete-Unused-Shots')

        drawOperatorAndHelp(layout, 'bpm.empty_recycle_bin', '', 'Empty-Recycle-Bin')

        drawOperatorAndHelp(layout, 'bpm.synchronize_audio_edit', '', 'Shot-Audio-Synchronization')

        drawOperatorAndHelp(layout, 'bpm.refresh_shot_datas_edit', '', 'Shot-Datas')


# sequencer management comment subpanel
class BPM_PT_sequencer_management_comment_subpanel(SequencerPanel):
    bl_label = ""
    bl_parent_id = "BPM_PT_sequencer_management_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if general_settings.file_type == 'EDIT':
                edit, shot, active = check_edit_poll_function(context)
                if edit:
                    return True

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Comments")
        drawWikiHelp(row, "Comments")

    def draw(self, context):

        layout = self.layout
        
        comments = context.window_manager.bpm_projectdatas.comments

        comment_draw(layout, comments, "edit")


# sequencer browse subpanel
class BPM_PT_sequencer_browse_subpanel(SequencerPanel):
    bl_label = "Browse"
    bl_parent_id = "BPM_PT_sequencer_management_panel"
    bl_options = {'DEFAULT_CLOSED'}
 
    def draw(self, context):

        draw_browse_panel(self.layout)


# sequencer management debug subpanel
class BPM_PT_sequencer_management_debug_subpanel(SequencerPanel):
    bl_label = "Debug"
    bl_parent_id = "BPM_PT_sequencer_management_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_projectdatas.debug

    def draw(self, context):

        layout = self.layout
        
        general_settings = context.window_manager.bpm_generalsettings

        drawDebugPanel(layout, general_settings)


# sequencer shot panel
class BPM_PT_sequencer_shot_panel(SequencerPanel):
    bl_label = "Shot"

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if general_settings.file_type == 'EDIT':
                edit, shot, active = check_edit_poll_function(context)
                if edit and shot:
                    return True

    def draw(self, context):        

        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        drawOpenedWarning(layout, general_settings)


# sequencer tracking shot subpanel
class BPM_PT_sequencer_shot_tracking_subpanel(SequencerPanel):
    bl_label = "Tracking"
    bl_parent_id = "BPM_PT_sequencer_shot_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        active = context.scene.sequence_editor.active_strip
        shot_settings = active.bpm_shotsettings

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_state', text="")
        if shot_settings.shot_state != "FINISHED":
            row.prop(shot_settings, getShotTaskComplete(shot_settings)[0], text="")
        drawWikiHelp(row, 'Shot-Datas')

        row = layout.row(align=True)
        row.label(text = "Deadline : " + getShotTaskDeadline(shot_settings)[1], icon = 'TIME')
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='GREASEPENCIL').behavior = 'active_strip'
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='SEQ_STRIP_DUPLICATE').behavior = 'selected_strips'
        drawWikiHelp(row, 'Shot-Task-System')


# sequencer version shot subpanel
class BPM_PT_sequencer_shot_version_subpanel(SequencerPanel):
    bl_label = "Version"
    bl_parent_id = "BPM_PT_sequencer_shot_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        active = context.scene.sequence_editor.active_strip
        shot_settings = active.bpm_shotsettings

        layout.label(text = "version " + str(shot_settings.shot_version) + "/" + str(shot_settings.shot_last_version))

        drawOperatorAndHelp(layout, 'bpm.bump_shot_version_edit', '', 'Shot-Version-Management')

        drawOperatorAndHelp(layout, 'bpm.change_shot_version_edit', '', 'Shot-Version-Management')

        row = layout.row(align=True)
        row.operator('bpm.change_shot_version_edit', text = "Last shot version").go_to_last_version = True
        row.operator('bpm.open_wiki_page', text='', icon='QUESTION').wiki_page = 'Shot-Version-Management'


# sequencer sync shot subpanel
class BPM_PT_sequencer_shot_sync_subpanel(SequencerPanel):
    bl_label = "Sync"
    bl_parent_id = "BPM_PT_sequencer_shot_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings

        drawOperatorAndHelp(layout, 'bpm.update_shot_duration', '', 'Update-Shot-Operator')

        row = layout.row(align=True)
        row.prop(shot_settings, 'auto_audio_sync')
        drawWikiHelp(row, 'Shot-Audio-Synchronization')


# sequencer comment shot subpanel
class BPM_PT_sequencer_shot_comment_subpanel(SequencerPanel):
    bl_label = ""
    bl_parent_id = "BPM_PT_sequencer_shot_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Comments")
        drawWikiHelp(row, "Comments")

    def draw(self, context):

        layout = self.layout
        
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings

        comment_draw(layout, shot_settings.comments, "edit_shot")


# sequencer display shot subpanel
class BPM_PT_sequencer_shot_display_subpanel(SequencerPanel):
    bl_label = "Display"
    bl_parent_id = "BPM_PT_sequencer_shot_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        active = context.scene.sequence_editor.active_strip
        shot_settings = active.bpm_shotsettings

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_timeline_display', text = "Display")
        drawWikiHelp(row, 'Timeline-Shot-Display-Mode')

        layout.prop(shot_settings, 'display_comments')


# sequencer render shot subpanel
class BPM_PT_sequencer_shot_render_subpanel(SequencerPanel):
    bl_label = "Render"
    bl_parent_id = "BPM_PT_sequencer_shot_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        active = context.scene.sequence_editor.active_strip
        shot_settings = active.bpm_shotsettings

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_render_state', text = "Render")
        drawWikiHelp(row, 'Render-Settings')

        drawOperatorAndHelp(layout, 'bpm.render_shot_edit', '', 'Shot-Rendering')


# sequencer shot debug subpanel
class BPM_PT_sequencer_shot_debug_subpanel(SequencerPanel):
    bl_label = "Debug"
    bl_parent_id = "BPM_PT_sequencer_shot_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_projectdatas.debug

    def draw(self, context):

        layout = self.layout
        
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings

        drawDebugPanel(layout, shot_settings)


# sequencer asset library panel
class BPM_PT_sequencer_asset_library_panel(SequencerPanel):
    bl_label = ""

    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type == 'EDIT':
                if context.window_manager.bpm_projectdatas.edit_scene_keyword in context.scene.name:
                    return True

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Assets")
        drawWikiHelp(row, 'Asset-Management')

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        drawOpenedWarning(layout, winman.bpm_generalsettings)

        drawAssetLibrary(layout, winman)


# sequencer UI panel
class BPM_PT_sequencer_ui_panel(SequencerPanel):
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'

    def draw_header(self, context):
        scn_settings = context.scene.bpm_scenesettings
        row = self.layout.row()
        row.prop(scn_settings, "extra_ui", text = "UI")
        drawWikiHelp(row, 'Extra-UI-in-Sequencer')

    def draw(self, context):

        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        drawOpenedWarning(layout, general_settings)


# sequencer UI shot subpanel
class BPM_PT_sequencer_ui_shot_subpanel(SequencerPanel):
    bl_label = "Shots"
    bl_parent_id = "BPM_PT_sequencer_ui_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.bpm_scenesettings.extra_ui

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        row = layout.row()
        row.prop(scn_settings, 'display_shot_strip')
        row.prop(scn_settings, 'color_shot_strip', text="")

        row = layout.row()
        row.prop(scn_settings, 'display_audio_sync_warning')
        row.prop(scn_settings, 'color_audio_sync', text="")

        row = layout.row()
        row.prop(scn_settings, 'display_shot_update_warning')
        row.prop(scn_settings, 'color_update_warning', text="")

        row = layout.row()
        row.prop(scn_settings, 'display_shot_version_warning')
        row.prop(scn_settings, 'color_version_warning', text="")

        row = layout.row()
        row.prop(scn_settings, 'display_working_warning')
        row.prop(scn_settings, 'color_strip_working', text="")


# sequencer UI shot subpanel
class BPM_PT_sequencer_ui_shot_state_subpanel(SequencerPanel):
    bl_label = "State"
    bl_parent_id = "BPM_PT_sequencer_ui_shot_subpanel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        
        scn_settings = context.scene.bpm_scenesettings
        self.layout.prop(scn_settings, "display_shot_state", text = "")

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings
        
        layout = self.layout

        col = layout.column(align=True)
        row = col.row()
        row.prop(scn_settings, 'color_state_storyboard')
        row = col.row()
        row.prop(scn_settings, 'color_state_layout')
        row = col.row()
        row.prop(scn_settings, 'color_state_animation')
        row = col.row()
        row.prop(scn_settings, 'color_state_lighting')
        row = col.row()
        row.prop(scn_settings, 'color_state_rendering')
        row = col.row()
        row.prop(scn_settings, 'color_state_compositing')
        row = col.row()
        row.prop(scn_settings, 'color_state_finished')


# sequencer UI frame comment subpanel
class BPM_PT_sequencer_ui_frame_comment_subpanel(SequencerPanel):
    bl_label = "Comments"
    bl_parent_id = "BPM_PT_sequencer_ui_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.bpm_scenesettings.extra_ui

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

        layout = self.layout

        row = layout.row()
        row.prop(scn_settings, 'display_comments', text = "")
        row.prop(scn_settings, 'color_comments', text="")

        row = layout.row()
        row.label(text = "Names")
        row.prop(scn_settings, 'display_comments_names', text = "")

        row = layout.row()
        row.prop(scn_settings, 'display_comments_boxes', text = "Boxes")
        row.prop(scn_settings, 'color_comments_boxes', text="")

        layout.prop(scn_settings, 'display_comments_text_limit')


# sequencer UI preview subpanel
class BPM_PT_sequencer_ui_preview_subpanel(SequencerPanel):
    bl_label = "Preview"
    bl_parent_id = "BPM_PT_sequencer_ui_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.bpm_scenesettings.extra_ui

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

        layout = self.layout

        row = layout.row()
        row.label(text = "Scheduling")

        row = layout.row()
        row.prop(scn_settings, 'display_shot_todo', text="")
        row.prop(scn_settings, 'color_shot_todo', text="")

        col = layout.column()
        if scn_settings.display_shot_todo != "SPECIFIC_DATE":
            col.enabled = False

        row = col.row(align=True)
        row.prop(scn_settings, 'shot_deadline_preview_yr', text = "")
        row.prop(scn_settings, 'shot_deadline_preview_mn', text = "")
        row.prop(scn_settings, 'shot_deadline_preview_da', text = "")


# shot settings viewport panel
class BPM_PT_properties_shot_viewport_panel(ViewportPanel):
    bl_label = "Shot"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'SHOT'

    def draw(self, context):
        winman = context.window_manager
        shot_settings = winman.bpm_shotsettings

        layout = self.layout

        drawOpenedWarning(layout, winman.bpm_generalsettings)

        drawOperatorAndHelp(layout, 'bpm.render_shot_playlast', '', 'Render-Settings')


# shot tracking viewport subpanel
class BPM_PT_properties_shot_tracking_viewport_subpanel(ViewportPanel):
    bl_label = "Tracking"
    bl_parent_id = "BPM_PT_properties_shot_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        winman = context.window_manager
        shot_settings = winman.bpm_shotsettings

        layout = self.layout

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_state', text="")
        if shot_settings.shot_state != "FINISHED":
            row.prop(shot_settings, getShotTaskComplete(shot_settings)[0], text="")
        drawWikiHelp(row, 'Shot-Datas')

        row = layout.row(align=True)
        row.label(text = "Deadline : " + getShotTaskDeadline(shot_settings)[1], icon = 'TIME')
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='GREASEPENCIL').behavior = 'active_strip'
        drawWikiHelp(row, 'Shot-Task-System')


# shot sync viewport subpanel
class BPM_PT_properties_shot_sync_viewport_subpanel(ViewportPanel):
    bl_label = "Sync"
    bl_parent_id = "BPM_PT_properties_shot_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        winman = context.window_manager
        shot_settings = winman.bpm_shotsettings

        layout = self.layout

        drawOperatorAndHelp(layout, 'bpm.refresh_shot_datas_shot', '', 'Shot-Datas')

        drawOperatorAndHelp(layout, 'bpm.synchronize_audio_shot', '', 'Shot-Audio-Synchronization')

        row = layout.row(align=True)
        row.prop(shot_settings, 'auto_audio_sync')
        drawWikiHelp(row, 'Shot-Audio-Synchronization')


# shot comment viewport subpanel
class BPM_PT_properties_shot_comment_viewport_subpanel(ViewportPanel):
    bl_label = ""
    bl_parent_id = "BPM_PT_properties_shot_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Comments")
        drawWikiHelp(row, "Comments")

    def draw(self, context):

        layout = self.layout

        shot_settings = context.window_manager.bpm_shotsettings

        comment_draw(self.layout, shot_settings.comments, "shot")


# shot render viewport subpanel
class BPM_PT_properties_shot_render_viewport_subpanel(ViewportPanel):
    bl_label = "Render"
    bl_parent_id = "BPM_PT_properties_shot_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        shot_settings = context.window_manager.bpm_shotsettings

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_render_state', text = "Render")
        drawWikiHelp(row, 'Render-Settings')


# shot debug viewport subpanel
class BPM_PT_properties_shot_debug_viewport_subpanel(ViewportPanel):
    bl_label = "Debug"
    bl_parent_id = "BPM_PT_properties_shot_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_projectdatas.debug

    def draw(self, context):

        layout = self.layout

        winman = context.window_manager
        shot_settings = winman.bpm_shotsettings

        drawDebugPanel(layout, shot_settings)


# asset settings viewport panel
class BPM_PT_properties_asset_viewport_panel(ViewportPanel):
    bl_label = "Asset"

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings
        return general_settings.is_project and general_settings.file_type == 'ASSET' and asset_settings.asset_type not in {'NODEGROUP', 'MATERIAL'}

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        drawPropertiesAssetPanel(layout, asset_settings, general_settings)


# asset comment viewport subpanel
class BPM_PT_properties_asset_comments_viewport_subpanel(ViewportPanel):
    bl_label = ""
    bl_parent_id = "BPM_PT_properties_asset_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Comments")
        drawWikiHelp(row, "Comments")

    def draw(self, context):
        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        comment_draw(self.layout, asset_settings.comments, "asset")


# asset settings debug viewport subpanel
class BPM_PT_properties_asset_debug_viewport_subpanel(ViewportPanel):
    bl_label = "Debug"
    bl_parent_id = "BPM_PT_properties_asset_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_projectdatas.debug

    def draw(self, context):

        layout = self.layout

        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        drawDebugAssetPanel(layout, asset_settings)


# asset settings nodetree panel
class BPM_PT_properties_asset_nodetree_panel(NodetreePanel):
    bl_label = "Asset"

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings
        return general_settings.is_project and general_settings.file_type == 'ASSET' and asset_settings.asset_type in {'NODEGROUP', 'MATERIAL'}

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        drawPropertiesAssetPanel(layout, asset_settings, general_settings)


# asset comment nodetree subpanel
class BPM_PT_properties_asset_comments_nodetree_subpanel(NodetreePanel):
    bl_label = ""
    bl_parent_id = "BPM_PT_properties_asset_nodetree_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Comments")
        drawWikiHelp(row, "Comments")

    def draw(self, context):
        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        comment_draw(self.layout, asset_settings.comments, "asset")


# asset settings nodetree debug subpanel
class BPM_PT_properties_asset_debug_nodetree_subpanel(NodetreePanel):
    bl_label = "Debug"
    bl_parent_id = "BPM_PT_properties_asset_nodetree_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_projectdatas.debug

    def draw(self, context):

        layout = self.layout

        winman = context.window_manager
        asset_settings = winman.bpm_assetsettings

        drawDebugAssetPanel(layout, asset_settings)


# shot browse viewport panel
class BPM_PT_properties_browse_viewport_panel(ViewportPanel):
    bl_label = "Browse"

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            return general_settings.file_type in {"SHOT", "ASSET"}
 
    def draw(self, context):

        draw_browse_panel(self.layout)


# shot browse nodetree panel
class BPM_PT_properties_browse_nodetree_panel(NodetreePanel):
    bl_label = "Browse"

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings
        return general_settings.is_project and general_settings.file_type == "ASSET" and asset_settings.asset_type in {"NODEGROUP","MATERIAL"}

    def draw(self, context):

        draw_browse_panel(self.layout)


# asset library nodetree panel
class BPM_PT_properties_asset_library_nodetree_panel(NodetreePanel):
    bl_label = ""

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings
        return general_settings.is_project and general_settings.file_type == 'ASSET' and asset_settings.asset_type in {'NODEGROUP', 'MATERIAL'}

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Assets")
        drawWikiHelp(row, 'Asset-Management')

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        drawOpenedWarning(layout, winman.bpm_generalsettings)

        drawAssetLibrary(layout, winman)

        if winman.bpm_generalsettings.file_type in {'SHOT', 'ASSET'}:
            layout.operator("bpm.import_asset", icon = "LINK_BLEND")


# asset library viewport panel
class BPM_PT_properties_asset_library_viewport_panel(ViewportPanel):
    bl_label = ""

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        if general_settings.is_project:
            if general_settings.file_type == 'SHOT':
                return True
            elif general_settings.file_type == 'ASSET':
                if winman.bpm_assetsettings.asset_type not in {'NODEGROUP', 'MATERIAL'}:
                    return True

    def draw_header(self, context):
        row = self.layout.row()
        row.label(text = "Assets")
        drawWikiHelp(row, 'Asset-Management')

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        drawOpenedWarning(layout, winman.bpm_generalsettings)

        drawAssetLibrary(layout, winman)

        if winman.bpm_generalsettings.file_type in {'SHOT', 'ASSET'}:
            layout.operator("bpm.import_asset", icon = "LINK_BLEND")


# topbar file menu
class BPM_MT_topbar_menu(bpy.types.Menu):
    bl_label = "BPM"
    bl_idname = "BPM_MT_topbar_menu"

    def draw(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        drawOpenedWarning(layout, general_settings)
        
        if not general_settings.is_project:
            layout.operator('bpm.create_project')  
        
        else:

            project_data = winman.bpm_projectdatas
            layout.label(text = project_data.name)

            layout.operator('bpm.display_modify_project_settings')
            layout.operator('bpm.display_modify_render_settings')
                                

# project folder ui list
class BPM_UL_Folders_Uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        layout.label(text = item.name)


# filebrowser gui
class BPM_PT_FileBrowser_Panel(FilebrowserPanel):
    bl_label = "BPM"
    
    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project
    
    def draw(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        row = layout.row(align=True)
        row.menu('BPM_MT_OpenFolder_Filebrowser_Menu')
        drawWikiHelp(row, 'Project-Architecture')
        
        layout.template_list("BPM_UL_Folders_Uilist", "", winman, "bpm_customfolders", general_settings, "custom_folders_index", rows=4)


# open folder menu
class BPM_MT_OpenFolder_Explorer_Menu(bpy.types.Menu):
    bl_label = "Open Folders"

    def draw(self, context):
        layout = self.layout
        
        drawOpenFoldersPanel(layout, False)


# open folder menu
class BPM_MT_OpenFolder_Filebrowser_Menu(bpy.types.Menu):
    bl_label = "Open Folders"

    def draw(self, context):
        layout = self.layout
        
        drawOpenFoldersPanel(layout, True)


# right click sequencer general menu
class BPM_MT_RightClickSequencerManagement_Menu(bpy.types.Menu):
    bl_label = "BPM Management"

    def draw(self, context):
        layout = self.layout

        layout.operator('bpm.create_shot')
        layout.operator('bpm.synchronize_audio_edit')
        layout.operator('bpm.refresh_shot_datas_edit')


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
        layout.menu('BPM_MT_RightClickSequencerManagement_Menu')

        if scn.sequence_editor.active_strip:
            active_strip = scn.sequence_editor.active_strip
            if active_strip.type in {'SCENE', 'IMAGE'}:
                if active_strip.bpm_shotsettings.is_shot:

                    layout.menu('BPM_MT_RightClickSequencerShot_Menu')

        layout.separator()