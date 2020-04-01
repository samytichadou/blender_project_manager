import bpy


from ..functions.dataset_functions import returnDatasetProperties


# display project settings
class BpmModifyProjectSettings(bpy.types.Operator):
    """Modify Project Settings"""
    bl_idname = "bpm.modify_project_settings"
    bl_label = "Modify Project Settings"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_isproject
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        datas = context.window_manager.bpm_datas

        layout = self.layout
        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for p in returnDatasetProperties(datas):
            box = col1.box()
            box.label(text=p[0].name)
            box = col2.box()
            box.prop(datas, '%s' % p[0].identifier, text='')

        layout.operator('bpm.save_project_settings_json')
        
    def execute(self, context):
        # reload from json
        return {'FINISHED'}