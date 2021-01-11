import bpy
import os


class BPMClearLockFileUser(bpy.types.Operator):
    """Clear lock file user"""
    bl_idname = "bpm.clear_lock_file_user"
    bl_label = "Clear user"
    bl_options = {'REGISTER', 'INTERNAL'}

    pid_to_clear : bpy.props.IntProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Are you sure ?")

    def execute(self, context):
        from ..functions.json_functions import read_json, create_json_file
        from ..functions.lock_file_functions import getLockFilepath, setupLockFile
        from ..functions.utils_functions import getCurrentPID
        from ..functions.file_functions import suppressExistingFile
        from ..global_variables import (
                                    reading_json_statement,
                                    saving_to_json_statement,
                                    starting_clear_user_statement,
                                    clearing_user_statement,
                                )

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = winman.bpm_generalsettings

        if debug: print(starting_clear_user_statement) #debug

        lock_filepath = getLockFilepath()
        pid = getCurrentPID()

        if os.path.isfile(lock_filepath):
            datas = read_json(lock_filepath)
            if debug: print(reading_json_statement + lock_filepath) #debug

            chk_free = True
            n = 0

            for o in datas['opened']:

                if o['pid'] == self.pid_to_clear:
                    del datas['opened'][n]
                    if debug: print(clearing_user_statement + o['hostname']) #debug

                elif o['pid'] != pid:
                    chk_free = False

                n += 1

            if debug: print(saving_to_json_statement) #debug

            # make sure this process is locked
            if len(datas['opened']) == 0:
                suppressExistingFile(lock_filepath)
                setupLockFile()
            else:
                create_json_file(datas, lock_filepath)

            # set file free if needed
            if chk_free:
                general_settings.blend_already_opened = False

            # redraw
            for area in context.screen.areas:
                area.tag_redraw()

        return {'FINISHED'}