import bpy


from .functions.filebrowser_update_function import updateFilebrowserPath
from .functions.shot_settings_json_update_function import updateShotSettingsProperties
from .functions.asset_assigning_update_function import updateAssetAssigning, updateChangingAssetType


asset_type_items = [
        ('CHARACTER', 'Character', ""),
        ('PROP', 'Prop', ""),
        ('SET', 'Set', ""),
        ('SHADER', 'Shader', ""),
        ]

asset_state_items = [
        ('CONCEPT', 'Concept', ""),
        ('INCREATION', 'In creation', ""),
        ('FNISHED', 'Finished', ""),
        ]

shot_state_items = [
        ('STORYBOARD', 'Storyboard', ""),
        ('LAYOUT', 'Layout', ""),
        ('ANIMATION', 'Animation', ""),
        ('LIGHTING', 'Lighting', ""),
        ('RENDERING', 'Rendering', ""),
        ('COMPOSITING', 'Compositing', ""),
        ('FINISHED', 'Finished', ""),
        ]


# project settings
class BPMProjectSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    #name : bpy.props.StringProperty(name = "Name", default = "Project Name")
    project_prefix : bpy.props.StringProperty(name = "Project Prefix", default = "Project_prefix")
    framerate : bpy.props.IntProperty(name = "Project Framerate", default = 25)
    resolution_x : bpy.props.IntProperty(name = "Resolution X", default = 1920)
    resolution_y : bpy.props.IntProperty(name = "Resolution Y", default = 1080)
    edit_file_pattern : bpy.props.StringProperty(name = "Edit File Pattern", default = "")
    edit_scene_keyword : bpy.props.StringProperty(name = "Edit Scene Keyword", default = "")
    shot_prefix : bpy.props.StringProperty(name = "Shot Prefix", default = "S")
    shot_digits : bpy.props.IntProperty(name = "Shot Digits", default = 3)
    shot_start_frame : bpy.props.IntProperty(name = "Shot Start Frame", default = 100)
    default_shot_length : bpy.props.IntProperty(name = "Default Shot Length", default = 100)
    version_suffix : bpy.props.StringProperty(name = "Version Suffix", default = "v")
    version_digits : bpy.props.IntProperty(name = "Version Digits", default = 3)
    # shot_version_suffix : bpy.props.StringProperty(name = "Shot Version Suffix", default = "v")
    # shot_version_digits : bpy.props.IntProperty(name = "Shot Version Digits", default = 3)


