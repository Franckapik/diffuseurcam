import bpy
from .ops import AddCadreCourtMortaise, AddCadreLongMortaise, AddCadreTenon, AddCarreau, AddPeigneCourt, AddPeigneLong
from .ui import TLA_PT_sidebar

bl_info = {
    "name": "Diffuseur CAM",
    "description": "Génération de plans de diffuseurs",
    "author": "Franckapik",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "category": "Generic",
}

classes = [AddCadreCourtMortaise, AddCadreLongMortaise, AddCadreTenon, AddCarreau, AddPeigneCourt, AddPeigneLong, TLA_PT_sidebar,]


def menu_func(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, icon="MESH_CUBE")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.Scene.my_use_x = bpy.props.IntProperty()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    del bpy.types.Scene.my_use_x

if __name__ == "__main__":
    register()
