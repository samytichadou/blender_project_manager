#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
https://sinestesia.co/blog/tutorials/using-uilists-in-blender/
https://docs.blender.org/api/current/blf.html
'''

import bpy , gpu
import blf
from gpu_extras.batch import batch_for_shader
from bgl import glEnable, glDisable, GL_BLEND

from bpy.types import Operator, UIList, Panel, PropertyGroup, SequenceEditor, Scene
from bpy.props import CollectionProperty, IntProperty, PointerProperty, StringProperty, BoolProperty


class VseChannelName(PropertyGroup) :
    def register():
        VseChannelName.list         = CollectionProperty(type = VseChannelName, name="vse_channel_name",  description="")
        VseChannelName.index        = IntProperty(       name = "index",          default=-1,             description="", min=-1, max=1000)
        VseChannelName.enable_names = BoolProperty(      name = "Enable Labels" , default = True,         description="Enable Drawing Names")
class Channel(PropertyGroup):
    def register():
        Channel.channel       = IntProperty(  name = "channel",        default = 1,    description="")
class VCN_UL_CHANNELLIST(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, 'name',emboss=False,text="")
        layout.prop(item.item, 'channel',text="",emboss=False)
class VCN_PT_ChannelNamePannel(Panel):
    bl_label       = "Channels Name"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Tool"
    def draw(self, context):
        vcn     = context.scene.channel_names
        layout = self.layout
        row    = layout.row()

        row = layout.row()
        row.prop(vcn,"enable_names")
        row = layout.row()

        row.template_list('VCN_UL_CHANNELLIST','vse_channel_name',vcn, "list", vcn, "index", rows=3)
        # row = layout.row()
        col = row.column(align=True)
        col.operator("vcn.manage_channels",icon = 'ADD'    ,text="").operation="ADD"
        col.operator("vcn.manage_channels",icon = 'REMOVE' ,text="").operation="DEL"
        col.separator()
class VCN_OT_manage_channels(Operator):
    '''add or remove channels in the list'''
    bl_idname = "vcn.manage_channels"
    bl_label  = "manage_channels"
    bl_options = {'REGISTER', 'INTERNAL'}
    operation : StringProperty(name = "op"  , default="ADD")

    def execute(self, context):
        if self.operation == "ADD" : add_channel()
        if self.operation == "DEL" : delete_channel()
        return {'FINISHED'}

##### ULLIST MANAGEMENT
def add_channel() :
    vcn = bpy.context.scene.channel_names
    vcn.list.add()
    vcn.list[-1].name             = "Enter Name"
    vcn.index = len(vcn.list)-1

def delete_channel() :
    vcn = bpy.context.scene.channel_names
    vcn.list.remove(vcn["index"])
    vcn.index = min(max(0, vcn["index"] - 1), len(vcn.list) - 1)


##### BGL
font_info = {"font_id": 0,"handler": None,}

# initialize fonts
def initializeExternalFontId():
    font_file = r"C:\Users\tonton\Downloads\JetBrainsMono-1.0.3\JetBrainsMono-1.0.3\ttf\JetBrainsMono-Regular.ttf"
    print("Font Loaded : " + font_file) #debug
    font_info["font_id"] = blf.load(font_file)
    
# initialize handler
def init_channel_names():
    """init function - runs once"""
    # set the font drawing routine to run every frame
    font_info["handler"] = bpy.types.SpaceSequenceEditor.draw_handler_add(
        draw_callback_px, (), 'WINDOW', 'POST_PIXEL')
        
        
# get bounding boxes
def getChannelTextCoordinates(channel, text_len, text_size, region, dpi_fac):
    step = text_size / 2 + 1
    width = text_len * step * dpi_fac
    x1, y1 = region.view2d.view_to_region(0, channel, clip=False)
    x2, y2 = region.view2d.view_to_region(0, channel + 1, clip=False)
    
    offs_x_l = 20
    offs_x_r = 2
    
    offs_t_x = 8
    offs_t_y = 4
    
    x1 = 0 + offs_x_l
    x2 = 0 + width + offs_x_l + offs_x_r + offs_t_x * 2
    
    v1 = (x1, y1)
    v2 = (x2, y1)
    v3 = (x1, y2)
    v4 = (x2, y2)
    
    text_position = (x1 + offs_t_x, y1 + offs_t_y)
    
    return ((v1, v2, v3, v4), text_position)

# get dpi factor from context
def getDpiFactorFromContext(context):
    pixel_size = context.preferences.system.pixel_size
    dpi = context.preferences.system.dpi
    dpi_fac = pixel_size * dpi / 72
    return dpi_fac

# draw callback
def draw_callback_px():
    """Draw on the viewports"""
    print("drawing") #debug
        
    ctx = bpy.context
    vcn = ctx.scene.channel_names
    
    if not vcn.enable_names : return

    region = ctx.region
    xwin1, ywin1   = region.view2d.region_to_view(0, 0)
    xwin2, ywin2   = region.view2d.region_to_view(region.width, region.height)
    zoom_level = round(((ywin1-ywin2)/32+1.02),1) # scale font DPI according to sequencer zoom level
    dpi = ctx.preferences.system.dpi
    dpi_fac = getDpiFactorFromContext(ctx)
    
    # get bg col size
    text_list = []
    for item in vcn.list:
        text_list.append(item.name)
    col_size = len(max(text_list, key=len))
    
    # font setup
    font_id = font_info["font_id"]
    color_text = (1.0, 1.0, 1.0, 1.0)
    font_size = int(10 + (12 * zoom_level))
    blf.size(font_id, font_size, dpi)
    blf.color(font_id, *color_text)
    text_to_draw = []
    
    # bg setup
    color_bg = (0.0, 0.0, 0.0, 0.5)
    vertices_bg = ()
    indices_bg = ()
    
    # lines setup
    color_lines = (1.0, 1.0, 1.0, 1.0)
    vertices_lines = ()
    indices_lines = ()
    thickness = 1
    offs_lines = thickness/2

    glEnable(GL_BLEND) # enable transparency
    
    # iterate through channels
    n_bg = 0
    n_l = 0
    for item in vcn.list:
        coords = getChannelTextCoordinates(item.item.channel, col_size, font_size, region, dpi_fac)
        
        # set bg
        vertices_bg += coords[0]
        indices_bg += ((n_bg, n_bg + 1, n_bg + 2), (n_bg + 2, n_bg + 1, n_bg + 3))
        n_bg += 4
        
        #set lines
        y1 = coords[0][0][1]
        y2 = coords[0][2][1]
#        x1, y1 = region.view2d.view_to_region(0, item.item.channel, clip=False)
#        x2, y2 = region.view2d.view_to_region(0, item.item.channel + 1, clip=False)
        #line dwn
        vertices_lines += ((0, y1-offs_lines), (region.width, y1-offs_lines), (0, y1+offs_lines), (region.width, y1+offs_lines))
        indices_lines += ((n_l, n_l + 1, n_l + 2), (n_l + 2, n_l + 1, n_l + 3))
        n_l += 4
        
        #line up
        vertices_lines += ((0, y2-offs_lines), (region.width, y2-offs_lines), (0, y2+offs_lines), (region.width, y2+offs_lines))
        indices_lines += ((n_l, n_l + 1, n_l + 2), (n_l + 2, n_l + 1, n_l + 3))
        n_l += 4
        
        # set texts
        text_to_draw.append((item.name, coords[1]))

    print(vertices_lines)
    
    # SHADER DRAW

    # channel bg
    VCN_BG_shader  = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    VCN_BG_batch      = batch_for_shader(VCN_BG_shader, 'TRIS', {"pos": vertices_bg}, indices=indices_bg)
    VCN_BG_shader.bind()
    VCN_BG_shader.uniform_float("color", color_bg)
    VCN_BG_batch.draw(VCN_BG_shader)
    
    #channel lines
    VCN_LINES_shader  = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    VCN_LINES_batch      = batch_for_shader(VCN_LINES_shader, 'TRIS', {"pos": vertices_lines}, indices=indices_lines)
    VCN_LINES_shader.bind()
    VCN_LINES_shader.uniform_float("color", color_lines)
    VCN_LINES_batch.draw(VCN_LINES_shader)

    # TEXT DRAW
    for item in text_to_draw :
        blf.position(font_id, item[1][0], item[1][1], 0)    
        blf.draw(font_id, item[0])
        
        
    glDisable(GL_BLEND)


classes = [VseChannelName, Channel, VCN_UL_CHANNELLIST, VCN_PT_ChannelNamePannel,VCN_OT_manage_channels]
reg, unregister = bpy.utils.register_classes_factory(classes)

def register() :
    reg()
    Scene.channel_names     = PointerProperty(type=VseChannelName, name="vse_channel_name", description=" ")
    VseChannelName.item    = PointerProperty(type=Channel,          name="Channel",         description=" ")

if __name__ == "__main__" :
    register()
    initializeExternalFontId()
    init_channel_names() # TODO : mettre en handler start / persistent ?
