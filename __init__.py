'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {  
 "name": "BPM - Blender Project Manager",  
 "author": "Samy Tichadou (tonton)",  
 "version": (0, 2, 0),  
 "blender": (2, 83, 0),  
 "location": "Timeline",  
 "description": "Manage small animation project from Blender",  
  "wiki_url": "https://github.com/samytichadou/blender_project_manager/wiki",  
 "tracker_url": "https://github.com/samytichadou/blender_project_manager/issues/new",  
 "category": "Animation",
 "warning": "Alpha version, use at your own risks"
 }


import bpy


# IMPORT SPECIFICS
##################################

from .startup_handler import bpmStartupHandler
from .render_handler import bpm_render_handler
from .timer_function import bpmTimerFunction
from .functions.lock_file_functions import deleteLockFileHandler
from .functions.filebrowser_update_function import updateFilebrowserPath

from .operators.open_shot import *
from .operators.back_to_edit import *
from .operators.create_shot import *
from .operators.create_project import *
from .operators.update_shot_duration import *
from .operators.create_asset import *
from .operators.open_webpage import *
from .operators.comments_operators import *
from .operators.delete_unused_shots import *
from .operators.empty_project_recycle_bin import *
from .operators.bump_shot_version import *
from .operators.change_shot_version import *
from .operators.synchronize_audio_edit import *
from .operators.synchronize_audio_shot import *
from .operators.refresh_shot_datas import *
from .operators.import_asset import *
from .operators.open_asset_file import *
from .operators.show_open_blend_lock_file import *
from .operators.clear_lock_file_user import *
from .operators.render_shot_playblast import *
from .operators.modify_shot_tasks_deadlines import *
from .operators.open_folder import *
from .operators.render_shot_edit import *
from .operators.go_to_comment import *
from .operators.custom_folder_operator import *
from .operators.dialog_popup import *


from .operators.display_modify_project_settings import *
from .operators.save_project_settings_to_json import *
from .operators.display_modify_render_settings import *
from .operators.save_render_settings_to_json import *

from .properties import *
from .gui import *
from .asset_ui_list import *
from .addon_prefs import BPM_PF_addon_prefs

from .vse_extra_ui import disableSequencerUICallback
from .dopesheet_extra_ui import disable_dope_sheet_ui_callback


# register
##################################

classes = (BPM_OT_open_shot,
            BPM_OT_back_to_edit,
            BPM_OT_create_shot,
            BPM_OT_create_project,
            BPM_OT_update_shot_duration,
            BPM_OT_display_modify_project_settings,
            BPM_OT_display_modify_render_settings,
            BPM_OT_save_project_settings_to_json,
            BPM_OT_save_render_settings_to_json,
            BPM_OT_create_asset,
            BPM_OT_add_comment,
            BPM_OT_remove_comment,
            BPM_OT_modify_comment,
            BPM_OT_reload_comments,
            BPM_OT_delete_unused_shots,
            BPM_OT_empty_recycle_bin,
            BPM_OT_bump_shot_version_edit,
            BPM_OT_bump_shot_version_shot,
            BPM_OT_change_shot_version_edit,
            BPM_OT_synchronize_audio_edit,
            BPM_OT_synchronize_audio_shot,
            BPM_OT_refresh_edit_datas,
            BPM_OT_refresh_shot_datas,
            BPM_OT_import_asset,
            BPM_OT_open_asset_file,
            BPM_OT_show_open_blend_lock_file,
            BPM_OT_clear_lock_file_user,
            BPM_OT_render_shot_playblast,
            BPM_OT_modify_shot_task_deadline,
            BPM_OT_render_shot_edit,
            BPM_OT_goto_next_previous_comment,
            BPM_OT_goto_comment,
            BPM_OT_Custom_Folder_Actions,
            BPM_OT_refresh_custom_folders,
            BPM_OT_dialog_popups,

            BPM_OT_open_shot_folder,
            BPM_OT_open_shot_render_folder,
            BPM_OT_open_project_folder,
            BPM_OT_open_custom_folder,

            BPM_OT_open_url,
            BPM_OT_open_wiki_page,

            BPM_PF_addon_prefs,

            BPM_PR_shot_comments,
            BPM_PR_shot_comments_strips,
            BPM_PR_project_settings,
            BPM_PR_custom_folders,
            BPM_PR_asset_list,
            BPM_PR_asset_settings,
            BPM_PR_shot_settings_strips,
            BPM_PR_shot_settings,
            BPM_PR_scene_settings,
            BPM_PR_general_settings,
            BPM_PR_render_settings,

            BPM_PT_sequencer_panels_display_panel,
            BPM_PT_sequencer_management_panel,
            BPM_PT_sequencer_files_panel,
            BPM_PT_sequencer_management_debug_panel,
            BPM_PT_sequencer_edit_panel,
            BPM_PT_sequencer_edit_comment_panel,
            BPM_PT_sequencer_edit_ui_panel,
            BPM_PT_sequencer_edit_ui_shot_subpanel,
            BPM_PT_sequencer_edit_ui_shot_state_subpanel,
            BPM_PT_sequencer_edit_ui_shot_frame_comment_subpanel,
            BPM_PT_sequencer_edit_ui_timeline_frame_comment_subpanel,
            BPM_PT_sequencer_edit_ui_scheduling_subpanel,
            BPM_PT_sequencer_shot_tracking_panel,
            BPM_PT_sequencer_shot_version_panel,
            BPM_PT_sequencer_shot_comment_panel,
            BPM_PT_sequencer_shot_display_panel,
            BPM_PT_sequencer_shot_debug_panel,
            BPM_PT_sequencer_asset_library_panel,
            BPM_PT_viewport_panels_display_panel,
            BPM_PT_viewport_management_panel,
            BPM_PT_viewport_files_panel,
            BPM_PT_viewport_management_debug_panel,
            BPM_PT_viewport_shot_tracking_panel,
            BPM_PT_viewport_shot_version_panel,
            BPM_PT_viewport_shot_comment_panel,
            BPM_PT_viewport_shot_ui_comment_subpanel,
            BPM_PT_viewport_shot_render_panel,
            BPM_PT_viewport_shot_debug_panel,
            BPM_PT_viewport_asset_settings_panel,
            BPM_PT_viewport_asset_comment_panel,
            BPM_PT_viewport_asset_ui_comment_subpanel,
            BPM_PT_viewport_asset_library_panel,
            BPM_PT_viewport_asset_debug_panel,
            BPM_PT_nodetree_panels_display_panel,
            BPM_PT_nodetree_management_panel,
            BPM_PT_nodetree_files_panel,
            BPM_PT_nodetree_management_debug_panel,
            BPM_PT_nodetree_shot_tracking_panel,
            BPM_PT_nodetree_shot_version_panel,
            BPM_PT_nodetree_shot_comment_panel,
            BPM_PT_nodetree_shot_render_panel,
            BPM_PT_nodetree_shot_debug_panel,
            BPM_PT_nodetree_asset_settings_panel,
            BPM_PT_nodetree_asset_comment_panel,
            BPM_PT_nodetree_asset_library_panel,
            BPM_PT_nodetree_asset_debug_panel,
            BPM_PT_FileBrowser_Panel,
            BPM_UL_Folders_Uilist,
            BPM_UL_Asset_UI_List,
            BPM_MT_topbar_menu,
            BPM_MT_OpenFolder_Explorer_Menu,
            BPM_MT_OpenFolder_Filebrowser_Menu,
            BPM_MT_RightClickSequencerEdit_Menu,
            BPM_MT_RightClickSequencerShot_Menu,
            )


