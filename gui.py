import bpy


from .properties import getAssetIcon
from .functions.project_data_functions import getShotTaskDeadline, getShotTaskComplete


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

# draw already opened blend warning
def drawOpenedWarning(container, general_settings):
    if general_settings.blend_already_opened:
        drawOperatorAndHelp(container, 'bpm.show_open_blend_lock_file', 'ERROR', "Lock-File-System")
        #container.label(text="File already opened", icon='ERROR')


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

        drawOpenedWarning(layout, general_settings)

        drawOperatorAndHelp(layout, 'bpm.create_shot', '', 'Create-Shot-Operator')

        drawOperatorAndHelp(layout, 'bpm.delete_unused_shots', '', 'Delete-Unused-Shots')

        drawOperatorAndHelp(layout, 'bpm.empty_recycle_bin', '', 'Empty-Recycle-Bin')

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
    #bl_parent_id = "BPM_PT_sequencer_management_panel"

    def draw(self, context):
        scn_settings = context.scene.bpm_scenesettings
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout

        drawOpenedWarning(layout, general_settings)

        row = layout.row(align=True)
        row.prop(scn_settings, 'extra_ui')
        drawWikiHelp(row, 'Extra-UI-in-Sequencer')
        if scn_settings.extra_ui:
            box = layout.box()
            row = box.row()
            row.prop(scn_settings, 'display_shot_strip')
            row.prop(scn_settings, 'color_shot_strip', text="")

            row = box.row()
            row.prop(scn_settings, 'display_shot_todo')
            row.prop(scn_settings, 'color_shot_todo', text="")

            row = box.row()
            row.prop(scn_settings, 'display_shot_state')
            row.prop(general_settings, 'ui_shot_state_subpanel', icon='COLORSET_04_VEC')

            if general_settings.ui_shot_state_subpanel:
                box2 = box.box()
                col = box2.column(align=True)
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

            row = box.row()
            row.prop(scn_settings, 'display_audio_sync')
            row.prop(scn_settings, 'color_audio_sync', text="")

            row = box.row()
            row.prop(scn_settings, 'display_shot_update_warning')
            row.prop(scn_settings, 'color_update_warning', text="")

            row = box.row()
            row.prop(scn_settings, 'display_shot_version_warning')
            row.prop(scn_settings, 'color_version_warning', text="")

            # markers
            box = layout.box()
            row = box.row()
            row.label(text = "Markers")
            row.prop(scn_settings, 'display_markers', text = "")
            row.prop(scn_settings, 'color_markers', text="")

            row = box.row()
            row.label(text = "Names")
            row.prop(scn_settings, 'display_marker_names', text = "")

            row = box.row()
            row.prop(scn_settings, 'display_marker_boxes', text = "Boxes")
            row.prop(scn_settings, 'color_marker_boxes', text="")

            box.prop(scn_settings, 'display_marker_text_limit')


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

        drawOpenedWarning(layout, general_settings)

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

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_state', text="")
        if shot_settings.shot_state != "FINISHED":
            row.prop(shot_settings, getShotTaskComplete(shot_settings)[0], text="")
        drawWikiHelp(row, 'Shot-Datas')

        row = layout.row(align=True)
        row.label(text = "Deadline : " + getShotTaskDeadline(shot_settings)[1], icon = 'TIME')
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='GREASEPENCIL').behavior = 'active_strip'
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='SEQ_STRIP_DUPLICATE').behavior = 'selected_strips'
        drawWikiHelp(row, 'Shot-Task-System')

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_render_state', text = "Render")
        drawWikiHelp(row, 'Render-Settings')

        layout.prop(shot_settings, 'display_markers')

        row = layout.row(align=True)
        row.prop(shot_settings, 'auto_audio_sync')
        drawWikiHelp(row, 'Shot-Audio-Synchronization')

        drawDebugPanel(layout, shot_settings, general_settings)#debug


# draw asset library
def drawAssetLibrary(container, winman):

    general_settings = winman.bpm_generalsettings

    drawOperatorAndHelp(container, 'bpm.create_asset', '', 'Asset-Management')

    container.prop(general_settings, 'panel_asset_display', text="Display")

    container.template_list("BPM_UL_Asset_UI_List", "", winman, "bpm_assets", general_settings, "asset_list_index", rows = 3)

    drawOperatorAndHelp(container, 'bpm.open_asset_file', 'FILE_FOLDER', 'Asset-Management')


