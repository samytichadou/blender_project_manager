import bpy


# sequencer function
def bpmSequencerMenuFunction(self, context):
    if context.space_data.view_type in {'SEQUENCER', 'SEQUENCER_PREVIEW'}:
        if context.window_manager.bpm_isproject and context.window_manager.bpm_isedit:
            self.layout.menu('BPM_MT_sequencer_menu')

# sequencer menu
class BPM_MT_sequencer_menu(bpy.types.Menu):
    bl_label = "BPM"
    bl_idname = "BPM_MT_sequencer_menu"

    def draw(self, context):
        winman = context.window_manager
        project_data = winman.bpm_datas[0]
        sequencer = context.scene.sequence_editor

        layout = self.layout

        #common
        layout.label(text = project_data.name)
        layout.operator('bpm.create_shot')
        layout.operator('bpm.open_shot')
        layout.operator('bpm.update_shot_duration')
        layout.separator()
        layout.label(text = "Markers")
        layout.prop(context.scene, 'bpm_displaymarkers', text='')
        layout.prop(context.scene, 'bpm_displaymarkernames', text='')
        layout.prop(context.scene, 'bpm_extraui')
        layout.prop(context.scene, 'bpm_displaymarkerboxes')
        layout.prop(context.scene, 'bpm_displaymarkerlimit', text='')
        layout.prop(context.scene, 'bpm_displayshotupdatewarning')
        layout.separator()
        if winman.bpm_debug: #debug
            layout.label(text = "Debug")
            if sequencer.active_strip:
                active = sequencer.active_strip
                if active.type == 'SCENE':
                    layout.prop(active, 'bpm_isshot')
                    layout.prop(active, 'bpm_displaymarkers')

# topbar function
def bpmTopbarFunction(self, context):
    if context.region.alignment == 'RIGHT':
        winman = context.window_manager
        if winman.bpm_isproject:
            if not winman.bpm_isedit:
                self.layout.operator('bpm.back_to_edit')
            # else:
            #     self.layout.operator('bpm.open_shot')
            self.layout.menu('BPM_MT_topbar_menu')

# topbar menu
class BPM_MT_topbar_menu(bpy.types.Menu):
    bl_label = "BPM"
    bl_idname = "BPM_MT_topbar_menu"

    def draw(self, context):
        winman = context.window_manager
        project_data = winman.bpm_datas[0]

        layout = self.layout
        layout.label(text = project_data.name)
        layout.operator('bpm.display_modify_project_settings')

        #debug
        layout.separator()
        layout.label(text='Debug')
        layout.prop(winman, 'bpm_debug')
        layout.prop(winman, 'bpm_isproject')
        layout.prop(winman, 'bpm_isedit')

# project folder ui list
class BPM_UL_Folders_Uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        layout.label(text = item.name)

# filebrowser gui
class BPM_PT_FileBrowser_Panel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "BPM"
    bl_label = "BPM Project Folders"
    bl_idname = "BPM_PT_FileBrowser_Panel"
    
    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_folders
    
    def draw(self, context):
        winman = context.window_manager

        layout = self.layout
        layout.template_list("BPM_UL_Folders_Uilist", "", winman, "bpm_folders", winman, "bpm_foldersindex", rows=4)

# new bpm function topbar app menu
def createProjectAppMenuFunction(self, context):
    self.layout.separator()
    self.layout.operator('bpm.create_project')    