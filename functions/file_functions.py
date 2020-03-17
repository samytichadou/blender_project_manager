import bpy, os


# absolute path
def absolutePath(path) :
    apath = os.path.abspath(bpy.path.abspath(path))
    return apath