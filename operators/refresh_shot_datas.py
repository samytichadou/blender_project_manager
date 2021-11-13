import bpy

from ..functions import project_data_functions as pjt_dta_fct
from ..functions.reload_comments_function import reload_comments
from .. import global_variables as g_var


class BPM_OT_refresh_edit_datas(bpy.types.Operator):
    """Refresh timeline datas from edit"""
    bl_idname = "bpm.refresh_edit_datas"
    bl_label = "Refresh timeline datas"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name

    def execute(self, context):
        
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug

        if debug: print(g_var.refreshing_timeline_shot_datas_statement) #debug

        pjt_dta_fct.refreshTimelineShotDatas(context, context.scene.sequence_editor)

        if debug: print(g_var.refreshed_timeline_shot_datas_statement) #debug

        return {'FINISHED'}


# refresh shot datas func
def refresh_shot_datas(context):
    winman = context.window_manager
    debug = winman.bpm_projectdatas.debug
    general_settings = winman.bpm_generalsettings

    shot_json = pjt_dta_fct.getShotSettingsFileFromBlend()

    if shot_json is None:
        return False

    if debug: print(g_var.shot_loading_statement + shot_json) #debug

    # load json in props
    shot_settings = winman.bpm_shotsettings

    general_settings.bypass_update_tag = True
    pjt_dta_fct.loadJsonDataToDataset(winman, shot_settings, shot_json, ())
    general_settings.bypass_update_tag = False

    # refresh comments
    reload_comments(context, "shot", None)

    if debug: print(g_var.shot_loaded_statement) #debug

    return True


class BPM_OT_refresh_shot_datas(bpy.types.Operator):
    """Refresh shot datas from shot"""
    bl_idname = "bpm.refresh_shot_datas"
    bl_label = "Refresh shot datas"
    bl_options = {'REGISTER'}


    @classmethod
    def poll(cls, context):
        if context.window_manager.bpm_generalsettings.is_project:
            if context.window_manager.bpm_generalsettings.file_type == 'SHOT':
                return True

    def execute(self, context):

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug

        if not refresh_shot_datas(context):
            self.report({'INFO'}, g_var.missing_shot_file_message)
            return {'FINISHED'}
    
        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_refresh_edit_datas)
    bpy.utils.register_class(BPM_OT_refresh_shot_datas)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_refresh_edit_datas)
    bpy.utils.unregister_class(BPM_OT_refresh_shot_datas)