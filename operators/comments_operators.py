import bpy, os, string


from ..functions.check_edit_poll_function import check_edit_poll_function
from ..functions.json_functions import create_json_file, createJsonDatasetFromProperties
from ..functions.date_functions import getDateTimeString, getDateTimeID
from ..functions.file_functions import absolutePath
from ..functions.strip_functions import getShotCommentPosition
from ..global_variables import (
                                comment_file,
                                start_edit_shot_comment_statement,
                                editing_shot_comment_statement,
                                edited_shot_comment_statement,
                                removed_shot_comment_statement,
                                comment_file_updated_statement,
                                bypass_shot_settings_update_statement,
                                no_active_shot_message,
                                no_active_shot_statement,
                            )


# reload library, thread endfunction
def modifyMarkerEndFunction(strip, library):
    library.reload()
    strip.bpm_shotsettings.is_working = False


class BPMAddModifyShotMarkerOld(bpy.types.Operator):
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
                                    if active.bpm_shotsettings.is_shot and active.scene.library and not active.bpm_shotsettings.is_working:
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

        # set strip working
        active.bpm_shotsettings.is_working = True
        bpy.ops.sequencer.refresh_all()

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
        launchSeparateThread([command, debug, modifyMarkerEndFunction, active, library])
        #launchCommand(command)

        if debug: print(edited_shot_marker_statement) #debug

        return {'FINISHED'}


def update_comments_json_file(comment_collection, folder_path):
    comment_filepath = os.path.join(folder_path, comment_file)
    datas = {}
    datas["comments"] = []

    for c in comment_collection:
        new_comment = createJsonDatasetFromProperties(c, ('hide'))
        datas["comments"].append(new_comment)

    create_json_file(datas, comment_filepath)


def update_comment_frame_property(self, context):
    general_settings = context.window_manager.bpm_generalsettings
    debug = general_settings.debug

    if general_settings.bypass_update_tag:
        if debug: print(bypass_shot_settings_update_statement) #debug
        return

    context.scene.frame_current = self.frame
  

def return_commentcoll_folderpath(comment_type, context):
    winman = context.window_manager

    if comment_type == "edit_shot":
        shot_settings = context.scene.sequence_editor.active_strip.bpm_shotsettings
        comment_collection = shot_settings.comments
        folder_path = os.path.dirname(bpy.path.abspath(shot_settings.shot_filepath))

    elif comment_type == "shot":
        shot_settings = winman.bpm_shotsettings
        comment_collection = shot_settings.comments
        folder_path = os.path.dirname(bpy.path.abspath(shot_settings.shot_filepath))

    elif comment_type == "edit":
        project_settings = winman.bpm_projectdatas
        comment_collection = project_settings.comments
        folder_path = os.path.dirname(bpy.data.filepath)

    elif comment_type == "asset":
        asset_settings = winman.bpm_assetsettings
        comment_collection = asset_settings.comments
        folder_path = os.path.dirname(bpy.data.filepath)

    return (comment_collection, folder_path)


class BPMAddComment(bpy.types.Operator):
    """Add comment to active"""
    bl_idname = "bpm.add_comment"
    bl_label = "Add comment"
    bl_options = {'REGISTER'}

    comment : bpy.props.StringProperty(name = "Comment", default = "Comment")
    frame_comment : bpy.props.BoolProperty(name = "Frame Comment")
    frame : bpy.props.IntProperty(name = "Comment Frame", update=update_comment_frame_property)
    author : bpy.props.StringProperty(name = "Author", default = "Me")

    comment_type : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if context.window_manager.bpm_generalsettings.file_type in {"SHOT", "ASSET", "EDIT"}:
                return True
                

    def invoke(self, context, event):
        self.frame = context.scene.frame_current
        return context.window_manager.invoke_props_dialog(self)
 

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "author")
        layout.prop(self, "comment", text="")
        layout.prop(self, "frame_comment")
        if self.frame_comment:
            layout.prop(self, "frame")


    def execute(self, context):

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = general_settings.debug

        # return if no active shot
        if self.comment_type == "edit_shot":
            edit, shot, active = check_edit_poll_function(context)
            if not shot or active.lock:
                self.report({'INFO'}, no_active_shot_message)
                if general_settings.debug: print(no_active_shot_statement) #debug
                return {'FINISHED'}

        if debug: print(start_edit_shot_comment_statement) #debug

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context)

        if debug: print(editing_shot_comment_statement + self.comment) #debug

        # set frame
        if not self.frame_comment:
            frame = -1
        elif self.comment_type == "edit_shot":
            active = context.scene.sequence_editor.active_strip
            frame = getShotCommentPosition(self.frame, active)

        # add new comment to strip settings
        new_comment = comment_collection.add()
        new_comment.name = getDateTimeID()
        new_comment.comment = self.comment
        new_comment.frame_comment = self.frame_comment
        new_comment.frame = frame
        new_comment.time = getDateTimeString()
        new_comment.author = self.author

        # update json file
        update_comments_json_file(comment_collection, folder_path)
        if debug: print(comment_file_updated_statement) #debug

        if debug: print(edited_shot_comment_statement) #debug

        for area in context.screen.areas:
            area.tag_redraw()
        
        return {'FINISHED'}


