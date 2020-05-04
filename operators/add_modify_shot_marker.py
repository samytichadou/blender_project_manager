import bpy


# reload library
def reloadLibrary(library):
    library.reload()


class BPMAddModifyShotMarker(bpy.types.Operator):
    """Add or modify shot marker to active strip"""
    bl_idname = "bpm.add_modify_shot_marker"
    bl_label = "Add/Modify shot marker"
    bl_options = {'REGISTER'}

    name : bpy.props.StringProperty(name = "Marker name", default = "Marker name")
    frame : bpy.props.IntProperty(name = "Marker frame")
    modify_delete_items = [
        ('MODIFY', 'Modify', ""),
        ('DELETE', 'Delete', ""),
        ]
    modify_delete : bpy.props.EnumProperty(items = modify_delete_items, default = 'MODIFY')
    existing_marker = False

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_projectdatas.edit_scene_keyword
        if context.window_manager.bpm_generalsettings.is_project and context.window_manager.bpm_generalsettings.file_type == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor.active_strip:
                    if context.scene.sequence_editor:
                        active = context.scene.sequence_editor.active_strip
                        if active.type in {'SCENE'}:
                            if not active.lock:
                                try:
                                    if active.bpm_shotsettings.is_shot and active.scene.library:
                                        return True
                                except AttributeError:
                                    return False

    def invoke(self, context, event):
        from ..vse_extra_ui import getMarkerFrameFromShotStrip

        scn = context.scene
        self.frame = context.scene.frame_current

        active = context.scene.sequence_editor.active_strip

        for m in getMarkerFrameFromShotStrip(active):
            if m[1] == scn.frame_current:
                self.name = m[0]
                self.existing_marker = True
                break
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        if not self.existing_marker:
            layout.label(text = "Add")
            # frame
            layout.prop(self, 'frame')
        else:
            layout.prop(self, 'modify_delete', expand=True)

        if self.modify_delete == 'MODIFY'or not self.existing_marker:
            # name
            layout.prop(self, 'name', text='')

    def execute(self, context):
        # import statements and functions
        from ..functions.file_functions import absolutePath
        from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
        from ..functions.project_data_functions import getArgumentForPythonScript
        from ..functions.strip_functions import getShotMarkerPosition
        from ..functions.threading_functions import launchSeparateThread
        from ..global_variables import (
                                    launching_command_statement,
                                    add_modify_marker_file,
                                    start_edit_shot_marker_statement,
                                    editing_shot_marker_statement,
                                    edited_shot_marker_statement,
                                )

        debug = context.window_manager.bpm_generalsettings.debug
        active = context.scene.sequence_editor.active_strip
        strip_scn = active.scene
        library = strip_scn.library

        if not self.existing_marker: 
            behaviour = "ADD"
        else:
            if self.modify_delete == "MODIFY":
                behaviour = "MODIFY"
            else:
                behaviour = "DELETE"
        
        if debug: print(start_edit_shot_marker_statement) #debug

        # get the filepath and the scene
        filepath = absolutePath(library.filepath)

        # get shot frame
        shot_frame = getShotMarkerPosition(self.frame, active, strip_scn)
        
        # build command
        arguments = getArgumentForPythonScript([self.name, shot_frame, behaviour])

        if debug: print(editing_shot_marker_statement + behaviour + " - " + self.name + " - frame " + str(shot_frame)) #debug

        # build command
        command = buildBlenderCommandBackgroundPython(add_modify_marker_file, filepath, arguments)

        # launch command
        if debug: print(launching_command_statement + command) #debug
        launchSeparateThread([command, debug, reloadLibrary, library])
        #launchCommand(command)

        if debug: print(edited_shot_marker_statement) #debug

        return {'FINISHED'}