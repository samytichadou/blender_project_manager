import bpy, os


# build blender command for launching with python script
def buildBlenderCommandBackgroundPython(python_script, arguments):
    command = "%s --background --python %s -- %s" % (bpy.app.binary_path, '"' + python_script + '"', arguments)
    return command

# launch command
def launchCommand(command):
    os.system(command)