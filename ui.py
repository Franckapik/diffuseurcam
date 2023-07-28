from bpy.types import Panel
import bpy
from .ops import classes

PROPS = [
    ("prefix", bpy.props.StringProperty(name="Prefix", default="Pref")),
    ("suffix", bpy.props.StringProperty(name="Suffix", default="Suff")),
    ("add_version", bpy.props.BoolProperty(name="Add Version", default=False)),
    ("version", bpy.props.IntProperty(name="Version", default=1)),
]

""" class OBJECT_OT_property_example(bpy.types.Operator):
    bl_idname = "object.property_example"
    bl_label = "Property Example"
    bl_options = {'REGISTER', 'UNDO'}

    my_float: bpy.props.FloatProperty(name="Some Floating Point")
    my_bool: bpy.props.BoolProperty(name="Toggle Option")
    my_string: bpy.props.StringProperty(name="String Value")

    def execute(self, context):
        self.report(
            {'INFO'}, 'F: %.2f  B: %s  S: %r' %
            (self.my_float, self.my_bool, self.my_string)
        )
        print('My float:', self.my_float)
        print('My bool:', self.my_bool)
        print('My string:', self.my_string)
        return {'FINISHED'} """


class Diffuseur_SideBar(Panel):
    """Display test button"""

    bl_label = "Diffuseurs"
    bl_idname = "DIFFUSEURS_PT_Diffuseurs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIFFUSEURS"

    def draw(self, context):
        col = self.layout.column(align=True)
        self.layout.label(text="Diffuseur Générateur")
        layout = self.layout
        for dim in ("x", "y", "z"):
            row = layout.row()
            row.prop(context.scene, f"cube_{dim}")
        print(context.scene.cube_x)
        row = layout.row()
        row.prop(context.scene, "cube")


def menu_func(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, icon="MESH_CUBE")


def update_cube_dimensions(self, context):
    # Prevent an error if no cube is selected and return early :
    if context.scene.cube is None:
        return
    context.scene.cube.dimensions = (
        context.scene.cube_x,
        context.scene.cube_y,
        context.scene.cube_z,
    )


def register():
    for dim in ("x", "y", "z"):
        exec(
            f"bpy.types.Scene.cube_{dim} = bpy.props.FloatProperty(min=0.01, default=2, update=update_cube_dimensions)"
        )
    bpy.types.Scene.largeur = bpy.props.FloatProperty(min=0.01, default=2)
    bpy.utils.register_class(Diffuseur_SideBar)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    del  bpy.types.Scene.largeur
    for dim in ("x", "y", "z"):
        exec(f"del bpy.types.Scene.cube_{dim}")
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(Diffuseur_SideBar)
