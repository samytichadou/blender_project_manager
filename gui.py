import bpy


class BpmSequencerPanel(bpy.types.Panel):
    bl_label = "Project Manager"
    bl_idname = "BPM_PT_sequencer"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "BPM"

    @staticmethod
    def has_sequencer(context):
        return (context.space_data.view_type in {'SEQUENCER', 'SEQUENCER_PREVIEW'})

    @classmethod
    def poll(cls, context):
        return cls.has_sequencer(context) and context.window_manager.bpm_isproject and context.window_manager.bpm_isedit

    def draw(self, context):
        winman = context.window_manager
        project_data = winman.bpm_datas[0]

        layout = self.layout

        #common
        layout.label(text = project_data.name)
        layout.operator('bpm.open_shot')

        #debug
        layout.prop(winman, 'bpm_debug')
        layout.prop(winman, 'bpm_isproject')
        layout.prop(winman, 'bpm_isedit')

