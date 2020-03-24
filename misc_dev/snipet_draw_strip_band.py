def draw_callback_px():
	context = bpy.context
	if not context.scene.sequence_editor : return
	# Calculate scroller width, dpi and pixelsize dependent
	# pixel_size = context.preferences.system.pixel_size
	# dpi        = context.preferences.system.dpi
	# dpi_fac    = pixel_size * dpi / 72

	# A normal widget unit is 20, but the scroller is apparently 16
	# scroller_width = 16 * dpi_fac
	region         = context.region
	xwin1, ywin1   = region.view2d.region_to_view(0, 0)
	xwin2, ywin2   = region.view2d.region_to_view(region.width, region.height)
	curx, cury     = region.view2d.region_to_view(1, 0)
	curx           = curx - xwin1
	cf_x           = context.scene.frame_current_final

	# draws[0->5] : les differents rectangles selon les couleurs, [10->15] : l'ordre dans lequel il faut tracer les faces
	draws = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[]}

	glEnable(GL_BLEND)

	#for strip in get_shots():
	for strip in context.sequences :
		if strip.studio :
			# Get corners (x1, y1), (x2, y2) of the strip rectangle in px region coords
			s = get_strip_rectf(strip,curx)

			#check if any of the coordinates are out of bounds
			if s[0] > xwin2 or s[2] < xwin1 or s[1] > ywin2 or s[3] < ywin1 : continue
			e = strip.etacolor
			l = len(draws[e])

			if s[0] < cf_x and cf_x < s[2] :
				# Bad luck, the line passes our strip
				draws[e]    += [ (s[0],s[1]), (cf_x-curx,s[1]), (cf_x-curx,s[3]), (s[0],s[3]) ]
				draws[e+10] += [ (l+0, l+1, l+2) ,(l+0, l+3, l+2) ]

				l = len(draws[e])
				draws[e]    += [ (cf_x+curx ,s[1]), (s[2],s[1]), (s[2],s[3]), (cf_x+curx,s[3]) ]
				draws[e+10] += [ (l+0, l+1, l+2) ,(l+0, l+3, l+2) ]

			else:
				# Normal, full rectangle draw
				draws[e]    += [ (s[0],s[1]), (s[2],s[1]), (s[2],s[3]), (s[0],s[3]) ]
				draws[e+10] += [ (l+0, l+1, l+2) ,(l+0, l+3, l+2) ]

	draw_underline(draws)
	glDisable(GL_BLEND)

def get_strip_rectf(strip,of):
	# Get x and y in terms of the grid's frames and channels
	of/=2
	percent =strip.etapercent *100 # le pourcentage de la barre qu'on affiche
	x1 = strip.frame_final_start
	x2 = strip.frame_final_end
	y1 = strip.channel + 0.051
	#y2 = y1 + 0.15
	x2-=(x2-x1)*((100-percent)/100)
	return [x1+of, y1, x2-of, y1 + 0.4]

def draw_underline(draws) :
	for i in range(6) :
		dr = draws[i]
		if dr :
			id = draws[10+i]
			shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
			batch  = batch_for_shader(shader, 'TRIS', {"pos" : dr}, indices=id)
			shader.bind()
			shader.uniform_float("color", get_color_from_idx(i) )
			batch.draw(shader)