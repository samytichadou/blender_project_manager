import bpy


class BPM_UL_Folders_Uilist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        layout.prop(item, "name", text="", emboss=False)


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_UL_Folders_Uilist)

def unregister():
    bpy.utils.unregister_class(BPM_UL_Folders_Uilist)