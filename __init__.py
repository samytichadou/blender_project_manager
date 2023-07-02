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
 "version": (2, 0, 0),
 "blender": (3, 0, 0),
 "location": "Timeline",  
 "description": "Manage small animation project from Blender",  
  "wiki_url": "https://github.com/samytichadou/blender_project_manager/wiki",  
 "tracker_url": "https://github.com/samytichadou/blender_project_manager/issues/new",  
 "category": "Animation",
 "warning": "Alpha version, use at your own risks"
 }




# IMPORT
##################################

from . import (
    addon_prefs,
    )

from .global_management import(
    manage_projects,
    manage_users,
    current_project_detection,
    )

from .project_management import(
    project_menu,
    project_users,
    )

from .asset_management import(
    asset_library_handler,
    reload_asset_list,
    )

# register
##################################

def register():
    addon_prefs.register()

    manage_projects.register()
    manage_users.register()
    current_project_detection.register()

    project_menu.register()
    project_users.register()

    asset_library_handler.register()
    reload_asset_list.register()

def unregister():
    addon_prefs.unregister()

    manage_projects.unregister()
    manage_users.unregister()
    current_project_detection.unregister()

    project_menu.unregister()
    project_users.unregister()

    asset_library_handler.unregister()
    reload_asset_list.unregister()
