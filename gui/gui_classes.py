import bpy

from ..functions.check_file_poll_function import check_file_poll_function


# sequencer class
class SequencerPanel_General(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "EDIT":
            return True

class SequencerPanel_Project(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "EDIT":
            return context.scene.bpm_scenesettings.display_panels == "PROJECT"

class SequencerPanel_Project_Debug(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "EDIT":
            if context.scene.bpm_scenesettings.display_panels == "PROJECT":
                return context.window_manager.bpm_projectdatas.debug

class SequencerPanel_Editing(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "EDIT":
            return context.scene.bpm_scenesettings.display_panels == "EDIT"

class SequencerPanel_Shot(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "EDIT" and active is not None:
            return context.scene.bpm_scenesettings.display_panels == "SHOT"

class SequencerPanel_Shot_Debug(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "EDIT" and active is not None:
            if context.scene.bpm_scenesettings.display_panels == "SHOT":
                return context.window_manager.bpm_projectdatas.debug

class SequencerPanel_Assets(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "EDIT":
            return context.scene.bpm_scenesettings.display_panels == "ASSETS"


# viewport class
class ViewportPanel_General(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            return True

class ViewportPanel_Project(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            return context.scene.bpm_scenesettings.display_panels == "PROJECT"

class ViewportPanel_Project_Debug(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            if context.scene.bpm_scenesettings.display_panels == "PROJECT":
                return context.window_manager.bpm_projectdatas.debug

class ViewportPanel_Shot(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "SHOT":
            return context.scene.bpm_scenesettings.display_panels == "SHOT"

class ViewportPanel_Shot_Debug(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "SHOT":
            if context.scene.bpm_scenesettings.display_panels == "SHOT":
                return context.window_manager.bpm_projectdatas.debug

class ViewportPanel_Assets_Library(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            return context.scene.bpm_scenesettings.display_panels == "ASSETS"

class ViewportPanel_Assets(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "ASSET":
            return context.scene.bpm_scenesettings.display_panels == "ASSETS"

class ViewportPanel_Assets_Debug(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            if context.scene.bpm_scenesettings.display_panels == "ASSETS":
                return context.window_manager.bpm_projectdatas.debug


# nodetree class
class NodetreePanel_General(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        return file_type in {"SHOT", "ASSET"}

class NodetreePanel_Project(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            return context.scene.bpm_scenesettings.display_panels == "PROJECT"

class NodetreePanel_Project_Debug(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            if context.scene.bpm_scenesettings.display_panels == "PROJECT":
                return context.window_manager.bpm_projectdatas.debug

class NodetreePanel_Shot(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "SHOT":
            return context.scene.bpm_scenesettings.display_panels == "SHOT"

class NodetreePanel_Shot_Debug(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "SHOT":
            if context.scene.bpm_scenesettings.display_panels == "SHOT":
                return context.window_manager.bpm_projectdatas.debug

class NodetreePanel_Assets_Library(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            return context.scene.bpm_scenesettings.display_panels == "ASSETS"

class NodetreePanel_Assets(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type == "ASSET":
            return context.scene.bpm_scenesettings.display_panels == "ASSETS"

class NodetreePanel_Assets_Debug(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "BPM"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        project, file_type, active = check_file_poll_function(context)
        if file_type in {"SHOT", "ASSET"}:
            if context.scene.bpm_scenesettings.display_panels == "ASSETS":
                return context.window_manager.bpm_projectdatas.debug


# filebrowser class
class FilebrowserPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "BPM"

