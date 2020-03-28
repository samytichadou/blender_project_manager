import bpy


# sequencer management
class BPM_PT_sequencer_management_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Management"
    bl_idname = "BPM_PT_sequencer_management_panel"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject and context.window_manager.bpm_filetype == 'EDIT'

    def draw(self, context):
        winman = context.window_manager
        project_data = winman.bpm_datas[0]

        layout = self.layout

        #common
        layout.label(text = project_data.name)
        layout.operator('bpm.create_shot')
        layout.operator('bpm.create_asset')
        layout.separator()
        layout.prop(winman, 'bpm_debug', text = "Debug")
        if winman.bpm_debug:
            layout.prop(winman, 'bpm_isproject')
            layout.prop(winman, 'bpm_filetype')


# sequencer UI panel
class BPM_PT_sequencer_ui_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "UI"
    bl_idname = "BPM_PT_sequencer_ui_panel"
    bl_category = "BPM"
    bl_parent_id = "BPM_PT_sequencer_management_panel"

    def draw(self, context):
        scn = context.scene

        layout = self.layout

        layout.prop(scn, 'bpm_extraui')
        if scn.bpm_extraui:
            layout.prop(scn, 'bpm_displayshotstrip')
            layout.prop(scn, 'bpm_displayshotupdatewarning')
            layout.prop(scn, 'bpm_displaymarkers')
            layout.prop(scn, 'bpm_displaymarkernames')
            layout.prop(scn, 'bpm_displaymarkerboxes')
            layout.prop(scn, 'bpm_displaymarkerlimit')


# sequencer shot panel
class BPM_PT_sequencer_shot_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Shot"
    bl_idname = "BPM_PT_sequencer_shot_panel"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        chk_isshot = False
        if context.scene.sequence_editor.active_strip:
            active = context.scene.sequence_editor.active_strip
            try:
                if active.bpm_isshot:
                    chk_isshot = True
            except AttributeError:
                return False
        return context.window_manager.bpm_isproject and context.window_manager.bpm_filetype == 'EDIT' and chk_isshot

    def draw(self, context):
        winman = context.window_manager
        sequencer = context.scene.sequence_editor

        layout = self.layout

        layout.operator('bpm.open_shot')
        layout.operator('bpm.update_shot_duration')
        layout.separator()
        if sequencer.active_strip:
            active = sequencer.active_strip
            if active.type == 'SCENE':
                layout.prop(active, 'bpm_displaymarkers')
            if winman.bpm_debug: #debug:
                layout.prop(active, 'bpm_isshot')


# bpm function topbar back/open operators
def bpmTopbarFunction(self, context):
    if context.region.alignment == 'RIGHT':
        winman = context.window_manager
        if winman.bpm_isproject:
            if winman.bpm_filetype in {'SHOT', 'ASSET'}:
                self.layout.operator('bpm.back_to_edit', icon = "SEQ_SEQUENCER")
            elif winman.bpm_filetype == 'EDIT':
                self.layout.operator('bpm.open_shot', icon = "SEQUENCE")
            #self.layout.menu('BPM_MT_topbar_menu')


# bpm function topbar file menu
def bpmFileMenuFunction(self, context):
    self.layout.separator()
    self.layout.menu('BPM_MT_topbar_menu')


# topbar file menu function
class BPM_MT_topbar_menu(bpy.types.Menu):
    bl_label = "BPM"
    bl_idname = "BPM_MT_topbar_menu"

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout
        
        if not winman.bpm_isproject:
            layout.operator('bpm.create_project')  
        
        else:
            project_data = winman.bpm_datas[0]
            layout.label(text = project_data.name)
            layout.operator('bpm.display_modify_project_settings')
            layout.separator()

            #debug
            layout.prop(winman, 'bpm_debug', text = "Debug")
            if winman.bpm_debug:
                layout.prop(winman, 'bpm_isproject')
                layout.prop(winman, 'bpm_filetype')


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