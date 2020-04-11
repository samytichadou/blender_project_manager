import bpy, os



# display project settings
class BpmSaveRenderSettingsToJson(bpy.types.Operator):
    """Save Render Settings to json"""
    bl_idname = "bpm.save_render_settings_json"
    bl_label = "Save Project Settings"

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Save Render Settings to json file ?")
        
    def execute(self, context):
        # import statements and functions
        from ..functions.json_functions import createJsonDatasetFromProperties, create_json_file, initializeAssetJsonDatas
        from ..global_variables import saving_to_json_statement, saved_to_json_statement, render_folder, render_file

        winman = context.window_manager
        general_settings = context.window_manager.bpm_generalsettings
        render_settings = winman.bpm_rendersettings

        if general_settings.debug: print(saving_to_json_statement)

        render_folder_path = os.path.join(general_settings.project_folder, render_folder)
        render_filepath = os.path.join(render_folder_path, render_file)

        # format the json dataset
        json_render_dataset = initializeAssetJsonDatas({"render_settings"})
        for r in render_settings:
            r_datas = createJsonDatasetFromProperties(r)
            json_render_dataset['render_settings'].append(r_datas)

        # create json file
        create_json_file(json_render_dataset, render_filepath)

        if general_settings.debug: print(saved_to_json_statement)

        return {'FINISHED'}