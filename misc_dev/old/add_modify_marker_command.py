import bpy, sys

# get arguments
def get_args() :
    ag  = [] ; add = False
    for a in sys.argv :
        if add : ag.append(a)
        if a == '--' : add = True
    ag_list = []
    arg = ""
    for i in ag:
        if i != "###":
            if arg != "":arg += " " 
            arg += i
        else:
            ag_list.append(arg)
            arg = ""
    return ag_list

args = get_args()
scn = bpy.context.scene

# set marker
if args[2] == "ADD":
    # add
    scn.timeline_markers.new(args[0], frame=int(args[1]))
else:
    for m in scn.timeline_markers:
        if m.frame == int(args[1]):
            # modify
            if args[2] == "MODIFY":
                m.name = args[0]
            # remove
            elif args[2] == "DELETE":
                scn.timeline_markers.remove(m)
            break

# save file
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)