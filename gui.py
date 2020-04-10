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


# draw all props for debug
def drawDebugPanel(container, dataset, general_settings):
    if not general_settings.debug:
        return
 
    box = container.box()

    box.prop(general_settings, 'show_debug_props', text = "Show debug props", icon = 'TOOL_SETTINGS')
    if general_settings.show_debug_props:
        box.label(text = str(dataset.bl_rna.identifier) + ' - Be careful', icon='ERROR')
        for p in dataset.bl_rna.properties:
            if not p.is_readonly and p.identifier != 'name':
                row = box.row()
                row.prop(dataset, '%s' % p.identifier)


# sequencer management
class BPM_PT_sequencer_management_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Management"
    bl_idname = "BPM_PT_sequencer_management_panel"
    bl_category = "BPM"

    debug_open : bpy.props.BoolProperty(name = 'Debug', default = False)

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'

    def draw(self, context):
        winman = context.window_manager
        project_data = context.window_manager.bpm_projectdatas
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        drawOperatorAndHelp(layout, 'bpm.create_shot', '', 'Create-Shot-Operator')

        drawOperatorAndHelp(layout, 'bpm.delete_unused_shots', '', 'Delete-Unused-Shots')

        drawOperatorAndHelp(layout, 'bpm.empty_recycle_bin', '', 'Empty-Recycle-Bin')

        drawOperatorAndHelp(layout, 'bpm.create_asset', '', 'Create-Asset-Operator')

        drawOperatorAndHelp(layout, 'bpm.synchronize_audio_edit', '', 'Shot-Audio-Synchronization')

        drawOperatorAndHelp(layout, 'bpm.refresh_shot_datas_edit', '', 'Shot-Datas')
                
        drawDebugPanel(layout, general_settings, general_settings)#debug


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
        general_settings = context.window_manager.bpm_generalsettings
        layout = self.layout

        row = layout.row(align=True)
        row.prop(scn_settings, 'extra_ui')
        drawWikiHelp(row, 'Extra-UI-in-Sequencer')
        if scn_settings.extra_ui:
            row = layout.row()
            row.prop(scn_settings, 'display_shot_strip')
            row.prop(scn_settings, 'color_shot_strip', text="")

            row = layout.row()
            row.prop(scn_settings, 'display_shot_state')
            row.prop(general_settings, 'ui_shot_state_subpanel', icon='COLORSET_04_VEC')

            if general_settings.ui_shot_state_subpanel:
                box = layout.box()
                col = box.column(align=True)
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

            row = layout.row()
            row.prop(scn_settings, 'display_audio_sync')
            row.prop(scn_settings, 'color_audio_sync', text="")

            row = layout.row()
            row.prop(scn_settings, 'display_shot_update_warning')
            row.prop(scn_settings, 'color_update_warning', text="")

            row = layout.row()
            row.prop(scn_settings, 'display_shot_version_warning')
            row.prop(scn_settings, 'color_version_warning', text="")

            # markers
            row = layout.row()
            row.label(text = "Markers")
            row.prop(scn_settings, 'display_markers', text = "")
            row.prop(scn_settings, 'color_markers', text="")

            row = layout.row()
            row.label(text = "Markers names")
            row.prop(scn_settings, 'display_marker_names', text = "")

            row = layout.row()
            row.prop(scn_settings, 'display_marker_boxes')
            row.prop(scn_settings, 'color_marker_boxes', text="")

            layout.prop(scn_settings, 'display_marker_text_limit')


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

        drawDebugPanel(layout, shot_settings, general_settings)#debug


# sequencer shot assets panel
class BPM_PT_sequencer_shot_asset_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Shot Assets"
    bl_idname = "BPM_PT_sequencer_shot_asset_panel"
    bl_category = "BPM"
    #bl_parent_id = "BPM_PT_sequencer_shot_panel"

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
        general_settings = winman.bpm_generalsettings
        asset_list = winman.bpm_assets

        layout = self.layout
        layout.prop(general_settings, 'panel_asset_display', text="")

        for asset in asset_list:
            if general_settings.panel_asset_display == 'ALL':
                row = layout.row(align=True)
                row.label(text = asset.name)
                row.label(text = asset.asset_type)
            else:
                if asset.asset_type == general_settings.panel_asset_display:
                    row = layout.row(align=True)
                    row.label(text = asset.name)
                    row.label(text = asset.asset_type)


# shot settings panel
class BPM_PT_properties_shot_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_label = "BPM Shot settings"
    bl_idname = "BPM_PT_properties_shot_panel"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'SHOT'

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        shot_settings = winman.bpm_shotsettings

        layout = self.layout

        drawOperatorAndHelp(layout, 'bpm.synchronize_audio_shot', '', 'Shot-Audio-Synchronization')

        drawOperatorAndHelp(layout, 'bpm.refresh_shot_datas_shot', '', 'Shot-Datas')

        layout.prop(shot_settings, 'shot_state', text = "")

        row = layout.row(align=True)
        row.prop(shot_settings, 'auto_audio_sync')
        drawWikiHelp(row, 'Shot-Audio-Synchronization')

        layout.prop(general_settings, 'asset_choose')
        layout.operator('bpm.import_asset')
        
        drawDebugPanel(layout, shot_settings, general_settings) #debug


# asset settings panel
class BPM_PT_properties_asset_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_label = "BPM Asset settings"
    bl_idname = "BPM_PT_properties_asset_panel"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'ASSET'

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        layout.prop(asset_settings, 'asset_type')
        layout.prop(asset_settings, 'asset_state')

        if asset_settings.asset_type != 'SHADER':
            target_prop = 'asset_collection'
        else:
            target_prop = 'asset_material'

        layout.prop(asset_settings, target_prop, text='')
        
        #debug
        box = layout.box()

        box.label(text = 'Debug', icon = 'ERROR')

        box.label(text = 'Collections', icon = 'GROUP')
        col = box.column(align=True)
        for i in bpy.data.collections:
            row = col.row(align=True)
            row.prop(i, 'bpm_isasset', text=i.name)

        box.label(text = 'Materials', icon = 'MATERIAL')
        col = box.column(align=True)
        for i in bpy.data.materials:
            row = col.row(align=True)
            row.prop(i, 'bpm_isasset', text=i.name)
        
        drawDebugPanel(layout, asset_settings, general_settings) #debug


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
            
            layout.prop(general_settings, 'debug')
                                


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