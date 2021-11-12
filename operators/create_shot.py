import bpy
import os
import shutil

from ..functions import file_functions as fl_fct
from ..functions.utils_functions import clearDataUsers
from ..functions import project_data_functions as pjt_dta_fct
from ..functions.command_line_functions import buildBlenderCommandBackgroundPython
from ..functions import strip_functions as str_fct
from ..functions import json_functions as js_fct
from ..functions.audio_sync_functions import syncAudioEdit
from ..functions.shot_settings_json_update_function import updateShotSettingsProperties
from ..functions.threading_functions import launchSeparateThread
from .. import global_variables as g_var



# link proper scene, thread endfunction
def linkSceneToStrip(strip, lib_file, scene_name, python_script, debug):
    scene_list = fl_fct.linkExternalScenes(lib_file)
    old_scene_name = strip.scene.name

    for s in scene_list:
        if s == scene_name:

            # relink proper scene
            strip.scene = bpy.data.scenes[s]

            # remove old scene and reload lib
            for scn in bpy.data.scenes:
                if scn.library:
                    if scn.name == old_scene_name and fl_fct.absolutePath(scn.library.filepath) == lib_file:
                        clearDataUsers(scn)
                        bpy.data.scenes.remove(scn, do_unlink = False)
            break
    
    # strip not working
    strip.bpm_shotsettings.is_working = False
    # bpy.ops.sequencer.refresh_all()

    # delete the python temp
    fl_fct.suppressExistingFile(python_script)


class BPM_OT_create_shot(bpy.types.Operator):
    """Create Shot from Timeline"""
    bl_idname = "bpm.create_shot"
    bl_label = "Create Shot"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        return general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name

    def execute(self, context):
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = context.window_manager.bpm_generalsettings
        scn = context.scene
        
        if debug: print(g_var.creating_shot_statement) #debug
        
        project_datas = winman.bpm_projectdatas
        project_folder = general_settings.project_folder
        shot_folder_path = os.path.join(project_folder, g_var.shot_folder)
        next_shot_folder, next_shot_file, next_shot_number = fl_fct.getNextShot(winman, project_datas, pjt_dta_fct.getShotPattern(project_datas), 1, shot_folder_path)

        # check timeline available space
        if debug: print(g_var.checking_available_timeline_space_statement) #debug
        name = project_datas.shot_prefix + next_shot_number
        start = scn.frame_current
        duration = project_datas.default_shot_length
        sequencer = scn.sequence_editor
        channel = str_fct.returnAvailablePositionStripChannel(start, duration, sequencer)

        # if no place to put the clip
        if channel == 0:
            # return no place to put the strip
            self.report({'INFO'}, g_var.no_available_timeline_space_message)
            if debug: print(g_var.no_available_timeline_space_statement) #debug
            return {'FINISHED'}

        # create shot dir
        fl_fct.createDirectory(next_shot_folder)
        if debug: print(g_var.folder_created_statement + next_shot_folder) #debug

        # copy shot file
        ressources_folderpath = os.path.join(project_folder, g_var.ressources_folder)
        startup_folderpath = os.path.join(ressources_folderpath, g_var.startup_files_folder)
        shot_startup_filepath = os.path.join(startup_folderpath, g_var.shot_startup_file)
        shutil.copy(shot_startup_filepath, next_shot_file)

        if debug: print(g_var.copying_file_statement + shot_startup_filepath) #debug

        # create the json file
        if debug: print(g_var.saving_to_json_statement) #debug

        shot_json = os.path.join(next_shot_folder, g_var.shot_file)
        # format the json dataset
        json_dataset = js_fct.createJsonDatasetFromProperties(winman.bpm_shotsettings, ())
        json_dataset['shot_folder'] = next_shot_folder
        json_dataset['shot_filepath'] = bpy.path.relpath(next_shot_file)

        js_fct.create_json_file(json_dataset, shot_json)

        if debug: print(g_var.saved_to_json_statement) #debug


        # modify and copy python script
        replacement_list = pjt_dta_fct.getScriptReplacementListShotCreation(project_datas, next_shot_folder, next_shot_file, next_shot_number)
        
        temp_python_script = os.path.join(next_shot_folder, g_var.python_temp)
        if debug: print(g_var.creating_python_script_statement + temp_python_script) #debug

        fl_fct.replaceContentInPythonScript(g_var.shot_setup_file, temp_python_script, replacement_list)
        if debug: print(g_var.python_script_created_statement) #debug

        # launch the blend command
        # command = buildBlenderCommandBackgroundPython(temp_python_script, next_shot_file, "")
        # launchCommand(command)
        # if debug: print(g_var.launching_command_statement + command) #debug

        # link shot
        scene_list = fl_fct.linkExternalScenes(next_shot_file)
        if debug: print(g_var.scenes_linked_statement + next_shot_file) #debug

        # set temp scene to link
        scn_to_link = bpy.data.scenes[scene_list[0]]
        scn_to_link.frame_start = project_datas.shot_start_frame
        scn_to_link.frame_end = project_datas.shot_start_frame + duration

        # add it to timeline
        linked_strip = sequencer.sequences.new_scene(
            name=name, 
            scene=scn_to_link, 
            channel=channel, 
            frame_start=start
            )

        # set strip settings
        shot_settings = linked_strip.bpm_shotsettings

        shot_settings.shot_filepath = json_dataset['shot_filepath']
        shot_settings.shot_frame_start = project_datas.shot_start_frame
        shot_settings.shot_frame_end = project_datas.shot_start_frame + duration
        linked_strip.bpm_shotsettings.is_shot = True
        linked_strip.bpm_shotsettings.shot_folder = next_shot_folder
        
        updateShotSettingsProperties(shot_settings, context)
        
        shot_settings.is_working = True

        # launch the blend command
        command = buildBlenderCommandBackgroundPython(temp_python_script, next_shot_file, "")
        if debug: print(g_var.launching_command_statement + command) #debug
        launchSeparateThread([command, debug, None, linkSceneToStrip, linked_strip, next_shot_file, name, temp_python_script, debug])

        # # delete the python temp
        # fl_fct.suppressExistingFile(temp_python_script)
        # if debug: print(deleted_file_statement + temp_python_script) #debug

        # create render folders
        #createShotRenderFolders(next_shot_file, winman)

        # select created strip
        sequencer.active_strip = linked_strip
        str_fct.deselectAllStrips(sequencer)
        linked_strip.select = True

        # update audio sync if existing
        audio_sync_filepath = os.path.join(project_folder, g_var.audio_sync_file)
        if os.path.isfile(audio_sync_filepath):
            syncAudioEdit(debug, general_settings.project_folder, scn)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_create_shot)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_create_shot)