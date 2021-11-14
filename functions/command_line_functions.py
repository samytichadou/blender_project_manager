import bpy
import os


# build blender command for launching with python script
def buildBlenderCommandBackgroundPython(python_script, blend_file, arguments):

    command = "%s %s --background --python %s" % ('"' + bpy.app.binary_path + '"', '"'+ blend_file + '"', '"' + python_script + '"')

    if arguments != "":
        command += " -- %s" % (arguments)

    return command

# build blender command for rendering in background
def buildBlenderCommandBackgroundRender(blend_file):

    command = "%s -b %s -a" % ('"' + bpy.app.binary_path + '"', '"'+ blend_file + '"')

    return command

# launch command
def launchCommand(command):
    os.system(command)
    