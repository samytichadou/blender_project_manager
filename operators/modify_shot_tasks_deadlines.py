import bpy

from ..functions.date_functions import getDateYearString
from ..functions.shot_settings_json_update_function import updateShotSettingsProperties
from ..functions.strip_functions import returnSelectedStrips
from .. import global_variables as g_var


class BPM_OT_modify_shot_task_deadline(bpy.types.Operator):
    """Modify shot tasks deadlines"""
    bl_idname = "bpm.modify_shot_tasks_deadlines"
    bl_label = "Modify deadlines"
    bl_options = {'REGISTER', 'INTERNAL'}

    shot_settings = None
    behavior : bpy.props.StringProperty()

    #calendar properties

    st_yr : bpy.props.IntProperty(name = "Year", min = int(getDateYearString()))
    st_mn : bpy.props.IntProperty(name = "Month", min = 1, max = 12)
    st_da : bpy.props.IntProperty(name = "Day", min = 1, max = 31)

    la_yr : bpy.props.IntProperty(name = "Year", min = int(getDateYearString()))
    la_mn : bpy.props.IntProperty(name = "Month", min = 1, max = 12)
    la_da : bpy.props.IntProperty(name = "Day", min = 1, max = 31)

    an_yr : bpy.props.IntProperty(name = "Year", min = int(getDateYearString()))
    an_mn : bpy.props.IntProperty(name = "Month", min = 1, max = 12)
    an_da : bpy.props.IntProperty(name = "Day", min = 1, max = 31)

    li_yr : bpy.props.IntProperty(name = "Year", min = int(getDateYearString()))
    li_mn : bpy.props.IntProperty(name = "Month", min = 1, max = 12)
    li_da : bpy.props.IntProperty(name = "Day", min = 1, max = 31)

    re_yr : bpy.props.IntProperty(name = "Year", min = int(getDateYearString()))
    re_mn : bpy.props.IntProperty(name = "Month", min = 1, max = 12)
    re_da : bpy.props.IntProperty(name = "Day", min = 1, max = 31)

    co_yr : bpy.props.IntProperty(name = "Year", min = int(getDateYearString()))
    co_mn : bpy.props.IntProperty(name = "Month", min = 1, max = 12)
    co_da : bpy.props.IntProperty(name = "Day", min = 1, max = 31)

    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type =='SHOT':
                return True
            elif context.window_manager.bpm_generalsettings.file_type =='EDIT':
                keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
                if keyword in context.scene.name:
                    if context.scene.sequence_editor:
                        if context.scene.sequence_editor.active_strip:
                            active = context.scene.sequence_editor.active_strip
                            if active.type in {'SCENE', 'IMAGE'}:
                                if not active.lock:
                                    if active.bpm_shotsettings.is_shot:
                                        return True

    def invoke(self, context, event):
        winman = context.window_manager

        # set settings depending on file type
        if winman.bpm_generalsettings.file_type == 'EDIT':
            self.shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        else:
            self.shot_settings = winman.bpm_shotsettings

        # storyboard
        self.st_yr = int(self.shot_settings.storyboard_deadline.split("-")[0])
        self.st_mn = int(self.shot_settings.storyboard_deadline.split("-")[1])
        self.st_da = int(self.shot_settings.storyboard_deadline.split("-")[2])

        # layout
        self.la_yr = int(self.shot_settings.layout_deadline.split("-")[0])
        self.la_mn = int(self.shot_settings.layout_deadline.split("-")[1])
        self.la_da = int(self.shot_settings.layout_deadline.split("-")[2])
        
        # animation
        self.an_yr = int(self.shot_settings.animation_deadline.split("-")[0])
        self.an_mn = int(self.shot_settings.animation_deadline.split("-")[1])
        self.an_da = int(self.shot_settings.animation_deadline.split("-")[2])

        # lighting
        self.li_yr = int(self.shot_settings.lighting_deadline.split("-")[0])
        self.li_mn = int(self.shot_settings.lighting_deadline.split("-")[1])
        self.li_da = int(self.shot_settings.lighting_deadline.split("-")[2])

        # rendering
        self.re_yr = int(self.shot_settings.rendering_deadline.split("-")[0])
        self.re_mn = int(self.shot_settings.rendering_deadline.split("-")[1])
        self.re_da = int(self.shot_settings.rendering_deadline.split("-")[2])

        # compositing
        self.co_yr = int(self.shot_settings.compositing_deadline.split("-")[0])
        self.co_mn = int(self.shot_settings.compositing_deadline.split("-")[1])
        self.co_da = int(self.shot_settings.compositing_deadline.split("-")[2])

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout

        if self.behavior == "selected_strips":
            layout.label(text = "Selected strips")
        else:
            layout.label(text = "Active strip")

        # storyboard
        row = layout.row(align=True)
        row.label(text="Storyboard")
        row.prop(self, 'st_yr', text='')
        row.prop(self, 'st_mn', text='')
        row.prop(self, 'st_da', text='')

        # layout
        row = layout.row(align=True)
        row.label(text="Layout")
        row.prop(self, 'la_yr', text='')
        row.prop(self, 'la_mn', text='')
        row.prop(self, 'la_da', text='')

        # storyboard
        row = layout.row(align=True)
        row.label(text="Animation")
        row.prop(self, 'an_yr', text='')
        row.prop(self, 'an_mn', text='')
        row.prop(self, 'an_da', text='')

        # storyboard
        row = layout.row(align=True)
        row.label(text="Lighting")
        row.prop(self, 'li_yr', text='')
        row.prop(self, 'li_mn', text='')
        row.prop(self, 'li_da', text='')

        # storyboard
        row = layout.row(align=True)
        row.label(text="Rendering")
        row.prop(self, 're_yr', text='')
        row.prop(self, 're_mn', text='')
        row.prop(self, 're_da', text='')

        # storyboard
        row = layout.row(align=True)
        row.label(text="Compositing")
        row.prop(self, 'co_yr', text='')
        row.prop(self, 'co_mn', text='')
        row.prop(self, 'co_da', text='')

    def execute(self, context):
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = context.window_manager.bpm_generalsettings

        if debug: print(g_var.shot_deadlines_modification_statement) #debug

        # format temp properties
        st = str(self.st_yr) + "-" + str(self.st_mn).zfill(2) + "-"  + str(self.st_da).zfill(2)
        la = str(self.la_yr) + "-" + str(self.la_mn).zfill(2) + "-"  + str(self.la_da).zfill(2)
        an = str(self.an_yr) + "-" + str(self.an_mn).zfill(2) + "-"  + str(self.an_da).zfill(2)
        li = str(self.li_yr) + "-" + str(self.li_mn).zfill(2) + "-"  + str(self.li_da).zfill(2)
        re = str(self.re_yr) + "-" + str(self.re_mn).zfill(2) + "-"  + str(self.re_da).zfill(2)
        co = str(self.co_yr) + "-" + str(self.co_mn).zfill(2) + "-"  + str(self.co_da).zfill(2)

        # update active shot
        self.shot_settings.storyboard_deadline = st
        self.shot_settings.layout_deadline = la
        self.shot_settings.animation_deadline = an
        self.shot_settings.lighting_deadline = li
        self.shot_settings.rendering_deadline = re
        self.shot_settings.compositing_deadline = co

        updateShotSettingsProperties(self.shot_settings, context)

        if debug: print(g_var.deadlines_modified_statement + "active shot") #debug

        if general_settings.file_type == 'EDIT' and self.behavior == "selected_strips":

            sequencer = context.scene.sequence_editor

            for s in returnSelectedStrips(sequencer):
               
                if s != sequencer.active_strip:

                    shot_settings = s.bpm_shotsettings
                    
                    shot_settings.storyboard_deadline = st
                    shot_settings.layout_deadline = la
                    shot_settings.animation_deadline = an
                    shot_settings.lighting_deadline = li
                    shot_settings.rendering_deadline = re
                    shot_settings.compositing_deadline = co

                    updateShotSettingsProperties(shot_settings, context)

                    if debug: print(g_var.deadlines_modified_statement + s.name) #debug

        # reload sequencer
        bpy.ops.sequencer.refresh_all()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_modify_shot_task_deadline)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_modify_shot_task_deadline)