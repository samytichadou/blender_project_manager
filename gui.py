import bpy


# sequencer menu
class BPM_PT_sequencer_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "BPM"
    bl_idname = "BPM_PT_sequencer_panel"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject and context.window_manager.bpm_isedit

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
        layout.label(text = "Extra UI")
        layout.prop(context.scene, 'bpm_extraui')
        layout.prop(context.scene, 'bpm_displayshotstrip')
        layout.prop(context.scene, 'bpm_displayshotupdatewarning')
        layout.prop(context.scene, 'bpm_displaymarkers')
        layout.prop(context.scene, 'bpm_displaymarkernames')
        layout.prop(context.scene, 'bpm_displaymarkerboxes')
        layout.prop(context.scene, 'bpm_displaymarkerlimit')
        layout.separator()
        if winman.bpm_debug: #debug
            layout.label(text = "Debug")
            if sequencer.active_strip:
                active = sequencer.active_strip
                if active.type == 'SCENE':
                    layout.prop(active, 'bpm_isshot')
                    layout.prop(active, 'bpm_displaymarkers')


# bpm function topbar back/open operators
def bpmTopbarFunction(self, context):
    if context.region.alignment == 'RIGHT':
        winman = context.window_manager
        if winman.bpm_isproject:
            if not winman.bpm_isedit:
                self.layout.operator('bpm.back_to_edit', icon = "SEQ_SEQUENCER")
            else:
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
        project_data = winman.bpm_datas[0]

        layout = self.layout
        
        if not winman.bpm_isproject:
            layout.operator('bpm.create_project')  
        
        else:
            layout.label(text = project_data.name)
            layout.operator('bpm.display_modify_project_settings')
            layout.separator()

            #debug
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