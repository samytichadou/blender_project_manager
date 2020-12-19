import bpy, os


from ..functions.dataset_functions import returnDatasetProperties
from ..functions.project_data_functions import loadJsonInCollection
from ..properties import shot_render_state_items
from ..global_variables import (
                            reading_json_statement,
                            render_folder,
                            render_file,
                            render_draft_folder,
                            render_render_folder,
                            render_final_folder,
                            render_playblast_folder,
                        )


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


# display project settings
class BpmDisplayModifyRenderSettings(bpy.types.Operator):
    """Display and Render Settings"""
    bl_idname = "bpm.display_modify_render_settings"
    bl_label = "Display/Modify Render Settings"

    shot_render_state_extended_items = shot_render_state_items.copy()
    shot_render_state_extended_items.append((render_playblast_folder, render_playblast_folder, ""))

    render_settings : bpy.props.EnumProperty(name = "Render settings", items = shot_render_state_extended_items)
    modify: bpy.props.BoolProperty(name = "Modify", default = False, update = reloadRenderSettingsFromJson)

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project # and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        render_settings = context.window_manager.bpm_rendersettings[self.render_settings]

        layout = self.layout     

        layout.prop(self, 'render_settings', text='') 

        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for p in returnDatasetProperties(render_settings):
            if p[0].identifier != 'name':
                box = col1.box()
                box.label(text=p[0].name)
                if not self.modify:
                    box = col2.box()
                    box.label(text=str(p[1]))
                else:
                    box = col2.box()
                    box.prop(render_settings, '%s' % p[0].identifier, text='')

        layout.operator('bpm.open_wiki_page', text="Help", icon='QUESTION').wiki_page = "Render-Settings"

        if not self.modify:
            layout.prop(self, 'modify', icon = 'GREASEPENCIL')
        else:
            row = layout.row(align=True)
            row.prop(self, 'modify', text='Cancel', icon = 'LOOP_BACK')
            row.operator('bpm.save_render_settings_json', icon = 'FILE_TICK')
        
    def execute(self, context):
        return {'FINISHED'}