import bpy
import os


from ..properties import shot_render_state_items


class BPMSetRenderShot(bpy.types.Operator):
    """Set render from shot"""
    bl_idname = "bpm.set_render_shot"
    bl_label = "Set render"
    bl_options = {'REGISTER'}

    render_settings : bpy.props.EnumProperty(name = "Render settings", items = shot_render_state_items)

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'SHOT'

    def invoke(self, context, event):       
        self.render_settings = context.window_manager.bpm_shotsettings.shot_render_state
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'render_settings', text='') 

    def execute(self, context):
        from ..functions.file_functions import createDirectory, deleteFolderContent
        from ..global_variables import (
                                    render_folder,
                                    render_shots_folder,
                                    setting_prop_statement,
                                    setting_prop_error_statement,
                                )

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = general_settings.debug
        render_settings = winman.bpm_rendersettings[self.render_settings]
        scn = context.scene
        render = scn.render

        # get render folder
        shot_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        render_folder_path = os.path.join(general_settings.project_folder, render_folder)
        render_shot_folder_path = os.path.join(render_folder_path, render_shots_folder)
        spec_render_folder_path = os.path.join(render_shot_folder_path, self.render_settings)

        shot_folder_path = os.path.join(spec_render_folder_path, shot_name)
        output_filepath = os.path.join(shot_folder_path, shot_name + "_#####")

        # create render folder if needed
        if not os.path.isdir(shot_folder_path):
            createDirectory(shot_folder_path)

        # clear previous if needed
        else:
            deleteFolderContent(shot_folder_path)

        # set render

        #filepath
        render.filepath = bpy.path.relpath(output_filepath)

        #props
        for p in render_settings.bl_rna.properties:
            if not p.is_readonly and p.identifier != 'name':
                # set dataset
                identif = p.identifier[3:]
                # render
                if "rd_" in p.identifier:
                    dataset = render
                # image settings
                elif "is_" in p.identifier:
                    dataset = render.image_settings
                # cycles
                elif "cy_" in p.identifier:
                    dataset = scn.cycles
                # eevee
                elif "ee_" in p.identifier:
                    dataset = scn.eevee

                # set props
                try:
                    if debug: print(setting_prop_statement + identif) #debug
                    setattr(dataset, identif, getattr(render_settings, p.identifier))
                except (KeyError, AttributeError, TypeError):
                    if debug: print(setting_prop_error_statement + identif) #debug
                    pass

        return {'FINISHED'}