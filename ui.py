from bpy.types import Panel, Menu, Operator
from bl_ui.utils import PresetPanel
import bpy
from .ops import classes
from bl_operators.presets import AddPresetBase


class Diffuseurs_MT_Presets(Menu):
    bl_label = "Diffuseurs Presets"
    preset_subdir = "object/display"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset

# Enregistrement du preset dans le fichier suivant
# /home/fanch/.config/blender/3.6/scripts/presets/object/display/

class OT_AddMyPreset(AddPresetBase, Operator):
    bl_idname = "my.add_preset"
    bl_label = "Ajouter un preset"
    preset_menu = "Diffuseurs_MT_Presets"
    # Common variable used for all preset values
    preset_defines = ["obj = bpy.context.object", "scene = bpy.context.scene"]
    # Properties to store in the preset
    preset_values = ["scene.dif_props"]
    # Directory to store the presets
    preset_subdir = "object/display"


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
        row = layout.row(align=True)
        row.menu(Diffuseurs_MT_Presets.__name__, text=Diffuseurs_MT_Presets.bl_label)
        row.operator(OT_AddMyPreset.bl_idname, text="", icon='ADD')
        row.operator(OT_AddMyPreset.bl_idname, text="", icon='REMOVE').remove_active = True


        for att in attributes:
            layout.prop(difprops, att)


        layout.operator("mesh.cadre_court_mortaise")
        layout.operator("mesh.cadre_long_mortaise")
        layout.operator("mesh.cadre_tenon")
        layout.operator("mesh.carreau")
        layout.operator("mesh.peigne_court")
        layout.operator("mesh.peigne_long")
        layout.operator("mesh.add_diffuseur")

ui_classes = [Diffuseurs_MT_Presets, OT_AddMyPreset]


def menu_func(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, icon="MESH_CUBE")    


def register():
    for cls in ui_classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_class(Diffuseur_SideBar)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    for cls in ui_classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(Diffuseur_SideBar)
