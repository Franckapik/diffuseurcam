from bpy.types import Panel, Menu, Operator
from bl_ui.utils import PresetPanel
import bpy
from .ops import classes
from bl_operators.presets import AddPresetBase


class DIF_MT_Presets(Menu):
    bl_label = "Diffuseurs Presets"
    preset_subdir = "object/display"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


# Enregistrement du preset dans le fichier suivant
# /home/fanch/.config/blender/3.6/scripts/presets/object/display/


class OT_AddMyPreset(AddPresetBase, Operator):
    bl_idname = "my.add_preset"
    bl_label = "Ajouter un preset"
    preset_menu = "DIF_MT_Presets"
    # Common variable used for all preset values
    preset_defines = ["obj = bpy.context.object", "scene = bpy.context.scene"]
    # Properties to store in the preset
    preset_values = ["scene.dif_props", "scene.array_props", "scene.pos_props"]
    # Directory to store the presets
    preset_subdir = "object/display"


class Diffuseur_SideBar(Panel):
    """Diffuseur options panel"""

    bl_label = "Diffuseurs"
    bl_idname = "DIFFUSEURS_PT_Diffuseurs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIFFUSEURS"

    enum_items = (("0", "Cube", ""), ("1", "Pyramid", ""))

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        posprops = scene.pos_props
        prepprops = scene.prep_props
        dif_attributes = difprops.listAttributes()
        array_attributes = arrayprops.listAttributes()
        prep_attributes = prepprops.listAttributes()

        row1 = layout.row(align=True)
        row1.menu(DIF_MT_Presets.__name__, text=DIF_MT_Presets.bl_label)
        row1.operator(OT_AddMyPreset.bl_idname, text="", icon="ADD")
        row1.operator(
            OT_AddMyPreset.bl_idname, text="", icon="REMOVE"
        ).remove_active = True

        layout.separator()
        for att in dif_attributes:
            layout.prop(difprops, att)

        layout.separator()
        layout.label(text=f"Rang : {difprops.getRang() * 1000} mm")

        layout.separator()
        row2 = layout.row()
        row2.prop(arrayprops, "array_offset")

        split = layout.split()
        col1 = split.column()
        col2 = split.column()

        col1.label(
            text="X count",
        )
        col2.label(text="Y count")

        for arr in (x for x in array_attributes if x != "array_offset"):
            if arr[-1] == "x":
                col1.prop(arrayprops, arr)
            if arr[-1] == "y":
                col2.prop(arrayprops, arr)

        layout.separator()

        for piece in [
            "peigne_court",
            "cadre_mortaise",
            "cadre_tenon",
            "carreau",
            "peigne_long",
            "accroche",
        ]:
            row = layout.row()
            row.prop(posprops, f"{piece}_position")
            row.operator(f"mesh.{piece}")

        layout.operator("mesh.add_diffuseur")

        layout.prop(prepprops, "selection_prepare", expand=True)

        layout.prop(prepprops, "isNewMesh_prepare")

        if prepprops.isNewMesh_prepare:
            layout.prop(prepprops, "isDeleteOldMesh_prepare")

        layout.prop(prepprops, "isConvertToCurve_prepare")
        if prepprops.isConvertToCurve_prepare:
            layout.prop(prepprops, "isCRemove_prepare")

            if prepprops.isJoin_prepare:
                layout.prop(prepprops, "isOvercuts")

        layout.prop(prepprops, "isJoin_prepare")

        layout.operator("mesh.prepare_cam")


ui_classes = [DIF_MT_Presets, OT_AddMyPreset]


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
