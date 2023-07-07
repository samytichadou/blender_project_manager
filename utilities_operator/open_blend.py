import bpy
import os
import subprocess

def get_last_version(folder, pattern):
    filename_list = []
    for file in os.listdir(folder):
        if pattern in file:
            filename_list.append(file)
    if not filename_list:
        return None
    return os.path.join(folder, max(filename_list))

class BPM_OT_open_blend(bpy.types.Operator):
    bl_idname = "bpm.open_blend"
    bl_label = "Open Blend"
    bl_description = "Open blend file, Shift for new instance"
    bl_options = {'INTERNAL'}

    filepath : bpy.props.StringProperty()
    folderpath : bpy.props.StringProperty()
    pattern : bpy.props.StringProperty()

    shift = False

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        if event.shift:
            self.shift=True
        return self.execute(context)

    def execute(self, context):
        if self.filepath:
            filepath = self.filepath
        else:
            filepath = get_last_version(self.folderpath, self.pattern)

        # Check if filepath exists
        if not os.path.isfile(filepath):
            self.report({'WARNING'}, "Invalid file path")

        # open
        if self.shift:
            print(f"BPM --- Opening in new instance : {self.filepath}")
            subprocess.Popen([bpy.app.binary_path, filepath])
        else:
            print(f"BPM --- Opening : {self.filepath}")
            bpy.ops.wm.open_mainfile(filepath=filepath)

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_open_blend)
def unregister():
    bpy.utils.unregister_class(BPM_OT_open_blend)
