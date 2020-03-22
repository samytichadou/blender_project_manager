import bpy, os


from ..functions.dataset_functions import returnDatasetProperties
from ..functions.file_functions import suppressExistingFile, absolutePath
from ..functions.json_functions import createJsonDatasetFromProperties, create_json_file
from ..global_variables import file_project, saving_to_json_statement, saved_to_json_statement, new_project_name

# display project settings
class BpmCreateProject(bpy.types.Operator):
    """Create new Blender Project Manager Project"""
    bl_idname = "bpm.create_project"
    bl_label = "Create BPM Project"

    @classmethod
    def poll(cls, context):
        return not context.window_manager.bpm_isproject and bpy.data.is_saved
    
    def invoke(self, context, event):
        # create properties
        winman = context.window_manager
        if not winman.bpm_datas:
            winman.bpm_datas.add()
        datas = winman.bpm_datas[0]

        # find project dir and project file
        project_dir = os.path.dirname(absolutePath(bpy.data.filepath))
        edit_file_name = os.path.splitext(os.path.basename(absolutePath(bpy.data.filepath)))[0]

        # set specific project properties
        datas.project_folder = project_dir
        datas.edit_file_pattern = edit_file_name
        datas.name = new_project_name

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        datas = context.window_manager.bpm_datas[0]

        layout = self.layout
        split = layout.split(align=True)
        col1 = split.column(align=True)
        col2 = split.column(align=True)

        for p in returnDatasetProperties(datas):
            box = col1.box()
            box.label(text=p[0].name)
            box = col2.box()
            box.prop(datas, '%s' % p[0].identifier, text='')
        
    def execute(self, context):
        winman = context.window_manager
        datas = winman.bpm_datas[0]

        if winman.bpm_debug: print(saving_to_json_statement)

        project_file = os.path.join(datas.project_folder, file_project)

        # format the json dataset
        json_dataset = createJsonDatasetFromProperties(datas)
        # delete previous file
        suppressExistingFile(project_file)
        # create json file
        create_json_file(json_dataset, project_file)

        if winman.bpm_debug: print(saved_to_json_statement)

        # set project as bpm edit project
        winman.bpm_isproject = True
        winman.bpm_isedit = True

        return {'FINISHED'}