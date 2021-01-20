import bpy
import os


from ..functions.update_custom_folder_file import update_custom_folder_file
from ..global_variables import (
                            custom_folder_added_statement,
                            custom_folder_moved_statement,
                            custom_folder_not_selected_message,
                            unable_to_move_custom_folder_message,
                        )

class BPM_OT_Custom_Folder_Actions(bpy.types.Operator):
    """Add, Remove or Move Project Custom Folders"""
    bl_idname = "bpm.custom_folder_actions"
    bl_label = "Custom Folders Actions"
    bl_options = {'REGISTER', 'INTERNAL'}

    actions_items = (
                ('UP', "Up", ""),
                ('DOWN', "Down", ""),
                ('REMOVE', "Remove", ""),
                ('ADD', "Add", ""),
                    )

    action = bpy.props.EnumProperty(items = actions_items)

    @classmethod
    def poll(cls, context):
        return context.window_manager.bpm_generalsettings.is_project

    def execute(self, context):

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        custom_folders_coll = winman.bpm_customfolders
        general_settings = winman.bpm_generalsettings
        area = context.area

        # refresh list
        
        # actions
        general_settings.bypass_update_tag = True

        if self.action == "ADD":
            new = custom_folders_coll.add()

            new.filepath = bytes.decode(area.spaces[0].params.directory)
            new.name = os.path.basename(os.path.normpath(new.filepath))
            general_settings.custom_folders_index = len(custom_folders_coll) - 1

            if debug: print(custom_folder_added_statement) #debug

        else:
            idx = general_settings.custom_folders_index

            if idx not in range(0, len(custom_folders_coll)):
                self.report({'INFO'}, custom_folder_not_selected_message)
                return {'FINISHED'}

            if self.action == 'REMOVE':
                general_settings.bypass_update_tag = False
                custom_folders_coll.remove(idx)
                if idx > 0:
                    general_settings.custom_folders_index -= 1

            elif self.action == 'UP' and idx > 0:
                custom_folders_coll.move(idx, idx - 1)
                general_settings.custom_folders_index -= 1
                if debug: print(custom_folder_moved_statement) #debug

            elif self.action == 'DOWN' and idx < len(custom_folders_coll) - 1:
                custom_folders_coll.move(idx, idx + 1)
                general_settings.custom_folders_index += 1
                if debug: print(custom_folder_moved_statement) #debug

            else:
                self.report({'INFO'}, unable_to_move_custom_folder_message)

        general_settings.bypass_update_tag = False

        # save to json
        update_custom_folder_file(winman)
        
        return {'FINISHED'}