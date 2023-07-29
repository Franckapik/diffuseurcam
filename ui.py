from bpy.types import Panel
import bpy
from .ops import classes
from .props import DiffuseurProps

class Diffuseur_SideBar(Panel):
    """Diffuseur options panel"""

    bl_label = "Diffuseurs"
    bl_idname = "DIFFUSEURS_PT_Diffuseurs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIFFUSEURS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        difprops = scene.dif_props
        attributes = difprops.listAttributes()


        for att in attributes :
            layout.prop(difprops, att)

        layout.operator("mesh.cadre_court_mortaise")
        layout.operator("mesh.cadre_long_mortaise")
        layout.operator("mesh.cadre_tenon")
        layout.operator("mesh.carreau")
        layout.operator("mesh.peigne_court")
        layout.operator("mesh.peigne_long")
        layout.operator("mesh.add_diffuseur")


def menu_func(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, icon="MESH_CUBE")


def register():
    bpy.utils.register_class(Diffuseur_SideBar)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(Diffuseur_SideBar)
