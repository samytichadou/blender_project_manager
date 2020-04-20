import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

# update function for timer refresh
def updateTimer(self, context):
    from .timer_function import bpmTimerFunction
    from .global_variables import timer_function_added_statement, timer_function_removed_statement, timer_function_updated_statement

    debug = context.window_manager.bpm_generalsettings.debug

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


# addon preferences
class BPMAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    use_timer_refresh : bpy.props.BoolProperty(
        name = "Use timer function",
        default = False,
        description = "Use timer function to refresh project information every N seconds",
        update = updateTimer,
        )
    
    timer_frequency : bpy.props.FloatProperty(
        name='Timer frequency (s)', 
        precision=2, 
        min=0.01, 
        max=3600.00, 
        default=60.00, 
        description='Frequency for timer function',
        update = updateTimer,
        )


    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "use_timer_refresh")

        subrow = row.row()
        if not self.use_timer_refresh:
            subrow.enabled = False
        subrow.prop(self, "timer_frequency")


# get addon preferences
def getAddonPreferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)