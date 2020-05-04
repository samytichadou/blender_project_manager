import bpy
import subprocess
import threading


# launch command in separate thread
def launchCommandFunction(command, debug):
    # launch command
    if debug : print(command) #debug
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # check on it
    while True:
        line = process.stdout.readline()

        if line != '' :
            if debug : print(line) #debug
            if b"Blender quit" in line :
                print("finish")
                break
        else:
            print("finish")
            break


# launch separate thread
def launchSeparateThread(arguments):
    render_thread = threading.Thread(target=launchCommandFunction, args=arguments)
    render_thread.start()