import bpy

from bpy.props import FloatProperty, BoolProperty


class DiffuseurProps(bpy.types.PropertyGroup):
    epaisseur: FloatProperty(
        name="epaisseur",
        description="Box epaisseur",
        min=0.003,
        max=0.008,
        default=0.003,
        unit="LENGTH",
        precision=4,
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
    offset_mortaise_interne: FloatProperty(
        name="offset_mortaise_interne",
        description="Box offset_mortaise_interne",
        min=0.000,
        max=0.005,
        default=0.01,
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

    offset_mortaise_interne: FloatProperty(
        name="offset_mortaise_interne",
        description="Box offset_mortaise_interne",
        min=0.000,
        max=0.005,
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
        unit="LENGTH",
        precision=4,
    )
    diffuseur_type_is2D: BoolProperty(
        name="Diffuseur 2D",
        description="Box Type de diffuseur",
    )

    is_accroche: BoolProperty(
        name="Accroche",
        description="Box Accroche",
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
            )
        ]
        return attributes


classes = [DiffuseurProps]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.dif_props = bpy.props.PointerProperty(type=DiffuseurProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.dif_props
