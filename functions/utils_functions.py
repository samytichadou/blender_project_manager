import bpy

# redraw areas
def redrawAreas(context, area_to_redraw):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == area_to_redraw: area.tag_redraw()