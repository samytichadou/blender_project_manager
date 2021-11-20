import bpy

from . import gui_classes
from . import gui_common

### PANELS ###

### SEQUENCER PANELS ###

# sequencer edit panel
class BPM_PT_sequencer_edit_panel(gui_classes.SequencerPanel_Editing):
    bl_label = "Edit"

    def draw(self, context):
        winman = context.window_manager
        project_data = context.window_manager.bpm_projectdatas
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        gui_common.draw_operator_and_help(layout, 'bpm.create_shot', '', 'Create-Shot-Operator')

        gui_common.draw_operator_and_help(layout, 'bpm.synchronize_audio_edit', '', 'Shot-Audio-Synchronization')

        gui_common.draw_operator_and_help(layout, 'bpm.refresh_edit_datas', '', 'Shot-Datas')

        gui_common.draw_operator_and_help(layout, 'bpm.update_shot_duration', '', 'Update-Shot-Operator')

        gui_common.draw_operator_and_help(layout, 'bpm.render_shot_edit', '', 'Shot-Rendering')

        gui_common.draw_next_previous_comment(layout)

# sequencer edit comment panel
class BPM_PT_sequencer_edit_comment_panel(gui_classes.SequencerPanel_Editing):
    bl_label = "Comments"

    def draw(self, context):

        layout = self.layout
        
        comments = context.window_manager.bpm_projectdatas.comments

        gui_common.draw_comment(layout, comments, "edit", context)

# sequencer UI panel
class BPM_PT_sequencer_edit_ui_panel(gui_classes.SequencerPanel_Editing):
    bl_label = "UI"

    def draw(self, context):

        general_settings = context.window_manager.bpm_generalsettings
        scn_settings = context.scene.bpm_scenesettings

        layout = self.layout

        row = layout.row(align=True)
        row.prop(scn_settings, "extra_ui", text = "UI")
        gui_common.draw_wiki_help(row, 'Extra-UI-in-Sequencer')

# sequencer UI shot subpanel
class BPM_PT_sequencer_edit_ui_shot_subpanel(gui_classes.SequencerPanel_Editing):
    bl_label = "Shots"
    bl_parent_id = "BPM_PT_sequencer_edit_ui_panel"

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

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

        row = layout.row()
        row.prop(scn_settings, 'display_rendering_warning')
        row.prop(scn_settings, 'color_strip_rendering', text="")

# sequencer UI shot state subpanel
class BPM_PT_sequencer_edit_ui_shot_state_subpanel(gui_classes.SequencerPanel_Editing):
    bl_label = ""
    bl_parent_id = "BPM_PT_sequencer_edit_ui_shot_subpanel"

    def draw_header(self, context):
        scn_settings = context.scene.bpm_scenesettings
        self.layout.label(text = "State")
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
class BPM_PT_sequencer_edit_ui_shot_frame_comment_subpanel(gui_classes.SequencerPanel_Editing):
    bl_label = ""
    bl_parent_id = "BPM_PT_sequencer_edit_ui_shot_subpanel"

    def draw_header(self, context):
        scn_settings = context.scene.bpm_scenesettings
        self.layout.label(text = "Comments")
        self.layout.prop(scn_settings, "display_shot_comments", text = "")

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

        gui_common.draw_shot_comments_ui(self.layout, scn_settings)

# sequencer UI frame comment subpanel
class BPM_PT_sequencer_edit_ui_timeline_frame_comment_subpanel(gui_classes.SequencerPanel_Editing):
    bl_label = ""
    bl_parent_id = "BPM_PT_sequencer_edit_ui_panel"

    def draw_header(self, context):
        scn_settings = context.scene.bpm_scenesettings
        self.layout.label(text = "Timeline Comments")
        self.layout.prop(scn_settings, "display_timeline_comments", text = "")

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

        layout = self.layout

        layout.prop(scn_settings, 'color_timeline_comments', text="Color")
        
        row = layout.row()
        row.label(text = "Names")
        row.prop(scn_settings, 'display_timeline_comments_names', text = "")

        row = layout.row()
        row.prop(scn_settings, 'display_timeline_comments_boxes', text = "Name Boxes")
        row.prop(scn_settings, 'color_timeline_comments_boxes', text="")

        layout.prop(scn_settings, 'display_timeline_comments_text_limit')

        #layout.prop(scn_settings, "test_prop")

# sequencer UI scheduling subpanel
class BPM_PT_sequencer_edit_ui_scheduling_subpanel(gui_classes.SequencerPanel_Editing):
    bl_label = "Scheduling"
    bl_parent_id = "BPM_PT_sequencer_edit_ui_panel"

    def draw(self, context):

        scn_settings = context.scene.bpm_scenesettings

        layout = self.layout

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



### REGISTER ---

def register():
    bpy.utils.register_class(BPM_PT_sequencer_edit_panel)
    bpy.utils.register_class(BPM_PT_sequencer_edit_comment_panel)
    bpy.utils.register_class(BPM_PT_sequencer_edit_ui_panel)
    bpy.utils.register_class(BPM_PT_sequencer_edit_ui_shot_subpanel)
    bpy.utils.register_class(BPM_PT_sequencer_edit_ui_shot_state_subpanel)
    bpy.utils.register_class(BPM_PT_sequencer_edit_ui_shot_frame_comment_subpanel)
    bpy.utils.register_class(BPM_PT_sequencer_edit_ui_timeline_frame_comment_subpanel)
    bpy.utils.register_class(BPM_PT_sequencer_edit_ui_scheduling_subpanel)


def unregister():
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_comment_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_ui_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_ui_shot_subpanel)
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_ui_shot_state_subpanel)
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_ui_shot_frame_comment_subpanel)
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_ui_timeline_frame_comment_subpanel)
    bpy.utils.unregister_class(BPM_PT_sequencer_edit_ui_scheduling_subpanel)