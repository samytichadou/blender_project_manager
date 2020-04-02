import bpy


from ..functions.file_functions import absolutePath
from ..global_variables import opening_statement

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
                if context.scene.sequence_editor.active_strip:
                    active = context.scene.sequence_editor.active_strip
                    if not active.lock:
                        try:
                            if active.bpm_shotsettings.is_shot and active.scene.library:
                                return True
                        except AttributeError:
                            pass

    def execute(self, context):
        winman = context.window_manager
        filepath = absolutePath(context.scene.sequence_editor.active_strip.scene.library.filepath)

        if winman.bpm_generalsettings.debug: print(opening_statement + filepath) #debug

        # save
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        # open
        bpy.ops.wm.open_mainfile(filepath=filepath)
        
        return {'FINISHED'}