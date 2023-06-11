import bpy

def bpm_project_topbar(self, context):
    if context.window_manager["bpm_project_datas"]:
        datas = context.window_manager["bpm_project_datas"]
        if context.region.alignment == 'RIGHT':
            layout=self.layout
            layout.label(text = datas["project_name"])

### REGISTER ---
def register():
    bpy.types.TOPBAR_HT_upper_bar.prepend(bpm_project_topbar)

def unregister():
    bpy.types.TOPBAR_HT_upper_bar.remove(bpm_project_topbar)
