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
 "name": "Project Manager",  
 "author": "Samy Tichadou (tonton)",  
 "version": (0, 1),  
 "blender": (2, 83, 0),  
 "location": "Timeline",  
 "description": "Manage small animation project from Blender",  
  "wiki_url": "https://github.com/samytichadou/blender_project_manager/wiki",  
 "tracker_url": "https://github.com/samytichadou/blender_project_manager/issues/new",  
 "category": "Animation"}


import bpy


# IMPORT SPECIFICS
##################################

from .startup_handler import bpmStartupHandler
from .functions.filebrowser_update_function import updateFilebrowserPath

from .operators.open_shot import *
from .operators.back_to_edit import *
from .operators.create_shot import *
from .operators.create_project import *
from .operators.update_shot_duration import *
from .operators.create_asset import *
from .operators.open_webpage import *
from .operators.add_modify_shot_marker import *
from .operators.delete_unused_shots import *
from .operators.empty_project_recycle_bin import *
from .operators.bump_shot_version import *
from .operators.change_shot_version import *
from .operators.synchronize_audio_edit import *
from .operators.synchronize_audio_shot import *
from .operators.refresh_shot_datas import *

from .operators.display_modify_project_settings import *
from .operators.save_project_settings_to_json import *

from .properties import *
from .gui import *

from .vse_extra_ui import disableSequencerCallback


# register
##################################

classes = (BPMOpenShot,
            BPMBackToEdit,
            BPMCreateShot,
            BpmCreateProject,
            BPMUpdateShotDuration,
            BpmDisplayModifyProjectSettings,
            BpmSaveProjectSettingsToJson,
            BPMCreateAsset,
            BPMAddModifyShotMarker,
            BPMDeleteUnusedShots,
            BPMEmptyRecycleBin,
            BPMBumpShotVersionFromEdit,
            BPMBumpChangeShotVersionFromEdit,
            BPMSynchronizeAudioEdit,
            BPMSynchronizeAudioShot,
            BPMRefreshShotDatasEdit,
            BPMRefreshShotDatasShot,

            BPMOpenWikiPage,

            BPMProjectSettings,
            BPMCustomFolders,
            BPMAssetList,
            BPMAssetSettings,
            BPMShotSettingsStrips,
            BPMShotSettings,
            BPMSceneSettings,
            BPMGeneralSettings,

            BPM_PT_sequencer_management_panel,
            BPM_PT_sequencer_shot_panel,
            BPM_PT_sequencer_shot_asset_panel,
            BPM_PT_sequencer_ui_panel,
            BPM_PT_properties_shot_panel,
            BPM_PT_properties_asset_panel,
            BPM_MT_topbar_menu,
            BPM_UL_Folders_Uilist,
            BPM_PT_FileBrowser_Panel,
            )


def register():

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPERTIES ###

    bpy.types.WindowManager.bpm_generalsettings = \
        bpy.props.PointerProperty(type = BPMGeneralSettings, name="BPM general settings")

    bpy.types.WindowManager.bpm_projectdatas = \
        bpy.props.PointerProperty(type = BPMProjectSettings)

    bpy.types.WindowManager.bpm_customfolders = \
        bpy.props.CollectionProperty(type = BPMCustomFolders)

    bpy.types.WindowManager.bpm_assets = \
        bpy.props.CollectionProperty(type = BPMAssetList)

    bpy.types.WindowManager.bpm_assetsettings = \
        bpy.props.PointerProperty(type = BPMAssetSettings, name="BPM asset settings")

    bpy.types.WindowManager.bpm_shotsettings = \
        bpy.props.PointerProperty(type = BPMShotSettings, name="BPM shot settings")

    bpy.types.SceneSequence.bpm_shotsettings = \
        bpy.props.PointerProperty(type = BPMShotSettingsStrips, name="BPM shot settings")

    bpy.types.Scene.bpm_scenesettings = \
        bpy.props.PointerProperty(type = BPMSceneSettings, name="BPM scene settings")

    bpy.types.Collection.bpm_isasset = \
        bpy.props.BoolProperty(default = False)

    bpy.types.Material.bpm_isasset = \
        bpy.props.BoolProperty(default = False)

    ### HANDLER ###
    bpy.app.handlers.load_post.append(bpmStartupHandler)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.prepend(bpmTopbarFunction)


def unregister():

    ### DISABLE EXTRA UI IF EXISTING ###
    disableSequencerCallback()
    
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

    del bpy.types.SceneSequence.bpm_shotsettings

    del bpy.types.Scene.bpm_scenesettings

    del bpy.types.Collection.bpm_isasset

    del bpy.types.Material.bpm_isasset

    ### HANDLER ###
    bpy.app.handlers.load_post.remove(bpmStartupHandler)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.remove(bpmTopbarFunction)