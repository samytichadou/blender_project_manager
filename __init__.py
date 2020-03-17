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
from .operators.open_shot import *
from .operators.back_to_edit import *
from .properties import *
from .gui import *


# register
##################################

classes = (OpenShot,
            BackToEdit,
            ProjectSettings,
            BpmSequencerPanel,
            )

def register():

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPERTIES ###
    bpy.types.WindowManager.bpm_isproject = \
        bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.bpm_isedit = \
        bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.bpm_debug = \
        bpy.props.BoolProperty(default=True)
    bpy.types.WindowManager.bpm_datas = \
        bpy.props.CollectionProperty(type = ProjectSettings)

    ### HANDLER ###
    bpy.app.handlers.load_post.append(bpmStartupHandler)

def unregister():
    
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPERTIES ###
    del bpy.types.WindowManager.bpm_isproject
    del bpy.types.WindowManager.bpm_isedit
    del bpy.types.WindowManager.bpm_debug
    del bpy.types.WindowManager.bpm_datas

    ### HANDLER ###
    bpy.app.handlers.load_post.remove(bpmStartupHandler)