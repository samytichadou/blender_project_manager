import bpy

# redraw areas
def redrawAreas(context, area_to_redraw):
    for area in context.screen.areas:
        if area.type == area_to_redraw: area.tag_redraw()


# list difference
def listDifference(li1, li2): 
    return (list(set(li1) - set(li2)))


# clear lib user
def clearLibraryUsers(lib):
    lib.use_fake_user = False
    while lib.users != 0:
        lib.user_clear()
    for datas in lib.users_id:
        datas.use_fake_user = False
        datas.user_clear()


# get host name
def getHostName():
    import socket
    return socket.gethostname()


# get current timestamp
def getTimestamp():
    import time
    return time.time()


# return formated timestamp^
def returnFormatedTimestamp(timestamp):
    import time
    return time.ctime(timestamp)


# get pid
def getCurrentPID():
    import os
    return os.getpid()