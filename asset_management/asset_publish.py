import bpy


# TODO Finish operator
class BPM_OT_publish_asset(bpy.types.Operator):
    bl_idname = "bpm.publish_asset"
    bl_label = "Publish BPM Asset"
    bl_description = "Publish BPM asset"

    @classmethod
    def poll(cls, context):
        # Check if bpm project
        try:
            wm = context.window_manager
            wm["bpm_project_datas"]
            return wm["bpm_file_datas"]["file_type"] == "asset"
        except KeyError:
            return False

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Placeholder")

    def execute(self, context):
        # Refresh UI
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "BPM Asset Published")

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_publish_asset)

def unregister():
    bpy.utils.unregister_class(BPM_OT_publish_asset)
