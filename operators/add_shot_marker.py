import bpy


from ..functions.file_functions import absolutePath, getLastVersion
from ..functions.command_line_functions import buildBlenderCommandBackgroundPython, launchCommand
from ..functions.project_data_functions import getArgumentForPythonScript
from ..functions.strip_functions import getShotMarkerPosition
from ..global_variables import (
                            back_to_edit_statement,
                            launching_command_statement,
                            add_marker_file,
                            start_add_shot_marker_statement,
                            adding_shot_marker_statement,
                            added_shot_marker_statement,
                        )
from ..vse_extra_ui import getMarkerFrameFromShotStrip


class BPMAddShotMarker(bpy.types.Operator):
    """Add shot marker to active strip"""
    bl_idname = "bpm.add_shot_marker"
    bl_label = "Add shot marker"
    #bl_options = {}

    name = bpy.props.StringProperty(name = "Marker name", default = "Marker name")
    frame = bpy.props.IntProperty(name = "Marker frame")

    @classmethod
    def poll(cls, context):
        keyword = context.window_manager.bpm_datas[0].edit_scene_keyword
        scn = context.scene
        if context.window_manager.bpm_isproject and context.window_manager.bpm_filetype == 'EDIT':
            if keyword in context.scene.name:
                if context.scene.sequence_editor.active_strip:
                    active = context.scene.sequence_editor.active_strip
                    if not active.lock:
                        try:
                            if active.bpm_isshot and active.scene.library: #TODO when other strip type than scene, change this
                                for m in getMarkerFrameFromShotStrip(active):
                                    if m[1] == scn.frame_current:
                                        return False
                                return True
                        except AttributeError:
                            return False

    def invoke(self, context, event):
        self.frame = context.scene.frame_current
        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        # name
        layout.prop(self, 'name', text='')
        # frame
        layout.prop(self, 'frame')

    def execute(self, context):
        winman = context.window_manager
        active = context.scene.sequence_editor.active_strip
        strip_scn = active.scene
        library = strip_scn.library
        
        if winman.bpm_debug: print(start_add_shot_marker_statement) #debug

        # get the filepath and the scene
        filepath = absolutePath(library.filepath)

        # get shot frame
        shot_frame = getShotMarkerPosition(self.frame, active, strip_scn)
        
        # build command
        arguments = getArgumentForPythonScript([self.name, shot_frame])

        if winman.bpm_debug: print(adding_shot_marker_statement + self.name + " - frame " + str(shot_frame)) #debug

        # build command
        command = buildBlenderCommandBackgroundPython(add_marker_file, filepath, arguments)

        # launch command
        if winman.bpm_debug: print(launching_command_statement + command) #debug
        launchCommand(command)

        # reload library
        library.reload()

        if winman.bpm_debug: print(added_shot_marker_statement) #debug

        return {'FINISHED'}