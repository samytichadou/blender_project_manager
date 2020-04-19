import bpy
import os


class BPMShowOpenBlendLockFile(bpy.types.Operator):
    """Show list of user for this blend file"""
    bl_idname = "bpm.show_open_blend_lock_file"
    bl_label = "File already opened"
    bl_options = {'REGISTER', 'INTERNAL'}

    host_name_list = []
    timestamp_list = []
    pid_list = []
    pid = None

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.blend_already_opened

    def invoke(self, context, event):
        from ..functions.json_functions import read_json
        from ..functions.lock_file_functions import getLockFilepath
        from ..functions.utils_functions import returnFormatedTimestamp, getCurrentPID

        self.host_name_list.clear()
        self.timestamp_list.clear()
        self.pid_list.clear()

        self.pid = getCurrentPID()

        lock_filepath = getLockFilepath()
        if os.path.isfile(lock_filepath):
            datas = read_json(lock_filepath)

        for o in datas['opened']:
            self.host_name_list.append(o['hostname'])
            self.timestamp_list.append(returnFormatedTimestamp(o['timestamp']))
            self.pid_list.append(o['pid'])

        return context.window_manager.invoke_props_dialog(self, width=400)
 
    def draw(self, context):
        layout = self.layout
        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)
        col3 = split.column(align=True)
        for i in range(0, len(self.host_name_list)):
            box1 = col1.box()
            box1.label(text=self.host_name_list[i], icon = 'USER')
            box2 = col2.box()
            box2.label(text=self.timestamp_list[i])
            if self.pid_list[i] != self.pid:
                box3 = col3.box()
                box3.operator('bpm.clear_lock_file_user').pid = self.pid_list[i]

    def execute(self, context):

        return {'FINISHED'}