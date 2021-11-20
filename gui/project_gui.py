import bpy

from . import gui_classes
from . import gui_common

### DRAW FCTS ###

# draw tasks panel
def draw_tasks_panel(container, winman):

    task_list = winman.bpm_tasklist

    if winman.bpm_generalsettings.is_rendering:
        container.label(text="Render(s) in progress", icon="SORTTIME")
    else:
        container.label(text="Not Rendering", icon="CHECKMARK")

    gui_common.draw_operator_and_help(container, 'bpm.reload_tasks', '', 'Tasks-Management')

    # draw task list
    col0 = container.column(align=True)
    for task in task_list:

        box = col0.box()
        row = box.row()

        if task.hide:
            icon = "TRIA_RIGHT"
        else:
            icon = "TRIA_DOWN"
        row.prop(task, "hide", text="", icon=icon, emboss=False)

        if task.type == "render":
            row.label(text="", icon="RENDER_ANIMATION")
        else:
            row.label(text="", icon="FILE_BLANK")

        row.label(text=task.name)
        row.label(text="%i/%i" % (task.completion, task.completion_total))
        if task.completed:
            row.label(text="", icon="CHECKMARK")
        else:
            row.label(text="", icon="SORTTIME")

        if not task.hide:
            split = box.split()

            col = split.column(align=True)
            col.label(text="Creation")
            col.label(text="Filepath")
            col.label(text="Type")
            col.label(text="ID")
            col.label(text="PID")

            col = split.column(align=True)
            col.label(text=task.creation_time)
            col.label(text=task.filepath)
            col.label(text=task.type)
            col.label(text=task.id)
            col.label(text=str(task.pid))

# draw management panel
def draw_management(container):

    gui_common.draw_operator_and_help(container, 'bpm.delete_unused_shots', '', 'Delete-Unused-Shots')

    gui_common.draw_operator_and_help(container, 'bpm.empty_recycle_bin', '', 'Empty-Recycle-Bin')

    gui_common.draw_operator_and_help(container, 'bpm.display_modify_project_settings', '', 'Project-Settings')
    
    gui_common.draw_operator_and_help(container, 'bpm.display_modify_render_settings', '', 'Render-Settings')

# draw browse panel
def draw_browse_folder(container):

    row = container.row(align=True)
    row.menu('BPM_MT_OpenFolder_Explorer_Menu')
    gui_common.draw_wiki_help(row, 'Project-Architecture')

# draw files general panel
def draw_files_general_panel(container, winman):

    draw_browse_folder(container)

    gui_common.draw_custom_folder_template_list(container, winman, False)


### PANELS ###

### SEQUENCER PANELS ###

# sequencer management panel
class BPM_PT_sequencer_management_panel(gui_classes.SequencerPanel_Project):
    bl_label = "Management"

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        draw_management(layout)

# sequencer files panel
class BPM_PT_sequencer_files_panel(gui_classes.SequencerPanel_Project):
    bl_label = "Files"

    def draw(self, context):

        winman = context.window_manager

        layout = self.layout

        draw_files_general_panel(layout, winman)

# sequencer tasks panel
class BPM_PT_sequencer_tasks_panel(gui_classes.SequencerPanel_Project):
    bl_label = "Task Management"

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        draw_tasks_panel(layout, winman)

# sequencer management debug panel
class BPM_PT_sequencer_management_debug_panel(gui_classes.SequencerPanel_Project_Debug):
    bl_label = "Debug"

    def draw(self, context):

        layout = self.layout
        
        general_settings = context.window_manager.bpm_generalsettings
        
        gui_common.draw_debug(layout, general_settings)

### VIEWPORT PANELS ###

# viewport management panel
class BPM_PT_viewport_management_panel(gui_classes.ViewportPanel_Project):
    bl_label = "Management"

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        layout = self.layout

        draw_management(layout)

# viewport files panel
class BPM_PT_viewport_files_panel(gui_classes.ViewportPanel_Project):
    bl_label = "Files"

    def draw(self, context):

        winman = context.window_manager

        layout = self.layout

        draw_files_general_panel(layout, winman)

# viewport management debug panel
class BPM_PT_viewport_management_debug_panel(gui_classes.ViewportPanel_Project_Debug):
    bl_label = "Debug"

    def draw(self, context):

        layout = self.layout
        
        general_settings = context.window_manager.bpm_generalsettings

        gui_common.draw_debug(layout, general_settings)

### NODETREE PANELS ###

# nodetree management
class BPM_PT_nodetree_management_panel(gui_classes.NodetreePanel_Project):
    bl_label = "Management"

    def draw(self, context):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        layout = self.layout

        draw_management(layout)

# nodetree files panel
class BPM_PT_nodetree_files_panel(gui_classes.NodetreePanel_Project):
    bl_label = "Files"

    def draw(self, context):

        winman = context.window_manager

        layout = self.layout

        draw_files_general_panel(layout, winman)

# nodetree management debug panel
class BPM_PT_nodetree_management_debug_panel(gui_classes.NodetreePanel_Project_Debug):
    bl_label = "Debug"

    def draw(self, context):

        layout = self.layout
        
        general_settings = context.window_manager.bpm_generalsettings

        gui_common.draw_debug(layout, general_settings)



### REGISTER ---

def register():
    bpy.utils.register_class(BPM_PT_sequencer_management_panel)
    bpy.utils.register_class(BPM_PT_sequencer_files_panel)
    bpy.utils.register_class(BPM_PT_sequencer_tasks_panel)
    bpy.utils.register_class(BPM_PT_sequencer_management_debug_panel)
    bpy.utils.register_class(BPM_PT_viewport_management_panel)
    bpy.utils.register_class(BPM_PT_viewport_management_debug_panel)
    bpy.utils.register_class(BPM_PT_nodetree_management_panel)
    bpy.utils.register_class(BPM_PT_nodetree_files_panel)
    bpy.utils.register_class(BPM_PT_nodetree_management_debug_panel)

def unregister():
    bpy.utils.unregister_class(BPM_PT_sequencer_management_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_files_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_tasks_panel)
    bpy.utils.unregister_class(BPM_PT_sequencer_management_debug_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_management_panel)
    bpy.utils.unregister_class(BPM_PT_viewport_management_debug_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_management_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_files_panel)
    bpy.utils.unregister_class(BPM_PT_nodetree_management_debug_panel)
