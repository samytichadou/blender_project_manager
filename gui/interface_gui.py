import bpy

from . import gui_classes

# sequencer panels display
class BPM_PT_sequencer_panels_display_panel(gui_classes.SequencerPanel_General):
    bl_label = "Interface"

    def draw(self, context):
        scn_settings = context.scene.bpm_scenesettings

        layout = self.layout

        layout.prop(scn_settings, "display_panels", expand=True)

# viewport display panel
class BPM_PT_viewport_panels_display_panel(gui_classes.ViewportPanel_General):
    bl_label = "Interface"

    def draw(self, context):
        scn_settings = context.scene.bpm_scenesettings
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        layout.prop(scn_settings, "display_panels", expand=True)

# nodetree panels display
class BPM_PT_nodetree_panels_display_panel(gui_classes.NodetreePanel_General):
    bl_label = "Interface"

    def draw(self, context):
        scn_settings = context.scene.bpm_scenesettings
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        layout.prop(scn_settings, "display_panels", expand=True)


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_PT_sequencer_panels_display_panel)
    bpy.utils.register_class(BPM_PT_viewport_panels_display_panel)
    bpy.utils.register_class(BPM_PT_nodetree_panels_display_panel)

def unregister():
    bpy.utils.unregister_class(BPM_PT_sequencer_panels_display_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_panels_display_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_panels_display_panel)
