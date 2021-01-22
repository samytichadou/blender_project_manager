import socket
import requests
import addon_utils


from ..global_variables import error_statement, addon_version_url


# check for internet connection
def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(error_statement + ex)
        return False


# read an online json
def read_online_json(url):
    file_object = requests.get(url)

    return file_object.json()


# get addon version 
def get_addon_version(addon_name):

    for addon in addon_utils.modules():

        if addon.bl_info['name'] == addon_name:
            addon_version = ""

            for n in addon.bl_info.get('version', (-1,-1,-1)):
                addon_version += str(n) + "."

            addon_version = addon_version[:-1]
            return addon_version

    return None


# check for addon new version
def check_addon_version(context):

    print("Checking for Addon New Version") #debug

    if not is_connected():
        print("No Internet Connection, unable to check for new version") #debug
        return False

    # if context:
    #     properties_coll = context.window_manager.an_templates_properties
    # else:
    #     properties_coll = bpy.data.window_managers[0].an_templates_properties

    new_addon_infos = read_online_json(addon_version_url)

    if new_addon_infos["version"] != get_addon_version("BPM - Blender Project Manager"):
        # properties_coll.update_needed = True
        # properties_coll.update_message = new_addon_infos["message"]
        # properties_coll.update_download_url = new_addon_infos["download_url"]

        print("New Version of the Addon Found") #debug

        return True

    print("Addon Up to Date") #debug
    
    return True