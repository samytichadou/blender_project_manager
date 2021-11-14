import subprocess
import threading

from .. import global_variables as g_var
from .task_functions import write_pid_task


# launch command in separate thread
def launchCommandFunction(command, debug, task_file, endfunction, *endfunction_args):

    if debug: print(g_var.thread_start_statement) #debug

    # launch command
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    previous_line = ""

    if task_file is not None:
        write_pid_task(task_file, process.pid)
    
    # check on it
    while True:
        line = process.stdout.readline()

        if line != '' :
            if line != previous_line:
                if debug : print(line) #debug
            if b"Blender quit" in line :
                break
            elif b"EXCEPTION_ACCESS_VIOLATION" in line:
                if debug: print(g_var.thread_error_statement) #debug
                break
            previous_line = line
        else:
            break
    
    # when ending
    if debug: print(g_var.thread_end_statement) #debug

    if endfunction is not None:
        if debug: print(g_var.thread_end_function_statement) #debug
        endfunction(*endfunction_args)


# launch separate thread
def launchSeparateThread(arguments):
    render_thread = threading.Thread(target=launchCommandFunction, args=arguments)
    render_thread.start()
    