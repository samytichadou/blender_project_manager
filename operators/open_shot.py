import bpy
import os


from ..functions.file_functions import absolutePath


class BPMOpenShot(bpy.types.Operator):
    """Open Shot from Timeline"""
    bl_idname = "bpm.open_shot"
    bl_label = "Open Shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        if context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor:
                    if context.scene.sequence_editor.active_strip:
                        active = context.scene.sequence_editor.active_strip
                        if active.type in {'SCENE', 'IMAGE'}:
                            if not active.lock:
                                if active.bpm_shotsettings.is_shot:
                                    if os.path.isfile(absolutePath(active.bpm_shotsettings.shot_filepath)):
                                        return True

    def execute(self, context):
        # import statements and functions
        from ..functions.file_functions import absolutePath
        from ..global_variables import opening_statement

        winman = context.window_manager
        filepath = absolutePath(context.scene.sequence_editor.active_strip.bpm_shotsettings.shot_filepath)

        if winman.bpm_generalsettings.debug: print(opening_statement + filepath) #debug

        # save if not temp
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        # open
        bpy.ops.wm.open_mainfile(filepath=filepath)
        
        return {'FINISHED'}