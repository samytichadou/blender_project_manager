import bpy


from .functions.filebrowser_update_function import updateFilebrowserPath
from .functions.shot_settings_json_update_function import updateShotSettingsProperties, updateShotRenderState
from .functions.asset_assigning_update_function import updateAssetAssigning, updateChangingAssetType, saveAssetToJson
from .functions.date_functions import getDateStringPlusDays, getDateYearString, getDateMonthString, getDateDayString
from .functions.change_strip_display_mode_functions import updateShotDisplayMode

from .global_variables import (
                            render_draft_folder,
                            render_render_folder,
                            render_final_folder,
                        )


# get asset icon from identifier
def getAssetIcon(identifier):
    icon = ''
    if identifier ==    'CHARACTER':    icon = 'ARMATURE_DATA'
    elif identifier ==  'PROP':         icon = 'MESH_CUBE'
    elif identifier ==  'SET':          icon = 'SCENE_DATA'
    elif identifier ==  'SHADER':       icon = 'MATERIAL'
    elif identifier ==  'WORLD':        icon = 'WORLD'
    elif identifier ==  'FX':           icon = 'SHADERFX'
    elif identifier ==  'NONE':         icon = ''
    return icon
    

# enum prop lists (identifier, name, description, icon, unique number)
asset_type_items = [
        ('CHARACTER', 'Character', "", getAssetIcon('CHARACTER'), 1),
        ('PROP', 'Prop', "", getAssetIcon('PROP'), 2),
        ('SET', 'Set', "", getAssetIcon('SET'), 3),
        ('SHADER', 'Shader', "", getAssetIcon('SHADER'), 4),
        ('WORLD', 'World', "", getAssetIcon('WORLD'), 5),
        ('FX', 'FX', "", getAssetIcon('FX'), 6),
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

shot_render_state_items = [
        (render_draft_folder, render_draft_folder, ""),
        (render_render_folder, render_render_folder, ""),
        (render_final_folder, render_final_folder, ""),
        ]

shot_display_items = shot_render_state_items.copy()
shot_display_items.insert(0, ("00_openGL", "00_openGL", ""))

asset_type_display_items = asset_type_items.copy()
asset_type_display_items.append(('ALL', 'All', "", "", 0))   


# update function for asset display type to change index
def updateAssetDisplayType(self, context):
    assets = context.window_manager.bpm_assets
    
    if self.panel_asset_display == 'ALL':
        self.asset_list_index = 0
        return
    else:
        for idx, asset in enumerate(assets):
            if asset.asset_type == self.panel_asset_display:
                self.asset_list_index = idx
                return
    
    self.asset_list_index = -1


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


# custom project folders
class BPMCustomFolders(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    filepath : bpy.props.StringProperty(name = "Filepath")


# asset list
class BPMAssetList(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    asset_type : bpy.props.EnumProperty(name = "Asset type", items = asset_type_items, default = 'CHARACTER')
    asset_state : bpy.props.EnumProperty(name = "Asset state", items = asset_state_items, default = 'CONCEPT')
    asset_collection : bpy.props.StringProperty(name="Asset collection name")
    asset_material : bpy.props.StringProperty(name="Asset material name")
    asset_world : bpy.props.StringProperty(name="Asset world name")
    is_thisassetfile : bpy.props.BoolProperty(default = False)


# asset settings
class BPMAssetSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    asset_type : bpy.props.EnumProperty(name = "Asset type", items = asset_type_items, default = 'CHARACTER', update = updateChangingAssetType)
    asset_state : bpy.props.EnumProperty(name = "Asset state", items = asset_state_items, default = 'CONCEPT', update = saveAssetToJson)
    asset_collection : bpy.props.PointerProperty(name="Asset collection", type=bpy.types.Collection, update = updateAssetAssigning)
    asset_material : bpy.props.PointerProperty(name="Asset material", type=bpy.types.Material, update = updateAssetAssigning)
    asset_world : bpy.props.PointerProperty(name="Asset world", type=bpy.types.World, update = updateAssetAssigning)

# shot settings strips
class BPMShotSettingsStrips(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    is_shot : bpy.props.BoolProperty(default=False)
    display_markers : bpy.props.BoolProperty(name = "Display markers", default=False)
    shot_state : bpy.props.EnumProperty(name = "Shot state", items = shot_state_items, default = 'STORYBOARD', update = updateShotSettingsProperties)
    shot_render_state : bpy.props.EnumProperty(name = "Shot render state", items = shot_render_state_items, default = render_draft_folder , update = updateShotSettingsProperties)
    
    shot_version : bpy.props.IntProperty(name = "Shot version", default = 1, min = 1)
    shot_last_version : bpy.props.IntProperty(name = "Shot last version", default = 1, min = 1, update = updateShotSettingsProperties)
    not_last_version : bpy.props.BoolProperty(default=False)
    
    auto_audio_sync : bpy.props.BoolProperty(name = "Automatic audio sync", default=True, update = updateShotSettingsProperties)
    
    #shot_folder : bpy.props.StringProperty(name = 'Shot folder', subtype = 'DIR_PATH')

    shot_filepath : bpy.props.StringProperty(name = 'Shot filepath', subtype = 'FILE_PATH')

    shot_frame_start : bpy.props.IntProperty(name = "Shot frame start", default = 100, min = 1)
    shot_frame_end:  bpy.props.IntProperty(name = "Shot frame end", default = 200, min = 1)

    shot_timeline_display : bpy.props.EnumProperty(name = "Shot display", items = shot_display_items, update = updateShotDisplayMode)
    is_draft : bpy.props.BoolProperty(default=False)
    is_render : bpy.props.BoolProperty(default=False)
    is_final : bpy.props.BoolProperty(default=False)

    # tasks
    storyboard_deadline : bpy.props.StringProperty(name = 'Storyboard deadline', default = getDateStringPlusDays(10))
    layout_deadline : bpy.props.StringProperty(name = 'Layout deadline', default = getDateStringPlusDays(20))
    animation_deadline : bpy.props.StringProperty(name = 'Animation deadline', default = getDateStringPlusDays(30))
    lighting_deadline : bpy.props.StringProperty(name = 'Lighting deadline', default = getDateStringPlusDays(40))
    rendering_deadline : bpy.props.StringProperty(name = 'Rendering deadline', default = getDateStringPlusDays(50))
    compositing_deadline : bpy.props.StringProperty(name = 'Compositing deadline', default = getDateStringPlusDays(60))

    storyboard_done : bpy.props.BoolProperty(name = "Storyboard done", update = updateShotSettingsProperties)
    layout_done : bpy.props.BoolProperty(name = "Layout done", update = updateShotSettingsProperties)
    animation_done : bpy.props.BoolProperty(name = "Animation done", update = updateShotSettingsProperties)
    lighting_done : bpy.props.BoolProperty(name = "Lighting done", update = updateShotSettingsProperties)
    rendering_done : bpy.props.BoolProperty(name = "Rendering done", update = updateShotSettingsProperties)
    compositing_done : bpy.props.BoolProperty(name = "Compositing done", update = updateShotSettingsProperties)


# shot settings file
class BPMShotSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    is_shot : bpy.props.BoolProperty(default=False)
    display_markers : bpy.props.BoolProperty(name = "Display markers", default=False)
    shot_state : bpy.props.EnumProperty(name = "Shot state", items = shot_state_items, default = 'STORYBOARD', update = updateShotSettingsProperties)
    shot_render_state : bpy.props.EnumProperty(name = "Shot render state", items = shot_render_state_items, default = render_draft_folder , update = updateShotRenderState)
    
    shot_version : bpy.props.IntProperty(name = "Shot version", default = 1, min = 1)
    shot_last_version : bpy.props.IntProperty(name = "Shot last version", default = 1, min = 1)
    not_last_version : bpy.props.BoolProperty(default=False)
    
    auto_audio_sync : bpy.props.BoolProperty(name = "Automatic audio sync", default=True, update = updateShotSettingsProperties)
    
    #shot_folder : bpy.props.StringProperty(name = 'Shot folder', subtype = 'DIR_PATH')

    shot_filepath : bpy.props.StringProperty(name = 'Shot filepath', subtype = 'FILE_PATH')

    shot_frame_start : bpy.props.IntProperty(name = "Shot frame start", default = 100, min = 1)
    shot_frame_end:  bpy.props.IntProperty(name = "Shot frame end", default = 100, min = 1)

    # tasks
    storyboard_deadline : bpy.props.StringProperty(name = 'Storyboard deadline', default = getDateStringPlusDays(10))
    layout_deadline : bpy.props.StringProperty(name = 'Layout deadline', default = getDateStringPlusDays(20))
    animation_deadline : bpy.props.StringProperty(name = 'Animation deadline', default = getDateStringPlusDays(30))
    lighting_deadline : bpy.props.StringProperty(name = 'Lighting deadline', default = getDateStringPlusDays(40))
    rendering_deadline : bpy.props.StringProperty(name = 'Rendering deadline', default = getDateStringPlusDays(50))
    compositing_deadline : bpy.props.StringProperty(name = 'Compositing deadline', default = getDateStringPlusDays(60))

    storyboard_done : bpy.props.BoolProperty(name = "Storyboard done", update = updateShotSettingsProperties)
    layout_done : bpy.props.BoolProperty(name = "Layout done", update = updateShotSettingsProperties)
    animation_done : bpy.props.BoolProperty(name = "Animation done", update = updateShotSettingsProperties)
    lighting_done : bpy.props.BoolProperty(name = "Lighting done", update = updateShotSettingsProperties)
    rendering_done : bpy.props.BoolProperty(name = "Rendering done", update = updateShotSettingsProperties)
    compositing_done : bpy.props.BoolProperty(name = "Compositing done", update = updateShotSettingsProperties)


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

    display_shot_todo : bpy.props.BoolProperty(name = "Shot to do", default=True)
    color_shot_todo : bpy.props.FloatVectorProperty(name="Shot to do color", subtype='COLOR', default=(0, 0, 1, 0.5), min=0.0, max=1.0, size=4)

    display_shot_deadline_preview : bpy.props.BoolProperty(name = "Deadline preview", default=False)
    shot_deadline_preview_until : bpy.props.BoolProperty(name = "Preview until this day", default=False)
    shot_deadline_preview_yr : bpy.props.IntProperty(name = "Year", min = int(getDateYearString())-10, default = int(getDateYearString()))
    shot_deadline_preview_mn : bpy.props.IntProperty(name = "Month", min = 1, max = 12, default = int(getDateMonthString()))
    shot_deadline_preview_da : bpy.props.IntProperty(name = "Day", min = 1, max = 31, default = int(getDateDayString()))

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
    project_folder : bpy.props.StringProperty(name = 'Project Folder', subtype = 'DIR_PATH')

    debug : bpy.props.BoolProperty(default=True)
    show_debug_props : bpy.props.BoolProperty(name = 'Debug properties', default=False)

    bypass_update_tag : bpy.props.BoolProperty(default=False)

    custom_folders_index : bpy.props.IntProperty(update = updateFilebrowserPath)

    ui_shot_state_subpanel : bpy.props.BoolProperty(name = "Display state colors", default=False)

    panel_asset_display : bpy.props.EnumProperty(name = "Asset type", items = asset_type_display_items, default='ALL', update = updateAssetDisplayType)

    asset_list_index : bpy.props.IntProperty(min = -1)

    blend_already_opened : bpy.props.BoolProperty(default=False)

    today_date : bpy.props.StringProperty(name = "Today date")


# render settings
class BPMRenderSettings(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    ### image settings ###

    file_format_items = [
        ('OPEN_EXR', 'Open EXR', ""),
        ('FFMPEG', 'FFmpeg video', ""),
        ]
    is_file_format : bpy.props.EnumProperty(name = "File format", items = file_format_items, default='OPEN_EXR')

    color_mode_items = [
        ('BW', 'Black and white', ""),
        ('RGB', 'RGB', ""),
        ('RGBA', 'RGB Alpha', ""),
        ]
    is_color_mode : bpy.props.EnumProperty(name = "Color mode", items = color_mode_items, default='RGB')

    color_depth_items = [
        ('16', '16 Bits', ""),
        ('32', '32 Bits', ""),
        ]
    is_color_depth : bpy.props.EnumProperty(name = "Color depth", items = color_depth_items, default='16')

    exr_codec_items = [
        ('NONE', 'None', ""),
        ('PXR24', 'Pxr24 (lossy)', ""),
        ('ZIP', 'ZIP (lossless)', ""),
        ('PIZ', 'PIZ (lossless)', ""),
        ('RLE', 'RLE (lossless)', ""),
        ('ZIPS', 'ZIPS (lossless)', ""),
        ('B44', 'B44 (lossy)', ""),
        ('B44A', 'B44A (lossy)', ""),
        ('DWAA', 'DWAA (lossy)', ""),
        ]
    is_exr_codec : bpy.props.EnumProperty(name = "Codec", items = exr_codec_items, default='ZIP')

    is_use_zbuffer : bpy.props.BoolProperty(name = 'Z Buffer', default=False)
    is_use_preview : bpy.props.BoolProperty(name = 'Preview', default=False)


    ### render settings ###

    rd_resolution_percentage : bpy.props.IntProperty(name = "Resolution percentage", default = 100)

    rd_film_transparent : bpy.props.BoolProperty(name = "Transparent background", default = False)
    
    rd_use_motion_blur : bpy.props.BoolProperty(name = "Cycles motion blur", default = False)

    rd_tile_x : bpy.props.IntProperty(name = "Cycles tiles X size", default = 64)
    rd_tile_y : bpy.props.IntProperty(name = "Cycles tiles Y size", default = 64)

    engine_items = [
        ('BLENDER_EEVEE', 'Eevee', ""),
        ('CYCLES', 'Cycles', ""),
        ]
    rd_engine : bpy.props.EnumProperty(name = "Render engine", items = engine_items, default='BLENDER_EEVEE')

    rd_use_overwrite : bpy.props.BoolProperty(name = "Overwrite output", default = True)

    rd_use_file_extension : bpy.props.BoolProperty(name = "File extensions output", default = True)

    rd_use_placeholder : bpy.props.BoolProperty(name = "Placeholders output", default = True)


    ### eevee settings ###

    ee_taa_render_samples : bpy.props.IntProperty(name = "EEVEE render samples", default = 64)

    ee_use_motion_blur : bpy.props.BoolProperty(name = "EEVEE motion blur", default = False)


    ### cycles settings ###

    cy_samples : bpy.props.IntProperty(name = "Cycles render samples", default = 128)

    device_items = [
        ('GPU', 'GPU Compute', ""),
        ('CPU', 'CPU', ""),
        ]
    cy_device : bpy.props.EnumProperty(name = "Cycles render device", items = device_items, default='CPU')


    ### ffmpeg settings ###

    ffmpeg_format_items = [
        ('QUICKTIME', 'Quicktime', ""),
        ]
    ff_format : bpy.props.EnumProperty(name = "Container", items = ffmpeg_format_items, default='QUICKTIME')

    video_codec_items = [
        ('H264', 'H.264', ""),
        ]
    ff_codec : bpy.props.EnumProperty(name = "Video Codec", items = video_codec_items, default='H264')

    audio_codec_items = [
        ('AAC', 'AAC', ""),
        ('NONE', 'No Audio', ""),
        ]
    ff_audio_codec : bpy.props.EnumProperty(name = "Audio Codec", items = audio_codec_items, default='AAC')