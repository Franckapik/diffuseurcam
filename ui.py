from bpy.types import Panel
import bpy

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

class TLA_PT_sidebar(Panel):
    """Display test button"""
    bl_label = "Diffuseurs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Diffuseurs"

    def draw(self, context):
        col = self.layout.column(align=True)
        self.layout.label(text="Diffuseur Générateur")
        col.operator('mesh.cadre_mortaise', text='Cadre Mortaise')

        """ props = self.layout.operator('object.property_example')
        props.my_bool = True
        props.my_string = "Shouldn't that be 47?" """

        row = self.layout.row()
        row.prop(context.scene, 'my_use_x')

               
"""         box = self.layout.box()
        box.label(text="Selection Tools")
        box.operator("object.select_all").action = 'TOGGLE' """

