import bpy
import os

def absolutePath(path):
    apath = os.path.abspath(bpy.path.abspath(path))
    return apath

print('Start relinking')

shot_folder = "shots"

for lib in bpy.data.libraries:
    abs = absolutePath(lib.filepath)
    
    file = os.path.basename(abs)
    
    parent = os.path.dirname(abs)
    parent_name = os.path.basename(parent)
    
    subparent = os.path.dirname(parent)
    
    print("---linking : " + file)
#    print(parent_name)
    
    temp1 = os.path.join(subparent, shot_folder)
#    print(temp1)
    temp2 = os.path.join(temp1, parent_name)
#    print(temp2)
    temp3 = os.path.join(temp2, file)
#    print(temp3)
    rel_path = bpy.path.relpath(temp3)
#    print(rel_path)

    lib.filepath = rel_path

    print("---success : " + rel_path)