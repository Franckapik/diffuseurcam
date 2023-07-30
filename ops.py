import bpy
import bmesh
from .shapes import (
    add_cadre_court_mortaise,
    add_cadre_long_mortaise,
    add_cadre_tenon,
    add_carreau,
    add_peigne_court,
    add_peigne_long,
)
from bpy_extras.object_utils import AddObjectHelper

class AddCadreCourtMortaise(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_court_mortaise"
    bl_label = "Ajouter Cadre Court Mortaise"
    bl_options = {"REGISTER", "UNDO"}
    
    

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges = add_cadre_court_mortaise(difprops)

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
    bl_idname = "mesh.cadre_long_mortaise"
    bl_label = "Ajouter Cadre Long Mortaise"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges = add_cadre_long_mortaise(difprops)

        #create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new("Cadre_long_mortaise")
        mesh.from_pydata(vertex, edges, [])

        # Load BMesh with mesh data
        bm.from_mesh(mesh)


        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()
    
        #Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        return {"FINISHED"}


class AddCadreTenon(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_tenon"
    bl_label = "Ajouter Cadre Tenon"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges = add_cadre_tenon(difprops)

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
    bl_idname = "mesh.carreau"
    bl_label = "Ajouter un carreau"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges = add_carreau(difprops)

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
    bl_idname = "mesh.peigne_court"
    bl_label = "Ajouter Peigne Court"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges = add_peigne_court(difprops)

        mesh = bpy.data.meshes.new("Peigne_court")

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
    bl_idname = "mesh.peigne_long"
    bl_label = "Ajouter Peigne Long"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges = add_peigne_long(difprops)

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
    
class AddDiffuseur(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.add_diffuseur"
    bl_label = "Ajouter Diffuseur"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges = add_peigne_long(difprops)
        vertex2, edges2 = add_cadre_tenon(difprops)

        mesh = bpy.data.meshes.new("Peigne_long")

        mesh.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.to_mesh(mesh)
        mesh.update()

        mesh2 = bpy.data.meshes.new("Cadre Tenon")

        mesh2.from_pydata(vertex, edges, [])
        bm = bmesh.new()
        bm.from_mesh(mesh2)
        bm.to_mesh(mesh2)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils

        object_utils.object_data_add(context, mesh, operator=self)

        return {"FINISHED"}


classes = [
    AddCadreCourtMortaise,
    AddCadreLongMortaise,
    AddCadreTenon,
    AddCarreau,
    AddPeigneCourt,
    AddPeigneLong,
    AddDiffuseur
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
