import bpy


# task list
class BPM_PR_task_list(bpy.types.PropertyGroup):
    '''name : StringProperty() '''
    name : bpy.props.StringProperty()
    creation_time : bpy.props.StringProperty()
    type : bpy.props.StringProperty()
    id : bpy.props.StringProperty()
    filepath : bpy.props.StringProperty()
    completion : bpy.props.IntProperty()
    completion_total : bpy.props.IntProperty()
    pid : bpy.props.IntProperty()

def register():   
    bpy.utils.register_class(BPM_PR_task_list)
    bpy.types.WindowManager.bpm_tasklist = \
        bpy.props.CollectionProperty(type = BPM_PR_task_list, name="BPM task list")


def unregister():
    bpy.utils.unregister_class(BPM_PR_task_list)
    del bpy.types.WindowManager.bpm_tasklist
