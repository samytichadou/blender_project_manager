import bpy
import os


from ..functions.file_functions import absolutePath
from ..functions.reload_comments_function import reload_comments
from ..functions.check_file_poll_function import check_file_poll_function


def updateShotDurationEndFunction(strip):
    strip.bpm_shotsettings.is_working = False
    reload_comments(bpy.context, "edit_shot", strip)
    bpy.ops.sequencer.refresh_all()


class BPM_OT_update_shot_duration(bpy.types.Operator):
    """Update selected shot(s) duration"""
    bl_idname = "bpm.update_shot_duration"
    bl_label = "Update Shot(s) duration"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        is_bpm_project, bpm_filetype, bpm_active_strip = check_file_poll_function(context)
        if bpm_filetype == "EDIT" and bpm_active_strip:
            if not bpm_active_strip.lock:
                if not bpm_active_strip.bpm_shotsettings.is_working:
                    if not bpm_active_strip.bpm_shotsettings.is_rendering:
                        return True


    def execute(self, context):
        # import statements and functions
        from ..global_variables import (
                                    launching_command_statement,
                                    start_update_shot_statement,
                                    checking_update_shot_statement,
                                    updating_shot_statement,
                                    update_shot_new_start_end_statement,
                                    updated_shot_statement,
                                    no_update_needed_statement,
                                    update_shot_file,
                                    shot_update_impossible_message,
                                    shot_update_impossible_statement,
                                    audio_sync_file,
                                    strip_already_working_statement,
                                )
        from ..functions.strip_functions import (
                                            returnSelectedStrips, 
                                            getStripOffsets, 
                                            getStripNewTiming, 
                                            updateSceneStripOnTimeline,
                                            returnShotStrips,
                                            updateImageSequenceShot,
                                        )
        from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
        from ..functions.project_data_functions import getArgumentForPythonScript
        from ..functions.audio_sync_functions import syncAudioEdit
        from ..functions.change_strip_display_mode_functions import updateShotDisplayMode
        from ..functions.shot_settings_json_update_function import updateShotSettingsProperties
        from ..functions.threading_functions import launchSeparateThread
        
        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug
        general_settings = winman.bpm_generalsettings
        project_folder = general_settings.project_folder
        scn = context.scene
        sequencer = scn.sequence_editor

        active = sequencer.active_strip

        new_active = None

        if debug: print(start_update_shot_statement) #debug

        chk_updated = False

        for strip in returnShotStrips(sequencer):

            if strip.select or strip == active:

                if not strip.bpm_shotsettings.is_working:

                    if debug: print(checking_update_shot_statement + strip.name) #debug
                    
                    shot_settings = strip.bpm_shotsettings
                    
                    new_start, new_end = getStripNewTiming(strip)

                    if new_start != shot_settings.shot_frame_start or new_end != shot_settings.shot_frame_end:

                        if debug: print(updating_shot_statement) #debug
                        if debug: print(update_shot_new_start_end_statement + str(new_start) + "-" + str(new_end)) #debug

                        # check if frame become negative and avoid it
                        if new_start < 0:

                            self.report({'INFO'}, shot_update_impossible_message)
                            if debug: print(shot_update_impossible_statement) #debug

                        else:

                            chk_updated = True

                            filepath = absolutePath(strip.bpm_shotsettings.shot_filepath)

                            arguments = getArgumentForPythonScript([new_start, new_end])

                            # build command
                            command = buildBlenderCommandBackgroundPython(update_shot_file, filepath, arguments)

                            if debug: print(launching_command_statement + command) #debug

                            # launch command
                            #launchCommand(command)
                            # launchSeparateThread([command, debug, None])

                            # update shot settings and save json
                            shot_settings.shot_frame_start = new_start
                            shot_settings.shot_frame_end = new_end

                            updateShotSettingsProperties(shot_settings, context)

                            shot_settings.is_working = True

                            general_settings.bypass_update_tag = True

                            # update scene frame_start frame_end if scene strip
                            if strip.type == 'SCENE':
                                strip.scene.frame_start = new_start
                                strip.scene.frame_end   = new_end

                                # update the strip
                                if strip == active:
                                    new_active = new_strip = updateSceneStripOnTimeline(strip, winman)
                                else:
                                    new_strip = updateSceneStripOnTimeline(strip, winman)

                            # update for image strip
                            elif strip.type == 'IMAGE':
                                if strip == active:
                                    new_active = new_strip = updateImageSequenceShot(strip, winman)   
                                else:
                                    new_strip = updateImageSequenceShot(strip, winman)

                            general_settings.bypass_update_tag = False

                            launchSeparateThread([command, debug, None, updateShotDurationEndFunction, new_strip])               

                            if debug: print(updated_shot_statement) #debug
                            
                    elif debug: print(no_update_needed_statement) #debug

                elif debug: print(strip_already_working_statement + strip.name) #debug


        if chk_updated:
            
            # set back active strip if needed
            if new_active is not None:
                sequencer.active_strip = new_active

            # update audio sync if existing
            audio_sync_filepath = os.path.join(project_folder, audio_sync_file)
            if os.path.isfile(audio_sync_filepath):
                syncAudioEdit(debug, project_folder, scn)
            
            # reload sequencer if needed
            bpy.ops.sequencer.refresh_all()

        return {'FINISHED'}