def register():

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPERTIES ###

    bpy.types.WindowManager.bpm_generalsettings = \
        bpy.props.PointerProperty(type = BPM_PR_general_settings, name="BPM general settings")

    bpy.types.WindowManager.bpm_projectdatas = \
        bpy.props.PointerProperty(type = BPM_PR_project_settings, name="BPM project datas")

    bpy.types.WindowManager.bpm_customfolders = \
        bpy.props.CollectionProperty(type = BPM_PR_custom_folders, name="BPM custom folders")

    bpy.types.WindowManager.bpm_assets = \
        bpy.props.CollectionProperty(type = BPM_PR_asset_list, name="BPM assets")

    bpy.types.WindowManager.bpm_assetsettings = \
        bpy.props.PointerProperty(type = BPM_PR_asset_settings, name="BPM asset settings")

    bpy.types.WindowManager.bpm_shotsettings = \
        bpy.props.PointerProperty(type = BPM_PR_shot_settings, name="BPM shot settings")

    bpy.types.WindowManager.bpm_rendersettings = \
        bpy.props.CollectionProperty(type = BPM_PR_render_settings, name="BPM render settings")

    bpy.types.SceneSequence.bpm_shotsettings = \
        bpy.props.PointerProperty(type = BPM_PR_shot_settings_strips, name="BPM shot settings")

    bpy.types.ImageSequence.bpm_shotsettings = \
        bpy.props.PointerProperty(type = BPM_PR_shot_settings_strips, name="BPM shot settings")

    bpy.types.Scene.bpm_scenesettings = \
        bpy.props.PointerProperty(type = BPM_PR_scene_settings, name="BPM scene settings")

    bpy.types.Collection.bpm_isasset = \
        bpy.props.BoolProperty(default = False)

    bpy.types.Material.bpm_isasset = \
        bpy.props.BoolProperty(default = False)

    bpy.types.NodeTree.bpm_isasset = \
        bpy.props.BoolProperty(default = False)

    bpy.types.World.bpm_isasset = \
        bpy.props.BoolProperty(default = False)

    ### HANDLER ###
    bpy.app.handlers.load_post.append(bpmStartupHandler)
    bpy.app.handlers.load_pre.append(deleteLockFileHandler)
    bpy.app.handlers.render_post.append(bpm_render_handler)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.prepend(draw_topbar)
    bpy.types.SEQUENCER_MT_context_menu.prepend(drawRightClickSequencerMenu)


def unregister():

    ### DISABLE EXTRA UI IF EXISTING ###
    disableSequencerUICallback()
    disable_dope_sheet_ui_callback()
    
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPERTIES ###
    del bpy.types.WindowManager.bpm_generalsettings
    del bpy.types.WindowManager.bpm_projectdatas
    del bpy.types.WindowManager.bpm_customfolders
    del bpy.types.WindowManager.bpm_assets
    del bpy.types.WindowManager.bpm_shotsettings
    del bpy.types.WindowManager.bpm_rendersettings

    del bpy.types.SceneSequence.bpm_shotsettings

    del bpy.types.ImageSequence.bpm_shotsettings

    del bpy.types.Scene.bpm_scenesettings

    del bpy.types.Collection.bpm_isasset

    del bpy.types.Material.bpm_isasset

    del bpy.types.NodeTree.bpm_isasset

    del bpy.types.World.bpm_isasset

    ### HANDLER ###
    bpy.app.handlers.load_post.remove(bpmStartupHandler)
    bpy.app.handlers.load_pre.remove(deleteLockFileHandler)
    bpy.app.handlers.render_post.remove(bpm_render_handler)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_topbar)
    bpy.types.SEQUENCER_MT_context_menu.remove(drawRightClickSequencerMenu)

    ### TIMER ###
    if bpy.app.timers.is_registered(bpmTimerFunction):
         bpy.app.timers.unregister(bpmTimerFunction)
