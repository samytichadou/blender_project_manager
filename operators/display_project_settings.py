import bpy

class BpmDisplayProjectSettings(bpy.types.Operator):
    """Display Project Settings"""
    bl_idname = "bpm.display_project_settings"
    bl_label = "Display Project Settings"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        winman = context.window_manager
        datas = winman.bmp_datas
        layout = self.layout
        
    def execute(self, context):
        return {'FINISHED'}