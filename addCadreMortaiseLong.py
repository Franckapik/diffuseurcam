import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    FloatProperty,
    BoolProperty
)


def add_cadre_mortaise(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset,
    tenon_peigne,
    longueur_diffuseur,
    diffuseur_type_is2D
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    largeurTotale = largeur_diffuseur + 2 * epaisseur
    longueurArray = largeurTotale - 2 * correction
    bloc = longueurArray / N
    longueurTotale = N * longueur_diffuseur * bloc

    vertsCadre = [
        (0, 0, 0),
        (0, longueurTotale, 0),
        ((profondeur / 2 - tenon_cadre / 2), longueurTotale, 0),
        ((profondeur / 2 - tenon_cadre / 2), longueurTotale - epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), longueurTotale - epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), longueurTotale, 0),
        ((profondeur), longueurTotale, 0),
        ((profondeur), 0, 0),
        ((profondeur / 2 + tenon_cadre / 2), 0, 0),
        ((profondeur / 2 + tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), 0, 0),
    ]

    vertsMortaisesInt = []

    for k in range(1, round(N * longueur_diffuseur)):
        if diffuseur_type_is2D : 
            vertsMortaisesInt += [
                (bord_cadre, bloc * k, 0),
                (bord_cadre + tenon_peigne + offset, bloc * k, 0),
                (
                    bord_cadre + tenon_peigne + offset,
                    bloc * k - epaisseur,
                    0,
                ),
                (bord_cadre, bloc * k - epaisseur, 0),
                (profondeur - bord_cadre, bloc * k - epaisseur, 0),
                (profondeur - bord_cadre, bloc * k, 0),
                (
                    profondeur - bord_cadre - tenon_peigne - offset,
                    bloc * k,
                    0,
                ),
                (
                    profondeur - bord_cadre - tenon_peigne - offset,
                    bloc * k - epaisseur,
                    0,
                ),
            ]

    edgesMortaisesInt = []

    i = 0

    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsMortaisesInt)):
        i += 1
        if i == 4 or k == len(vertsCadre):
            i = 0
            edgesMortaisesInt += [
                (k, k + 1),
                (k + 1, k + 2),
                (k + 2, k + 3),
                (k + 3, k),
            ]

    edgesCadre = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 11),
        (11, 0),
    ]

    verts = [*list(vertsCadre), *list(vertsMortaisesInt)]
    edges = [*list(edgesCadre), *list(edgesMortaisesInt)]

    return verts, edges


class AddCadreMortaise(bpy.types.Operator, AddObjectHelper):
    """Ajouter un Cadre mortaise"""

    bl_idname = "mesh.cadre_mortaise"
    bl_label = "Ajouter Cadre mortaise"
    bl_options = {"REGISTER", "UNDO"}

    epaisseur: FloatProperty(
        name="epaisseur",
        description="Box epaisseur",
        min=0.003,
        max=0.008,
        default=0.003,
    )
    profondeur: FloatProperty(
        name="profondeur",
        description="Box profondeur",
        min=0.05,
        max=0.2,
        default=0.1,
    )
    bord_cadre: FloatProperty(
        name="bord_cadre",
        description="Box bord_cadre",
        min=0.01,
        max=0.5,
        default=0.015,
    )
    largeur_diffuseur: FloatProperty(
        name="largeur_diffuseur",
        description="Box largeur_diffuseur",
        min=0.05,
        max=1,
        default=0.5,
    )
    tenon_cadre: FloatProperty(
        name="tenon_cadre",
        description="Box tenon_cadre",
        min=0.01,
        max=0.1,
        default=0.05,
    )
    offset: FloatProperty(
        name="offset",
        description="Box offset",
        min=0.000,
        max=0.005,
        default=0.01,
    )
    tenon_peigne: FloatProperty(
        name="tenon_peigne",
        description="Box tenon_peigne",
        min=0.01,
        max=0.05,
        default=0.01,
    )
    longueur_diffuseur: FloatProperty(
        name="longueur_diffuseur",
        description="Box longueur_diffuseur",
        min=0.5,
        max=2,
        default=1,
        step=25,
    )
    diffuseur_type_is2D: BoolProperty(
        name="Diffuseur 2D",
        description="Box Type de diffuseur",
    )

    def execute(self, context):
        vertex, edges = add_cadre_mortaise(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.largeur_diffuseur,
            self.offset,
            self.tenon_peigne,
            self.longueur_diffuseur,
            self.diffuseur_type_is2D,
        )

        mesh = bpy.data.meshes.new("cadre_mortaise")

        mesh.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils

        object_utils.object_data_add(context, mesh, operator=self)

        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(AddCadreMortaise.bl_idname, icon="MESH_CUBE")


# Register and add to the "add mesh" menu (required to use F3 search "Add Box" for quick access).
def register():
    bpy.utils.register_class(AddCadreMortaise)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddCadreMortaise)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.cadre_mortaise()
