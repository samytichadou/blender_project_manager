import bpy


# display project settings
class BpmSaveProjectSettingsToJson(bpy.types.Operator):
    """Save Project Settings to json"""
    bl_idname = "bpm.save_project_settings_json"
    bl_label = "Save Project Settings"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Save Project Settings to json file ?")
        
    def execute(self, context):
        # save
        return {'FINISHED'}