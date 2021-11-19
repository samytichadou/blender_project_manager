import bpy

from . import gui
from . import gui_classes

# draw tasks panel
def draw_tasks_panel(container, winman):

    task_list = winman.bpm_tasklist

    gui.draw_operator_and_help(container, 'bpm.reload_tasks', '', 'Tasks-Management')

    # draw task list
    for task in task_list:

        box = container.box()
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



# sequencer tasks panel
class BPM_PT_sequencer_tasks_panel(gui_classes.SequencerPanel_Project):
    bl_label = "Task Management"

    def draw(self, context):
        winman = context.window_manager

        layout = self.layout

        draw_tasks_panel(layout, winman)


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_PT_sequencer_tasks_panel)

def unregister():
    bpy.utils.unregister_class(BPM_PT_sequencer_tasks_panel)