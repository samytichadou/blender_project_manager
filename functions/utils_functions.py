import bpy
import platform
import os
import subprocess


# redraw areas
def redrawAreas(context, area_to_redraw):
    for area in context.screen.areas:
        if area.type == area_to_redraw: area.tag_redraw()


# list difference
def listDifference(li1, li2): 
    return (list(set(li1) - set(li2)))


# clear lib user
def clearDataUsers(lib):
    lib.use_fake_user = False
    while lib.users != 0:
        lib.user_clear()
    try:
        for datas in lib.users_id:
            datas.use_fake_user = False
            datas.user_clear()
    except AttributeError:
        pass


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


# ensure collection exist
def ensureCollectionExists(scene, coll_name):
    try:
        link_to_coll = scene.collection.children[coll_name]
    except KeyError:
        link_to_coll = bpy.data.collections.new(coll_name)
        scene.collection.children.link(link_to_coll)
    
    return link_to_coll


# open folder in explorer
def openFolderInExplorer(absolute_path) :
    if platform.system() == "Windows":
        os.startfile(absolute_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", absolute_path])
    else:
        subprocess.Popen(["xdg-open", absolute_path])
