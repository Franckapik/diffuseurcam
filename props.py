import bpy

from bpy.props import (
    FloatProperty,
    BoolProperty,
    IntProperty,
    FloatVectorProperty,
    EnumProperty,
)

class UIProductProps(bpy.types.PropertyGroup):
    product_type: EnumProperty(
        items=(("0", "Diffuseur 2D", ""), ("1", "Diffuseur 1D", ""), ("2", "Absorbeur", ""))
    )


class DiffuseurProps(bpy.types.PropertyGroup):
    epaisseur: FloatProperty(
        name="epaisseur",
        description="Box epaisseur",
        default=0.003,
        step=0.001,
        unit="LENGTH",
        precision=4,
    )

    type: IntProperty(
        name="type",
        description="Type du diffuseur",
        min=6,
        max=13,
        default=7,
    )

    profondeur: FloatProperty(
        name="profondeur",
        description="Box profondeur",
        min=0.05,
        max=0.2,
        default=0.1,
        unit="LENGTH",
        precision=4,
    )
    bord_cadre: FloatProperty(
        name="bord_cadre",
        description="Box bord_cadre",
        min=0.01,
        max=0.5,
        default=0.015,
        unit="LENGTH",
        precision=4,
    )
    largeur_diffuseur: FloatProperty(
        name="largeur_diffuseur",
        description="Box largeur_diffuseur",
        min=0.05,
        max=1,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )
    tenon_cadre: FloatProperty(
        name="tenon_cadre",
        description="Box tenon_cadre",
        min=0.01,
        max=0.1,
        default=0.05,
        unit="LENGTH",
        precision=4,
    )
    offset: FloatProperty(
        name="offset",
        description="Box offset",
        min=0.000,
        max=0.005,
        default=0.001,
        unit="LENGTH",
        precision=4,
    )
    tenon_peigne: FloatProperty(
        name="tenon_peigne",
        description="Box tenon_peigne",
        min=0.01,
        max=0.05,
        default=0.01,
        unit="LENGTH",
        precision=4,
    )

    longueur_diffuseur: FloatProperty(
        name="longueur_diffuseur",
        description="Box longueur_diffuseur",
        min=0.5,
        max=2,
        default=1,
        step=25,
    )

    largeur_accroche: FloatProperty(
        name="largeur_accroche",
        description="Box largeur_accroche",
        min=0.05,
        max=1,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )
    largeur_cadre_central: FloatProperty(
        name="largeur cadre central",
        description="Box largeur cadre central",
        min=0.05,
        max=1,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )
    cadre_avant: BoolProperty(
        name="Cadre avant",
        description="Cadre avant absorbeur",
    )
    cadre_central: BoolProperty(
        name="Cadre central",
        description="Cadre central absorbeur",
    )

    product_type: EnumProperty(
        items=(("0", "Diffuseur 2D", ""), ("1", "Diffuseur 1D", ""), ("2", "Absorbeur", ""))
    )

    def getDifName(self):
        dif_name = (
            "D"
            + ("2" if self.product_type == "0" else "1")
            + "N"
            + str(self.type)
            + "W"
            + str(round(self.largeur_diffuseur * 100))
            + "P"
            + str(round(self.profondeur * 100))
            + "L"
            + str(round(self.longueur_diffuseur))
            + "E"
            + str(round(self.epaisseur * 1000))
        )
        return dif_name

    def getRang(self):
        rang = (self.largeur_diffuseur - self.epaisseur) / self.type
        return round(rang, 4)

    def getLongueur(self):
        longueurTotale = (
            round(self.type * self.longueur_diffuseur) * self.getRang() + self.epaisseur
        )
        return longueurTotale

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                        "epaisseur","type","profondeur", "bord_cadre", "largeur_diffuseur","tenon_cadre", "offset", "tenon_peigne", "longueur_diffuseur"
                    ]
            case "1":
                return [
                        "epaisseur","type","profondeur", "bord_cadre", "largeur_diffuseur","tenon_cadre", "offset", "tenon_peigne", "longueur_diffuseur"
                    ]
            case "2":
                return [
                        "epaisseur","profondeur", "bord_cadre", "largeur_diffuseur","tenon_cadre", "offset", "longueur_diffuseur", "largeur_accroche", "largeur_cadre_central", "cadre_avant", "cadre_central"
                    ]
            case _:
                return 
        


