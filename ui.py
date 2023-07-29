from bpy.types import Panel
import bpy
from .ops import classes


class Diffuseur_SideBar(Panel):
    """Display test button"""

    bl_label = "Diffuseurs"
    bl_idname = "DIFFUSEURS_PT_Diffuseurs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIFFUSEURS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "my_string")
        layout.prop(mytool, "my_float_vector")
        layout.prop(mytool, "epaisseur")

        layout.operator("mesh.cadre_court_mortaise")


def menu_func(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, icon="MESH_CUBE")


def register():
    bpy.utils.register_class(Diffuseur_SideBar)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(Diffuseur_SideBar)
