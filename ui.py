from bpy.types import Panel, Menu, Operator
import bpy
from .ops import classes
from bl_operators.presets import AddPresetBase
from math import ceil
from collections import Counter


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
    preset_values = [
        "scene.dif_props",
        "scene.array_props",
        "scene.pos_props",
        "scene.prep_props",
        "scene.product_props",
        "scene.usinage_props",
    ]
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
        arrayprops = scene.array_props
        posprops = scene.pos_props
        prepprops = scene.prep_props
        productprops = scene.product_props
        usinageprops = scene.usinage_props
        devisprops = scene.devis_props
        devislist = scene.devis_list
        areaCutted = (
            difprops.getLongueur() * difprops.profondeur * (difprops.type + 1)
            + difprops.largeur_diffuseur * difprops.profondeur * (difprops.type + 1)
            + len(difprops.getMotif("depth")) * difprops.getRang() * difprops.getRang()
        )
        areaMaterial = (
            (difprops.getLongueur() + arrayprops.array_offset)
            * (difprops.profondeur + arrayprops.array_offset)
            * (difprops.type + 1)
            + (difprops.largeur_diffuseur + arrayprops.array_offset)
            * (difprops.profondeur + arrayprops.array_offset)
            * (difprops.type + 1)
            + len(difprops.getMotif("depth"))
            * (difprops.getRang() + arrayprops.array_offset)
            * (difprops.getRang() + arrayprops.array_offset)
        )
        areaPanel = devisprops.panelx * devisprops.panely
        percentPanel = areaMaterial * 100 / areaPanel
        qtyPanel = devisprops.qtyDif * areaMaterial / areaPanel

        # presets
        row1 = layout.row(align=True)
        row1.menu(DIF_MT_Presets.__name__, text=DIF_MT_Presets.bl_label)
        row1.operator(OT_AddMyPreset.bl_idname, text="", icon="ADD")
        row1.operator(
            OT_AddMyPreset.bl_idname, text="", icon="REMOVE"
        ).remove_active = True

        # Diffuseur name
        box = layout.box()
        box.label(text="Usinage ", icon="X")
        """ for att in (x for x in usinageprops.listAttributes()):
            box.prop(usinageprops, att) """
        box.prop(usinageprops, "fraise")
        box.prop(difprops, "offset_peigne")

        box.label(text=f"Offset de fraise : {usinageprops.getOffset() * 1000} mm")
        box.label(text=f"Offset des peignes : {difprops.getOffsetPeigne() * 1000} mm")

        # Dimensions
        layout.separator()
        box = layout.box()
        box.label(
            text="Dimensions : "
            + (
                "D2"
                if productprops.product_type == "0"
                else (
                    "D1"
                    if productprops.product_type == "1"
                    else "A" if productprops.product_type == "2" else "M"
                )
            )
            + difprops.getDifName(),
            icon="X",
        )
        
        row = box.row()
        row2 = box.row()
        row.prop(productprops, "product_type", expand=True)
        if productprops.product_type == "3":
            row2.prop(difprops, "moule_type", expand=True)
        for att in (x for x in difprops.listAttributes(productprops.product_type)):
            box.prop(difprops, att)
        if productprops.product_type is not "2":
            box.label(text=f"Rang : {difprops.getRang() * 1000} mm")
            box.label(text=f"Pilier : {round(difprops.getLargeurPilier() * 1000 , 3)} mm")
        
        if productprops.product_type is "2" :
            is_splitted = True if difprops.longueur_absorbeur > difprops.split and difprops.split != 0 else False
            box.label(text=f"Splitted : {is_splitted}")

        # Array
        layout.separator()
        box = layout.box()
        box.label(text="Array", icon="X")
        row = box.row()
        row.label(text="Option")
        split = row.split()
        col1 = split.column()
        col2 = split.column()

        col1.operator(
            "mesh.set_array_offset", text="Standard (3x)"
        ).arrayOffsetFactor = 3
        col2.operator(
            "mesh.set_array_offset", text="Minimal (2x)"
        ).arrayOffsetFactor = 2
        box.prop(arrayprops, "array_offset")

        box.separator()
        box.operator("mesh.set_array_recommended", text="Pré-remplir")

        split = box.split()
        col1 = split.column()
        col2 = split.column()
        col1.label(
            text="X count",
        )
        col2.label(text="Y count")
        for arr in (
            x
            for x in arrayprops.listAttributes(productprops.product_type)
            if x != "array_offset"
        ):
            if arr[-1] == "x":
                col1.prop(arrayprops, arr)
            if arr[-1] == "y":
                col2.prop(arrayprops, arr)

        box.label(
            text=f"Nombre de pièces : {arrayprops.nbPieces(productprops.product_type)}"
        )

        # Generateur
        layout.separator()
        box = layout.box()
        box.label(text="Générateur", icon="X")

        if bpy.context.selected_objects:
            # Obtient le premier objet sélectionné
            selected_object = bpy.context.selected_objects[0]
            cursor = selected_object.location

        else:
            cursor = bpy.context.scene.cursor.location

        box.label(
            text=f"{'Mesh selectionné' if bpy.context.selected_objects else 'Cursor 3D'} : X{round(cursor[0], 2)}  Y{round(cursor[1], 2)}  Z{round(cursor[2], 2)}"
        )

        for piece in posprops.listAttributes(productprops.product_type):
            row = box.row()
            if "_position" in piece:
                row.prop(posprops, piece)
                op = row.operator("mesh.pick_position", text="", icon="EYEDROPPER")
                op.cursor = cursor
                op.target = piece
                row.prop(
                    posprops,
                    piece.replace("_position", "_rotation"),
                    icon="EVENT_R",
                    text="",
                )
                row.operator(
                    f"mesh.{piece.replace('_position', '')}", text="", icon="ADD"
                )

        match productprops.product_type:
            case "0":
                box.operator("mesh.add_diffuseur")
            case "1":
                box.operator("mesh.add_diffuseur")
            case "2":
                box.operator("mesh.add_absorbeur")
            case "3":
                box.operator("mesh.add_moule")

        box.operator("mesh.no_overlap")

        # Prepare to Cam
        layout.separator()
        box = layout.box()
        box.label(text="Préparation CAM", icon="X")

        row = box.row()
        row.prop(prepprops, "selection_prepare", expand=True)

        box.prop(prepprops, "isNewMesh_prepare")

        if prepprops.isNewMesh_prepare:
            box.prop(prepprops, "isHidingOldMesh_prepare")
            box.prop(prepprops, "isDeleteOldMesh_prepare")
        """ else:
            prepprops.isDeleteOldMesh_prepare = False """

        box.prop(prepprops, "isConvertToCurve_prepare")
        if prepprops.isConvertToCurve_prepare:
            box.prop(prepprops, "isCRemove_prepare")

            if prepprops.isJoin_prepare:
                box.prop(prepprops, "isOvercuts")

        box.prop(prepprops, "isJoin_prepare")

        box.operator("mesh.prepare_cam")

        # Devis
        layout.separator()
        box = layout.box()
        box.label(text="Devis", icon="X")

        row = box.row()
        box.prop(devisprops, "qtyDif")
        split = box.split()
        col1 = split.column()
        col2 = split.column()
        col1.label(
            text="Longueur",
        )
        col2.label(text="Largeur")
        col1.prop(devisprops, "panelx")
        col2.prop(devisprops, "panely")
        split = box.split()
        col1 = split.column()
        col2 = split.column()
        col1.label(text=f"Aire D2 cutted: {round(areaCutted, 3)} m2")
        col1.label(text=f"Aire D2 material : {round(areaMaterial, 3)} m2")
        col2.label(text=f"Aire panneau : {round(areaPanel, 3)} m2")
        col2.label(text=f"% Panel coupé : {round(percentPanel)} %")
        box.label(text=f"Nb Panel : {ceil(qtyPanel)} panneau(x)")
        box.prop(devisprops, "panelPrice")
        box.prop(devisprops, "marge")
        box.prop(devisprops, "priceByPiece")
        box.prop(devisprops, "alea")
        box.prop(devisprops, "consommable")
        box.prop(devisprops, "urssaf")

        split = box.split()
        col8 = split.column()
        col9 = split.column()
        col8.label(
            text=f"Matière première/Diffuseur) : {ceil(ceil(devisprops.getPriceMP(ceil(qtyPanel))) / devisprops.qtyDif)} € "
        )
        col9.label(
            text=f"Matière première Totale) : {ceil(ceil(devisprops.getPriceMP(ceil(qtyPanel))))} € "
        )

        split = box.split()
        col3 = split.column()
        col4 = split.column()
        col3.label(text="--- Marge ---")
        col3.label(
            text=f"Prix du Diffuseur : {ceil(ceil(devisprops.getTTCMarge(ceil(qtyPanel))) / devisprops.qtyDif)} € "
        )
        col3.label(
            text=f"Prix Total : {ceil(devisprops.getTTCMarge(ceil(qtyPanel)) )} € "
        )
        col3.label(
            text=f"Dont Urssaf : {ceil(devisprops.getTTCMarge(ceil(qtyPanel) ) * devisprops.urssaf/100)} € "
        )

        col3.label(
            text=f"Bénéfice : {ceil(devisprops.getBenefMarge(ceil(qtyPanel)) )} € "
        )

        col4.label(text="--- Piece ---")
        col4.label(
            text=f"Prix du Diffuseur : {ceil(ceil(devisprops.getTTCPiece(arrayprops.nbPieces(productprops.product_type), ceil(qtyPanel) )) / devisprops.qtyDif)} € "
        )
        col4.label(
            text=f"Prix Total : {ceil(devisprops.getTTCPiece(arrayprops.nbPieces(productprops.product_type), ceil(qtyPanel) ))} € "
        )
        col4.label(
            text=f"Dont Urssaf : {ceil(devisprops.getTTCPiece(arrayprops.nbPieces(productprops.product_type), ceil(qtyPanel) ) * devisprops.urssaf/100)} € "
        )
        col4.label(
            text=f"Bénéfice : {ceil(devisprops.getBenefPiece(arrayprops.nbPieces(productprops.product_type)) )} € "
        )

        box.operator("mesh.add_list")
        box2 = box.box()
        for i, listDif in enumerate(devislist):
            row = box2.row()
            row.label(text=listDif.listDif, icon="FILE_VOLUME")
            oprm = row.operator("mesh.remove_list", icon="X")
            oprm.item = i

        # Motif
        layout.separator()
        box = layout.box()
        box.label(text="Motif", icon="X")
        row = box.row(align=True)
        row.prop(productprops, "motif_display", expand=True)

        box.prop(difprops, "decalage_h")
        box.prop(difprops, "decalage_v")
             
        ratio = difprops.getMotif(productprops.motif_display)
        ratio_readable = [int(x * 1000) for x in ratio]
        compteur = Counter(ratio_readable)

        rowC = box.row()
        rowC.scale_y = 3
        split = rowC.split() 
        
        for x, occurence in compteur.items():
            col = split.column()
            col.label(text=f"{x}:{occurence}x")

        if difprops.moule_type  =="1d":
            row = box.row()
            split = box.split()
            for k in range(difprops.type):
                col = split.column()
                col.label(text=str(int(ratio[k] * 1000)))
        else:
            for i in range(round(difprops.type * difprops.longueur_diffuseur)):
                row = box.row()
                split = box.split()
                for k in range(difprops.type):

                    col = split.column()
                    col.label(text=str(int(ratio[i * difprops.type + k] * 1000)))

        box.operator("mesh.colle")
        box.operator("mesh.simulation")

        # Addon
        layout.separator()
        box = layout.box()
        box.label(text="Addon", icon="X")
        row = box.row(align=True)
        box.operator("addon.update_git", text="Mettre à jour l'addon")

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
"""  """