class ArrayProps(bpy.types.PropertyGroup):
    array_offset: FloatProperty(
        name="Offset Array",
        description="Espace entre les pièces",
        min=0.000,
        default=0.01,
        unit="LENGTH",
        precision=4,
    )

    peigne_court_x: IntProperty(
        name="Peigne court",
        default=1,
        min=0,
    )

    peigne_court_y: IntProperty(
        name="Peigne court",
        default=1,
        min=0,
    )

    peigne_long_x: IntProperty(
        name="Peigne long",
        default=1,
        min=0,
    )

    peigne_long_y: IntProperty(
        name="Peigne long",
        default=1,
        min=0,
    )
    cadre_mortaise_x: IntProperty(
        name="Cadre mortaise",
        default=1,
        min=0,
    )

    cadre_mortaise_y: IntProperty(
        name="Cadre mortaise",
        default=1,
        min=0,
    )

    cadre_tenon_x: IntProperty(
        name="Cadre tenon",
        default=1,
        min=0,
    )

    cadre_tenon_y: IntProperty(
        name="Cadre tenon",
        default=1,
        min=0,
    )
    carreau_x: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )

    carreau_y: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )
    carreau_x: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )

    carreau_y: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )
    accroche_x: IntProperty(
        name="Accroche",
        default=1,
        min=0,
    )

    accroche_y: IntProperty(
        name="Accroche",
        default=1,
        min=0,
    )
    cadre_central_x: IntProperty(
        name="Cadre Central",
        default=1,
        min=0,
    )

    cadre_central_y: IntProperty(
        name="Cadre Central",
        default=1,
        min=0,
    )

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                        "peigne_court_x","peigne_court_y","peigne_long_x", "peigne_long_y", "cadre_mortaise_x","cadre_mortaise_y", "cadre_tenon_x", "cadre_tenon_y", "carreau_x", "carreau_y","accroche_x","accroche_y" 
                    ]
            case "1":
                return [
                        "peigne_court_x","peigne_court_y","peigne_long_x", "peigne_long_y", "cadre_mortaise_x","cadre_mortaise_y", "cadre_tenon_x", "cadre_tenon_y", "carreau_x", "carreau_y","accroche_x","accroche_y" 
                    ]
            case "2":
                return [
                        "cadre_mortaise_x","cadre_mortaise_y", "cadre_tenon_x", "cadre_tenon_y", "accroche_x","accroche_y", "cadre_central_x", "cadre_central_y" 
                    ]
            case _:
                return 


class PositionProps(bpy.types.PropertyGroup):
    peigne_court_position: FloatVectorProperty(
        name="Peigne court",
        unit="LENGTH",
        precision=4,
    )

    peigne_long_position: FloatVectorProperty(
        name="Peigne long",
        unit="LENGTH",
        precision=4,
    )

    cadre_mortaise_position: FloatVectorProperty(
        name="Cadre mortaise",
        unit="LENGTH",
        precision=4,
    )

    cadre_tenon_position: FloatVectorProperty(
        name="Cadre tenon",
        unit="LENGTH",
        precision=4,
    )

    carreau_position: FloatVectorProperty(
        name="Carreau",
        unit="LENGTH",
        precision=4,
    )
    accroche_position: FloatVectorProperty(
        name="Accroche",
        unit="LENGTH",
        precision=4,
    )
    cadre_central_position: FloatVectorProperty(
        name="Cadre Central",
        unit="LENGTH",
        precision=4,
    )

    def update(self, target, cursor):
        self[target] = cursor

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                        "peigne_court_position","peigne_long_position","cadre_mortaise_position", "cadre_tenon_position", "carreau_position","accroche_position" 
                    ]
            case "1":
                return [
                        "peigne_court_position","peigne_long_position","cadre_mortaise_position", "cadre_tenon_position", "carreau_position","accroche_position" 
                    ]
            case "2":
                return [
                        "cadre_mortaise_position", "cadre_tenon_position", "accroche_position", "cadre_central_position" 
                    ]
            case _:
                return 


class PrepareProps(bpy.types.PropertyGroup):
    selection_prepare: EnumProperty(
        items=(("0", "Generated", ""), ("1", "Selected", ""), ("2", "All", ""))
    )

    isConvertToCurve_prepare: BoolProperty(
        name="Convert to curve",
        description="Convert mesh to curve",
    )
    isCRemove_prepare: BoolProperty(
        name="Remove curve doubles",
        description="Remove curve doubles",
    )
    isOvercuts: BoolProperty(
        name="Overcuts",
        description="Add overcuts",
    )
    isJoin_prepare: BoolProperty(
        name="Join all",
        description="Join all parts to one",
    )
    isNewMesh_prepare: BoolProperty(
        name="Create new mesh",
        description="Create a copy from selection",
    )
    isDeleteOldMesh_prepare: BoolProperty(
        name="Delete old mesh",
        description="Delete old mesh",
    )

    def listAttributes(self):
        attributes = [
            a
            for a in dir(self)
            if not (
                a.startswith("__")
                or "bl_rna" in a
                or "name" in a
                or "rna_type" in a
                or "listAttributes" in a
                or "getRang" in a
                or "getLongueur" in a
                or "getDifName" in a
            )
        ]
        return attributes


classes = [DiffuseurProps, ArrayProps, PositionProps, PrepareProps, UIProductProps]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dif_props = bpy.props.PointerProperty(type=DiffuseurProps)
    bpy.types.Scene.array_props = bpy.props.PointerProperty(type=ArrayProps)
    bpy.types.Scene.pos_props = bpy.props.PointerProperty(type=PositionProps)
    bpy.types.Scene.prep_props = bpy.props.PointerProperty(type=PrepareProps)
    bpy.types.Scene.product_props = bpy.props.PointerProperty(type=UIProductProps)
    bpy.types.Scene.dif_parts = []


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.dif_props
    del bpy.types.Scene.array_props
    del bpy.types.Scene.pos_props
    del bpy.types.Scene.prep_props
    del bpy.types.Scene.dif_parts
    del bpy.types.Scene.product_props
