import bpy


from ..functions.file_functions import absolutePath
from ..global_variables import opening_statement

class BPMOpenShot(bpy.types.Operator):
    """Open Shot from Timeline"""
    bl_idname = "bpm.open_shot"
    bl_label = "Open Shot"
    #bl_options = {}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_datas[0].edit_scene_keyword
        if context.window_manager.bpm_isproject and context.window_manager.bpm_filetype == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor.active_strip:
                    active = context.scene.sequence_editor.active_strip
                    if not active.lock:
                        try:
                            if active.bpm_isshot and active.scene.library:
                                return True
                        except AttributeError:
                            pass

    def execute(self, context):
        winman = context.window_manager
        filepath = absolutePath(context.scene.sequence_editor.active_strip.scene.library.filepath)

        if winman.bpm_debug: print(opening_statement + filepath) #debug

        # save
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        # open
        bpy.ops.wm.open_mainfile(filepath=filepath)
        
        return {'FINISHED'}