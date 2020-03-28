import bpy


class BPMCreateAsset(bpy.types.Operator):
    """Create new asset"""
    bl_idname = "bpm.create_asset"
    bl_label = "Create asset"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
            return context.window_manager.bpm_isproject

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        datas = context.window_manager.bpm_datas[0]

        layout = self.layout
        # name
        layout.label(text="Asset name")
        # type
        layout.label(text="Asset type")
        # state
        layout.label(text="Asset state")

    def execute(self, context):


        return {'FINISHED'}