import bpy
import os

from ..functions import dataset_functions as dtset_fct
from ..functions.json_functions import read_json
from .. import global_variables as g_var



#update function for reloading from json
def reloadProjectSettingsFromJson(self, context):
    if not self.modify:
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        debug = winman.bpm_projectdatas.debug

        datas = winman.bpm_projectdatas
        json_project_file = os.path.join(general_settings.project_folder, g_var.file_project)

        if debug: print(g_var.reading_json_statement + json_project_file) #debug

        json_dataset = read_json(json_project_file)

        dtset_fct.setPropertiesFromJsonDataset(json_dataset, datas, False, ())


# display project settings
class BPM_OT_display_modify_project_settings(bpy.types.Operator):
    """Display and Modify Project Settings"""
    bl_idname = "bpm.display_modify_project_settings"
    bl_label = "Project Settings"

    modify: bpy.props.BoolProperty(name = "Modify", default = False, update = reloadProjectSettingsFromJson)

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project # and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        datas = context.window_manager.bpm_projectdatas

        layout = self.layout      

        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for p in dtset_fct.returnDatasetProperties(datas):
            box = col1.box()
            box.label(text=p[0].name)
            if not self.modify:
                box = col2.box()
                box.label(text=str(p[1]))
            else:
                box = col2.box()
                box.prop(datas, '%s' % p[0].identifier, text='')

        layout.operator('bpm.open_wiki_page', text="Help", icon='QUESTION').wiki_page = "Project-Settings"

        if not self.modify:
            layout.prop(self, 'modify', icon = 'GREASEPENCIL')
        else:
            row = layout.row(align=True)
            row.prop(self, 'modify', text='Cancel', icon = 'LOOP_BACK')
            row.operator('bpm.save_project_settings_json', icon = 'FILE_TICK')
        
    def execute(self, context):
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_display_modify_project_settings)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_display_modify_project_settings)