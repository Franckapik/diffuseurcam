import bpy
import math

from bpy.props import (
    FloatProperty,
    BoolProperty,
    IntProperty,
    FloatVectorProperty,
    EnumProperty,
    StringProperty
)

productType = (
    ("0", "Diffuseur 2D", ""),
    ("1", "Diffuseur 1D", ""),
    ("2", "Absorbeur", ""),
    ("3", "Moule", ""),
)


class UIProductProps(bpy.types.PropertyGroup):
    product_type: EnumProperty(items=productType)


class Usinageprops(bpy.types.PropertyGroup):
    fraise: FloatProperty(
        name="Fraise diametre",
        description="Diametre de la fraise",
        default=0.005,
        step=0.001,
        unit="LENGTH",
        precision=4,
    )
    offset: EnumProperty(
        name="Offset %",
        items=(
            ("0", "Aucune", ""),
            ("0.05", "5%", ""),
            ("0.10", "10%", ""),
            ("0.20", "20%", ""),
            ("0.30", "30%", ""),
            ("0.50", "50%", ""),
        ),
    )
    

    def getOffset(self):
        offset = float(self.offset) * float(self.fraise)
        return round(offset, 4)
        


    def listAttributes(self):
        return [
            "fraise",
            "offset",
            "offset_peigne",
        ]
    

class DevisProps(bpy.types.PropertyGroup):
    qtyDif: IntProperty(
        name="Quantité",
        description="Quantité de diffuseurs",
        min=1,
        default=1,
    )
    panelx: FloatProperty(
        name="x",
        description="Longueur du panneau",
        default=1.250,
        step=0.001,
        unit="LENGTH",
        precision=3,
    )
    panely: FloatProperty(
        name="y",
        description="Largeur du panneau",
        default=1.220,
        step=0.001,
        unit="LENGTH",
        precision=3,
    )

class DevisList(bpy.types.PropertyGroup):
    listDif : StringProperty()
    


