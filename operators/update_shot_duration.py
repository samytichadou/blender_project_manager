import bpy
import os


from ..functions.file_functions import absolutePath


class BPMUpdateShotDuration(bpy.types.Operator):
    """Update selected shot(s) duration"""
    bl_idname = "bpm.update_shot_duration"
    bl_label = "Update Shot(s) duration"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project and general_settings.file_type == 'EDIT' and keyword in context.scene.name:
            if context.scene.sequence_editor:
                if context.scene.sequence_editor.active_strip:
                    active = context.scene.sequence_editor.active_strip
                    if active.type in {'SCENE'}:
                        if not active.lock:
                            if active.bpm_shotsettings.is_shot:
                                if os.path.isfile(absolutePath(active.bpm_shotsettings.shot_filepath)):
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
                                )
        from ..functions.strip_functions import (
                                            returnSelectedStrips, 
                                            getStripOffsets, 
                                            getStripNewTiming, 
                                            updateStripOnTimeline,
                                            returnShotStrips,
                                        )
        from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
        from ..functions.project_data_functions import getArgumentForPythonScript
        from ..functions.audio_sync_functions import syncAudioEdit
        
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        project_folder = general_settings.project_folder
        scn = context.scene

        active = scn.sequence_editor.active_strip

        if general_settings.debug: print(start_update_shot_statement) #debug

        for strip in returnShotStrips(scn.sequence_editor):

            if strip.select or strip == active:

                if general_settings.debug: print(checking_update_shot_statement + strip.name) #debug
                
                strip_scene = strip.scene
                new_start, new_end = getStripNewTiming(strip)

                if new_start != strip_scene.frame_start or new_end != strip_scene.frame_end:
                    if general_settings.debug: print(updating_shot_statement) #debug
                    if general_settings.debug: print(update_shot_new_start_end_statement + str(new_start) + "-" + str(new_end)) #debug

                    # check if frame become negative and avoid it
                    if new_start < 0:

                        self.report({'INFO'}, shot_update_impossible_message)
                        if general_settings.debug: print(shot_update_impossible_statement) #debug

                    else:

                        filepath = absolutePath(strip.bpm_shotsettings.shot_filepath)

                        arguments = getArgumentForPythonScript([new_start, new_end])

                        # build command
                        command = buildBlenderCommandBackgroundPython(update_shot_file, filepath, arguments)

                        if general_settings.debug: print(launching_command_statement + command) #debug

                        # launch command
                        launchCommand(command)

                        # update scene fram_start frame_end
                        strip_scene.frame_start = new_start
                        strip_scene.frame_end   = new_end

                        # update the strip
                        updateStripOnTimeline(strip, winman)

                        if general_settings.debug: print(updated_shot_statement) #debug

                elif general_settings.debug: print(no_update_needed_statement) #debug

        # update audio sync if existing
        audio_sync_filepath = os.path.join(project_folder, audio_sync_file)
        if os.path.isfile(audio_sync_filepath):
            syncAudioEdit(general_settings.debug, project_folder, scn)
        
        # reload sequencer if needed
        bpy.ops.sequencer.refresh_all()

        return {'FINISHED'}