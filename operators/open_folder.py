import bpy
import os

# shot folder
class BPMOpenShotFolder(bpy.types.Operator):
    """Open Shot Folder"""
    bl_idname = "bpm.open_shot_folder"
    bl_label = "Open Shot Folder"
    bl_options = {'REGISTER'}

    context : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if general_settings.file_type == 'SHOT':
                return True
            elif general_settings.file_type == 'EDIT':
                keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
                if keyword in context.scene.name:
                    if context.scene.sequence_editor:
                        if context.scene.sequence_editor.active_strip:
                            active = context.scene.sequence_editor.active_strip
                            if active.type in {'SCENE', 'IMAGE'}:
                                if not active.lock:
                                    if active.bpm_shotsettings.is_shot:
                                        return True

    def execute(self, context):
        from ..functions.utils_functions import openFolderInExplorer
        from ..functions.file_functions import absolutePath
        from ..global_variables import opening_folder_statement, no_folder_statement

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        absolute_path = None

        # get shot settings and filepath 
        if general_settings.file_type == 'EDIT':
            shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
            absolute_path = os.path.dirname(absolutePath(shot_settings.shot_filepath))

        elif general_settings.file_type == 'SHOT':
            absolute_path = os.path.dirname(bpy.data.filepath)

        # open if available        
        if os.path.isdir(absolute_path):

            if general_settings.debug: print(opening_folder_statement + absolute_path) #debug

            if self.context == 'filebrowser':
                area = context.area
                area.spaces[0].params.directory = str.encode(absolute_path)

            else:
                openFolderInExplorer(absolute_path)

        else:
            if general_settings.debug: print(no_folder_statement + absolute_path) #debug

        return {'FINISHED'}


# shot render folder
class BPMOpenShotRenderFolder(bpy.types.Operator):
    """Open Shot Render Folder"""
    bl_idname = "bpm.open_shot_render_folder"
    bl_label = "Open Shot Render Folder"
    bl_options = {'REGISTER'}

    context : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if general_settings.file_type == 'SHOT':
                return True
            elif general_settings.file_type == 'EDIT':
                keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
                if keyword in context.scene.name:
                    if context.scene.sequence_editor:
                        if context.scene.sequence_editor.active_strip:
                            active = context.scene.sequence_editor.active_strip
                            if active.type in {'SCENE', 'IMAGE'}:
                                if not active.lock:
                                    if active.bpm_shotsettings.is_shot:
                                        return True

    def execute(self, context):
        from ..functions.utils_functions import openFolderInExplorer
        from ..functions.file_functions import absolutePath
        from ..global_variables import opening_folder_statement, no_folder_statement

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        absolute_path = None

        # get shot settings and filepath 
        if general_settings.file_type == 'EDIT':
            shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
            absolute_path = os.path.dirname(absolutePath(shot_settings.shot_filepath))

        elif general_settings.file_type == 'SHOT':
            absolute_path = os.path.dirname(bpy.data.filepath)

        # open if available        
        if os.path.isdir(absolute_path):

            if general_settings.debug: print(opening_folder_statement + absolute_path) #debug

            if self.context == 'filebrowser':
                area = context.area
                area.spaces[0].params.directory = str.encode(absolute_path)

            else:
                openFolderInExplorer(absolute_path)

        else:
            if general_settings.debug: print(no_folder_statement + absolute_path) #debug

        return {'FINISHED'}