# sequencer assets panel
class BPM_PT_sequencer_asset_panel(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Assets"
    bl_idname = "BPM_PT_sequencer_asset_panel"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type == 'EDIT':
                if context.window_manager.bpm_projectdatas.edit_scene_keyword in context.scene.name:
                    return True

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        drawOpenedWarning(layout, winman.bpm_generalsettings)

        drawAssetLibrary(layout, winman)


# shot settings panel
class BPM_PT_properties_shot_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_label = "Shot settings"
    bl_idname = "BPM_PT_properties_shot_panel"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'SHOT'

    def draw(self, context):
        winman = context.window_manager
        shot_settings = winman.bpm_shotsettings

        layout = self.layout

        drawOpenedWarning(layout, winman.bpm_generalsettings)

        drawOperatorAndHelp(layout, 'bpm.synchronize_audio_shot', '', 'Shot-Audio-Synchronization')

        drawOperatorAndHelp(layout, 'bpm.refresh_shot_datas_shot', '', 'Shot-Datas')

        drawOperatorAndHelp(layout, 'bpm.render_shot_playlast', '', 'Render-Settings')

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_state', text="")
        if shot_settings.shot_state != "FINISHED":
            row.prop(shot_settings, getShotTaskComplete(shot_settings)[0], text="")
        drawWikiHelp(row, 'Shot-Datas')

        row = layout.row(align=True)
        row.label(text = "Deadline : " + getShotTaskDeadline(shot_settings)[1], icon = 'TIME')
        row.operator('bpm.modify_shot_tasks_deadlines', text='', icon='GREASEPENCIL').behavior = 'active_strip'
        drawWikiHelp(row, 'Shot-Task-System')

        row = layout.row(align=True)
        row.prop(shot_settings, 'auto_audio_sync')
        drawWikiHelp(row, 'Shot-Audio-Synchronization')

        row = layout.row(align=True)
        row.prop(shot_settings, 'shot_render_state', text = "Render")
        drawWikiHelp(row, 'Render-Settings')

        drawDebugPanel(layout, shot_settings, winman.bpm_generalsettings) #debug


# asset library panel
class BPM_PT_properties_asset_library_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_label = "Assets Library"
    bl_idname = "BPM_PT_properties_asset_library_panel"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type in {'SHOT', 'ASSET'}

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        drawOpenedWarning(layout, winman.bpm_generalsettings)

        drawAssetLibrary(layout, winman)

        if winman.bpm_generalsettings.file_type == 'SHOT':
            drawOperatorAndHelp(layout, 'bpm.import_asset', 'LINK_BLEND', 'Asset-Management')


# asset settings panel
class BPM_PT_properties_asset_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_label = "Asset settings"
    bl_idname = "BPM_PT_properties_asset_panel"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'ASSET'

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        asset_settings = winman.bpm_assetsettings

        layout = self.layout

        drawOpenedWarning(layout, general_settings)

        layout.prop(asset_settings, 'asset_type')
        layout.prop(asset_settings, 'asset_state')

        if asset_settings.asset_type == 'SHADER': target_prop = 'asset_material'
        elif asset_settings.asset_type == 'WORLD': target_prop = 'asset_world'
        else: target_prop = 'asset_collection'

        layout.prop(asset_settings, target_prop, text='')
        layout.label(text = "Manually update when changing collection name", icon = "INFO")
        
        drawDebugPanel(layout, asset_settings, general_settings) #debug
        
        if general_settings.show_debug_props:
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

            box.label(text = 'Worlds', icon = 'WORLD')
            col = box.column(align=True)
            for i in bpy.data.worlds:
                row = col.row(align=True)
                row.prop(i, 'bpm_isasset', text=i.name)


# bpm function topbar back/open operators
def bpmTopbarFunction(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        general_settings = context.window_manager.bpm_generalsettings

        if general_settings.is_project:

            if general_settings.blend_already_opened:
                drawOpenedWarning(layout, general_settings)

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

        drawOpenedWarning(layout, general_settings)
        
        if not general_settings.is_project:
            layout.operator('bpm.create_project')  
        
        else:

            project_data = winman.bpm_projectdatas
            layout.label(text = project_data.name)

            if general_settings.file_type == 'EDIT':

                layout.operator('bpm.display_modify_project_settings')
                layout.operator('bpm.display_modify_render_settings')
            
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
        general_settings = context.window_manager.bpm_generalsettings
        return context.window_manager.bpm_customfolders and general_settings.is_project
    
    def draw(self, context):
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings

        layout = self.layout
        #shot
        #asset
        layout.template_list("BPM_UL_Folders_Uilist", "", winman, "bpm_customfolders", general_settings, "custom_folders_index", rows=4)