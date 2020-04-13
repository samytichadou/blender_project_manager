import bpy


from .properties import getAssetIcon


# asset ui list
class BPM_UL_Asset_UI_List(bpy.types.UIList): 

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        icon = getAssetIcon(item.asset_type)        

        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text = item.name, icon = icon) 
            
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text = "", icon = icon)

    # Called once to filter/reorder items.
    def filter_items(self, context, data, propname):

        display = context.window_manager.bpm_generalsettings.panel_asset_display

        # Default return values.
        flt_flags = []
        flt_neworder = []

        col = getattr(data, propname)
        
        ### FILTERING ###
        if display != "ALL":
            flt_flags = [self.bitflag_filter_item] * len(col)

            for idx, asset in enumerate(col):
                if asset.asset_type != display:
                    flt_flags[idx] = 0

        return flt_flags, flt_neworder