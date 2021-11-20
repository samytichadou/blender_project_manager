import bpy

from . import gui_classes
from . import gui_common
from ..functions import project_data_functions as pjt_dta_fct


### DRAW FCTS ###

# draw shot tracking
def draw_shot_tracking_shot_file(container, winman):

    shot_settings = winman.bpm_shotsettings

    row = container.row(align=True)
    row.prop(shot_settings, 'shot_state', text="")
    if shot_settings.shot_state != "FINISHED":
        row.prop(shot_settings, pjt_dta_fct.getShotTaskComplete(shot_settings)[0], text="")
    gui_common.draw_wiki_help(row, 'Shot-Datas')

    row = container.row(align=True)
    row.label(text = "Deadline : " + pjt_dta_fct.getShotTaskDeadline(shot_settings)[1], icon = 'TIME')
    row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='GREASEPENCIL').behavior = 'active_strip'
    gui_common.draw_wiki_help(row, 'Shot-Task-System')

    gui_common.draw_operator_and_help(container, 'bpm.refresh_shot_datas', '', 'Shot-Datas')

    gui_common.draw_operator_and_help(container, 'bpm.synchronize_audio_shot', '', 'Shot-Audio-Synchronization')

    row = container.row(align=True)
    row.prop(shot_settings, 'auto_audio_sync')
    gui_common.draw_wiki_help(row, 'Shot-Audio-Synchronization')

    row = container.row(align=True)
    row.prop(shot_settings, 'shot_render_state', text = "Render")
    gui_common.draw_wiki_help(row, 'Render-Settings')

# draw shot version
def draw_shot_version_shot_file(container, winman):

    shot_settings = winman.bpm_shotsettings

    container.label(text = "version " + str(shot_settings.shot_version_file) + "/" + str(shot_settings.shot_last_version))

    container.label(text = "used in edit " + str(shot_settings.shot_version_used) + "/" + str(shot_settings.shot_last_version))
    
    gui_common.draw_operator_and_help(container, "bpm.bump_shot_version_shot", "", "Shot-Version-Management")

# draw shot render
def draw_shot_render_shot_file(container):
    
    gui_common.draw_operator_and_help(container, 'bpm.render_shot_playlast', '', 'Render-Settings')


### PANELS ###

### SEQUENCER PANELS ###

# sequencer tracking shot panel
class BPM_PT_sequencer_shot_tracking_panel(gui_classes.SequencerPanel_Shot):
    bl_label = "Tracking"

    def draw(self, context):

        layout = self.layout

        active = context.scene.sequence_editor.active_strip
        shot_settings = active.bpm_shotsettings

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_state', text="")
        if shot_settings.shot_state != "FINISHED":
            row.prop(shot_settings, pjt_dta_fct.getShotTaskComplete(shot_settings)[0], text="")
        gui_common.draw_wiki_help(row, 'Shot-Datas')

        row = layout.row(align=True)
        row.label(text = "Deadline : " + pjt_dta_fct.getShotTaskDeadline(shot_settings)[1], icon = 'TIME')
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='GREASEPENCIL').behavior = 'active_strip'
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='SEQ_STRIP_DUPLICATE').behavior = 'selected_strips'
        gui_common.draw_wiki_help(row, 'Shot-Task-System')

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_render_state', text = "Render")
        gui_common.draw_wiki_help(row, 'Render-Settings')

        row = layout.row(align=True)
        row.prop(shot_settings, 'auto_audio_sync')
        gui_common.draw_wiki_help(row, 'Shot-Audio-Synchronization')

# sequencer version shot panel
class BPM_PT_sequencer_shot_version_panel(gui_classes.SequencerPanel_Shot):
    bl_label = "Version"

    def draw(self, context):

        layout = self.layout

        active = context.scene.sequence_editor.active_strip
        shot_settings = active.bpm_shotsettings

        layout.label(text = "version " + str(shot_settings.shot_version_used) + "/" + str(shot_settings.shot_last_version))

        gui_common.draw_operator_and_help(layout, 'bpm.bump_shot_version_edit', '', 'Shot-Version-Management')

        gui_common.draw_operator_and_help(layout, 'bpm.change_shot_version_edit', '', 'Shot-Version-Management')

        row = layout.row(align=True)
        row.operator('bpm.change_shot_version_edit', text = "Last shot version").go_to_last_version = True
        row.operator('bpm.open_wiki_page', text='', icon='QUESTION').wiki_page = 'Shot-Version-Management'

# sequencer comment shot panel
class BPM_PT_sequencer_shot_comment_panel(gui_classes.SequencerPanel_Shot):
    bl_label = "Comments"

    def draw(self, context):

        layout = self.layout
        
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings

        gui_common.draw_next_previous_comment(layout)

        gui_common.draw_comment(layout, shot_settings.comments, "edit_shot", context)

# sequencer display shot panel
class BPM_PT_sequencer_shot_display_panel(gui_classes.SequencerPanel_Shot):
    bl_label = "Timeline Display"

    def draw(self, context):

        layout = self.layout

        active = context.scene.sequence_editor.active_strip
        shot_settings = active.bpm_shotsettings

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_timeline_display', text = "")
        gui_common.draw_wiki_help(row, 'Timeline-Shot-Display-Mode')

        layout.prop(shot_settings, 'display_comments')

# sequencer shot debug panel
class BPM_PT_sequencer_shot_debug_panel(gui_classes.SequencerPanel_Shot_Debug):
    bl_label = "Debug"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings

        gui_common.draw_debug(layout, shot_settings)

### VIEWPORT PANELS ###

