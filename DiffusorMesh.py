import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    FloatProperty,
)


def add_cadre(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    longueur_cadre,
    offset_mortaise_interne,
    tenon_peigne,
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    longueurTotale = longueur_cadre + 2 * epaisseur
    longueurArray = longueurTotale - 2 * correction

    firstM = longueurArray / N

    verts = [
        (0, epaisseur, 0),
        (0, longueur_cadre - epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), longueur_cadre - epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), longueur_cadre, 0),
        ((profondeur / 2 + tenon_cadre / 2), longueur_cadre, 0),
        ((profondeur / 2 + tenon_cadre / 2), longueur_cadre - epaisseur, 0),
        ((profondeur), longueur_cadre - epaisseur, 0),
        ((profondeur), epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), 0, 0),
        ((profondeur / 2 - tenon_cadre / 2), 0, 0),
        ((profondeur / 2 - tenon_cadre / 2), epaisseur, 0),
    ]

    """ List = []

    for k in range(1, N):
        List += [
            (bord_cadre, firstM * k, 0),
            (bord_cadre + tenon_peigne + offset_mortaise_interne, firstM * k, 0),
            (
                bord_cadre + tenon_peigne + offset_mortaise_interne,
                firstM * k - epaisseur,
                0,
            ),
            (bord_cadre, firstM * k - epaisseur, 0),
        ] """

    """ print(
        tuple([
            (bord_cadre, firstM * N, 0),
            (
                bord_cadre + tenon_peigne + offset_mortaise_interne,
                firstM * N,
                0,
            ),
            (
                bord_cadre + tenon_peigne + offset_mortaise_interne,
                firstM * N - epaisseur,
                0,
            ),
            (bord_cadre, firstM * N - epaisseur, 0),
        ]
        for N in range(1, N))
    ) """

    """ numbers = [
        1,
        2,
        3,
        4,
        5,
        *map(lambda x: x*x, range(1,6)  ),  # use * to "splat" the iterable out
    ]

    print(numbers) """

    def vertsMortaisesInt(n) :
        return (bord_cadre, firstM * N,0 ),(bord_cadre + tenon_peigne + offset_mortaise_interne,firstM * N,0 ),(bord_cadre + tenon_peigne + offset_mortaise_interne,firstM * N - epaisseur,0 ),(bord_cadre,firstM * N - epaisseur,0 )

    verts2 = list(map(vertsMortaisesInt, range(1,N)))
    print(len(verts2), verts2)

    # a = [i*i for i in range(10)]
    #
    #
    edges = [
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

    return verts, edges


class AddBox(bpy.types.Operator, AddObjectHelper):
    """Add a simple box mesh"""

    bl_idname = "mesh.primitive_box_add"
    bl_label = "Add Box"
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
    longueur_cadre: FloatProperty(
        name="longueur_cadre",
        description="Box longueur_cadre",
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
    offset_mortaise_interne: FloatProperty(
        name="offset_mortaise_interne",
        description="Box offset_mortaise_interne",
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

    def execute(self, context):
        vertex, edges = add_cadre(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.longueur_cadre,
            self.offset_mortaise_interne,
            self.tenon_peigne,
        )

        mesh = bpy.data.meshes.new("Cadre_Long")

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
    self.layout.operator(AddBox.bl_idname, icon="MESH_CUBE")


# Register and add to the "add mesh" menu (required to use F3 search "Add Box" for quick access).
def register():
    bpy.utils.register_class(AddBox)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddBox)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.primitive_box_add()
