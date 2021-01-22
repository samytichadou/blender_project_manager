import bpy


class BPM_OT_dialog_popups(bpy.types.Operator):
    bl_idname = "bpm.dialog_popups"
    bl_label = "Dialog Popups"
    bl_options = {'INTERNAL'}
 
    message : bpy.props.StringProperty()
    icon : bpy.props.StringProperty()
    operator : bpy.props.StringProperty()
    operator_icon : bpy.props.StringProperty()
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        
        layout = self.layout

        row = layout.row()

        if self.message:
            row.label(text = self.message)
        
        if self.icon:
            row.label(text = "", icon = self.icon)

        if self.operator and self.operator_icon:
            row = layout.row()
            row.operator(self.operator, icon = self.operator_icon)

        elif self.operator:
            row = layout.row()
            row.operator(self.operator)

    def execute(self, context):
        return {'FINISHED'}