# on fait le menage dans les collections et les libs...
    for col in bpy.data.collections : col.use_fake_user = False
    for act in bpy.data.actions     : act.use_fake_user = False
    for lib in bpy.data.libraries   : unlink_lib_recursive(lib)

def unlink_lib_recursive(lib) :
    if not lib.parent :
        lib.user_clear()
        return()

    # scene = False
    ob    = lib
    for i in range(10) : # 10 niveau de recursion , jsuis trop guedin !
        #if scene : continue
        if ob.parent :
            ob.user_clear
            ob = ob.parent
        else :
            ob.user_clear