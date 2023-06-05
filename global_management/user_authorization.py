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

def get_athcode(dataset):
    athcode = ""
    for k in dataset.bl_rna.properties:
        if k.identifier.startswith("ath_"):
            ath_code += getattr(dataset, k.identifier)
    print(ath_code)

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
