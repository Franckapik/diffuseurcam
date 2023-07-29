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

""" def update_cube_dimensions(self, context):
    # Prevent an error if no cube is selected and return early :
    if context.scene.cube is None:
        return
    context.scene.cube.dimensions = (
        context.scene.cube_x,
        context.scene.cube_y,
        context.scene.cube_z,
    ) """


        """ print(row.operator("mesh.cadre_court_mortaise").epaisseur)
        print(context.scene.largeur)
        row.operator("mesh.primitive_cube_add") """

col = self.layout.column(align=True)
        self.layout.label(text="Diffuseur Générate²ur")
        layout = self.layout
        row = layout.row()
        layout.prop(context.scene, "largeur")
        props = row.operator("mesh.cadre_court_mortaise", text="What?")
        print(props)

""" bpy.data.scenes['Scene'].dif_props.epaisseur """