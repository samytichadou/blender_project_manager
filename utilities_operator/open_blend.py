import bpy
import os
import subprocess

def get_last_version(folder, pattern, extension=".blend"):
    filename_list = []
    for file in os.listdir(folder):
        if pattern in file\
        and file.endswith(extension):
            filename_list.append(file)
    if not filename_list:
        return None
    return os.path.join(folder, max(filename_list))

def get_previous_filepath_list():
    previous_list = []
    try:
        previous_list = bpy.context.window_manager["bpm_previous_filepath"]
    except KeyError:
        pass
    return previous_list

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

        # Check if filepath is the current one
        if filepath == bpy.data.filepath:
            self.report({'WARNING'}, "Blend currently opened")
            return {'CANCELLED'}

        # Check if filepath exists
        if not os.path.isfile(filepath):
            self.report({'WARNING'}, "Invalid file path")
            return {'CANCELLED'}

        # Save if needed
        previous_filepath = None
        if bpy.data.is_saved:
            print(f"BPM --- Saving : {bpy.data.filepath}")
            bpy.ops.wm.save_mainfile()
            previous_filepath = bpy.data.filepath

        # Get previous filepath list
        if not self.shift:
            print("BPM --- Storing previous list")
            old_previous_list = get_previous_filepath_list()

        # open
        if self.shift:
            print(f"BPM --- Opening in new instance : {self.filepath}")
            subprocess.Popen([bpy.app.binary_path, filepath])
        else:
            print(f"BPM --- Opening : {self.filepath}")
            bpy.ops.wm.open_mainfile(filepath=filepath)

        # Saving previous filepath
        if not self.shift:
            if previous_filepath is not None:
                print(f"BPM --- Saving previous filepath : {previous_filepath}")
                old_previous_list.append(f"{str(len(old_previous_list)).zfill(3)}_{previous_filepath}")
            if old_previous_list:
                print("BPM --- Saving previous filepath list")
                context.window_manager["bpm_previous_filepath"] = old_previous_list

        return {'FINISHED'}

class BPM_OT_open_back_blend(bpy.types.Operator):
    bl_idname = "bpm.open_back_blend"
    bl_label = "Open Back Blend"
    bl_description = "Open previous blend file, Shift for new instance"
    bl_options = {'INTERNAL'}

    shift = False

    @classmethod
    def poll(cls, context):
        try:
            context.window_manager["bpm_previous_filepath"]
            return True
        except KeyError:
            return False

    def invoke(self, context, event):
        if event.shift:
            self.shift=True
        return self.execute(context)

    def execute(self, context):
        # Get previous filepath list
        previous_filepath_list = get_previous_filepath_list()

        # Check if filepath
        if not previous_filepath_list:
            # Remove wm entry
            del context.window_manager["bpm_previous_filepath"]
            self.report({'WARNING'}, "Invalid file path list")
            return {'CANCELLED'}

        # Get last filepath
        fp_entry = max(previous_filepath_list)
        filepath = fp_entry[4:]

        # Check if filepath exists
        if not os.path.isfile(filepath):
            # Remove filepath entry
            previous_filepath_list.remove(fp_entry)
            self.report({'WARNING'}, "Invalid file path")
            return {'CANCELLED'}

        # Save if needed
        if bpy.data.is_saved:
            print(f"BPM --- Saving : {bpy.data.filepath}")
            bpy.ops.wm.save_mainfile()

        # open
        if self.shift:
            print(f"BPM --- Opening in new instance : {filepath}")
            subprocess.Popen([bpy.app.binary_path, filepath])
        else:
            print(f"BPM --- Opening : {filepath}")
            bpy.ops.wm.open_mainfile(filepath=filepath)

        # Saving previous filepath
        if not self.shift:
            # Refresh previous filepath list
            previous_filepath_list.remove(fp_entry)
            # Save filepath list
            if previous_filepath_list:
                print("BPM --- Saving previous filepath list")
                context.window_manager["bpm_previous_filepath"] = previous_filepath_list

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_OT_open_blend)
    bpy.utils.register_class(BPM_OT_open_back_blend)
def unregister():
    bpy.utils.unregister_class(BPM_OT_open_blend)
    bpy.utils.unregister_class(BPM_OT_open_back_blend)
