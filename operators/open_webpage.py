import bpy
import webbrowser

from .. import global_variables as g_var


class BPM_OT_open_url(bpy.types.Operator):
    """Open URL in web browser"""
    bl_idname = "bpm.open_url"
    bl_label = "Open URL"
    bl_options = {'REGISTER', 'INTERNAL'}

    url : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        debug = context.window_manager.bpm_projectdatas.debug

        if self.url == "":
            self.report({'INFO'}, g_var.no_url_message)

        else:
            webbrowser.open(self.url)
            if debug: print(g_var.opening_web_page_statement + self.url) #debug
            
        return {'FINISHED'}


class BPM_OT_open_wiki_page(bpy.types.Operator):
    """Find help on the wiki page"""
    bl_idname = "bpm.open_wiki_page"
    bl_label = "Help"
    bl_options = {'REGISTER', 'INTERNAL'}

    wiki_page : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        debug = context.window_manager.bpm_projectdatas.debug

        url = g_var.wiki_url + self.wiki_page

        if debug: print(g_var.opening_web_page_statement + url) #debug
        
        webbrowser.open(url)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_OT_open_url)
    bpy.utils.register_class(BPM_OT_open_wiki_page)
    
def unregister():
    bpy.utils.unregister_class(BPM_OT_open_url)
    bpy.utils.unregister_class(BPM_OT_open_wiki_page)