class BPMRemoveComment(bpy.types.Operator):
    """Remove comment"""
    bl_idname = "bpm.remove_comment"
    bl_label = "Remove comment"
    bl_options = {'REGISTER', 'INTERNAL'}

    index : bpy.props.IntProperty()
    comment_type : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if context.window_manager.bpm_generalsettings.file_type in {"SHOT", "ASSET", "EDIT"}:
                return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 

    def draw(self, context):
        layout = self.layout
        layout.label(text="Continue ?")


    def execute(self, context):

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = general_settings.debug

        # return if no active shot
        if self.comment_type == "edit_shot":
            edit, shot, active = check_edit_poll_function(context)
            if not shot or active.lock:
                self.report({'INFO'}, no_active_shot_message)
                if general_settings.debug: print(no_active_shot_statement) #debug
                return {'FINISHED'}

        if debug: print(start_edit_shot_comment_statement) #debug

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context)

        if debug: print(editing_shot_comment_statement + comment_collection[self.index].name) #debug

        # remove comment
        comment_collection.remove(self.index)

        # update json file
        update_comments_json_file(comment_collection, folder_path)
        if debug: print(comment_file_updated_statement) #debug

        if debug: print(removed_shot_comment_statement) #debug

        for area in context.screen.areas:
            area.tag_redraw()
        
        return {'FINISHED'}


class BPMModifyComment(bpy.types.Operator):
    """Modify comment"""
    bl_idname = "bpm.modify_comment"
    bl_label = "Modify comment"
    bl_options = {"REGISTER", "INTERNAL"}

    index : bpy.props.IntProperty()
    comment : bpy.props.StringProperty(name = "Comment", default = "Comment")
    frame_comment : bpy.props.BoolProperty(name = "Frame Comment")
    frame : bpy.props.IntProperty(name = "Frame", update=update_comment_frame_property)
    author : bpy.props.StringProperty(name = "Author", default = "Me")

    comment_type : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if context.window_manager.bpm_generalsettings.file_type in {"SHOT", "ASSET", "EDIT"}:
                return True


    def invoke(self, context, event):
        winman = context.window_manager
        general_settings = winman.bpm_generalsettings

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context)
        active_comment = comment_collection[self.index]

        self.author = active_comment.author
        self.comment = active_comment.comment
        self.frame_comment = active_comment.frame_comment
        general_settings.bypass_update_tag = True
        self.frame = active_comment.frame
        general_settings.bypass_update_tag = False
        return context.window_manager.invoke_props_dialog(self)
 

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "author")
        layout.prop(self, "comment", text="")
        layout.prop(self, "frame_comment")
        if self.frame_comment:
            layout.prop(self, "frame")


    def execute(self, context):

        winman = context.window_manager
        general_settings = winman.bpm_generalsettings
        debug = general_settings.debug

        # return if no active shot
        if self.comment_type == "edit_shot":
            edit, shot, active = check_edit_poll_function(context)
            if not shot or active.lock:
                self.report({'INFO'}, no_active_shot_message)
                if general_settings.debug: print(no_active_shot_statement) #debug
                return {'FINISHED'}

        if debug: print(start_edit_shot_comment_statement) #debug

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context)
            
        active_comment = comment_collection[self.index]

        if debug: print(editing_shot_comment_statement + active_comment.comment) #debug

        # modify comment to strip settings
        active_comment.comment = self.comment
        active_comment.frame_comment = self.frame_comment
        active_comment.frame = self.frame
        active_comment.author = self.author
        active_comment.edit_time = getDateTimeString()

        # update json file
        update_comments_json_file(comment_collection, folder_path)
        if debug: print(comment_file_updated_statement) #debug

        if debug: print(edited_shot_comment_statement) #debug

        for area in context.screen.areas:
            area.tag_redraw()
        
        return {'FINISHED'}