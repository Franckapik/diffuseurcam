import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import FloatProperty, BoolProperty


def add_carreau(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset_mortaise_interne,
    tenon_peigne,
    longueur_diffuseur,
    diffuseur_type_is2D,
    is_accroche
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

    if diffuseur_type_is2D:
        vertsCadre = [(0, 0, 0), (0, bloc, 0), (bloc, bloc, 0), (bloc, 0, 0), (0, 0, 0)]
    else:
        vertsCadre = [(0, 0, 0), (0, longueurTotale, 0), (bloc, longueurTotale, 0), (bloc, 0, 0), (0, 0, 0)]

    if is_accroche and diffuseur_type_is2D:
        bpy.ops.mesh.primitive_circle_add(radius=0.01, enter_editmode=True, align='WORLD', location= (bloc/2,bloc/2, 0), scale=(1, 1, 1))
        
    if is_accroche and not diffuseur_type_is2D :    
        bpy.ops.mesh.primitive_circle_add(radius=0.01, enter_editmode=True, align='WORLD', location= (bloc/2,longueurTotale/5, 0), scale=(1, 1, 1))
        bpy.ops.mesh.primitive_circle_add(radius=0.01, enter_editmode=True, align='WORLD', location= (bloc/2,longueurTotale/5 * 4, 0), scale=(1, 1, 1))


    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre


class AddCarreau(bpy.types.Operator, AddObjectHelper):
    """Ajouter un carreau"""

    bl_idname = "mesh.carreau"
    bl_label = "Ajouter un carreau"
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
    is_accroche: BoolProperty(
        name="Accroche",
        description="Box Accroche",
    )

    def execute(self, context):
        vertex, edges = add_carreau(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.largeur_diffuseur,
            self.offset_mortaise_interne,
            self.tenon_peigne,
            self.longueur_diffuseur,
            self.diffuseur_type_is2D,
            self.is_accroche
        )

        mesh = bpy.data.meshes.new("Carreau")

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
    self.layout.separator()
    self.layout.operator(AddCarreau.bl_idname, icon="MESH_CUBE")


# Register and add to the "add mesh" menu (required to use F3 search "Add Box" for quick access).
def register():
    bpy.utils.register_class(AddCarreau)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddCarreau)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.carreau()
