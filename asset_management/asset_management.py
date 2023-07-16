import bpy
from bpy.app.handlers import persistent

asset_types = {
    "actions",
    "armatures",
    "brushes",
    "cameras",
    "collections",
    "curves",
    "grease_pencils",
    "images",
    "lattices",
    "lightprobes",
    "lights",
    "masks",
    "materials",
    "meshes",
    "metaballs",
    "movieclips",
    "node_groups",
    "objects",
    "paint_curves",
    "particles",
    "pointclouds",
    "scenes",
    "screens",
    "sounds",
    "speakers",
    "texts",
    "textures",
    "volumes",
    "workspaces",
    "worlds",
    }


class BPM_PR_scene_asset_list(bpy.types.PropertyGroup):
    data_type : bpy.props.StringProperty()
    actions : bpy.props.PointerProperty(type = bpy.types.Action)
    armature : bpy.props.PointerProperty(type = bpy.types.Armature)
    brushes : bpy.props.PointerProperty(type = bpy.types.Brush)
    # Cache files
    cameras : bpy.props.PointerProperty(type = bpy.types.Camera)
    collections : bpy.props.PointerProperty(type = bpy.types.Collection)
    curves : bpy.props.PointerProperty(type = bpy.types.Curve)
    # Font
    grease_pencils : bpy.props.PointerProperty(type = bpy.types.GreasePencil)
    # Hair curves
    images : bpy.props.PointerProperty(type = bpy.types.Image)
    lattices : bpy.props.PointerProperty(type = bpy.types.Lattice)
    lightprobes : bpy.props.PointerProperty(type = bpy.types.LightProbe)
    lights : bpy.props.PointerProperty(type = bpy.types.Light)
    # Linestyles
    masks : bpy.props.PointerProperty(type = bpy.types.Mask)
    materials : bpy.props.PointerProperty(type = bpy.types.Material)
    meshes : bpy.props.PointerProperty(type = bpy.types.Mesh)
    metaballs : bpy.props.PointerProperty(type = bpy.types.MetaBall)
    movieclips : bpy.props.PointerProperty(type = bpy.types.MovieClip)
    node_groups : bpy.props.PointerProperty(type = bpy.types.GeometryNodeTree) # NodeGroup
    objects : bpy.props.PointerProperty(type = bpy.types.Object)
    paint_curves : bpy.props.PointerProperty(type = bpy.types.PaintCurve)
    # Palettes
    particles : bpy.props.PointerProperty(type = bpy.types.ParticleSettings) # Particle
    pointclouds : bpy.props.PointerProperty(type = bpy.types.PointCloud)
    scenes : bpy.props.PointerProperty(type = bpy.types.Scene)
    screens : bpy.props.PointerProperty(type = bpy.types.Screen)
    # Simulation
    sounds : bpy.props.PointerProperty(type = bpy.types.Sound)
    speakers : bpy.props.PointerProperty(type = bpy.types.Speaker)
    texts : bpy.props.PointerProperty(type = bpy.types.Text)
    textures : bpy.props.PointerProperty(type = bpy.types.Texture)
    volumes : bpy.props.PointerProperty(type = bpy.types.Volume)
    workspaces : bpy.props.PointerProperty(type = bpy.types.WorkSpace)
    worlds : bpy.props.PointerProperty(type = bpy.types.World)

class BPM_PR_scene_assets(bpy.types.PropertyGroup):
    asset_list : bpy.props.CollectionProperty(
        type = BPM_PR_scene_asset_list,
        )
    asset_index : bpy.props.IntProperty()

def reload_project_assets():
    asset_list = bpy.context.window_manager.bpm_scene_assets.asset_list

    # Clear list
    asset_list.clear()

    for type in asset_types:
        datas = getattr(bpy.data, type)
        for ob in datas:
            try:
                asset_datas = ob["bpm_asset_datas"]
            except KeyError:
                continue

            print(f"BPM --- Logging as asset : {ob.name}")
            # Add
            new = asset_list.add()
            new.name = ob.name
            new.data_type = type
            setattr(new, type, ob)

# TODO Remove operator
# TODO Switch version operator

class BPM_OT_reload_project_assets(bpy.types.Operator):
    bl_idname = "bpm.reload_project_assets"
    bl_label = "Reload BPM Project Asset"
    bl_description = "Reload BPM assets in this project"

    @classmethod
    def poll(cls, context):
        # Check if bpm asset file
        try:
            wm = context.window_manager
            wm["bpm_project_datas"]
            return True
        except KeyError:
            return False

    def execute(self, context):
        print("BPM --- Reloading current project assets")
        reload_project_assets()

        # TODO Write dependencies to json files
        self.report({'INFO'}, "BPM  Project Assets Reloaded")
        return {'FINISHED'}


@persistent
def asset_project_reload_handler(scene):
    # Check if bpm project
    try:
        bpy.context.window_manager["bpm_project_datas"]
    except KeyError:
        return
    reload_project_assets()


### REGISTER ---
def register():
    bpy.utils.register_class(BPM_PR_scene_asset_list)
    bpy.utils.register_class(BPM_PR_scene_assets)
    bpy.types.WindowManager.bpm_scene_assets = \
        bpy.props.PointerProperty(
            type = BPM_PR_scene_assets,
            name="BPM Scene Assets",
            )
    bpy.utils.register_class(BPM_OT_reload_project_assets)

    bpy.app.handlers.load_post.append(asset_project_reload_handler)

def unregister():
    bpy.utils.unregister_class(BPM_PR_scene_asset_list)
    bpy.utils.unregister_class(BPM_PR_scene_assets)
    del bpy.types.WindowManager.bpm_scene_assets
    bpy.utils.unregister_class(BPM_OT_reload_project_assets)

    bpy.app.handlers.load_post.remove(asset_project_reload_handler)
