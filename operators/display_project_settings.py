import bpy


from ..functions.dataset_functions import returnDatasetProperties


# display project settings
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
        datas = context.window_manager.bpm_datas[0]

        layout = self.layout
        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for p in returnDatasetProperties(datas):
            box = col1.box()
            box.label(text=p[0].name)
            box = col2.box()
            box.label(text=str(p[1]))

        layout.label(text="Modify")
        
    def execute(self, context):
        return {'FINISHED'}