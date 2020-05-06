import bpy
import os
import shutil


from ..global_variables import (
                            render_folder, 
                            render_shots_folder, 
                            render_draft_folder, 
                            render_render_folder, 
                            render_final_folder,
                            folder_created_statement,
                        )


# absolute path
def absolutePath(path):
    apath = os.path.abspath(bpy.path.abspath(path))
    return apath


# get last version of file
def getLastVersion(folder, pattern, extension):
    # print("DEBUG --- folder : "+folder) #debug
    # print("DEBUG --- pattern : "+pattern) #debug

    corresponding_files = []
    for filename in os.listdir(folder):
        
        # print("DEBUG --- iterate filename : "+filename) #debug
        if pattern in filename and filename.endswith(extension):
            temp_name = os.path.splitext(filename)[0]
            temp_name_2 = temp_name.split(pattern)[1]
            try:
                version_number = int(temp_name_2)
            except ValueError:
                if len(temp_name_2) == 0:
                    version_number = 0
                else:
                    version_number = -1
            if version_number != -1:
                corresponding_files.append([filename, version_number])

    # print("DEBUG --- corresponding files : "+str(corresponding_files)) #debug
    corresponding_files_sorted = sorted(corresponding_files, key=lambda item: item[1], reverse=True)

    # print("DEBUG --- corresponding files sorted : "+str(corresponding_files_sorted)) #debug
    filepath = os.path.join(folder, corresponding_files_sorted[0][0])

    return filepath


# suppress existing file
def suppressExistingFile(filepath) :
    if os.path.isfile(filepath) :
        os.remove(filepath)
        return True
    else:
        return False


# delete folder content
def deleteFolderContent(folder):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        # folder
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
        else:
            os.remove(filepath)


# get next shot
def getNextShot(winman, project_datas, pattern, shot_version, shot_folder):
    shot_digits = project_datas.shot_digits
    version_suffix = project_datas.version_suffix
    version_digits = project_datas.version_digits

    version = ""
    if not pattern.endswith("_"):
        version += "_"
    version += version_suffix + str(shot_version).zfill(version_digits)

    shot_subdirs = []
    subdir = [f.path for f in os.scandir(shot_folder) if f.is_dir()]
    path_pattern = os.path.join(shot_folder, pattern)

    for s in subdir:
        if path_pattern in s:
            shot_number = int(s.split(path_pattern)[1])
            shot_subdirs.append([s, shot_number])

    if len(shot_subdirs) != 0:
        shot_subdirs_sorted = sorted(shot_subdirs, key=lambda item: item[1], reverse=True)
        next_shot_number = str(shot_subdirs_sorted[0][1] + 1).zfill(shot_digits)
    else:
        next_shot_number = str(1).zfill(shot_digits)
    next_shot = pattern + next_shot_number
    next_shot_folder = os.path.join(shot_folder, next_shot)
    next_shot_file = os.path.join(next_shot_folder, next_shot + version + ".blend")

    return [next_shot_folder, next_shot_file, next_shot_number]


# create directory if doesn't exist
def createDirectory(dir_path):
    if os.path.isdir(dir_path) == False :
        os.makedirs(dir_path)


# replace content in py scripts with a list ([to_replace, replacement])
def replaceContentInPythonScript(python_script_in, python_script_out, replacement_list):
    python_code= open(python_script_in, 'r').read()

    for r in replacement_list:
        if type(r[1]) is str:
            python_code = python_code.replace(r[0], 'r"' + r[1] + '"')
        else:
            python_code = python_code.replace(r[0], str(r[1]))

    with open(python_script_out, 'w') as file:
        file.write(python_code)


# link all scenes as libraries
def linkExternalScenes(filepath):
    try: #debug
        with bpy.data.libraries.load(filepath, link=True, relative=True) as (data_from, data_to):
            scene_list = []
            data_to.scenes = data_from.scenes
            for s in data_to.scenes:
                scene_list.append(s)
            return scene_list
    except OSError as err: #debug
        print("OS error: {0}".format(err)) #debug


# create folder if doesn't exist
def createFolder(dir_path) :
    path = absolutePath(dir_path)
    if not os.path.isdir(path):
            os.makedirs(path)


# get blend name
def getBlendName():
    file_name = os.path.basename(bpy.data.filepath)
    name = os.path.splitext(file_name)[0]
    return name


