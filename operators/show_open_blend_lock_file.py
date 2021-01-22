import bpy
import os


from ..functions.lock_file_functions import getLockFilepath
from ..functions.json_functions import read_json
from ..functions.utils_functions import returnFormatedTimestamp, getCurrentPID
from ..addon_prefs import getAddonPreferences


class BPM_OT_show_open_blend_lock_file(bpy.types.Operator):
    """Show list of user for this blend file"""
    bl_idname = "bpm.show_open_blend_lock_file"
    bl_label = "File already opened"
    bl_options = {'REGISTER', 'INTERNAL'}

    lock_filepath = None
    pid = None

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if getAddonPreferences().use_lock_file_system:
                if general_settings.blend_already_opened:
                    if os.path.isfile(getLockFilepath()):
                        return True

    def invoke(self, context, event):
        self.lock_filepath = getLockFilepath()
        self.pid = getCurrentPID()

        return context.window_manager.invoke_props_dialog(self, width=400)
 
    def draw(self, context):

        datas = read_json(self.lock_filepath)

        layout = self.layout

        op = layout.operator('bpm.open_wiki_page', text="Lock file system Help", icon='QUESTION')
        op.wiki_page = "Lock-File-System"

        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for i in datas['opened']:

            box1 = col1.box()
            row = box1.row(align=True)

            if i['pid'] != self.pid:
                row.operator('bpm.clear_lock_file_user', text="", icon = 'X').pid_to_clear = i['pid']

            else:
                row.label(text="", icon = 'BLENDER')
            
            row.label(text = i['hostname'])

            box2 = col2.box()
            box2.label(text = returnFormatedTimestamp(i['timestamp']))


    def execute(self, context):
        return {'FINISHED'}