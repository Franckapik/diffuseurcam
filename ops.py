import bpy
import bmesh
from .shapes import add_cadre_court_mortaise, add_cadre_long_mortaise, add_cadre_tenon, add_carreau, add_peigne_court, add_peigne_long
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    FloatProperty,
    BoolProperty
)

class AddCadreCourtMortaise(bpy.types.Operator, AddObjectHelper):
    """Ajouter un cadre mortaise"""

    bl_idname = "mesh.cadre_court_mortaise"
    bl_label = "Ajouter Cadre Court Mortaise"
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

    def execute(self, context):
        vertex, edges = add_cadre_court_mortaise(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.largeur_diffuseur,
            self.offset_mortaise_interne,
            self.tenon_peigne,
        )

        mesh = bpy.data.meshes.new("Cadre_court_mortaise")

        mesh.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils

        object_utils.object_data_add(context, mesh, operator=self)

        return {"FINISHED"}
    
class AddCadreLongMortaise(bpy.types.Operator, AddObjectHelper):
    """Ajouter un cadre long mortaise"""

    bl_idname = "mesh.cadre_long_mortaise"
    bl_label = "Ajouter Cadre Long Mortaise"
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

    def execute(self, context):
        vertex, edges = add_cadre_long_mortaise(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.largeur_diffuseur,
            self.offset_mortaise_interne,
            self.tenon_peigne,
            self.longueur_diffuseur,
            self.diffuseur_type_is2D,
        )

        mesh = bpy.data.meshes.new("Cadre_long_mortaise")

        mesh.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils

        object_utils.object_data_add(context, mesh, operator=self)

        return {"FINISHED"}

class AddCadreTenon(bpy.types.Operator, AddObjectHelper):
    """Ajouter un cadre tenon"""

    bl_idname = "mesh.cadre_tenon"
    bl_label = "Ajouter Cadre Tenon"
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

    def execute(self, context):
        vertex, edges = add_cadre_tenon(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.largeur_diffuseur,
            self.offset_mortaise_interne,
            self.tenon_peigne,
        )

        mesh = bpy.data.meshes.new("Cadre_court_tenon")

        mesh.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils

        object_utils.object_data_add(context, mesh, operator=self)

        return {"FINISHED"}

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

class AddPeigneCourt(bpy.types.Operator, AddObjectHelper):
    """Ajouter un cadre tenon"""

    bl_idname = "mesh.peigne_court"
    bl_label = "Ajouter Peigne Court"
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

    def execute(self, context):
        vertex, edges = add_peigne_court(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.largeur_diffuseur,
            self.offset_mortaise_interne,
            self.tenon_peigne,
        )

        mesh = bpy.data.meshes.new("Cadre_court_tenon")

        mesh.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils

        object_utils.object_data_add(context, mesh, operator=self)

        return {"FINISHED"}

class AddPeigneLong(bpy.types.Operator, AddObjectHelper):
    """Ajouter un peigne long"""

    bl_idname = "mesh.peigne_long"
    bl_label = "Ajouter Peigne Long"
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
        step=25
    )


    def execute(self, context):
        vertex, edges = add_peigne_long(
            self.epaisseur,
            self.profondeur,
            self.tenon_cadre,
            self.bord_cadre,
            self.largeur_diffuseur,
            self.offset_mortaise_interne,
            self.tenon_peigne,
            self.longueur_diffuseur,
        )

        mesh = bpy.data.meshes.new("Peigne_long")

        mesh.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils

        object_utils.object_data_add(context, mesh, operator=self)

        return {"FINISHED"}


classes = [AddCadreCourtMortaise, AddCadreLongMortaise, AddCadreTenon, AddCarreau, AddPeigneCourt, AddPeigneLong]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