# custom project folders
class BPMCustomFolders(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    filepath : bpy.props.StringProperty(name = "Filepath")


# asset list
class BPMAssetList(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    asset_type : bpy.props.EnumProperty(name = "Asset type", items = asset_type_items, default = 'CHARACTER')
    asset_state : bpy.props.EnumProperty(name = "Asset state", items = asset_state_items, default = 'CONCEPT')


# asset settings
class BPMAssetSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    asset_type : bpy.props.EnumProperty(name = "Asset type", items = asset_type_items, default = 'CHARACTER', update = updateChangingAssetType)
    asset_state : bpy.props.EnumProperty(name = "Asset state", items = asset_state_items, default = 'CONCEPT')
    asset_collection : bpy.props.PointerProperty(name="Asset collection", type=bpy.types.Collection, update = updateAssetAssigning)
    asset_material : bpy.props.PointerProperty(name="Asset material", type=bpy.types.Material, update = updateAssetAssigning)
    

# shot settings strips
class BPMShotSettingsStrips(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    is_shot : bpy.props.BoolProperty(default=False)
    display_markers : bpy.props.BoolProperty(name = "Display markers", default=False)
    shot_state : bpy.props.EnumProperty(name = "Shot state", items = shot_state_items, default = 'STORYBOARD', update = updateShotSettingsProperties)
    shot_version : bpy.props.IntProperty(name = "Shot version", default = 1, min = 1)
    shot_last_version : bpy.props.IntProperty(name = "Shot last version", default = 1, min = 1, update = updateShotSettingsProperties)
    not_last_version : bpy.props.BoolProperty(default=False)
    auto_audio_sync : bpy.props.BoolProperty(name = "Automatic audio sync", default=True, update = updateShotSettingsProperties)
    shot_folder : bpy.props.StringProperty(name = 'Shot folder', subtype = 'DIR_PATH')


# shot settings file
class BPMShotSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    is_shot : bpy.props.BoolProperty(default=False)
    display_markers : bpy.props.BoolProperty(name = "Display markers", default=False)
    shot_state : bpy.props.EnumProperty(name = "Shot state", items = shot_state_items, default = 'STORYBOARD', update = updateShotSettingsProperties)
    shot_version : bpy.props.IntProperty(name = "Shot version", default = 1, min = 1)
    shot_last_version : bpy.props.IntProperty(name = "Shot last version", default = 1, min = 1)
    not_last_version : bpy.props.BoolProperty(default=False)
    auto_audio_sync : bpy.props.BoolProperty(name = "Automatic audio sync", default=True, update = updateShotSettingsProperties)
    shot_folder : bpy.props.StringProperty(name = 'Shot folder', subtype = 'DIR_PATH')


# scene settings
class BPMSceneSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    extra_ui : bpy.props.BoolProperty(name = "Extra UI", default=True)

    display_shot_strip : bpy.props.BoolProperty(name = "Shot strips", default=True)
    color_shot_strip : bpy.props.FloatVectorProperty(name="Shot strip color", subtype='COLOR', default=(0, 1, 0, 0.25), min=0.0, max=1.0, size=4)

    display_shot_state : bpy.props.BoolProperty(name = "Shot state", default=True)
    color_state_storyboard : bpy.props.FloatVectorProperty(name="Storyboard", subtype='COLOR', default=(0.996, 0.898, 0.0, 1), min=0.0, max=1.0, size=4)
    color_state_layout : bpy.props.FloatVectorProperty(name="Layout", subtype='COLOR', default=(0.996, 0.431, 0.0, 1), min=0.0, max=1.0, size=4)
    color_state_animation : bpy.props.FloatVectorProperty(name="Animation", subtype='COLOR', default=(0.413, 0.002, 0.006, 1), min=0.0, max=1.0, size=4)
    color_state_lighting : bpy.props.FloatVectorProperty(name="Lighting", subtype='COLOR', default=(0.0, 0.996, 0.98, 1), min=0.0, max=1.0, size=4)
    color_state_rendering : bpy.props.FloatVectorProperty(name="Rendering", subtype='COLOR', default=(0.0, 0.424, 0.996, 1), min=0.0, max=1.0, size=4)
    color_state_compositing : bpy.props.FloatVectorProperty(name="Compositing", subtype='COLOR', default=(0.0, 0.0, 0.25, 1), min=0.0, max=1.0, size=4)
    color_state_finished : bpy.props.FloatVectorProperty(name="Finished", subtype='COLOR', default=(0.0, 0.386, 0.0, 1), min=0.0, max=1.0, size=4)

    display_audio_sync : bpy.props.BoolProperty(name = "Shot audio sync", default=True)
    color_audio_sync : bpy.props.FloatVectorProperty(name="Shot strip color", subtype='COLOR', default=(1.0, 0.0, 0.924, 1.0), min=0.0, max=1.0, size=4)

    display_marker_items = [
        ('NONE', 'None', ""),
        ('SELECTED', 'Selected', ""),
        ('PERSTRIP', 'Per strip', ""),
        ('ALL', 'All', ""),
        ]
    display_markers : bpy.props.EnumProperty(name = "Shot markers", items = display_marker_items, default = 'ALL')
    color_markers : bpy.props.FloatVectorProperty(name="Shot strip color", subtype='COLOR', default=(1, 1, 1, 1), min=0.0, max=1.0, size=4)

    display_marker_name_items = [
        ('NONE', 'None', ""),
        ('CURRENT', 'Current', ""),
        ('ALL', 'All', ""),
        ]
    display_marker_names : bpy.props.EnumProperty(name = "Marker names", items = display_marker_name_items, default = 'ALL')

    display_marker_boxes : bpy.props.BoolProperty(name = "Marker boxes", default=True)
    color_marker_boxes : bpy.props.FloatVectorProperty(name="Shot strip color", subtype='COLOR', default=(0, 0, 0, 0.5), min=0.0, max=1.0, size=4)

    display_marker_text_limit : bpy.props.IntProperty(name = "Marker text limit", default = 15, min = 0)

    display_shot_update_warning : bpy.props.BoolProperty(name = "Shot update warning", default=True)
    color_update_warning : bpy.props.FloatVectorProperty(name="Shot strip color", subtype='COLOR', default=(1, 0, 0, 1), min=0.0, max=1.0, size=4)

    display_shot_version_warning : bpy.props.BoolProperty(name = "Shot version warning", default=True)
    color_version_warning : bpy.props.FloatVectorProperty(name="Shot strip color", subtype='COLOR', default=(0, 0, 1, 1), min=0.0, max=1.0, size=4)


# general settings
class BPMGeneralSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    is_project : bpy.props.BoolProperty(default=False)
    file_type = [
        ('EDIT', 'Edit', ""),
        ('SHOT', 'Shot', ""),
        ('ASSET', 'Asset', ""),
        ('NONE', 'None', ""),
        ]
    file_type : bpy.props.EnumProperty(items = file_type, default='NONE')
    debug : bpy.props.BoolProperty(default=True)
    show_debug_props : bpy.props.BoolProperty(name = 'Debug properties', default=False)
    custom_folders_index : bpy.props.IntProperty(update = updateFilebrowserPath)
    project_folder : bpy.props.StringProperty(name = 'Project Folder', subtype = 'DIR_PATH')
    ui_shot_state_subpanel : bpy.props.BoolProperty(name = "Display state colors", default=False)
    bypass_update_tag : bpy.props.BoolProperty(default=False)