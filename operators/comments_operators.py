import bpy, os, string


from ..functions.check_file_poll_function import check_file_poll_function
from ..functions.json_functions import create_json_file, createJsonDatasetFromProperties
from ..functions.date_functions import getDateTimeString, getDateTimeID
from ..functions.file_functions import absolutePath
from ..functions.strip_functions import getShotCommentPosition
from ..functions.reload_comments_function import return_commentcoll_folderpath, reload_comments, get_shot_comment_frame
from ..global_variables import (
                                comment_file,
                                start_edit_comment_statement,
                                editing_comment_statement,
                                edited_comment_statement,
                                removed_comment_statement,
                                comment_file_updated_statement,
                                bypass_shot_settings_update_statement,
                                no_active_shot_message,
                                no_active_shot_statement,
                                lock_strip_message,
                                lock_strip_statement,
                                loading_comments_statement,
                            )


def update_comments_json_file(comment_collection, folder_path):
    comment_filepath = os.path.join(folder_path, comment_file)
    datas = {}
    datas["comments"] = []

    for c in comment_collection:
        new_comment = createJsonDatasetFromProperties(c, ('hide'))
        datas["comments"].append(new_comment)

    create_json_file(datas, comment_filepath)


def update_comment_frame_property(self, context):
    winman = context.window_manager
    general_settings = winman.bpm_generalsettings
    debug = winman.bpm_projectdatas.debug

    if general_settings.bypass_update_tag:
        if debug: print(bypass_shot_settings_update_statement) #debug
        return

    context.scene.frame_current = self.frame
  

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
        debug = winman.bpm_projectdatas.debug

        # return if no active shot
        edit = None 
        shot = None 
        active = None
        if self.comment_type == "edit_shot":
            project, file_type, active = check_file_poll_function(context)
            if active is None:
                self.report({'INFO'}, no_active_shot_message)
                if debug: print(no_active_shot_statement) #debug
                return {'FINISHED'}
            elif active.lock:
                self.report({'INFO'}, lock_strip_message)
                if debug: print(lock_strip_statement) #debug
                return {'FINISHED'}

        if debug: print(start_edit_comment_statement) #debug

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context, active)

        if debug: print(editing_comment_statement + self.comment) #debug

        # set frame
        if not self.frame_comment:
            frame = -1
        elif self.comment_type == "edit_shot":
            active = context.scene.sequence_editor.active_strip
            frame = getShotCommentPosition(self.frame, active)
        else:
            frame = self.frame

        # add new comment to strip settings
        new_comment = comment_collection.add()
        new_comment.name = getDateTimeID()
        new_comment.comment = self.comment
        new_comment.frame_comment = self.frame_comment
        new_comment.frame = frame
        new_comment.time = getDateTimeString()
        new_comment.author = self.author

        # timeline frame comment
        if self.comment_type == "edit_shot":
            new_comment.timeline_frame = self.frame

        # update json file
        update_comments_json_file(comment_collection, folder_path)
        if debug: print(comment_file_updated_statement) #debug

        if debug: print(edited_comment_statement) #debug

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
        debug = winman.bpm_projectdatas.debug

        # return if no active shot
        edit = None 
        shot = None 
        active = None
        if self.comment_type == "edit_shot":
            project, file_type, active = check_file_poll_function(context)
            if active is None:
                self.report({'INFO'}, no_active_shot_message)
                if debug: print(no_active_shot_statement) #debug
                return {'FINISHED'}
            elif active.lock:
                self.report({'INFO'}, lock_strip_message)
                if debug: print(lock_strip_statement) #debug
                return {'FINISHED'}

        if debug: print(start_edit_comment_statement) #debug

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context, active)

        if debug: print(editing_comment_statement + comment_collection[self.index].name) #debug

        # remove comment
        comment_collection.remove(self.index)

        # update json file
        update_comments_json_file(comment_collection, folder_path)
        if debug: print(comment_file_updated_statement) #debug

        if debug: print(removed_comment_statement) #debug

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

        active = None

        if self.comment_type == "edit_shot":
            active = context.scene.sequence_editor.active_strip

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context, active)
        active_comment = comment_collection[self.index]

        print(str(active_comment.frame))

        if active_comment.frame_comment:
            if self.comment_type == "edit_shot":
                frame = active_comment.timeline_frame
            else:
                frame = active_comment.frame
        else:
            frame = context.scene.frame_current

        print(str(frame))

        self.author = active_comment.author
        self.comment = active_comment.comment
        self.frame_comment = active_comment.frame_comment
        general_settings.bypass_update_tag = True
        self.frame = frame
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
        debug = winman.bpm_projectdatas.debug

        # return if no active shot
        edit = None 
        shot = None 
        active = None
        if self.comment_type == "edit_shot":
            project, file_type, active = check_file_poll_function(context)
            if active is None:
                self.report({'INFO'}, no_active_shot_message)
                if debug: print(no_active_shot_statement) #debug
                return {'FINISHED'}
            elif active.lock:
                self.report({'INFO'}, lock_strip_message)
                if debug: print(lock_strip_statement) #debug
                return {'FINISHED'}

        if debug: print(start_edit_comment_statement) #debug

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context, active)
            
        active_comment = comment_collection[self.index]

        if debug: print(editing_comment_statement + active_comment.comment) #debug

        if self.frame_comment:
            if self.comment_type == "edit_shot":
                active = context.scene.sequence_editor.active_strip
                frame = getShotCommentPosition(self.frame, active)
            else:
                frame = self.frame
        else:
            frame = -1

        # modify comment to strip settings
        active_comment.comment = self.comment
        active_comment.frame_comment = self.frame_comment
        active_comment.frame = frame
        active_comment.author = self.author
        active_comment.edit_time = getDateTimeString()

        # timeline frame comment
        if self.comment_type == "edit_shot":
            active_comment.timeline_frame = self.frame

        # update json file
        update_comments_json_file(comment_collection, folder_path)
        if debug: print(comment_file_updated_statement) #debug

        if debug: print(edited_comment_statement) #debug

        for area in context.screen.areas:
            area.tag_redraw()
        
        return {'FINISHED'}


class BPMReloadComment(bpy.types.Operator):
    """Reload comments"""
    bl_idname = "bpm.reload_comment"
    bl_label = "Reload comment"
    bl_options = {'REGISTER', 'INTERNAL'}

    comment_type : bpy.props.StringProperty()


    @classmethod
    def poll(cls, context):
        general_settings = context.window_manager.bpm_generalsettings
        if general_settings.is_project:
            if context.window_manager.bpm_generalsettings.file_type in {"SHOT", "ASSET", "EDIT"}:
                return True


    def execute(self, context):

        winman = context.window_manager
        debug = winman.bpm_projectdatas.debug

        # return if no active shot
        edit = None 
        shot = None 
        active = None
        if self.comment_type == "edit_shot":
            project, file_type, active = check_file_poll_function(context)
            if active is None:
                self.report({'INFO'}, no_active_shot_message)
                if debug: print(no_active_shot_statement) #debug
                return {'FINISHED'}

        if debug: print(loading_comments_statement) #debug

        # get comment collection and folder path
        comment_collection, folder_path = return_commentcoll_folderpath(self.comment_type, context, active)

        reload_comments(context, self.comment_type, active)
        
        return {'FINISHED'}