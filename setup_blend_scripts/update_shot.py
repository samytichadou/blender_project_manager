import bpy, sys

# get arguments
def get_args() :
	ag  = [] ; add = False
	for a in sys.argv :
		if add : ag.append(a)
		if a == '--' : add = True
	return(ag) 

args = get_args()
scn = bpy.context.scene

# set start and end frame
scn.frame_start = int(args[0])
scn.frame_end = int(args[1])

# save file
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)