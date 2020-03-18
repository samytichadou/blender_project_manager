import bpy


# sequencer panel
class BPM_PT_sequencer(bpy.types.Panel):
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
class BpmTopbarMenu(bpy.types.Menu):
    bl_label = "BPM"
    bl_idname = "BPM_MT_topbar_menu"

    def draw(self, context):
        winman = context.window_manager
        project_data = winman.bpm_datas[0]

        layout = self.layout
        layout.label(text = project_data.name)
        layout.operator('bpm.display_project_settings')

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