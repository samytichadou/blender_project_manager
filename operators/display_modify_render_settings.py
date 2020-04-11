import bpy, os


from ..functions.dataset_functions import returnDatasetProperties
from ..functions.project_data_functions import loadJsonInCollection
from ..global_variables import reading_json_statement, render_folder, render_file


#update function for reloading from json
def reloadRenderSettingsFromJson(self, context):
    if not self.modify:
        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        debug = winman.bpm_generalsettings.debug

        render_folderpath = os.path.join(general_settings.project_folder, render_folder)
        render_filepath = os.path.join(render_folderpath, render_file)

        if debug: print(reading_json_statement + render_filepath) #debug

        loadJsonInCollection(winman, render_filepath, winman.bpm_rendersettings, 'render_settings')


# return render settings list
def renderSettingsListCallback(scene, context):

    items = []
    for a in context.window_manager.bpm_rendersettings:
        name = a.name
        items.append((name, name, ""))

    return items


# display project settings
class BpmDisplayModifyRenderSettings(bpy.types.Operator):
    """Display and Render Settings"""
    bl_idname = "bpm.display_modify_render_settings"
    bl_label = "Display/Modify Render Settings"

    render_settings : bpy.props.EnumProperty(name = "Render settings", items = renderSettingsListCallback)
    modify: bpy.props.BoolProperty(name = "Modify", default = False, update = reloadRenderSettingsFromJson)

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        datas = context.window_manager.bpm_rendersettings[self.render_settings]

        layout = self.layout     

        layout.prop(self, 'render_settings', text='') 

        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for p in returnDatasetProperties(datas):
            if p[0].identifier != "name":
                box = col1.box()
                box.label(text=p[0].name)
                if not self.modify:
                    box = col2.box()
                    box.label(text=str(p[1]))
                else:
                    box = col2.box()
                    box.prop(datas, '%s' % p[0].identifier, text='')

        layout.operator('bpm.open_wiki_page', text="Help", icon='QUESTION').wiki_page = "Render-Settings"

        if not self.modify:
            layout.prop(self, 'modify', icon = 'GREASEPENCIL')
        else:
            row = layout.row(align=True)
            row.prop(self, 'modify', text='Cancel', icon = 'LOOP_BACK')
            row.operator('bpm.save_project_settings_json', icon = 'FILE_TICK')
        
    def execute(self, context):
        return {'FINISHED'}