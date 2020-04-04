import bpy


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


# sequencer management
class BPM_PT_sequencer_management_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Management"
    bl_idname = "BPM_PT_sequencer_management_panel"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'

    def draw(self, context):
        winman = context.window_manager
        project_data = context.window_manager.bpm_projectdatas
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        #common
        layout.label(text = project_data.name)

        drawOperatorAndHelp(layout, 'bpm.create_shot', '', 'Create-Shot-Operator')

        drawOperatorAndHelp(layout, 'bpm.delete_unused_shots', '', 'Delete-Unused-Shots')

        drawOperatorAndHelp(layout, 'bpm.empty_recycle_bin', '', 'Empty-Recycle-Bin')

        drawOperatorAndHelp(layout, 'bpm.create_asset', '', 'Create-Asset-Operator')

        drawOperatorAndHelp(layout, 'bpm.synchronize_audio_edit', '', 'Shot-Audio-Synchronization')

        layout.separator()
        layout.prop(general_settings, 'debug', text = "Debug")
        if general_settings.debug:
            box = layout.box()
            box.label(text = 'debug', icon = 'ERROR')
            box.prop(general_settings, 'is_project')
            box.prop(general_settings, 'file_type')


# sequencer UI panel
class BPM_PT_sequencer_ui_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "UI"
    bl_idname = "BPM_PT_sequencer_ui_panel"
    bl_category = "BPM"
    bl_parent_id = "BPM_PT_sequencer_management_panel"

    def draw(self, context):
        scn_settings = context.scene.bpm_scenesettings

        layout = self.layout

        row = layout.row(align=True)
        row.prop(scn_settings, 'extra_ui')
        drawWikiHelp(row, 'Extra-UI-in-Sequencer')
        if scn_settings.extra_ui:
            layout.prop(scn_settings, 'display_shot_strip')
            layout.prop(scn_settings, 'display_shot_update_warning')
            layout.prop(scn_settings, 'display_shot_version_warning')
            layout.prop(scn_settings, 'display_markers')
            layout.prop(scn_settings, 'display_marker_names')
            layout.prop(scn_settings, 'display_marker_boxes')
            layout.prop(scn_settings, 'display_marker_limit')


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
        if context.scene.sequence_editor:
            if context.scene.sequence_editor.active_strip:
                active = context.scene.sequence_editor.active_strip
                try:
                    if active.bpm_shotsettings.is_shot:
                        chk_isshot = True
                except AttributeError:
                    return False
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT' and chk_isshot

    def draw(self, context):
        winman = context.window_manager
        active = context.scene.sequence_editor.active_strip
        general_settings = context.window_manager.bpm_generalsettings
        shot_settings = active.bpm_shotsettings

        layout = self.layout

        drawOperatorAndHelp(layout, 'bpm.open_shot', '', 'Open-Shot-and-Back-to-Edit')

        drawOperatorAndHelp(layout, 'bpm.update_shot_duration', '', 'Update-Shot-Operator')

        drawOperatorAndHelp(layout, 'bpm.add_modify_shot_marker', '', 'Add-Modify-Shot-Marker-Operator')

        drawOperatorAndHelp(layout, 'bpm.bump_shot_version_edit', '', 'Shot-Version-Management')

        drawOperatorAndHelp(layout, 'bpm.change_shot_version_edit', '', 'Shot-Version-Management')

        row = layout.row(align=True)
        row.operator('bpm.change_shot_version_edit', text = "Last shot version").go_to_last_version = True
        row.operator('bpm.open_wiki_page', text='', icon='QUESTION').wiki_page = 'Shot-Version-Management'

        layout.separator()
        layout.label(text = "version " + str(shot_settings.shot_version) + "/" + str(shot_settings.shot_last_version))
        layout.prop(shot_settings, 'shot_state')
        layout.prop(shot_settings, 'display_markers')

        row = layout.row(align=True)
        row.prop(shot_settings, 'auto_audio_sync')
        drawWikiHelp(row, 'Shot-Audio-Synchronization')

        if general_settings.debug: #debug:
            box = layout.box()
            box.label(text = 'debug', icon = 'ERROR')
            box.prop(shot_settings, 'is_shot')
            box.prop(shot_settings, 'shot_version')
            box.prop(shot_settings, 'shot_last_version')
            box.prop(shot_settings, 'not_last_version')


# bpm function topbar back/open operators
def bpmTopbarFunction(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        general_settings = context.window_manager.bpm_generalsettings

        if general_settings.is_project:

            if general_settings.file_type in {'SHOT', 'ASSET'}:

                drawOperatorAndHelp(layout, 'bpm.back_to_edit', '', 'Open-Shot-and-Back-to-Edit')

            elif general_settings.file_type == 'EDIT':

                drawOperatorAndHelp(layout, 'bpm.open_shot', '', 'Open-Shot-and-Back-to-Edit')

        layout.menu('BPM_MT_topbar_menu')


# topbar file menu
class BPM_MT_topbar_menu(bpy.types.Menu):
    bl_label = "BPM"
    bl_idname = "BPM_MT_topbar_menu"

    def draw(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout
        
        if not general_settings.is_project:
            layout.operator('bpm.create_project')  
        
        else:

            project_data = winman.bpm_projectdatas
            layout.label(text = project_data.name)

            if general_settings.file_type == 'EDIT':

                layout.operator('bpm.display_modify_project_settings')

            elif general_settings.file_type == 'SHOT':
                
                drawOperatorAndHelp(layout, 'bpm.synchronize_audio_shot', '', 'Shot-Audio-Synchronization')                


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
        return context.window_manager.bpm_customfolders
    
    def draw(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout
        layout.template_list("BPM_UL_Folders_Uilist", "", winman, "bpm_customfolders", general_settings, "custom_folders_index", rows=4)