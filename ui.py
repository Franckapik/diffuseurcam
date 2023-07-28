from bpy.types import Panel
import bpy
from .ops import classes

PROPS = [
    ('prefix', bpy.props.StringProperty(name='Prefix', default='Pref')),
    ('suffix', bpy.props.StringProperty(name='Suffix', default='Suff')),
    ('add_version', bpy.props.BoolProperty(name='Add Version', default=False)),
    ('version', bpy.props.IntProperty(name='Version', default=1)),
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

def menu_func(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, icon="MESH_CUBE")

def register():
    bpy.utils.register_class(Diffuseur_SideBar)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(Diffuseur_SideBar) 