# shot tracking viewport panel
class BPM_PT_viewport_shot_tracking_panel(gui_classes.ViewportPanel_Shot):
    bl_label = "Tracking"

    def draw(self, context):

        winman = context.window_manager

        layout = self.layout

        draw_shot_tracking_shot_file(layout, winman)
       
# shot version viewport panel
class BPM_PT_viewport_shot_version_panel(gui_classes.ViewportPanel_Shot):
    bl_label = "Version"

    def draw(self, context):
        
        winman = context.window_manager

        layout = self.layout

        draw_shot_version_shot_file(layout, winman)

# shot comment viewport panel
class BPM_PT_viewport_shot_comment_panel(gui_classes.ViewportPanel_Shot):
    bl_label = "Comments"

    def draw(self, context):

        layout = self.layout

        shot_settings = context.window_manager.bpm_shotsettings

        gui_common.draw_next_previous_comment(layout)

        gui_common.draw_comment(layout, shot_settings.comments, "shot", context)

# shot comment ui viewport subpanel
class BPM_PT_viewport_shot_ui_comment_subpanel(gui_classes.ViewportPanel_Shot):
    bl_label = ""
    bl_parent_id = "BPM_PT_viewport_shot_comment_panel"

    def draw_header(self, context):
        scn_settings = context.scene.bpm_scenesettings
        self.layout.label(text = "Comments UI")
        self.layout.prop(scn_settings, "extra_ui", text = "")

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

        gui_common.draw_shot_comments_ui(self.layout, scn_settings)

# shot render viewport subpanel
class BPM_PT_viewport_shot_render_panel(gui_classes.ViewportPanel_Shot):
    bl_label = "Render"

    def draw(self, context):

        layout = self.layout

        draw_shot_render_shot_file(layout)

# shot debug viewport subpanel
class BPM_PT_viewport_shot_debug_panel(gui_classes.ViewportPanel_Shot_Debug):
    bl_label = "Debug"

    def draw(self, context):

        layout = self.layout

        winman = context.window_manager
        shot_settings = winman.bpm_shotsettings

        gui_common.draw_debug(layout, shot_settings)

### NODETREE PANELS ###

# nodetree shot tracking panel
class BPM_PT_nodetree_shot_tracking_panel(gui_classes.NodetreePanel_Shot):
    bl_label = "Tracking"

    def draw(self, context):

        winman = context.window_manager

        layout = self.layout

        draw_shot_tracking_shot_file(layout, winman)

# nodetree shot version panel
class BPM_PT_nodetree_shot_version_panel(gui_classes.NodetreePanel_Shot):
    bl_label = "Version"

    def draw(self, context):

        winman = context.window_manager

        layout = self.layout

        draw_shot_version_shot_file(layout, winman)

# nodetree shot comment panel
class BPM_PT_nodetree_shot_comment_panel(gui_classes.NodetreePanel_Shot):
    bl_label = "Comments"

    def draw(self, context):

        layout = self.layout

        shot_settings = context.window_manager.bpm_shotsettings

        gui_common.draw_next_previous_comment(layout)

        gui_common.draw_comment(layout, shot_settings.comments, "shot", context)

# nodetree shot render panel
class BPM_PT_nodetree_shot_render_panel(gui_classes.NodetreePanel_Shot):
    bl_label = "Render"

    def draw(self, context):

        layout = self.layout

        draw_shot_render_shot_file(layout)

# nodetree shot debug panel
class BPM_PT_nodetree_shot_debug_panel(gui_classes.NodetreePanel_Shot_Debug):
    bl_label = "Debug"

    def draw(self, context):

        layout = self.layout

        winman = context.window_manager
        shot_settings = winman.bpm_shotsettings

        gui_common.draw_debug(layout, shot_settings)



### REGISTER ---

def register():
    bpy.utils.register_class(BPM_PT_sequencer_shot_tracking_panel)
    bpy.utils.register_class(BPM_PT_sequencer_shot_version_panel)
    bpy.utils.register_class(BPM_PT_sequencer_shot_comment_panel)
    bpy.utils.register_class(BPM_PT_sequencer_shot_display_panel)
    bpy.utils.register_class(BPM_PT_sequencer_shot_debug_panel)

    bpy.utils.register_class(BPM_PT_viewport_shot_tracking_panel)
    bpy.utils.register_class(BPM_PT_viewport_shot_version_panel)
    bpy.utils.register_class(BPM_PT_viewport_shot_comment_panel)
    bpy.utils.register_class(BPM_PT_viewport_shot_ui_comment_subpanel)
    bpy.utils.register_class(BPM_PT_viewport_shot_render_panel)
    bpy.utils.register_class(BPM_PT_viewport_shot_debug_panel)

    bpy.utils.register_class(BPM_PT_nodetree_shot_tracking_panel)
    bpy.utils.register_class(BPM_PT_nodetree_shot_version_panel)
    bpy.utils.register_class(BPM_PT_nodetree_shot_comment_panel)
    bpy.utils.register_class(BPM_PT_nodetree_shot_render_panel)
    bpy.utils.register_class(BPM_PT_nodetree_shot_debug_panel)


def unregister():
    bpy.utils.unregister_class(BPM_PT_sequencer_shot_tracking_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_shot_version_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_shot_comment_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_shot_display_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_shot_debug_panel)

    bpy.utils.unregister_class(BPM_PT_viewport_shot_tracking_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_shot_version_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_shot_comment_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_shot_ui_comment_subpanel)
    bpy.utils.unregister_class(BPM_PT_viewport_shot_render_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_shot_debug_panel)

    bpy.utils.unregister_class(BPM_PT_nodetree_shot_tracking_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_shot_version_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_shot_comment_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_shot_render_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_shot_debug_panel)
