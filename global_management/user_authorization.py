### USER AUTHORIZATIONS ###
# 00 ath_project_create
# 01 ath_project_modify
# 02 ath_episode_create
# 03 ath_episode_modify
# 04 ath_shot_create
# 05 ath_shot_modify
# 06 ath_storyboard_create
# 07 ath_storyboard_modify
# 08 ath_render_create
# 09 ath_render_modify
# 10 ath_asset_create
# 11 ath_asset_modify
# 12 ath_planning_create
# 13 ath_planning_modify

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
        if l == 1:
            if not athcode[idx] == 1:
                return False
        idx += 1
    return True
