import bpy
import os


class BPMClearLockFileUser(bpy.types.Operator):
    """Clear lock file user"""
    bl_idname = "bpm.clear_lock_file_user"
    bl_label = "Clear user"
    bl_options = {'REGISTER', 'INTERNAL'}

    pid = bpy.props.IntProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Are you sure ?")

    def execute(self, context):
        from ..functions.json_functions import read_json, create_json_file
        from ..functions.lock_file_functions import getLockFilepath

        lock_filepath = getLockFilepath()

        if os.path.isfile(lock_filepath):
            datas = read_json(lock_filepath)

            n = 0
            for o in datas['opened']:
                if o['pid'] == self.pid:
                    del datas['opened'][n]
                    break
                n += 1

            create_json_file(datas, lock_filepath)

        return {'FINISHED'}