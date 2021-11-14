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
 "version": (0, 3, 0),  
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

from . import(
    folders_ui_list,
    asset_ui_list,
    gui,
    properties,
    addon_prefs,
    dopesheet_extra_ui,
    vse_extra_ui,
    startup_handler,
    render_handler,
    timer_function,
)

from .operators import(
    back_to_edit,
    open_shot,
    create_shot,
    create_project,
    update_shot_duration,
    display_modify_project_settings,
    display_modify_render_settings,
    save_project_settings_to_json,
    save_render_settings_to_json,
    create_asset,
    comments_operators,
    delete_unused_shots,
    empty_project_recycle_bin,
    bump_shot_version,
    change_shot_version,
    synchronize_audio_edit,
    synchronize_audio_shot,
    refresh_shot_datas,
    import_asset,
    open_asset_file,
    show_open_blend_lock_file,
    clear_lock_file_user,
    render_shot_playblast,
    modify_shot_tasks_deadlines,
    render_shot_edit,
    go_to_comment,
    custom_folder_operator,
    dialog_popup,
    open_folder,
    open_webpage,
)

from .functions.lock_file_functions import deleteLockFileHandler


# register
##################################

def register():

    folders_ui_list.register()
    asset_ui_list.register()
    gui.register()
    properties.register()
    addon_prefs.register()

    ### HANDLERS ###
    startup_handler.register()
    render_handler.register()

    ### OPERATORS ###
    back_to_edit.register()
    open_shot.register()
    create_shot.register()
    create_project.register()
    update_shot_duration.register()
    display_modify_project_settings.register()
    display_modify_render_settings.register()
    save_project_settings_to_json.register()
    save_render_settings_to_json.register()
    create_asset.register()
    comments_operators.register()
    delete_unused_shots.register()
    empty_project_recycle_bin.register()
    bump_shot_version.register()
    change_shot_version.register()
    synchronize_audio_edit.register()
    synchronize_audio_shot.register()
    refresh_shot_datas.register()
    import_asset.register()
    open_asset_file.register()
    show_open_blend_lock_file.register()
    clear_lock_file_user.register()
    render_shot_playblast.register()
    modify_shot_tasks_deadlines.register()
    render_shot_edit.register()
    go_to_comment.register()
    custom_folder_operator.register()
    dialog_popup.register()
    open_folder.register()
    open_webpage.register()

    ### HANDLER ###
    bpy.app.handlers.load_pre.append(deleteLockFileHandler)


def unregister():

    folders_ui_list.unregister()
    asset_ui_list.unregister()
    gui.unregister()
    properties.unregister()
    addon_prefs.unregister()

    ### EXTRA UI ###
    dopesheet_extra_ui.unregister()
    vse_extra_ui.unregister()

    ### HANDLERS ###
    startup_handler.unregister()
    render_handler.unregister()

    timer_function.unregister()

    ### OPERATORS ###
    back_to_edit.unregister()
    open_shot.unregister()
    create_shot.unregister()
    create_project.unregister()
    update_shot_duration.unregister()
    display_modify_project_settings.unregister()
    display_modify_render_settings.unregister()
    save_project_settings_to_json.unregister()
    save_render_settings_to_json.unregister()
    create_asset.unregister()
    comments_operators.unregister()
    delete_unused_shots.unregister()
    empty_project_recycle_bin.unregister()
    bump_shot_version.unregister()
    change_shot_version.unregister()
    synchronize_audio_edit.unregister()
    synchronize_audio_shot.unregister()
    refresh_shot_datas.unregister()
    import_asset.unregister()
    open_asset_file.unregister()
    show_open_blend_lock_file.unregister()
    clear_lock_file_user.unregister()
    render_shot_playblast.unregister()
    modify_shot_tasks_deadlines.unregister()
    render_shot_edit.unregister()
    go_to_comment.unregister()
    custom_folder_operator.unregister()
    dialog_popup.unregister()
    open_folder.unregister()
    open_webpage.unregister()

    ### HANDLER ###
    bpy.app.handlers.load_pre.remove(deleteLockFileHandler)