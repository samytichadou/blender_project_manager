import bpy

from . import gui_classes
from . import gui_common


### DRAW FCTS ###

# draw open folders panel
def draw_open_folders_menu(container, filebrowser):

    col = container.column(align=True)

    for f in ('Datas', 'Project', 'Asset', 'Shot', 'Render', 'Ressources', 'Playblast'):
        op = col.operator('bpm.open_project_folder', text = f)
        op.folder = f
        op.filebrowser = filebrowser

    col.operator('bpm.open_shot_folder', text='Active Shot').filebrowser=filebrowser
    
    col.operator('bpm.open_shot_render_folder', text='Active Render').filebrowser=filebrowser

# bpm function topbar back/open operators
def draw_topbar(self, context):
    if context.region.alignment == 'RIGHT':
        layout = self.layout
        general_settings = context.window_manager.bpm_generalsettings

        if general_settings.is_project:

            if general_settings.file_type in {'SHOT', 'ASSET'}:

                gui_common.draw_operator_and_help(layout, 'bpm.back_to_edit', '', 'Open-Shot-and-Back-to-Edit')

            elif general_settings.file_type == 'EDIT':
                row = layout.row(align=True)
                row.operator("bpm.open_shot", icon = "FILE_FOLDER").new_blender_instance = False
                row.operator("bpm.open_shot", text = "", icon = "BLENDER").new_blender_instance = True
                gui_common.draw_wiki_help(row, "Open-Shot-and-Back-to-Edit")

        # draw menu
        if general_settings.blend_already_opened or general_settings.update_needed:
            layout.menu('BPM_MT_topbar_menu', icon = "ERROR")
        else:
            layout.menu('BPM_MT_topbar_menu')

# right click sequencer menu
def drawRightClickSequencerMenu(self, context):

    general_settings = context.window_manager.bpm_generalsettings
    scn = context.scene

    if general_settings.is_project and general_settings.file_type == 'EDIT':

        layout = self.layout
        layout.menu('BPM_MT_RightClickSequencerEdit_Menu')

        if scn.sequence_editor.active_strip:
            active_strip = scn.sequence_editor.active_strip
            if active_strip.type in {'SCENE', 'IMAGE'}:
                if active_strip.bpm_shotsettings.is_shot:

                    layout.menu('BPM_MT_RightClickSequencerShot_Menu')

        layout.separator()


### CLASSES ###

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

            # opened blend
            if general_settings.blend_already_opened:
                layout.separator()
                layout.operator("bpm.show_open_blend_lock_file", icon = "ERROR")

            # addon update needed
            if general_settings.update_needed:
                layout.separator()
                op = layout.operator("wm.url_open", text = "New addon version available", icon = "URL")
                op.url = general_settings.update_download_url
                                
# filebrowser gui
class BPM_PT_FileBrowser_Panel(gui_classes.FilebrowserPanel):
    bl_label = "BPM"
    
    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project
    
    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        row = layout.row(align = True)
        row.menu('BPM_MT_OpenFolder_Filebrowser_Menu')
        gui_common.draw_wiki_help(row, 'Project-Architecture')
        
        gui_common.draw_custom_folder_template_list(layout, winman, True)

# open folder menu
class BPM_MT_OpenFolder_Explorer_Menu(bpy.types.Menu):
    bl_label = "Open Folders"

    def draw(self, context):
        layout = self.layout
        
        draw_open_folders_menu(layout, False)

# open folder menu
class BPM_MT_OpenFolder_Filebrowser_Menu(bpy.types.Menu):
    bl_label = "Open Folders"

    def draw(self, context):
        layout = self.layout
        
        draw_open_folders_menu(layout, True)

# right click sequencer general menu
class BPM_MT_RightClickSequencerEdit_Menu(bpy.types.Menu):
    bl_label = "BPM Edit"

    def draw(self, context):
        layout = self.layout

        layout.operator("bpm.create_shot")
        layout.operator("bpm.synchronize_audio_edit")
        layout.operator("bpm.refresh_edit_datas")
        layout.separator()
        layout.operator("bpm.goto_next_previous_comment", text = "Previous Comment").next = False
        layout.operator("bpm.goto_next_previous_comment", text = "Next Comment").next = True

# right click sequencer active shot menu
class BPM_MT_RightClickSequencerShot_Menu(bpy.types.Menu):
    bl_label = "BPM Active Shot"

    def draw(self, context):
        layout = self.layout
        
        layout.operator('bpm.open_shot')
        layout.operator('bpm.update_shot_duration')
        layout.operator('bpm.bump_shot_version_edit')
        layout.operator('bpm.render_shot_edit')


def register():
    bpy.utils.register_class(BPM_MT_topbar_menu)
    bpy.utils.register_class(BPM_PT_FileBrowser_Panel)
    bpy.utils.register_class(BPM_MT_OpenFolder_Explorer_Menu)
    bpy.utils.register_class(BPM_MT_OpenFolder_Filebrowser_Menu)
    bpy.utils.register_class(BPM_MT_RightClickSequencerEdit_Menu)
    bpy.utils.register_class(BPM_MT_RightClickSequencerShot_Menu)

    bpy.types.TOPBAR_HT_upper_bar.prepend(draw_topbar)
    bpy.types.SEQUENCER_MT_context_menu.prepend(drawRightClickSequencerMenu)

def unregister():
    bpy.utils.unregister_class(BPM_MT_topbar_menu)
    bpy.utils.unregister_class(BPM_PT_FileBrowser_Panel)
    bpy.utils.unregister_class(BPM_MT_OpenFolder_Explorer_Menu)
    bpy.utils.unregister_class(BPM_MT_OpenFolder_Filebrowser_Menu)
    bpy.utils.unregister_class(BPM_MT_RightClickSequencerEdit_Menu)
    bpy.utils.unregister_class(BPM_MT_RightClickSequencerShot_Menu)

    bpy.types.TOPBAR_HT_upper_bar.remove(draw_topbar)
    bpy.types.SEQUENCER_MT_context_menu.remove(drawRightClickSequencerMenu)