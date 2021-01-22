import bpy
import os


from .functions.lock_file_functions import setupLockFile, clearLockFile, getLockFilepath
from .functions.project_data_functions import getProjectDataFile
from .global_variables import (
                            timer_function_added_statement,
                            timer_function_removed_statement,
                            timer_function_updated_statement,
                            deleted_lock_file_statement,
                            created_lock_file_statement,
                        )

addon_name = os.path.basename(os.path.dirname(__file__))

# update function for timer refresh
def updateTimer(self, context):

    from .timer_function import bpmTimerFunction


    if getProjectDataFile()[0] is None:
        return

    debug = context.window_manager.bpm_projectdatas.debug

    if self.use_timer_refresh:

        if bpy.app.timers.is_registered(bpmTimerFunction):
            bpy.app.timers.unregister(bpmTimerFunction)
            if debug: print(timer_function_updated_statement) #debug
        else:
            if debug: print(timer_function_added_statement) #debug

        bpy.app.timers.register(bpmTimerFunction)

    else:
        if bpy.app.timers.is_registered(bpmTimerFunction):
            bpy.app.timers.unregister(bpmTimerFunction)
            if debug: print(timer_function_removed_statement) #debug


# update function for lock file on/off
def updateLockFileToggle(self, context):

    if getProjectDataFile()[0] is None:
        return
    
    debug = context.window_manager.bpm_projectdatas.debug

    if self.use_lock_file_system:
        setupLockFile()
        if debug: print(created_lock_file_statement) #debug
    else:
        clearLockFile(getLockFilepath())
        if debug: print(deleted_lock_file_statement) #debug


# addon preferences
class BPM_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    use_lock_file_system : bpy.props.BoolProperty(
        name = "Use lock file system",
        default = False,
        description = "Use lock file system for collaborative work",
        update = updateLockFileToggle,
        )

    use_timer_refresh : bpy.props.BoolProperty(
        name = "Use timer function",
        default = True,
        description = "Use timer function to refresh project information every N seconds",
        update = updateTimer,
        )
    
    timer_frequency : bpy.props.FloatProperty(
        name="Timer frequency (s)", 
        precision=2, 
        min=0.01, 
        max=3600.00, 
        default=60.00, 
        description="Frequency for timer function",
        update = updateTimer,
        )

    timer_datas_refresh : bpy.props.BoolProperty(
        name="Refresh file datas", 
        default = True,
        description="Refresh file datas on timer",
        )

    timer_custom_folders_refresh : bpy.props.BoolProperty(
        name="Refresh custom folders", 
        default = True,
        description="Refresh project custom folders datas on timer",
        )


    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "use_lock_file_system")

        # timer
        box = layout.box()
        row = box.row()
        row.prop(self, "use_timer_refresh")

        subrow = row.row()
        if not self.use_timer_refresh:
            subrow.enabled = False
        subrow.prop(self, "timer_frequency")

        col = box.column(align=True)

        if not self.use_timer_refresh:
            col.enabled = False

        col.prop(self, "timer_datas_refresh")

        col.prop(self, "timer_custom_folders_refresh")


# get addon preferences
def getAddonPreferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)