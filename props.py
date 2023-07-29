import bpy


class MyProperties(bpy.types.PropertyGroup):
    my_string: bpy.props.StringProperty(name="Enter Text")
    my_float_vector: bpy.props.FloatVectorProperty(
        name="Scale", soft_min=0, soft_max=1000, default=(1, 1, 1)
    )
    epaisseur: bpy.props.FloatProperty(
        name="epaisseur",
        description="Box epaisseur",
        min=0.003,
        max=0.008,
        default=0.003,
    )


classes = [MyProperties]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.my_tool
