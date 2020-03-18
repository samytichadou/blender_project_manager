import bpy, os


# build blender command for launching with python script
def buildBlenderCommandBackgroundPython(python_script):
    command = "%s --background --python %s" % (bpy.app.binary_path, '"' + python_script + '"')
    return command

# launch command
def launchCommand(command):
    os.system(command)