import bpy


class BPMModifyShotTasks(bpy.types.Operator):
    """Modify shot tasks"""
    bl_idname = "bpm.modify_shot_tasks"
    bl_label = "Modify shot tasks"
    bl_options = {'REGISTER', 'INTERNAL'}

    shot_settings = None

    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type =='SHOT':
                return True
            elif context.window_manager.bpm_generalsettings.file_type =='EDIT':
                keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
                if keyword in context.scene.name:
                    if context.scene.sequence_editor:
                        if context.scene.sequence_editor.active_strip:
                            active = context.scene.sequence_editor.active_strip
                            if not active.lock:
                                try:
                                    if active.bpm_shotsettings.is_shot and active.scene.library:
                                        return True
                                except AttributeError:
                                    pass

    def invoke(self, context, event):
        winman = context.window_manager

        if winman.bpm_generalsettings.file_type == 'EDIT':
            self.shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        else:
            self.shot_settings = winman.bpm_shotsettings

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout

        layout.prop(self.shot_settings, 'storyboard_deadline', text='Storyboard')
        layout.prop(self.shot_settings, 'layout_deadline', text='Layout')
        layout.prop(self.shot_settings, 'animation_deadline', text='Animation')
        layout.prop(self.shot_settings, 'lighting_deadline', text='Lighting')
        layout.prop(self.shot_settings, 'rendering_deadline', text='Rendering')
        layout.prop(self.shot_settings, 'compositing_deadline', text='Compositing')

    def execute(self, context):
        # import statement and functions
        from ..functions.shot_settings_json_update_function import updateShotSettingsProperties
        
        updateShotSettingsProperties(self.shot_settings, context)

        return {'FINISHED'}