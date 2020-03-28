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
        layout = self.layout
        # name
        layout.label(text="Asset name")
        # type
        layout.label(text="Asset type")
        # state
        layout.label(text="Asset state")

    def execute(self, context):
        # check json file if existing and get datas

        # format new asset datas

        # add it if name doesn't exist

        return {'FINISHED'}