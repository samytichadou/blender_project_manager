### USER AUTHORIZATIONS ###
# 00 ath_user_create
# 01 ath_user_modify
# 02 ath_project_create
# 03 ath_project_modify
# 04 ath_episode_create
# 05 ath_episode_modify
# 06 ath_shot_create
# 07 ath_shot_modify
# 08 ath_storyboard_create
# 09 ath_storyboard_modify
# 10 ath_render_create
# 11 ath_render_modify
# 12 ath_compositing_create
# 13 ath_compositing_modify
# 14 ath_asset_create
# 15 ath_asset_modify
# 16 ath_planning_create
# 17 ath_planning_modify

ath_list = [
    "ath_user_create"       ,
    "ath_user_modify"       ,
    "ath_project_create"    ,
    "ath_project_modify"    ,
    "ath_episode_create"    ,
    "ath_episode_modify"    ,
    "ath_shot_create"       ,
    "ath_shot_modify"       ,
    "ath_storyboard_create" ,
    "ath_storyboard_modify" ,
    "ath_render_create"     ,
    "ath_render_modify"     ,
    "ath_compositing_create",
    "ath_compositing_modify",
    "ath_asset_create"      ,
    "ath_asset_modify"      ,
    "ath_planning_create"   ,
    "ath_planning_modify"   ,
    ]

### CUSTOM CLASS ###
import bpy
class BPM_user_authorizations():
    # TODO dynamically create props from list
    ath_user_create       : bpy.props.BoolProperty(
        name = "User Creation",
        )
    ath_user_modify       : bpy.props.BoolProperty(
        name = "User Modification",
        )
    ath_project_create    : bpy.props.BoolProperty(
        name = "Project Creation",
        )
    ath_project_modify    : bpy.props.BoolProperty(
        name = "Project Modification",
        )
    ath_episode_create    : bpy.props.BoolProperty(
        name = "Episode Creation",
        )
    ath_episode_modify    : bpy.props.BoolProperty(
        name = "Episode Modification",
        )
    ath_shot_create       : bpy.props.BoolProperty(
        name = "Shot Creation",
        )
    ath_shot_modify       : bpy.props.BoolProperty(
        name = "Shot Modification",
        )
    ath_storyboard_create : bpy.props.BoolProperty(
        name = "Storyboard Creation",
        )
    ath_storyboard_modify : bpy.props.BoolProperty(
        name = "Storyboard Modification",
        )
    ath_render_create     : bpy.props.BoolProperty(
        name = "Render Creation",
        )
    ath_render_modify     : bpy.props.BoolProperty(
        name = "Render Modification",
        )
    ath_compositing_create: bpy.props.BoolProperty(
        name = "Compositing Creation",
        )
    ath_compositing_modify: bpy.props.BoolProperty(
        name = "Compositing Modification",
        )
    ath_asset_create      : bpy.props.BoolProperty(
        name = "Asset Creation",
        )
    ath_asset_modify      : bpy.props.BoolProperty(
        name = "Asset Modification",
        )
    ath_planning_create   : bpy.props.BoolProperty(
        name = "Planning Creation",
        )
    ath_planning_modify   : bpy.props.BoolProperty(
        name = "Planning Modification",
        )

### PATTERNS ###
patt_user_creation        = "1xxxxxxxxxxxxxxxxx"
patt_user_modification    = "x1xxxxxxxxxxxxxxxx"
patt_project_creation     = "xx1xxxxxxxxxxxxxxx"

patt_asset_creation       = "xxxxxxxxxxxxxx1xxx"
patt_asset_modification   = "xxxxxxxxxxxxxxx1xx"


### FUNCTIONS ###
def get_athcode_from_props(dataset):
    athcode = ""
    for key in dataset.bl_rna.properties:
        if key.identifier.startswith("ath_"):
            athcode += str(getattr(dataset, key.identifier))
    print(athcode)

def get_athcode_from_dict(dataset):
    athcode = ""
    for key in dataset:
        if key.startswith("ath_"):
            athcode += str(dataset[key])
    return athcode

def compare_athcode(pattern, athcode):
    if not athcode:
        return False
    idx = 0
    for l in pattern:
        if l == "1":
            if athcode[idx] != "1":
                return False
        idx += 1
    return True
