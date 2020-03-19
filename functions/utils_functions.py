import bpy

# redraw areas
def redrawAreas(context, area_to_redraw):
    for area in context.screen.areas:
        if area.type == area_to_redraw: area.tag_redraw()