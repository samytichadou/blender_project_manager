import bpy


from ..functions.strip_functions import returnShotStrips
from ..vse_extra_ui import get_shot_comment_frame
from ..global_variables import (
                            no_more_comments_message,
                            getting_edit_comments_statement,
                            getting_shot_comments_statement,
                            searching_comment_statement,
                            getting_asset_comments_statement,
                        )


# return all frame from comment collection
def return_frame_from_comments(comments_collection):
    frames = []
    for c in comments_collection:
        if c.frame_comment:
            frames.append(c.frame)
    return frames


# return previous and next value in list from int
def return_previous_next_int_from_list(integer_list, target):

    list = sorted(integer_list)
    previous = None
    next = None

    for f in list:
        if f < target:
            previous = f
        elif f > target:
            next = f
            break

    return previous, next


class BPM_OT_go_to_comment(bpy.types.Operator):
    """Go to Previous/Next Comment"""
    bl_idname = "bpm.go_to_comment"
    bl_label = "Go to Comment"
    bl_options = {"REGISTER", "INTERNAL"}

    next : bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        winman = context.window_manager
        scn = context.scene

        debug = winman.bpm_projectdatas.debug

        frames = []

        file_type = winman.bpm_generalsettings.file_type

        if file_type == "EDIT":
            # get edit comments
            if debug: print(getting_edit_comments_statement) #debug
            frames.extend(return_frame_from_comments(winman.bpm_projectdatas.comments))

            # get all shot comments
            if debug: print(getting_shot_comments_statement) #debug
            for s in returnShotStrips(context.scene.sequence_editor):
                for f in return_frame_from_comments(s.bpm_shotsettings.comments):
                    frames.append(get_shot_comment_frame(f, s))

        elif file_type == "SHOT":
            # get shot comments
            if debug: print(getting_shot_comments_statement) #debug
            frames.extend(return_frame_from_comments(winman.bpm_shotsettings.comments))

        elif file_type == "ASSET":
            # get asset comments
            if debug: print(getting_asset_comments_statement) #debug
            frames.extend(return_frame_from_comments(winman.bpm_assetsettings.comments))

        current = scn.frame_current

        previous, next = return_previous_next_int_from_list(frames, current)

        if debug: print(searching_comment_statement) #debug
            
        if not self.next:
            if previous is not None:
                scn.frame_current = previous
            else:
                self.report({'INFO'}, no_more_comments_message)
        else:
            if next is not None:
                scn.frame_current = next
            else:
                self.report({'INFO'}, no_more_comments_message)
            

        return {'FINISHED'}