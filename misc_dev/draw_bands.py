import bpy
import gpu
from gpu_extras.batch import batch_for_shader


def get_strip_rectf(strip):
     # Get x and y in terms of the grid's frames and channels
    x1 = strip.frame_final_start
    x2 = strip.frame_final_end
    y1 = strip.channel
    y2 = y1 + 0.25

    return [x1, y1, x2, y2]

def draw():
    print('drawing')
    context = bpy.context
    region = context.region
    xwin1, ywin1 = region.view2d.region_to_view(0, 0)
    xwin2, ywin2 = region.view2d.region_to_view(region.width, region.height)
    curx, cury = region.view2d.region_to_view(1, 0)
    curx = curx - xwin1
    
    vertices = ()
    indices = ()
    
    #strip
    n = 0
    for strip in bpy.context.scene.sequence_editor.sequences_all:
        # Strip coords
        x1, y1, x2, y2 = get_strip_rectf(strip)
        
        v1 = region.view2d.view_to_region(x1, y1, clip=False)
        v2 = region.view2d.view_to_region(x2, y1, clip=False)
        v3 = region.view2d.view_to_region(x1, y2, clip=False)
        v4 = region.view2d.view_to_region(x2, y2, clip=False)
        
        #### la partie intéressante #####
        vertices += (v1, v2, v3, v4)

        indices += ((n, n+1, n+2), (n+2, n+1, n+3))
        
        n += 4
        
        #### fin de la partie intéressante #####
        
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", (0, 0.5, 0.5, 1.0))
    batch.draw(shader)


bpy.types.SpaceSequenceEditor.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')