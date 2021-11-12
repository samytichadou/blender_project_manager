import bpy


from .properties import getAssetIcon


# asset ui list
class BPM_UL_Asset_UI_List(bpy.types.UIList): 

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        icon = getAssetIcon(item.asset_type)

        file_type = context.window_manager.bpm_generalsettings.file_type
        
        if item.is_thisassetfile:
            layout.enabled = False
            isthis_icon = "RADIOBUT_ON"
        else:
            layout.enabled = True
            isthis_icon = "RADIOBUT_OFF"

        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text = item.name, icon = icon)
            if file_type == "ASSET":
                layout.label(text = "", icon = isthis_icon)
            
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text = "", icon = icon)
            if file_type == "ASSET":
                layout.label(text = "", icon = isthis_icon)


    # Called once to filter/reorder items.
    def filter_items(self, context, data, propname):

        helper_funcs = bpy.types.UI_UL_list

        display = context.window_manager.bpm_generalsettings.panel_asset_display

        # Default return values.
        flt_flags = []
        flt_neworder = []

        col = getattr(data, propname)
        
        ### FILTERING ###
        if self.filter_name or display != "ALL" or self.use_filter_sort_alpha:
            flt_flags = [self.bitflag_filter_item] * len(col)

            # name search
            if self.filter_name :
                flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, col, "name", flags=None, reverse=False)

            # category search
            if display != "ALL":
                for idx, asset in enumerate(col):
                    if asset.asset_type != display:
                        flt_flags[idx] = 0

            # Reorder by name
            if self.use_filter_sort_alpha:
                flt_neworder = helper_funcs.sort_items_by_name(col, "name")

        return flt_flags, flt_neworder


### REGISTER ---

def register():
    bpy.utils.register_class(BPM_UL_Asset_UI_List)

def unregister():
    bpy.utils.unregister_class(BPM_UL_Asset_UI_List)