# link asset libraries
def linkAssetLibrary(filepath, asset, debug):
    from .utils_functions import clearDataUsers, ensureCollectionExists
    from ..global_variables import(
                                library_cleared_statement,
                                asset_linked_statement,
                            )

    asset_type = asset.asset_type

    blend_name = os.path.basename(filepath)

    imported = []
    lib = bpy.data.libraries.load(filepath, link=True, relative=True)

    # shader
    if asset_type == "SHADER":
        name = asset.asset_material
        with lib as (data_from, data_to):
            data_to.materials = data_from.materials

        for new_mat in data_to.materials:
            imported.append(new_mat)
            if not new_mat.bpm_isasset or new_mat.name != name:
                bpy.data.materials.remove(bpy.data.materials[new_mat.name])
            else:
                if debug: print(asset_linked_statement + new_mat.name) #debug

    # nodetree
    elif asset_type == "NODEGROUP":
        name = asset.asset_nodegroup
        with lib as (data_from, data_to):
            data_to.node_groups = data_from.node_groups

        for new_node in data_to.node_groups:
            imported.append(new_node)
            if not new_node.bpm_isasset or new_node.name != name:
                bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])
            else:
                if debug: print(asset_linked_statement + new_node.name) #debug

    # world
    elif asset_type == "WORLD":
        name = asset.asset_world
        with lib as (data_from, data_to):
            data_to.worlds = data_from.worlds

        for new_world in data_to.worlds:
            imported.append(new_world)
            if not new_world.bpm_isasset or new_world.name != name:
                bpy.data.worlds.remove(bpy.data.worlds[new_world.name])
            else:
                if debug: print(asset_linked_statement + new_world.name) #debug

    # collections
    else:
        name = asset.asset_collection

        with lib as (data_from, data_to):
            data_to.collections = data_from.collections

        for new_coll in data_to.collections:
            if new_coll.bpm_isasset and new_coll.name == name:

                link_to_coll = ensureCollectionExists(bpy.context.scene, asset_type)

                if debug: print(asset_linked_statement + new_coll.name) #debug

                instance = bpy.data.objects.new(new_coll.name, None)
                instance.instance_type = 'COLLECTION'
                instance.instance_collection = new_coll
                link_to_coll.objects.link(instance)

                imported.append(instance)

    # remove lib if nothing imported
    if len(imported) == 0:

        clearDataUsers(bpy.data.libraries[blend_name])
        bpy.data.orphans_purge()

        if debug: print(library_cleared_statement + blend_name) #debug

        return False

    else:
        return True


# get file count in a folder
def counFilesInFolder(folder):
    n = 0
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            n += 1
    return n


# return all files in folder
def returnAllFilesInFolder(folder):
    filename_list = []
    
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            filename_list.append(f)
            
    return filename_list


# return render folder from strip
def returnRenderFolderFromStrip(shot_filepath, project_folder):

    #shot_filepath = absolutePath(strip.bpm_shotsettings.shot_filepath)
    shot_name = os.path.splitext(os.path.basename(shot_filepath))[0]

    render_folder_path = os.path.join(project_folder, render_folder)
    render_shot_folder_path = os.path.join(render_folder_path, render_shots_folder)

    draft_folder_path = os.path.join(render_shot_folder_path, render_draft_folder)
    render_folder_path = os.path.join(render_shot_folder_path, render_render_folder)
    final_folder_path = os.path.join(render_shot_folder_path, render_final_folder)

    shot_draft_folder_path = os.path.join(draft_folder_path, shot_name)
    shot_render_folder_path = os.path.join(render_folder_path, shot_name)
    shot_final_folder_path = os.path.join(final_folder_path, shot_name)

    return shot_draft_folder_path, shot_render_folder_path, shot_final_folder_path


# create shot render function
def createShotRenderFolders(shot_filepath, winman):
    general_settings = winman.bpm_generalsettings

    # create render folders
    shot_draft, shot_render, shot_final = returnRenderFolderFromStrip(shot_filepath, general_settings.project_folder)

    createDirectory(shot_draft)
    if general_settings.debug: print(folder_created_statement + shot_draft) #debug

    createDirectory(shot_render)
    if general_settings.debug: print(folder_created_statement + shot_render) #debug

    createDirectory(shot_final)
    if general_settings.debug: print(folder_created_statement + shot_final) #debug


# return render filepath
def returnRenderFilePathFromShot(shot_filepath, winman, shot_render_state):
    project_folder = winman.bpm_generalsettings.project_folder
    render_settings = winman.bpm_rendersettings[shot_render_state]

    shot_name = os.path.splitext(os.path.basename(shot_filepath))[0]
    render_folder_path = os.path.join(project_folder, render_folder)
    render_shot_folder_path = os.path.join(render_folder_path, render_shots_folder)
    spec_render_folder_path = os.path.join(render_shot_folder_path, shot_render_state)

    if render_settings.is_file_format == 'FFMPEG':
        output_filepath = os.path.join(spec_render_folder_path, shot_name + "_")
    else:
        shot_folder_path = os.path.join(spec_render_folder_path, shot_name)
        output_filepath = os.path.join(shot_folder_path, shot_name + "_")

    return output_filepath