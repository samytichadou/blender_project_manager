import bpy, os


from ..functions.dataset_functions import returnDatasetProperties, setPropertiesFromJsonDataset
from ..functions.json_functions import read_json
from ..global_variables import file_project, reading_json_statement


#update function for reloading from json
def reloadProjectSettingsFromJson(self, context):
    if not self.modify:
        winman = context.window_manager

        if winman.bpm_debug: print(reading_json_statement) #debug

        datas = winman.bpm_datas[0]
        json_project_file = os.path.join(winman.bpm_projectfolder, file_project)

        json_dataset = read_json(json_project_file)

        setPropertiesFromJsonDataset(json_dataset, datas, winman)

# display project settings
class BpmDisplayModifyProjectSettings(bpy.types.Operator):
    """Display and Modify Project Settings"""
    bl_idname = "bpm.display_modify_project_settings"
    bl_label = "Display/Modify Project Settings"

    modify: bpy.props.BoolProperty(name = "Modify", default = False, update = reloadProjectSettingsFromJson)

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
            if not self.modify:
                box = col2.box()
                box.label(text=str(p[1]))
            else:
                box = col2.box()
                box.prop(datas, '%s' % p[0].identifier, text='')

        if not self.modify:
            layout.prop(self, 'modify', icon = 'GREASEPENCIL')
        else:
            row = layout.row(align=True)
            row.prop(self, 'modify', text='Cancel', icon = 'LOOP_BACK')
            row.operator('bpm.save_project_settings_json', icon = 'FILE_TICK')
        
    def execute(self, context):
        return {'FINISHED'}