class DiffuseurProps(bpy.types.PropertyGroup):
    epaisseur: FloatProperty(
        name="Epaisseur modèle",
        description="Box epaisseur",
        default=0.003,
        step=0.001,
        unit="LENGTH",
        precision=4,
    )

    type: IntProperty(
        name="Type",
        description="Type du diffuseur",
        min=6,
        max=13,
        default=7,
    )

    profondeur: FloatProperty(
        name="Profondeur",
        description="Box profondeur",
        min=0.05,
        max=0.2,
        default=0.1,
        unit="LENGTH",
        precision=4,
    )
    bord_cadre: FloatProperty(
        name="Bord cadre",
        description="Box bord_cadre",
        min=0.01,
        max=0.5,
        default=0.015,
        unit="LENGTH",
        precision=4,
    )
    largeur_diffuseur: FloatProperty(
        name="Largeur",
        description="Box largeur_diffuseur",
        min=0.05,
        max=1,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )
    tenon_cadre: FloatProperty(
        name="Tenon_cadre",
        description="Box tenon_cadre",
        min=0.01,
        max=0.1,
        default=0.05,
        unit="LENGTH",
        precision=4,
    )

    tenon_peigne: FloatProperty(
        name="Tenon peigne",
        description="Box tenon_peigne",
        min=0.01,
        max=0.05,
        default=0.01,
        unit="LENGTH",
        precision=4,
    )

    longueur_diffuseur: FloatProperty(
        name="Longueur_diffuseur",
        description="Box longueur_diffuseur",
        min=0.5,
        max=2,
        default=1,
        step=25,
    )

    largeur_accroche: FloatProperty(
        name="Largeur accroche",
        description="Box largeur_accroche",
        min=0.05,
        max=1,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )
    largeur_cadre_central: FloatProperty(
        name="Largeur cadre central",
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

    type_tenon_peigne: EnumProperty(
        name="Interface Peigne/Cadre",
        items=(
            ("0", "Pas de tenon", ""),
            ("1", "Double Tenon mi-traversant", ""),
            ("2", "Double Tenon entier", ""),
            ("3", "Mono Tenon mi-traversant", ""),
        ),
    )

    type_tenon_cadre: EnumProperty(
        name="Interface Cadre/Cadre",
        items=(
            ("0", "Pas de tenon", ""),
            ("1", "Tenon mortaise", ""),
        ),
    )

    epaisseur_moule: FloatProperty(
        name="Epaisseur_moule",
        description="Epaisseur du moule",
        min=0.005,
        max=1,
        default=0.01,
        unit="LENGTH",
        precision=4,
    )
    pillier_1d_only: BoolProperty(
        name="Pillier 1D seulement",
        description="Generer les pilliers utiles au 1D seulement",
    )
    epaisseur_pilier: FloatProperty(
        name="Epaisseur_pilier",
        description="Epaisseur des piliers",
        min=0.003,
        max=1,
        default=0.003,
        unit="LENGTH",
        precision=4,
    )

    pilier_reduction: EnumProperty(
        name="Reduction des piliers",
        items=(
            ("0", "Aucune", ""),
            ("0.05", "5%", ""),
            ("0.10", "10%", ""),
            ("0.20", "20%", ""),
            ("0.30", "30%", ""),
            ("0.50", "50%", ""),
        ),
    )

    decalage_h: IntProperty(
        name="Horizontal",
        description="Décalage",
        min=0,
        max=13,
        default=0,
    )

    decalage_v: IntProperty(
        name="Vertical",
        description="Décalage",
        min=0,
        max=13,
        default=0,
    )

    type_moule: EnumProperty(
        name="Type de moule",
        items=(
            ("stable", "Stable - 2 epaisseurs", ""),
            ("eco", "Eco - 1 epaisseur", ""),
        ),
    )

    offset_peigne: IntProperty(
        name="Offset peigne %",
        description="Offset sur les peignes en %",
        min=0,
        max=10,
        default=0,
    )

    def getOffsetPeigne(self):
        offset = float(self.offset_peigne/100) * float(self.epaisseur)
        return round(offset, 4)

    def getDifName(self):
        dif_name = (
            "N"
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

    def getHauteurTenon(self):
        match self.type_tenon_peigne:
            case "0":
                """ Pas de tenons """
                return 0
            case "1":
                return self.epaisseur / 2
            case "2":
                return self.epaisseur
            case "3":
                """ Mono tenon mi traversant """
                return self.epaisseur / 2



    def getLongueur(self):
        longueurTotale = (
            round(self.type * self.longueur_diffuseur) * self.getRang() + self.epaisseur
        )
        return longueurTotale

    def getLargeurPilier(self):
        largeur_pilier = (
            self.getRang()
            - self.epaisseur
            - self.getRang() * float(self.pilier_reduction)
        )
        return round(largeur_pilier, 4)

    def getRatio(self):
        ratio = []
        for k in range(0, self.type * round(self.type * self.longueur_diffuseur) ):
            n = k % self.type
            m = math.floor(k / self.type)
            an = int(
                (math.pow(n + self.decalage_h, 2) + math.pow(m + self.decalage_v, 2))
                % self.type
            )
            ratio.append(an)

        amax = max(ratio)

        depth = []
        for k in range(0, self.type * round(self.type * self.longueur_diffuseur) ):
            y = (ratio[k] * self.profondeur) / amax
            depth.append(y)

        
        if(self.pillier_1d_only):
            return depth[0:self.type]
        else:
             return depth
    
    def getArea(self):
        area = (self.getLongueur() * self.profondeur * (self.type + 1) + self.largeur_diffuseur * self.profondeur * (self.type + 1) + len(self.getRatio()) * self.getRang() * self.getRang()) 
        print(self.largeur_diffuseur)
        return area

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                    "epaisseur",
                    "type",
                    "profondeur",
                    "bord_cadre",
                    "largeur_diffuseur",
                    "tenon_cadre",
                    "tenon_peigne",
                    "longueur_diffuseur",
                    "type_tenon_peigne",
                    "type_tenon_cadre"
                ]
            case "1":
                return [
                    "epaisseur",
                    "type",
                    "profondeur",
                    "bord_cadre",
                    "largeur_diffuseur",
                    "tenon_cadre",
                    "tenon_peigne",
                    "longueur_diffuseur",
                    "type_tenon_peigne",
                    "type_tenon_cadre"
                ]
            case "2":
                return [
                    "epaisseur",
                    "profondeur",
                    "bord_cadre",
                    "largeur_diffuseur",
                    "tenon_cadre",
                    "longueur_diffuseur",
                    "largeur_accroche",
                    "largeur_cadre_central",
                    "cadre_avant",
                    "cadre_central",
                    "type_tenon_cadre"
                ]
            case "3":
                attributes = [
                    "type_moule",
                    "epaisseur",
                    "epaisseur_moule",
                    "pilier_reduction",
                    "type",
                    "profondeur",
                    "largeur_diffuseur",
                    "longueur_diffuseur",
                    "pillier_1d_only"
                ]
                
                if self.type_moule == "stable":
                    attributes.append("epaisseur_pilier")
                    
                return attributes

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
    accroche_inverse_x: IntProperty(
        name="Accroche Inverse",
        default=1,
        min=0,
    )

    accroche_inverse_y: IntProperty(
        name="Accroche Invserse",
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
    cadre_avant_x: IntProperty(
        name="Cadre Avant",
        default=1,
        min=0,
    )

    cadre_avant_y: IntProperty(
        name="Cadre Avant",
        default=1,
        min=0,
    )

    fond_moule_x: IntProperty(
        name="Fond Moule",
        default=1,
        min=0,
    )
    fond_moule_y: IntProperty(
        name="Fond Moule",
        default=1,
        min=0,
    )
    cadre_moule_x: IntProperty(
        name="Cadre Moule",
        default=1,
        min=0,
    )
    cadre_moule_y: IntProperty(
        name="Cadre Moule",
        default=1,
        min=0,
    )
    cadre_moule_long_x: IntProperty(
        name="Cadre Moule Long",
        default=1,
        min=0,
    )
    cadre_moule_long_y: IntProperty(
        name="Cadre Moule Long",
        default=1,
        min=0,
    )
    pilier_moule_x: IntProperty(
        name="Piliers Moule",
        default=1,
        min=0,
    )
    pilier_moule_y: IntProperty(
        name="Piliers Moule",
        default=1,
        min=0,
    )

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                    "peigne_court_x",
                    "peigne_court_y",
                    "peigne_long_x",
                    "peigne_long_y",
                    "cadre_mortaise_x",
                    "cadre_mortaise_y",
                    "cadre_tenon_x",
                    "cadre_tenon_y",
                    "carreau_x",
                    "carreau_y",
                    "accroche_x",
                    "accroche_y",
                ]
            case "1":
                return [
                    "peigne_court_x",
                    "peigne_court_y",
                    "peigne_long_x",
                    "peigne_long_y",
                    "cadre_mortaise_x",
                    "cadre_mortaise_y",
                    "cadre_tenon_x",
                    "cadre_tenon_y",
                    "carreau_x",
                    "carreau_y",
                    "accroche_x",
                    "accroche_y",
                ]
            case "2":
                return [
                    "cadre_mortaise_x",
                    "cadre_mortaise_y",
                    "cadre_tenon_x",
                    "cadre_tenon_y",
                    "accroche_x",
                    "accroche_y",
                    "accroche_inverse_x",
                    "accroche_inverse_y",
                    "cadre_central_x",
                    "cadre_central_y",
                    "cadre_avant_x",
                    "cadre_avant_y",
                ]
            case "3":
                return [
                    "fond_moule_x",
                    "fond_moule_y",
                    "cadre_moule_x",
                    "cadre_moule_y",
                    "cadre_moule_long_x",
                    "cadre_moule_long_y",
                    "pilier_moule_x",
                    "pilier_moule_y"
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
    accroche_inverse_position: FloatVectorProperty(
        name="Accroche inverse",
        unit="LENGTH",
        precision=4,
    )
    cadre_central_position: FloatVectorProperty(
        name="Cadre Central",
        unit="LENGTH",
        precision=4,
    )
    cadre_avant_position: FloatVectorProperty(
        name="Cadre Avant",
        unit="LENGTH",
        precision=4,
    )
    fond_moule_position: FloatVectorProperty(
        name="Fond Moule",
        unit="LENGTH",
        precision=4,
    )
    pilier_moule_position: FloatVectorProperty(
        name="Pilier Moule",
        unit="LENGTH",
        precision=4,
    )
    cadre_moule_position: FloatVectorProperty(
        name="Cadre Moule",
        unit="LENGTH",
        precision=4,
    )
    cadre_moule_long_position: FloatVectorProperty(
        name="Cadre Moule Long",
        unit="LENGTH",
        precision=4,
    )
    peigne_court_rotation: BoolProperty(name="Peigne court", description="Rotation")

    peigne_long_rotation: BoolProperty(name="Peigne long", description="Rotation")

    cadre_mortaise_rotation: BoolProperty(name="Cadre mortaise", description="Rotation")

    cadre_tenon_rotation: BoolProperty(name="Cadre tenon", description="Rotation")

    carreau_rotation: BoolProperty(name="Carreau", description="Rotation")
    accroche_rotation: BoolProperty(name="Accroche", description="Rotation")
    accroche_inverse_rotation: BoolProperty(
        name="Accroche inverse", description="Rotation"
    )
    cadre_central_rotation: BoolProperty(name="Cadre Central", description="Rotation")
    cadre_avant_rotation: BoolProperty(name="Cadre Avant", description="Rotation")
    fond_moule_rotation: BoolProperty(name="Fond Moule", description="Rotation")
    pilier_moule_rotation: BoolProperty(name="Pilier Moule", description="Rotation")
    cadre_moule_rotation: BoolProperty(name="Cadre Moule", description="Rotation")
    cadre_moule_long_rotation: BoolProperty(name="Cadre Moule", description="Rotation")

    def update(self, target, cursor):
        self[target] = cursor

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                    "peigne_court_position",
                    "peigne_long_position",
                    "cadre_mortaise_position",
                    "cadre_tenon_position",
                    "carreau_position",
                    "accroche_position",
                    "peigne_court_rotation",
                    "peigne_long_rotation",
                    "cadre_mortaise_rotation",
                    "cadre_tenon_rotation",
                    "carreau_rotation",
                    "accroche_rotation",
                ]
            case "1":
                return [
                    "peigne_court_position",
                    "peigne_long_position",
                    "cadre_mortaise_position",
                    "cadre_tenon_position",
                    "carreau_position",
                    "accroche_position",
                    "peigne_court_rotation",
                    "peigne_long_rotation",
                    "cadre_mortaise_rotation",
                    "cadre_tenon_rotation",
                    "carreau_rotation",
                    "accroche_rotation",
                ]
            case "2":
                return [
                    "cadre_mortaise_position",
                    "cadre_tenon_position",
                    "accroche_position",
                    "accroche_inverse_position",
                    "cadre_central_position",
                    "cadre_avant_position",
                    "cadre_mortaise_rotation",
                    "cadre_tenon_rotation",
                    "accroche_rotation",
                    "accroche_inverse_rotation",
                    "cadre_central_rotation",
                    "cadre_avant_rotation",
                ]
            case "3":
                return [
                    "fond_moule_position",
                    "fond_moule_rotation",
                    "pilier_moule_position",
                    "pilier_moule_rotation",
                    "cadre_moule_position",
                    "cadre_moule_rotation",
                    "cadre_moule_long_position",
                    "cadre_moule_long_rotation",
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


classes = [
    DiffuseurProps,
    ArrayProps,
    PositionProps,
    PrepareProps,
    UIProductProps,
    Usinageprops,
    DevisProps,
    DevisList

]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.usinage_props = bpy.props.PointerProperty(type=Usinageprops)
    bpy.types.Scene.dif_props = bpy.props.PointerProperty(type=DiffuseurProps)
    bpy.types.Scene.array_props = bpy.props.PointerProperty(type=ArrayProps)
    bpy.types.Scene.pos_props = bpy.props.PointerProperty(type=PositionProps)
    bpy.types.Scene.prep_props = bpy.props.PointerProperty(type=PrepareProps)
    bpy.types.Scene.product_props = bpy.props.PointerProperty(type=UIProductProps)
    bpy.types.Scene.devis_props = bpy.props.PointerProperty(type=DevisProps)
    bpy.types.Scene.devis_list = bpy.props.CollectionProperty(type=DevisList)
    bpy.types.Scene.dif_parts = []


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.usinage_props
    del bpy.types.Scene.dif_props
    del bpy.types.Scene.array_props
    del bpy.types.Scene.pos_props
    del bpy.types.Scene.prep_props
    del bpy.types.Scene.dif_parts
    del bpy.types.Scene.product_props
    del bpy.types.Scene.devis_props
    del bpy.types.Scene.devis_list
