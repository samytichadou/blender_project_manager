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

def init_channel_names():
	"""init function - runs once"""
	# set the font drawing routine to run every frame
	font_info["handler"] = bpy.types.SpaceSequenceEditor.draw_handler_add(
		draw_callback_px, (), 'WINDOW', 'POST_PIXEL')

def draw_callback_px():
	"""Draw on the viewports"""
	ctx = bpy.context
	vcn = ctx.scene.channel_names

	if not vcn.enable_names : return()

	glEnable(GL_BLEND) # enable transparency

	region         = ctx.region
	
	xwin1, ywin1   = region.view2d.region_to_view(0, 0)
	xwin2, ywin2   = region.view2d.region_to_view(region.width, region.height)
	x              = 22 # x position/offset
	f_size         = (32-(ywin2-ywin1))*0.1 # scale font DPI according to sequencer zoom level
	dpi            = int(72*(f_size+1))

	# BG
	width          = 100 +(50* f_size) # width + scaling depending on zoom level
	vertices       = ( (15, 15), (width, 15), (15, region.height), (width, region.height))
	indices        = ((0, 1, 2), (2, 1, 3))
	VCN_BG_shader  = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
	VCN_batch      = batch_for_shader(VCN_BG_shader, 'TRIS', {"pos": vertices}, indices=indices)
	VCN_BG_shader.bind()
	VCN_BG_shader.uniform_float("color", (0.0, 0.0, 0.0, 0.8))
	VCN_batch.draw(VCN_BG_shader)

	# TEXT
	blf.size(0, 10, dpi)
	for item in vcn.list :
		y = item.item.channel
		pos_x, pos_y = region.view2d.view_to_region(x, y, clip=False)
		blf.position(0, x, pos_y+10, 0)
		blf.color(0,1,1,1,1)
		blf.draw(0, item.name)
	glDisable(GL_BLEND)

classes = [VseChannelName, Channel, VCN_UL_CHANNELLIST, VCN_PT_ChannelNamePannel,VCN_OT_manage_channels]
reg, unregister = bpy.utils.register_classes_factory(classes)

def register() :
	reg()
	Scene.channel_names     = PointerProperty(type=VseChannelName, name="vse_channel_name", description=" ")
	VseChannelName.item    = PointerProperty(type=Channel,          name="Channel",         description=" ")

if __name__ == "__main__" :
	register()
	init_channel_names() # TODO : mettre en handler start / persistent ?
