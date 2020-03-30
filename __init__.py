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
  "wiki_url": "https://github.com/samytichadou/blender_project_manager",  
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

            BPMOpenWikiPage,

            BPMProjectSettings,
            BPMCustomFolders,
            BPMAssetSettings,
            BPMShotSettings,

            BPM_PT_sequencer_management_panel,
            BPM_PT_sequencer_shot_panel,
            BPM_PT_sequencer_ui_panel,
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
    bpy.types.WindowManager.bpm_isproject = \
        bpy.props.BoolProperty(default=False)
    file_type = [
        ('EDIT', 'Edit', ""),
        ('SHOT', 'Shot', ""),
        ('ASSET', 'Asset', ""),
        ('NONE', 'None', ""),
        ]
    bpy.types.WindowManager.bpm_filetype = \
        bpy.props.EnumProperty(items = file_type, default='NONE')
    bpy.types.WindowManager.bpm_debug = \
        bpy.props.BoolProperty(default=True)
    bpy.types.WindowManager.bpm_foldersindex = \
        bpy.props.IntProperty(update = updateFilebrowserPath)
    bpy.types.WindowManager.bpm_projectfolder = \
        bpy.props.StringProperty(name = 'Project Folder', subtype = 'DIR_PATH')
    bpy.types.WindowManager.bpm_datas = \
        bpy.props.CollectionProperty(type = BPMProjectSettings)
    bpy.types.WindowManager.bpm_folders = \
        bpy.props.CollectionProperty(type = BPMCustomFolders)
    bpy.types.WindowManager.bpm_assets = \
        bpy.props.CollectionProperty(type = BPMAssetSettings)
    bpy.types.WindowManager.bpm_shots = \
        bpy.props.CollectionProperty(type = BPMShotSettings)

    bpy.types.SceneSequence.bpm_isshot = \
        bpy.props.BoolProperty(default=False)
    bpy.types.SceneSequence.bpm_displaymarkers = \
        bpy.props.BoolProperty(name = "Display markers", default=False)
    bpy.types.SceneSequence.bpm_shotstate = \
        bpy.props.EnumProperty(name = "Shot state", items = shot_state_items, default = 'STORYBOARD')
    bpy.types.SceneSequence.bpm_shotassets = \
        bpy.props.PointerProperty(type = BPMAssetSettings, name="Assets list") # test prop test TODO

    bpy.types.Scene.bpm_extraui = \
        bpy.props.BoolProperty(name = "Extra UI", default=True)
    bpy.types.Scene.bpm_displayshotstrip = \
        bpy.props.BoolProperty(name = "Shot strips", default=True)
    display_marker_items = [
        ('NONE', 'None', ""),
        ('SELECTED', 'Selected', ""),
        ('PERSTRIP', 'Per strip', ""),
        ('ALL', 'All', ""),
        ]
    bpy.types.Scene.bpm_displaymarkers = \
        bpy.props.EnumProperty(name = "Shot markers", items = display_marker_items, default = 'ALL')
    display_marker_name_items = [
        ('NONE', 'None', ""),
        ('CURRENT', 'Current', ""),
        ('ALL', 'All', ""),
        ]
    bpy.types.Scene.bpm_displaymarkernames = \
        bpy.props.EnumProperty(name = "Marker names", items = display_marker_name_items, default = 'ALL')
    bpy.types.Scene.bpm_displaymarkerboxes = \
        bpy.props.BoolProperty(name = "Marker boxes", default=True)
    bpy.types.Scene.bpm_displaymarkerlimit = \
        bpy.props.IntProperty(name = "Marker text limit", default = 15)
    bpy.types.Scene.bpm_displayshotupdatewarning = \
        bpy.props.BoolProperty(name = "Shot update warning", default=True)

    ### HANDLER ###
    bpy.app.handlers.load_post.append(bpmStartupHandler)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.prepend(bpmTopbarFunction)
    bpy.types.TOPBAR_MT_file.prepend(bpmFileMenuFunction)


def unregister():

    ### DISABLE EXTRA UI IF EXISTING ###
    disableSequencerCallback()
    
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPERTIES ###
    del bpy.types.WindowManager.bpm_isproject
    del bpy.types.WindowManager.bpm_filetype
    del bpy.types.WindowManager.bpm_debug
    del bpy.types.WindowManager.bpm_foldersindex
    del bpy.types.WindowManager.bpm_projectfolder
    del bpy.types.WindowManager.bpm_datas
    del bpy.types.WindowManager.bpm_folders
    del bpy.types.WindowManager.bpm_assets
    del bpy.types.WindowManager.bpm_shots

    del bpy.types.SceneSequence.bpm_isshot
    del bpy.types.SceneSequence.bpm_displaymarkers
    del bpy.types.SceneSequence.bpm_shotstate
    del bpy.types.SceneSequence.bpm_shotassets # test prop test TODO

    del bpy.types.Scene.bpm_extraui
    del bpy.types.Scene.bpm_displayshotstrip
    del bpy.types.Scene.bpm_displaymarkers
    del bpy.types.Scene.bpm_displaymarkernames
    del bpy.types.Scene.bpm_displaymarkerboxes
    del bpy.types.Scene.bpm_displaymarkerlimit
    del bpy.types.Scene.bpm_displayshotupdatewarning

    ### HANDLER ###
    bpy.app.handlers.load_post.remove(bpmStartupHandler)

    ### SPECIAL GUI ###
    bpy.types.TOPBAR_HT_upper_bar.remove(bpmTopbarFunction)
    bpy.types.TOPBAR_MT_file.remove(bpmFileMenuFunction)