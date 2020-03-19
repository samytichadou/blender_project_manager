import bpy, os


# build blender command for launching with python script
def buildBlenderCommandBackgroundPython(python_script, blend_file, arguments):
    if blend_file:
        blend_file = '"' + blend_file + '"'
    command = "%s %s --background --python %s -- %s" % (bpy.app.binary_path, blend_file, '"' + python_script + '"', arguments)
    return command

# launch command
def launchCommand(command):
    os.system(command)