import bpy
import socket
import requests
import addon_utils

from .. import global_variables as g_var


# check for internet connection
def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(g_var.error_statement + ex)
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
def check_addon_version(winman):

    debug = winman.bpm_projectdatas.debug

    if debug: print(g_var.check_addon_version_statement) #debug

    if not is_connected():
        if debug: print(g_var.no_internet_statement) #debug
        return False
    
    general_settings = winman.bpm_generalsettings

    new_addon_infos = read_online_json(g_var.addon_version_url)

    if new_addon_infos["version"] != get_addon_version("BPM - Blender Project Manager"):
        general_settings.update_message = new_addon_infos["message"]
        general_settings.update_download_url = new_addon_infos["download_url"]
        if not general_settings.update_needed:
            general_settings.update_needed = True

        if debug: print(g_var.addon_new_version_statement) #debug

        return True

    if debug: print(g_var.addon_up_to_date_statement) #debug
    
    return True


# update function for update_needed property
def update_function_updateneeded(self, context):
    if self.update_needed:
        general_settings = context.window_manager.bpm_generalsettings
        if self.update_message:
            bpy.ops.bpm.dialog_popups(
                                'INVOKE_DEFAULT',
                                message = general_settings.update_message,
                                operator = "wm.url_open",
                                operator_text = "New addon version available",
                                operator_icon = "URL",
                                operator_url = general_settings.update_download_url
                                )
        else:
            bpy.ops.bpm.dialog_popups(
                                'INVOKE_DEFAULT',
                                operator = "wm.url_open",
                                operator_text = "New addon version available",
                                operator_icon = "URL",
                                operator_url = general_settings.update_download_url
                                )
