import bpy
import bmesh
from .shapes import *
from .difarray import difArray
from .bridges import place_empties_on_bounding_box
from .pack import place_selected_objects_no_overlap
from bpy_extras.object_utils import AddObjectHelper
from bpy.props import FloatVectorProperty, StringProperty, IntProperty
import math
import os
import re
import time
from mathutils import Vector


def _batch_sort_key(obj):
    """Clé de tri numérique pour les objets batch.
    Format attendu : D{dim}N{type}W{largeur}P{profondeur}L{longueur}E{epaisseur}[.suffix]
    Exemples : D1N7W50P5L1E5, D2N11W50P10L2E5.001
    Ordre : D1 < D2, puis N7 < N11 < N13, puis P5 < P10 < P15 < P20, etc."""
    m = re.match(r'D(\d+)N(\d+)W(\d+)P(\d+)L(\d+)E(\d+)', obj.name)
    if m:
        return tuple(int(x) for x in m.groups()) + (obj.name,)
    # Fallback : noms sans préfixe D (anciens objets)
    m2 = re.match(r'N(\d+)W(\d+)P(\d+)L(\d+)E(\d+)', obj.name)
    if m2:
        return (9999,) + tuple(int(x) for x in m2.groups()) + (obj.name,)
    return (9999, 9999, 9999, 9999, 9999, 9999, obj.name)


class AddCadreMortaise(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_mortaise"
    bl_label = "Ajouter Cadre mortaise"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_cadre_mortaise(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props
        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        """ ne fonctionne pas  """
        total_area = sum(f.calc_area() for f in bm.faces)
        print("Total Surface Area:", total_area)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        """ place_empties_on_bounding_box(mesh_obj) """

        mesh_obj.location = (
            posprops.cadre_mortaise_position[0],
            posprops.cadre_mortaise_position[1],
            posprops.cadre_mortaise_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_mortaise_x,
            arrayprops.cadre_mortaise_y,
            difprops.profondeur,
            difprops.largeur_diffuseur * difprops.longueur_diffuseur,
        )

        if posprops.cadre_mortaise_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddCadreTenon(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_tenon"
    bl_label = "Ajouter Cadre Tenon"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_cadre_tenon(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.cadre_tenon_position[0],
            posprops.cadre_tenon_position[1],
            posprops.cadre_tenon_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_tenon_x,
            arrayprops.cadre_tenon_y,
            difprops.profondeur,
            difprops.largeur_diffuseur,
        )

        if posprops.cadre_tenon_rotation:
            mesh_obj.rotation_euler = [0, 0, math.pi / 2]

        return {"FINISHED"}


class AddCarreau(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.carreau"
    bl_label = "Ajouter un carreau"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_carreau(scene.dif_props, scene.product_props, scene.usinage_props)
        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.carreau_position[0],
            posprops.carreau_position[1],
            posprops.carreau_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.carreau_x,
            arrayprops.carreau_y,
            difprops.getRang(),
            (
                difprops.getRang()
                if scene.product_props.product_type == "0"
                else difprops.largeur_diffuseur * difprops.longueur_diffuseur
            ),
        )

        if posprops.carreau_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddAccroche(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.accroche"
    bl_label = "Ajouter une accroche"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_accroche(scene.dif_props, scene.product_props, scene.usinage_props, False)
        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.accroche_position[0],
            posprops.accroche_position[1],
            posprops.accroche_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.accroche_x,
            arrayprops.accroche_y,
            difprops.getRang(),
            difprops.getRang(),
        )

        if posprops.accroche_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddAccrocheInverse(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.accroche_inverse"
    bl_label = "Ajouter une accroche inverse"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_accroche(scene.dif_props, scene.product_props, scene.usinage_props, True)
        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.accroche_inverse_position[0],
            posprops.accroche_inverse_position[1],
            posprops.accroche_inverse_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.accroche_inverse_x,
            arrayprops.accroche_inverse_y,
            difprops.getRang(),
            difprops.getRang(),
        )

        if posprops.accroche_inverse_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddCadreAvant(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.renfort_angle"
    bl_label = "Ajouter un Renfort angle"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_renfort_angle(scene.dif_props, scene.product_props, scene.usinage_props)
        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.renfort_angle_position[0],
            posprops.renfort_angle_position[1],
            posprops.renfort_angle_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.renfort_angle_x,
            arrayprops.renfort_angle_y,
            difprops.getRang(),
            difprops.getRang(),
        )
        if posprops.renfort_angle_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddPeigneCourt(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.peigne_court"
    bl_label = "Ajouter Peigne Court"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_peigne_court(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.peigne_court_position[0],
            posprops.peigne_court_position[1],
            posprops.peigne_court_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.peigne_court_x,
            arrayprops.peigne_court_y,
            difprops.profondeur,
            difprops.largeur_diffuseur,
        )
        if posprops.peigne_court_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddCadreCentral(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.renfort_central"
    bl_label = "Ajouter Renfort central"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_renfort_central(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.renfort_central_position[0],
            posprops.renfort_central_position[1],
            posprops.renfort_central_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.renfort_central_x,
            arrayprops.renfort_central_y,
            difprops.profondeur,
            difprops.longueur_diffuseur,
        )

        if posprops.renfort_central_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddPeigneLong(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.peigne_long"
    bl_label = "Ajouter Peigne Long"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_peigne_long(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.peigne_long_position[0],
            posprops.peigne_long_position[1],
            posprops.peigne_long_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.peigne_long_x,
            arrayprops.peigne_long_y,
            difprops.profondeur,
            difprops.longueur_diffuseur * difprops.largeur_diffuseur,
        )

        if posprops.peigne_long_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddFondMoule(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.fond_moule"
    bl_label = "Ajouter Fond Moule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_fond_moule(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.fond_moule_position[0],
            posprops.fond_moule_position[1],
            posprops.fond_moule_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.fond_moule_x,
            arrayprops.fond_moule_y,
            difprops.profondeur,
            difprops.longueur_diffuseur,
        )

        if posprops.fond_moule_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddCadreMoule(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_moule"
    bl_label = "Ajouter Cadre Moule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_cadre_moule(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.cadre_moule_position[0],
            posprops.cadre_moule_position[1],
            posprops.cadre_moule_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_moule_x,
            arrayprops.cadre_moule_y,
            difprops.largeur_diffuseur,
            difprops.profondeur + difprops.epaisseur_moule,
        )

        if posprops.cadre_moule_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddCadreMouleLong(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_moule_long"
    bl_label = "Ajouter Cadre Moule Long"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_cadre_moule_long(scene.dif_props, scene.product_props, scene.usinage_props)

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.cadre_moule_long_position[0],
            posprops.cadre_moule_long_position[1],
            posprops.cadre_moule_long_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_moule_long_x,
            arrayprops.cadre_moule_long_y,
            difprops.largeur_diffuseur,
            difprops.profondeur + difprops.epaisseur_moule,
        )

        if posprops.cadre_moule_long_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddColle(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.colle"
    bl_label = "Ajouter Colle"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_colle(scene.dif_props, scene.product_props, scene.usinage_props, scene.array_props)

        gcode_lines = []
        gcode_lines.append("G21 ; Set units to millimeters")
        gcode_lines.append("G17G90 ; Absolute positioning")
        for points in vertex:
            x, y, z = points
            x, y, z = x * 1000, y * 1000, z * 1000
            print(x)
            gcode_lines.append(f"G1 X{x:.2f} Y{y:.2f} Z{difprops.profondeur * 1000:.2f} F500")
            gcode_lines.append(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f}")
            gcode_lines.append(f"G1 X{x:.2f} Y{y:.2f} Z{difprops.profondeur * 1000:.2f}")

        gcode_lines.append("G00 Z20.0")
        gcode_lines.append("M30 ; End of program")

        # Sauvegarder le G-code dans un fichier
        with open("/home/fanch/output.gcode", "w") as f:
            for line in gcode_lines:
                f.write(line + "\n")

        print("G-code exporté avec succès.")

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        return {"FINISHED"}


class Add3DModel(bpy.types.Operator, AddObjectHelper):
    """Génère un modèle 3D assemblé complet du diffuseur acoustique QRD (Schroeder)
    avec cadres, peignes et carreaux extrudés à l'épaisseur du bois,
    positionnés selon la séquence de profondeurs QRD."""

    bl_idname = "mesh.simulation"
    bl_label = "Ajouter Modele 3D"
    bl_options = {"REGISTER", "UNDO"}

    def _create_box(self, bm, x, y, z, sx, sy, sz, mat_index=0):
        """Crée un parallélépipède solide dans le bmesh.
        Position (x, y, z) = coin inférieur-gauche-arrière.
        Dimensions (sx, sy, sz) = taille selon X, Y, Z."""
        verts = [
            bm.verts.new((x, y, z)),
            bm.verts.new((x + sx, y, z)),
            bm.verts.new((x + sx, y + sy, z)),
            bm.verts.new((x, y + sy, z)),
            bm.verts.new((x, y, z + sz)),
            bm.verts.new((x + sx, y, z + sz)),
            bm.verts.new((x + sx, y + sy, z + sz)),
            bm.verts.new((x, y + sy, z + sz)),
        ]
        faces_data = [
            (verts[0], verts[3], verts[2], verts[1]),  # Dessous (Z-)
            (verts[4], verts[5], verts[6], verts[7]),  # Dessus (Z+)
            (verts[0], verts[1], verts[5], verts[4]),  # Avant (Y-)
            (verts[2], verts[3], verts[7], verts[6]),  # Arrière (Y+)
            (verts[0], verts[4], verts[7], verts[3]),  # Gauche (X-)
            (verts[1], verts[2], verts[6], verts[5]),  # Droite (X+)
        ]
        for fd in faces_data:
            f = bm.faces.new(fd)
            f.material_index = mat_index

    def _load_material_from_blend(self):
        """Charge le matériau 'ctp' depuis le fichier materials.blend."""
        import os
        addon_dir = os.path.dirname(__file__)
        blend_path = os.path.join(addon_dir, "materials.blend")
        
        if not os.path.exists(blend_path):
            print(f"⚠️ Fichier {blend_path} introuvable, matériau par défaut créé")
            return None
        
        try:
            # Charger le matériau depuis le fichier .blend
            with bpy.data.libraries.load(blend_path) as (data_from, data_to):
                if "ctp" in data_from.materials:
                    data_to.materials.append("ctp")
            
            # Récupérer le matériau chargé
            mat = bpy.data.materials.get("ctp")
            if mat:
                print(f"✅ Matériau 'ctp' chargé depuis {blend_path}")
                return mat
            else:
                print(f"⚠️ Matériau 'ctp' non trouvé après chargement")
                return None
                
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement du matériau: {e}")
            return None

    def _get_or_create_material(self, name, color):
        """Récupère ou crée un matériau PBR bois avec la couleur donnée."""
        mat = bpy.data.materials.get(name)
        if mat is None:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = color
                if "Roughness" in bsdf.inputs:
                    bsdf.inputs["Roughness"].default_value = 0.75
        return mat

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        product_type = scene.product_props.product_type
        invert_depth = difprops.invert_depth

        if product_type not in ("0", "1"):
            self.report({"WARNING"}, "Le modèle 3D est disponible uniquement pour les diffuseurs 1D et 2D")
            return {"CANCELLED"}

        # ── Paramètres du diffuseur ──────────────────────────────────────
        e = difprops.epaisseur              # Épaisseur du bois (ex: 3mm)
        D = difprops.profondeur             # Profondeur totale (ex: 100mm)
        W = difprops.largeur_diffuseur      # Largeur totale (ex: 500mm)
        N = difprops.type                   # Ordre QRD (ex: 7)
        rang = difprops.getRang()           # Pas de cellule = (W - e) / N
        L = difprops.getLongueur()          # Longueur totale

        # Séquence de profondeurs QRD (Schroeder)
        depth = difprops.getMotif("depth")

        # 1D ou 2D
        is_1d = (difprops.moule_type == "1d") or (product_type == "1")
        num_cols = N
        num_rows = 1 if is_1d else round(N * difprops.longueur_diffuseur)

        # ── Matériaux (3 teintes bois) ───────────────────────────────────
        MAT_CADRE = 0       # Cadres (chêne foncé)
        MAT_PEIGNE = 1      # Peignes (chêne moyen)
        MAT_CARREAU = 2     # Carreaux (chêne clair)

        # Essayer de charger le matériau depuis materials.blend
        mat_ctp = self._load_material_from_blend()
        
        if mat_ctp:
            # Utiliser le matériau chargé pour tous les éléments
            mat_cadre = mat_ctp
            mat_peigne = mat_ctp
            mat_carreau = mat_ctp
        else:
            # Créer les matériaux par défaut si le chargement échoue
            mat_cadre = self._get_or_create_material(
                "DIF_Cadre", (0.40, 0.24, 0.10, 1.0))
            mat_peigne = self._get_or_create_material(
                "DIF_Peigne", (0.58, 0.40, 0.20, 1.0))
            mat_carreau = self._get_or_create_material(
                "DIF_Carreau", (0.76, 0.56, 0.35, 1.0))

        bm = bmesh.new()

        # ── CADRES (rectangle extérieur) ─────────────────────────────────
        # Convention: X = largeur, Y = longueur, Z = profondeur (face à la pièce)
        #
        #  Cadre mortaise gauche   │  cellules  │   Cadre mortaise droit
        #        (e × L × D)       │            │      (e × L × D)
        #  ────────────────────────┼────────────┼───────────────────────
        #  Cadre tenon bas (W-2e × e × D)       Cadre tenon haut

        # Cadre mortaise gauche (côté long)
        self._create_box(bm, 0, 0, 0, e, L, D, MAT_CADRE)
        # Cadre mortaise droit
        self._create_box(bm, W - e, 0, 0, e, L, D, MAT_CADRE)
        # Cadre tenon bas (côté court, entre les mortaises)
        self._create_box(bm, e, 0, 0, W - 2 * e, e, D, MAT_CADRE)
        # Cadre tenon haut
        self._create_box(bm, e, L - e, 0, W - 2 * e, e, D, MAT_CADRE)

        # ── PEIGNES LONGS (divisent la largeur en N colonnes) ────────────
        # Orientés selon Y, de épaisseur e, entre les cadres tenon
        # En 2D : rainures (mi-profondeur) aux croisements avec les peignes courts
        half_D = D / 2

        for k in range(1, num_cols):
            px = k * rang

            if is_1d:
                # 1D : pas de croisement, peigne pleine hauteur
                self._create_box(bm, px, e, 0, e, L - 2 * e, D, MAT_PEIGNE)
            else:
                # 2D : le peigne long a des rainures dans la moitié HAUTE (Z >= half_D)
                # aux positions Y des peignes courts.
                # Partie basse (0 → half_D) : continue sur toute la longueur
                self._create_box(bm, px, e, 0, e, L - 2 * e, half_D, MAT_PEIGNE)

                # Partie haute (half_D → D) : découpée aux croisements
                y_start = e  # début après le cadre tenon bas
                for j in range(1, num_rows):
                    cross_y = j * rang
                    # Segment avant la rainure
                    seg_len = cross_y - y_start
                    if seg_len > 0.0001:
                        self._create_box(bm, px, y_start, half_D, e, seg_len, half_D, MAT_PEIGNE)
                    # Sauter la rainure (largeur = e)
                    y_start = cross_y + e

                # Dernier segment après la dernière rainure
                seg_len = (L - e) - y_start
                if seg_len > 0.0001:
                    self._create_box(bm, px, y_start, half_D, e, seg_len, half_D, MAT_PEIGNE)

        # ── PEIGNES COURTS (2D uniquement, divisent la longueur) ─────────
        # Orientés selon X, entre les cadres mortaises
        # Rainures dans la moitié BASSE (Z < half_D) aux croisements avec les peignes longs
        if not is_1d:
            for k in range(1, num_rows):
                py = k * rang

                # Partie haute (half_D → D) : continue sur toute la largeur
                self._create_box(bm, e, py, half_D, W - 2 * e, e, half_D, MAT_PEIGNE)

                # Partie basse (0 → half_D) : découpée aux croisements
                x_start = e  # début après le cadre mortaise gauche
                for j in range(1, num_cols):
                    cross_x = j * rang
                    # Segment avant la rainure
                    seg_len = cross_x - x_start
                    if seg_len > 0.0001:
                        self._create_box(bm, x_start, py, 0, seg_len, e, half_D, MAT_PEIGNE)
                    # Sauter la rainure (largeur = e)
                    x_start = cross_x + e

                # Dernier segment après la dernière rainure
                seg_len = (W - e) - x_start
                if seg_len > 0.0001:
                    self._create_box(bm, x_start, py, 0, seg_len, e, half_D, MAT_PEIGNE)

        # ── CARREAUX (tuiles de fond aux profondeurs QRD) ────────────────
        # Chaque carreau est un rectangle extrudé de l'épaisseur du bois,
        # positionné en Z selon la séquence quadratique de Schroeder :
        #   depth=0 → fond du puits (contre le mur)
        #   depth≈D → surface (face à la pièce)
        tile_w = rang - e   # largeur claire d'une cellule

        if is_1d:
            # 1D : carreaux allongés sur toute la longueur
            tile_l = L - 2 * e
            for col in range(num_cols):
                if col < len(depth):
                    z = depth[col]
                    # Inverser Z si demandé
                    if invert_depth:
                        z = D - z - e
                    tx = col * rang + e
                    self._create_box(bm, tx, e, z, tile_w, tile_l, e, MAT_CARREAU)
        else:
            # 2D : carreaux carrés dans chaque cellule de la grille
            tile_l = rang - e
            for row in range(num_rows):
                for col in range(num_cols):
                    idx = row * num_cols + col
                    if idx < len(depth):
                        z = depth[idx]
                        # Inverser Z si demandé
                        if invert_depth:
                            z = D - z - e
                        tx = col * rang + e
                        ty = row * rang + e
                        self._create_box(bm, tx, ty, z, tile_w, tile_l, e, MAT_CARREAU)

        # ── Création du mesh et de l'objet Blender ───────────────────────
        mesh_name = "3D_" + difprops.getDifName(scene)
        mesh = bpy.data.meshes.new(mesh_name)
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()

        obj = bpy.data.objects.new(mesh.name, mesh)
        obj.data.materials.append(mat_cadre)
        obj.data.materials.append(mat_peigne)
        obj.data.materials.append(mat_carreau)

        bpy.context.collection.objects.link(obj)
        bpy.types.Scene.dif_parts.append(obj.name)

        # Sélectionner et centrer l'origine
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Unwrap automatique pour les UV (nécessaire pour les textures)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(margin_method='SCALED')
        
        # Mettre à l'échelle les UVs pour améliorer la résolution de la texture
        # Évite le flou en augmentant la densité de texture sur chaque pièce
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        uv_layer = bm.loops.layers.uv.active
        if uv_layer:
            for face in bm.faces:
                for loop in face.loops:
                    loop[uv_layer].uv *= 3
        bmesh.update_edit_mesh(mesh)
        
        bpy.ops.object.mode_set(mode='OBJECT')

        print(f"✅ Modèle 3D généré: {mesh_name}")
        print(f"   Type: {'1D' if is_1d else '2D'} QRD N={N} | Grille {num_cols}×{num_rows}")
        print(f"   Dimensions: {W*1000:.0f} × {L*1000:.0f} × {D*1000:.0f} mm")
        print(f"   Pièces: 4 cadres + {num_cols - 1} peignes longs"
              + (f" + {num_rows - 1} peignes courts" if not is_1d else "")
              + f" + {min(num_cols * num_rows, len(depth))} carreaux")
        print(f"   ✅ Smart UV project appliqué (scale ×3) - textures optimisées")

        return {"FINISHED"}


class AddPilierMoule(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.pilier_moule"
    bl_label = "Ajouter Piliers Moule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        vertex, edges, name = add_pilier_moule(
            scene.dif_props, scene.product_props, scene.usinage_props, scene.array_props
        )

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.pilier_moule_position[0],
            posprops.pilier_moule_position[1],
            posprops.pilier_moule_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.pilier_moule_x,
            arrayprops.pilier_moule_y,
            (difprops.getLargeurPilier() + arrayprops.array_offset) * (difprops.type + 1),
            difprops.longueur_diffuseur,  # calcul à faire sur l'addition des ratios
        )

        if posprops.pilier_moule_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        # --- Codage par trous traversants (mono-piliers uniquement) ---
        if difprops.type_moule == "mono" and getattr(difprops, "pilier_codage", False):
            circles = get_codage_monopilier_circles(difprops, arrayprops)

            curve_data = bpy.data.curves.new("Codage_Piliers", type='CURVE')
            curve_data.dimensions = '2D'

            segments = 32
            for (cx, cy, radius) in circles:
                spline = curve_data.splines.new('POLY')
                spline.use_cyclic_u = True
                spline.points.add(segments - 1)  # déjà 1 point par défaut
                for j in range(segments):
                    angle = 2 * math.pi * j / segments
                    x = cx + radius * math.cos(angle)
                    y = cy + radius * math.sin(angle)
                    spline.points[j].co = (x, y, 0, 1)

            codage_obj = bpy.data.objects.new("Codage_Piliers", curve_data)
            bpy.context.collection.objects.link(codage_obj)
            bpy.types.Scene.dif_parts.append(codage_obj.name)

            codage_obj.location = (
                posprops.pilier_moule_position[0],
                posprops.pilier_moule_position[1],
                posprops.pilier_moule_position[2],
            )
            if posprops.pilier_moule_rotation:
                codage_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddContrePilierMoule(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.contre_pilier_moule"
    bl_label = "Ajouter Contre Piliers Moule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        productprops = scene.product_props
        usinageprops = scene.usinage_props
        
        # Vérifier que nous sommes bien dans le bon cas
        if productprops.product_type != "3":
            print(f"❌ [DEBUG] ERREUR: product_type doit être '3' (moule), reçu: '{productprops.product_type}'")
            return {"CANCELLED"}
            
        try:
            vertex, edges, name = add_contre_pilier_moule(
                scene.dif_props, scene.product_props, scene.usinage_props, scene.array_props
            )
            
            if len(vertex) == 0:
                print("❌ [DEBUG] ERREUR: Aucun vertex généré pour les contre-piliers!")
                return {"CANCELLED"}
                
        except Exception as e:
            print(f"❌ [DEBUG] ERREUR dans add_contre_pilier_moule: {e}")
            import traceback
            traceback.print_exc()
            return {"CANCELLED"}

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.contre_pilier_moule_position[1],
            posprops.contre_pilier_moule_position[2],
            posprops.contre_pilier_moule_position[0],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.contre_pilier_moule_x,
            arrayprops.contre_pilier_moule_y,
            (difprops.getLargeurPilier() + arrayprops.array_offset) * (difprops.type + 1),
            difprops.longueur_diffuseur,  # calcul à faire sur l'addition des ratios
        )

        if posprops.contre_pilier_moule_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddCadreTissuLong(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_tissu_long"
    bl_label = "Ajouter Cadre Tissu Long"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        vertex, edges, name = add_cadre_tissu_long(
            scene.dif_props, scene.product_props, scene.usinage_props, scene.array_props
        )

        is_splitted = True if difprops.longueur_absorbeur > difprops.split and difprops.split != 0 else False
        longueurAbsorbeur = (difprops.longueur_absorbeur - 2 * difprops.epaisseur) if not is_splitted else (difprops.longueur_absorbeur - 2 * difprops.epaisseur) / 2


        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.cadre_tissu_long_position[0],
            posprops.cadre_tissu_long_position[1],
            posprops.cadre_tissu_long_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_tissu_long_x,
            arrayprops.cadre_tissu_long_y,
            0.03,
            longueurAbsorbeur,
        )

        if posprops.cadre_tissu_long_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddCadreTissuCourt(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_tissu_court"
    bl_label = "Ajouter Cadre Tissu Court"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        vertex, edges, name = add_cadre_tissu_court(
            scene.dif_props, scene.product_props, scene.usinage_props, scene.array_props
        )

        arrayprops = scene.array_props

        # create a bmesh
        bm = bmesh.new()

        # Create new mesh data.
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertex, edges, [])

        # Positionning according to position props
        posprops = scene.pos_props

        mesh.update(calc_edges=True)

        # Load BMesh with mesh data
        bm.from_mesh(mesh)

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)
        bpy.types.Scene.dif_parts.append(mesh_obj.name)

        mesh_obj.location = (
            posprops.cadre_tissu_court_position[0],
            posprops.cadre_tissu_court_position[1],
            posprops.cadre_tissu_court_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_tissu_court_x,
            arrayprops.cadre_tissu_court_y,
            0.03,
            difprops.largeur_diffuseur,
        )

        if posprops.cadre_tissu_court_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddDiffuseur(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.add_diffuseur"
    bl_label = "Generer Diffuseur"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene

        AddCadreMortaise.execute(self, context)
        AddCadreTenon.execute(self, context)
        AddCarreau.execute(self, context)
        AddPeigneLong.execute(self, context)
        AddAccroche.execute(self, context)
        if scene.product_props.product_type == "0":
            AddPeigneCourt.execute(self, context)

        return {"FINISHED"}


class AddAbsorbeur(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.add_absorbeur"
    bl_label = "Generer Absorbeur"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        AddCadreMortaise.execute(self, context)
        AddCadreTenon.execute(self, context)
        AddAccroche.execute(self, context)
        AddAccrocheInverse.execute(self, context)
        AddCadreCentral.execute(self, context)
        AddCadreAvant.execute(self, context)
        AddCadreTissuCourt.execute(self, context)
        AddCadreTissuLong.execute(self, context)

        return {"FINISHED"}


class AddMoule(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.add_moule"
    bl_label = "Generer Moule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        print("🔧 [DEBUG] Génération complète du moule...")
        AddCadreMoule.execute(self, context)
        AddFondMoule.execute(self, context)
        AddPilierMoule.execute(self, context)
        AddContrePilierMoule.execute(self, context)  # AJOUT DES CONTRE-PILIERS
        AddCadreMouleLong.execute(self, context)
        print("✅ [DEBUG] Génération complète du moule terminée!")

        return {"FINISHED"}


class AddList(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.add_list"
    bl_label = "Ajouter au devis"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        devisprops = scene.devis_props
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
        qtyPanel = math.ceil(devisprops.qtyDif * areaMaterial / areaPanel)

        newItem = bpy.context.scene.devis_list.add()
        newItem.listDif = f"{difprops.getDifName()} : {qtyPanel} panneaux"

        return {"FINISHED"}


class RemoveList(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.remove_list"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}
    item: IntProperty(name="item to remove")

    def execute(self, context):
        scene = context.scene
        scene.devis_list.remove(self.item)

        return {"FINISHED"}


class PickPosition(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.pick_position"
    bl_label = "Set position from Cursor 3D"
    bl_options = {"REGISTER", "UNDO"}
    cursor: FloatVectorProperty(name="cursor3d_position")
    target: StringProperty(name="Name of part to change position")

    def execute(self, context):
        print(self.target)
        scene = context.scene
        posprops = scene.pos_props
        posprops.update(self.target, self.cursor)

        return {"FINISHED"}


class SetArrayOffset(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.set_array_offset"
    bl_label = "Offset standard (3>x)"
    bl_options = {"REGISTER", "UNDO"}
    arrayOffsetFactor: IntProperty(name="array offset factor")

    def execute(self, context):
        scene = context.scene
        arrayprops = scene.array_props
        usinageprops = scene.usinage_props
        arrayprops.array_offset = self.arrayOffsetFactor * usinageprops.fraise

        return {"FINISHED"}


class SetRecommendedArray(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.set_array_recommended"
    bl_label = "Pré-remplissage Array"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        arrayprops = scene.array_props
        difprops = scene.dif_props
        if scene.product_props.product_type == "0":
            arrayprops.peigne_court_x = int(difprops.type * difprops.longueur_diffuseur - 1)
            arrayprops.peigne_court_y = 1
            arrayprops.peigne_long_x = difprops.type - 1
            arrayprops.peigne_long_y = 1
            arrayprops.cadre_mortaise_x = 2
            arrayprops.cadre_mortaise_y = 1
            arrayprops.cadre_tenon_x = 2
            arrayprops.cadre_tenon_y = 1
            arrayprops.carreau_x = difprops.type
            arrayprops.carreau_y = difprops.type
            arrayprops.accroche_x = 2
            arrayprops.accroche_y = 2

        if scene.product_props.product_type == "1":
            arrayprops.peigne_long_x = difprops.type - 1
            arrayprops.peigne_long_y = 1
            arrayprops.cadre_mortaise_x = 2
            arrayprops.cadre_mortaise_y = 1
            arrayprops.cadre_tenon_x = 2
            arrayprops.cadre_tenon_y = 1
            arrayprops.carreau_x = difprops.type
            arrayprops.carreau_y = 1
            arrayprops.accroche_x = 2
            arrayprops.accroche_y = 2

        return {"FINISHED"}


class NoOverlap(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.no_overlap"
    bl_label = "Disperser la selection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Call the function to pack all objects
        bin_width = 1.0
        place_selected_objects_no_overlap(bin_width)

        return {"FINISHED"}


class PrepareToCam(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.prepare_cam"
    bl_label = "Transformer"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        prepprops = scene.prep_props
        difprops = scene.dif_props
        usinageprops = scene.usinage_props

        # mesh selection

        if prepprops.selection_prepare == "0":
            bpy.ops.object.select_all(action="DESELECT")
            for o in bpy.data.objects:
                if o.name in bpy.types.Scene.dif_parts:
                    bpy.context.view_layer.objects.active = o
                    o.select_set(True)

        if prepprops.selection_prepare == "1":
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

        if prepprops.selection_prepare == "2":
            bpy.ops.object.select_all(action="SELECT")

        # copy selected mesh>
        if prepprops.isNewMesh_prepare:
            C = bpy.context
            old_select_objects = C.selected_objects
            for o in C.selected_objects:
                new_obj = o.copy()
                new_obj.name += "_cam"
                C.collection.objects.link(new_obj)

            bpy.ops.object.select_all(action="DESELECT")

            if prepprops.isHidingOldMesh_prepare:
                new_collection = bpy.data.collections.new("origine")
                bpy.context.scene.collection.children.link(new_collection)

                for obj in old_select_objects:
                    # Délier l'objet de toutes les collections actuelles
                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                    # Ajouter l'objet à la nouvelle collection
                    new_collection.objects.link(obj)

                # Rendre la nouvelle collection non visible dans le viewport
                new_collection.hide_viewport = True

            if prepprops.isDeleteOldMesh_prepare:
                for obj in old_select_objects:
                    obj.select_set(True)
                    bpy.ops.object.delete()

            # Sélectionner et convertir uniquement les objets _cam de type MESH
            cam_mesh_objects = [o for o in bpy.data.objects if "_cam" in o.name and o.type == 'MESH']
            if cam_mesh_objects:
                bpy.ops.object.select_all(action="DESELECT")
                for obj in cam_mesh_objects:
                    obj.select_set(True)
                bpy.context.view_layer.objects.active = cam_mesh_objects[0]
                # Vérification du contexte
                if bpy.context.selected_objects and bpy.context.view_layer.objects.active and bpy.context.view_layer.objects.active.type == 'MESH':
                    print(f"🔄 Conversion de {len(cam_mesh_objects)} objets _cam MESH en courbes")
                    bpy.ops.object.convert(target="CURVE")
                    # Optionnel : reconvertir en mesh si besoin
                    # bpy.ops.object.convert(target="MESH")
                else:
                    print("⚠️ Impossible de convertir : contexte ou type incorrect")
            else:
                print("⚠️ Aucun objet _cam de type MESH à convertir")

        # convert to curve
        if prepprops.isConvertToCurve_prepare:
            # Vérifier qu'il y a des objets sélectionnés et qu'ils sont des mesh
            if bpy.context.selected_objects:
                # Filtrer uniquement les objets de type MESH
                mesh_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
                
                if mesh_objects:
                    # S'assurer qu'un objet mesh est actif
                    bpy.context.view_layer.objects.active = mesh_objects[0]
                    print(f"🔄 Conversion de {len(mesh_objects)} objet(s) MESH en courbes")
                    
                    # Sélectionner seulement les mesh objects
                    bpy.ops.object.select_all(action="DESELECT")
                    for obj in mesh_objects:
                        obj.select_set(True)
                    
                    bpy.ops.object.convert(target="CURVE")

                    # remove double if curve
                    if prepprops.isCRemove_prepare:
                        bpy.ops.object.curve_remove_doubles()
                else:
                    print("⚠️ Aucun objet MESH trouvé pour la conversion en courbe")
            else:
                print("⚠️ Aucun objet sélectionné pour la conversion en courbe")

        # Offset de ponçage des carreaux (simplifié au maximum)
        if prepprops.isOffsetCarreau_prepare and prepprops.isConvertToCurve_prepare:
            for obj in bpy.context.selected_objects:
                if "Carreau" in obj.name and obj.type == 'CURVE':
                    bpy.ops.object.select_all(action="DESELECT")
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                    try:
                        bpy.ops.object.silhouete_offset(offset=0.001, style='2')

                        if bpy.context.active_object != obj:
                            bpy.data.objects.remove(obj, do_unlink=True)
                    except:
                        pass

        # join selected object
        if prepprops.isJoin_prepare:
            bpy.ops.object.join()
            bpy.context.object.name = difprops.getDifName()
            if prepprops.isConvertToCurve_prepare and prepprops.isOvercuts:
                # Sauvegarder l'objet avant overcuts pour le supprimer après
                old_object = bpy.context.object
                old_object_name = old_object.name
                
                # Appliquer les overcuts
                bpy.ops.object.curve_overcuts(diameter=usinageprops.fraise, threshold=1.569)
                
                # Supprimer l'ancien mesh si un nouveau a été créé
                if bpy.context.object != old_object and old_object_name in bpy.data.objects:
                    # Déselectionner tout
                    bpy.ops.object.select_all(action='DESELECT')
                    # Sélectionner et supprimer l'ancien objet
                    old_object.select_set(True)
                    bpy.data.objects.remove(old_object, do_unlink=True)

        return {"FINISHED"}


class PositionSelected(bpy.types.Operator):
    """Opérateur pour positionner une pièce par rapport à une autre avec des options configurables"""
    bl_idname = "mesh.position_selected"
    bl_label = "Positionner la selection"
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.EnumProperty(
        name="Direction",
        description="Direction de déplacement",
        items=[
            ('X+', "Droite", "Déplacer la pièce à droite selon X+ et aligner Y"),
            ('X-', "Gauche", "Déplacer la pièce à gauche selon X- et aligner Y"),
            ('Y+', "Haut", "Déplacer la pièce en haut selon Y+ et aligner X"),
            ('Y-', "Bas", "Déplacer la pièce en bas selon Y- et aligner X")
        ],
        default='X+'
    )

    array_offset: bpy.props.FloatProperty(
        name="Array Offset",
        description="Distance de déplacement en mètres",
        default=0.015
    )

    def execute(self, context):
        scene = context.scene
        arrayprops = scene.array_props
        array_offset = arrayprops.array_offset

        # Vérifier si deux objets sont sélectionnés
        if len(context.selected_objects) != 2:
            self.report({'ERROR'}, "Veuillez sélectionner exactement deux objets.")
            return {'CANCELLED'}

        # Obtenir les deux objets sélectionnés
        active_obj = context.view_layer.objects.active  # L'objet actif
        selected_objs = [obj for obj in context.selected_objects if obj != active_obj]

        if not active_obj or len(selected_objs) != 1:
            self.report({'ERROR'}, "Veuillez sélectionner deux objets, avec un actif.")
            return {'CANCELLED'}

        obj1 = selected_objs[0]  # L'objet à déplacer
        obj2 = active_obj         # L'objet actif, utilisé comme référence

        # Placer l'origine des objets au centre de leur géométrie
        bpy.ops.object.convert(target='MESH') #apply array
        
        bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        bpy.context.view_layer.objects.active = obj1
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        bpy.context.view_layer.objects.active = obj2
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

        # Calculer les dimensions des objets via le bounding box
        bbox1 = [obj1.matrix_world @ Vector(corner) for corner in obj1.bound_box]
        bbox2 = [obj2.matrix_world @ Vector(corner) for corner in obj2.bound_box]

        min1 = tuple(min(bbox1, key=lambda v: v[i])[i] for i in range(3))
        max1 = tuple(max(bbox1, key=lambda v: v[i])[i] for i in range(3))
        min2 = tuple(min(bbox2, key=lambda v: v[i])[i] for i in range(3))
        max2 = tuple(max(bbox2, key=lambda v: v[i])[i] for i in range(3))
        

        # Appliquer le déplacement en fonction de la direction
        if self.direction == 'X+':
            obj1.location.x = max2[0] + array_offset + (max1[0] - min1[0]) / 2
            bpy.ops.object.align(bb_quality=False, align_mode='OPT_1', relative_to='OPT_4', align_axis={'Y'})

        elif self.direction == 'X-':
            obj1.location.x = min2[0] - array_offset - (max1[0] - min1[0]) / 2
            bpy.ops.object.align(bb_quality=False, align_mode='OPT_1', relative_to='OPT_4', align_axis={'Y'})

        elif self.direction == 'Y+':
            obj1.location.y = max2[1] + array_offset + (max1[1] - min1[1]) / 2
            bpy.ops.object.align(align_mode='OPT_1', align_axis={'X'})

        elif self.direction == 'Y-':
            obj1.location.y = min2[1] - array_offset - (max1[1] - min1[1]) / 2
            bpy.ops.object.align(align_mode='OPT_1', align_axis={'X'})


        # Conserver la position Z
        obj1.location.z = (min2[2] + max2[2]) / 2  # Centrer sur Z

        self.report({'INFO'}, f"{obj1.name} positionné par rapport à {obj2.name} ({self.direction}).")
        return {'FINISHED'}
    
addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    for direction, key in [('X+', 'RIGHT_ARROW'), ('X-', 'LEFT_ARROW'), ('Y+', 'UP_ARROW'), ('Y-', 'DOWN_ARROW')]:
        kmi = km.keymap_items.new(PositionSelected.bl_idname, key, 'PRESS')
        kmi.properties.direction = direction
        addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        addon_keymaps.clear()


class Batch3DGenerate(bpy.types.Operator):
    """Génère un batch de modèles 3D avec toutes les combinaisons de type, profondeur et longueur,
    disposés en quadrillage pour une vue d'ensemble"""
    bl_idname = "mesh.batch_3d"
    bl_label = "Générer Batch 3D"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from itertools import product as iterproduct

        scene = context.scene
        batch_props = scene.batch_3d_props
        difprops = scene.dif_props

        # Parse des valeurs depuis les champs texte
        try:
            types = [int(x.strip()) for x in batch_props.batch_types.split(",") if x.strip()]
            profondeurs = [float(x.strip()) / 1000 for x in batch_props.batch_profondeurs.split(",") if x.strip()]
            longueurs = [float(x.strip()) for x in batch_props.batch_longueurs.split(",") if x.strip()]
        except ValueError:
            self.report({"ERROR"}, "Format invalide. Utilisez des nombres séparés par des virgules.")
            return {"CANCELLED"}

        if not types or not profondeurs or not longueurs:
            self.report({"ERROR"}, "Spécifiez au moins une valeur pour chaque variable.")
            return {"CANCELLED"}

        # Validation des plages
        for t in types:
            if t < 6 or t > 13:
                self.report({"ERROR"}, f"Type {t} invalide (doit être entre 6 et 13).")
                return {"CANCELLED"}
        for p in profondeurs:
            if p < 0.05 or p > 0.5:
                self.report({"ERROR"}, f"Profondeur {p*1000:.0f}mm invalide (50-500mm).")
                return {"CANCELLED"}
        for l in longueurs:
            if l < 0.5 or l > 2:
                self.report({"ERROR"}, f"Longueur {l} invalide (0.5-2).")
                return {"CANCELLED"}

        # Sauvegarder les valeurs originales
        orig_type = difprops.type
        orig_profondeur = difprops.profondeur
        orig_longueur = difprops.longueur_diffuseur
        orig_product_type = scene.product_props.product_type
        orig_moule_type = difprops.moule_type

        # Déterminer les types de produits à générer
        if batch_props.batch_product_type == "2":
            product_types = ["0", "1"]
        else:
            product_types = [batch_props.batch_product_type]

        # Toutes les combinaisons (product_type, type, profondeur, longueur)
        combinations = list(iterproduct(product_types, types, profondeurs, longueurs))
        total = len(combinations)

        # Créer une collection dédiée au batch
        batch_name = f"Batch_3D_{total}x"
        batch_collection = bpy.data.collections.new(batch_name)
        bpy.context.scene.collection.children.link(batch_collection)

        num_cols = math.ceil(math.sqrt(total))
        gap = batch_props.batch_grid_gap
        generated_objects = []

        print(f"\n{'='*50}")
        print(f"BATCH 3D : {total} modèles à générer")
        print(f"Types: {types} | Profondeurs(mm): {[p*1000 for p in profondeurs]} | Longueurs: {longueurs}")
        print(f"{'='*50}")

        for i, (pt, t, p, l) in enumerate(combinations):
            # Appliquer les paramètres de cette combinaison
            scene.product_props.product_type = pt
            difprops.moule_type = "1d" if pt == "1" else "2d"
            difprops.type = t
            difprops.profondeur = p
            difprops.longueur_diffuseur = l

            # Générer le modèle 3D
            bpy.ops.mesh.simulation()

            obj = context.active_object
            if obj:
                # Utiliser la nomenclature centralisée (D1/D2 + paramètres)
                obj.name = difprops.getDifName(scene)

                # Déplacer dans la collection batch
                for coll in list(obj.users_collection):
                    coll.objects.unlink(obj)
                batch_collection.objects.link(obj)

                generated_objects.append(obj)
                print(f"  [{i+1}/{total}] {obj.name} — {obj.dimensions.x*1000:.0f}×{obj.dimensions.y*1000:.0f}×{obj.dimensions.z*1000:.0f}mm")

        # Positionner en quadrillage
        if generated_objects:
            col_widths = {}
            row_heights = {}

            for i, obj in enumerate(generated_objects):
                row_idx = i // num_cols
                col_idx = i % num_cols
                dims = obj.dimensions
                col_widths[col_idx] = max(col_widths.get(col_idx, 0), dims.x)
                row_heights[row_idx] = max(row_heights.get(row_idx, 0), dims.y)

            for i, obj in enumerate(generated_objects):
                row_idx = i // num_cols
                col_idx = i % num_cols
                x = sum(col_widths.get(c, 0) + gap for c in range(col_idx))
                y = -sum(row_heights.get(r, 0) + gap for r in range(row_idx))
                obj.location = (x, y, 0)

        # Restaurer les valeurs originales
        difprops.type = orig_type
        difprops.profondeur = orig_profondeur
        difprops.longueur_diffuseur = orig_longueur
        scene.product_props.product_type = orig_product_type
        difprops.moule_type = orig_moule_type

        # Sélectionner tous les objets générés
        bpy.ops.object.select_all(action="DESELECT")
        for obj in generated_objects:
            obj.select_set(True)

        print(f"\n✅ Batch terminé : {len(generated_objects)} modèles dans '{batch_name}'")
        self.report({"INFO"}, f"{len(generated_objects)} modèles 3D générés dans '{batch_name}'")
        return {"FINISHED"}


class ClearBatch3D(bpy.types.Operator):
    """Supprime tous les modèles et collections du batch 3D"""
    bl_idname = "mesh.clear_batch_3d"
    bl_label = "Supprimer Batch 3D"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        collections_removed = 0
        objects_removed = 0
        for coll in list(bpy.data.collections):
            if coll.name.startswith("Batch_3D"):
                for obj in list(coll.objects):
                    bpy.data.objects.remove(obj, do_unlink=True)
                    objects_removed += 1
                bpy.data.collections.remove(coll)
                collections_removed += 1

        if collections_removed == 0:
            self.report({"WARNING"}, "Aucun batch 3D trouvé")
        else:
            self.report({"INFO"}, f"Batch supprimé : {objects_removed} objets, {collections_removed} collections")
        return {"FINISHED"}


class AddBatchPreset(bpy.types.Operator):
    """Sauvegarde la configuration batch actuelle comme nouveau preset"""
    bl_idname = "mesh.add_batch_preset"
    bl_label = "Ajouter Preset Batch"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        batch_props = context.scene.batch_3d_props
        preset = context.scene.batch_presets.add()
        preset.name = batch_props.preset_name
        preset.types = batch_props.batch_types
        preset.profondeurs = batch_props.batch_profondeurs
        preset.longueurs = batch_props.batch_longueurs
        batch_props.active_preset_index = len(context.scene.batch_presets) - 1
        self.report({"INFO"}, f"Preset '{preset.name}' ajouté")
        return {"FINISHED"}


class RemoveBatchPreset(bpy.types.Operator):
    """Supprime le preset batch sélectionné de la liste"""
    bl_idname = "mesh.remove_batch_preset"
    bl_label = "Supprimer Preset Batch"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.scene.batch_presets) > 0

    def execute(self, context):
        batch_props = context.scene.batch_3d_props
        index = batch_props.active_preset_index
        if 0 <= index < len(context.scene.batch_presets):
            name = context.scene.batch_presets[index].name
            context.scene.batch_presets.remove(index)
            batch_props.active_preset_index = min(index, max(0, len(context.scene.batch_presets) - 1))
            self.report({"INFO"}, f"Preset '{name}' supprimé")
        return {"FINISHED"}


class LoadBatchPreset(bpy.types.Operator):
    """Charge le preset sélectionné dans les champs de configuration batch"""
    bl_idname = "mesh.load_batch_preset"
    bl_label = "Charger Preset"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.scene.batch_presets) > 0

    def execute(self, context):
        batch_props = context.scene.batch_3d_props
        index = batch_props.active_preset_index
        if 0 <= index < len(context.scene.batch_presets):
            preset = context.scene.batch_presets[index]
            batch_props.batch_types = preset.types
            batch_props.batch_profondeurs = preset.profondeurs
            batch_props.batch_longueurs = preset.longueurs
            self.report({"INFO"}, f"Preset '{preset.name}' chargé")
        return {"FINISHED"}


class SaveBatchPreset(bpy.types.Operator):
    """Met à jour le preset sélectionné avec la configuration batch actuelle"""
    bl_idname = "mesh.save_batch_preset"
    bl_label = "Sauvegarder Preset"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.scene.batch_presets) > 0

    def execute(self, context):
        batch_props = context.scene.batch_3d_props
        index = batch_props.active_preset_index
        if 0 <= index < len(context.scene.batch_presets):
            preset = context.scene.batch_presets[index]
            preset.types = batch_props.batch_types
            preset.profondeurs = batch_props.batch_profondeurs
            preset.longueurs = batch_props.batch_longueurs
            self.report({"INFO"}, f"Preset '{preset.name}' mis à jour")
        return {"FINISHED"}


class UpdateAddonOperator(bpy.types.Operator):
    """Met à jour l'addon depuis le dépôt Git"""

    bl_idname = "addon.update_git"
    bl_label = "Mettre à jour l'addon"

    def execute(self, context):
        addon_path = os.path.dirname(os.path.abspath(__file__))
        try:
            import git
        except ImportError:
            print("[ERREUR] Le module 'git' n'est pas installé. Assurez-vous que 'gitpython' est installé.")
            self.report({"ERROR"}, "Le module 'git' n'est pas installé.")
            return {"CANCELLED"}
        
        try:
            # Ouvre le dépôt Git
            repo = git.Repo(addon_path)
            
            # Récupère les informations avant la mise à jour
            current_commit = repo.head.commit.hexsha[:7]
            current_branch = repo.active_branch.name
            
            print(f"[UPDATE] Commit actuel: {current_commit}")
            print(f"[UPDATE] Branche actuelle: {current_branch}")
            
            # Vérifie l'état du repository
            if repo.is_dirty():
                print("[UPDATE] Détection de modifications locales non commitées")
                # Sauvegarde les modifications locales
                try:
                    repo.git.stash('push', '-m', 'Auto-stash before update')
                    print("[UPDATE] Modifications locales sauvegardées")
                except:
                    print("[UPDATE] Pas de modifications à sauvegarder")
            
            # Récupère les dernières modifications depuis le serveur
            origin = repo.remotes.origin
            print("[UPDATE] Récupération des mises à jour depuis GitHub...")
            origin.fetch()
            
            # Vérifie s'il y a des mises à jour
            try:
                commits_behind = list(repo.iter_commits(f'HEAD..origin/{current_branch}'))
            except:
                # Si la branche n'existe pas sur origin, utiliser main
                commits_behind = list(repo.iter_commits('HEAD..origin/main'))
                current_branch = 'main'
            
            if not commits_behind:
                self.report({"INFO"}, "L'addon est déjà à jour.")
                return {"FINISHED"}
            
            print(f"[UPDATE] {len(commits_behind)} commits en retard")
            
            # Effectue une mise à jour forcée pour éviter les conflits
            print("[UPDATE] Mise à jour forcée en cours...")
            repo.git.reset('--hard', f'origin/{current_branch}')
            
            # Nettoie les fichiers non suivis qui pourraient causer des problèmes
            repo.git.clean('-fd')
            
            new_commit = repo.head.commit.hexsha[:7]
            
            print(f"[UPDATE] Mise à jour terminée: {current_commit} → {new_commit}")
            self.report({"INFO"}, f"Addon mis à jour avec succès. ({current_commit} → {new_commit})")

            # Recharge l'addon
            print("[UPDATE] Rechargement de l'addon...")
            bpy.ops.script.reload()
            
        except git.exc.InvalidGitRepositoryError:
            error_msg = "Ce dossier n'est pas un dépôt Git. Mise à jour impossible."
            print(f"[ERREUR] {error_msg}")
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}
        except git.exc.GitCommandError as e:
            error_msg = f"Erreur Git lors de la mise à jour : {str(e)}"
            print(f"[ERREUR] {error_msg}")
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}
        except Exception as e:
            error_msg = f"Erreur inattendue lors de la mise à jour : {str(e)}"
            print(f"[ERREUR] {error_msg}")
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}

        return {"FINISHED"}


class CheckUpdateOperator(bpy.types.Operator):
    """Vérifie s'il y a une nouvelle version disponible sur GitHub"""
    
    bl_idname = "addon.check_update"
    bl_label = "Vérifier les mises à jour"
    
    def execute(self, context):
        try:
            import urllib.request
            import json
            from .version import __version__, UPDATE_CHECK_URL
            
            # Requête vers l'API GitHub
            with urllib.request.urlopen(UPDATE_CHECK_URL) as response:
                data = json.loads(response.read().decode())
                
            latest_version = data['tag_name'].lstrip('v')  # Enlève le 'v' du début si présent
            current_version = __version__
            
            if self.compare_versions(latest_version, current_version) > 0:
                self.report({"INFO"}, f"Nouvelle version disponible: {latest_version} (actuelle: {current_version})")
            else:
                self.report({"INFO"}, f"Vous avez la dernière version: {current_version}")
                
        except Exception as e:
            self.report({"ERROR"}, f"Erreur lors de la vérification: {str(e)}")
            return {"CANCELLED"}
            
        return {"FINISHED"}
    
    def compare_versions(self, version1, version2):
        """Compare deux versions au format semver. Retourne 1 si v1 > v2, -1 si v1 < v2, 0 si égales"""
        def version_tuple(v):
            return tuple(map(int, v.split('.')))
        
        v1_tuple = version_tuple(version1)
        v2_tuple = version_tuple(version2)
        
        if v1_tuple > v2_tuple:
            return 1
        elif v1_tuple < v2_tuple:
            return -1
        else:
            return 0


class AddonInfoOperator(bpy.types.Operator):
    """Affiche les informations détaillées de l'addon"""
    
    bl_idname = "addon.show_info"
    bl_label = "Informations de l'addon"
    
    def execute(self, context):
        self.report({"INFO"}, "Informations affichées dans la console")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        
        # Informations de base
        box = layout.box()
        box.label(text="Diffuseur CAM", icon="BLENDER")
        
        try:
            from .version import __version__
            box.label(text=f"Version: {__version__}")
        except ImportError:
            box.label(text="Version: inconnue")
        
        box.label(text="Auteur: Franckapik")
        
        # Informations Git
        try:
            import git
            addon_path = os.path.dirname(os.path.abspath(__file__))
            repo = git.Repo(addon_path)
            
            box.separator()
            box.label(text="Informations Git:")
            
            current_commit = repo.head.commit.hexsha[:7]
            box.label(text=f"Commit: {current_commit}")
            
            branch = repo.active_branch.name
            box.label(text=f"Branche: {branch}")
            
            # Vérifie s'il y a des modifications non commitées
            if repo.is_dirty():
                box.label(text="⚠ Modifications non sauvegardées", icon="ERROR")
            else:
                box.label(text="✓ Repository propre", icon="CHECKMARK")
                
        except Exception as e:
            box.label(text=f"Git: {str(e)}")
        
        # Liens utiles
        box.separator()
        col = box.column()
        col.operator("wm.url_open", text="GitHub Repository", icon="URL").url = "https://github.com/Franckapik/diffuseurcam"


class GitDiagnosticOperator(bpy.types.Operator):
    """Diagnostique l'état du repository Git pour le débogage"""
    
    bl_idname = "addon.git_diagnostic"
    bl_label = "Diagnostic Git"
    
    def execute(self, context):
        addon_path = os.path.dirname(os.path.abspath(__file__))
        
        print("\n" + "="*50)
        print("DIAGNOSTIC GIT - DIFFUSEUR CAM")
        print("="*50)
        
        try:
            import git
        except ImportError:
            error_msg = "Le module 'git' n'est pas installé"
            print(f"[ERREUR] {error_msg}")
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}
        
        try:
            repo = git.Repo(addon_path)
            
            # Informations de base
            print(f"Chemin du repository: {addon_path}")
            print(f"Commit actuel: {repo.head.commit.hexsha}")
            print(f"Commit court: {repo.head.commit.hexsha[:7]}")
            print(f"Branche active: {repo.active_branch.name}")
            print(f"Remote URL: {repo.remotes.origin.url}")
            
            # État du repository
            print(f"\nÉtat du repository:")
            print(f"  - Repository sale (modifications): {repo.is_dirty()}")
            print(f"  - Fichiers non suivis: {len(repo.untracked_files)}")
            
            if repo.untracked_files:
                print("  - Fichiers non suivis:", repo.untracked_files)
            
            # Vérifier les commits en retard
            try:
                origin = repo.remotes.origin
                origin.fetch()
                
                current_branch = repo.active_branch.name
                commits_behind = list(repo.iter_commits(f'HEAD..origin/{current_branch}'))
                commits_ahead = list(repo.iter_commits(f'origin/{current_branch}..HEAD'))
                
                print(f"\nÉtat de synchronisation:")
                print(f"  - Commits en retard: {len(commits_behind)}")
                print(f"  - Commits en avance: {len(commits_ahead)}")
                
                if commits_behind:
                    print("  - Derniers commits distants:")
                    for commit in commits_behind[:3]:
                        print(f"    {commit.hexsha[:7]}: {commit.summary}")
                
                if commits_ahead:
                    print("  - Commits locaux non poussés:")
                    for commit in commits_ahead[:3]:
                        print(f"    {commit.hexsha[:7]}: {commit.summary}")
                        
            except Exception as e:
                print(f"[ERREUR] Impossible de vérifier la synchronisation: {e}")
            
            # Informations sur la version
            try:
                from .version import __version__
                print(f"\nVersion de l'addon: {__version__}")
            except ImportError:
                print("\n[ERREUR] Impossible de lire la version")
            
            print("="*50)
            
            self.report({"INFO"}, "Diagnostic affiché dans la console")
            
        except git.exc.InvalidGitRepositoryError:
            error_msg = "Ce dossier n'est pas un dépôt Git"
            print(f"[ERREUR] {error_msg}")
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}
        except Exception as e:
            error_msg = f"Erreur lors du diagnostic: {str(e)}"
            print(f"[ERREUR] {error_msg}")
            self.report({"ERROR"}, error_msg)
            return {"CANCELLED"}

        return {"FINISHED"}


class BatchRender(bpy.types.Operator):
    """Génère automatiquement un rendu Cycles pour chaque modèle 3D du batch,
    avec caméra et éclairage positionnés automatiquement.
    Opérateur modal : affiche la progression et supporte l'annulation (ESC)."""
    bl_idname = "render.batch_render"
    bl_label = "Batch Render"
    bl_options = {"REGISTER"}

    # ── Constantes ──────────────────────────────────────────────────────
    _FORMAT_EXT = {'PNG': '.png', 'JPEG': '.jpg', 'OPEN_EXR': '.exr'}

    # ── État interne (par instance d'opérateur) ─────────────────────────
    _timer = None
    _batch_objects = []       # Objets dans l'intervalle (à rendre)
    _all_batch_objects = []   # Tous les objets Batch_3D_* (pour masquage complet)
    _current_index = 0
    _current_orbit_step = 0
    _orbit_angles = []
    _rendered = 0
    _output_dir = ""
    _cam_obj = None
    _cam_data = None
    _orig_rotations = {}  # Sauvegarde des rotations originales {obj.name: Euler}
    _orig_shadow_rotation = None  # Rotation originale du shadow plane
    _lights = []
    _shadow_plane = None
    _shadow_plane_data = None
    _orig = None
    _orig_world = None
    _orig_hide_render = {}    # Sauvegarde hide_render pour TOUS les objets batch
    _orig_display_type = None
    _orig_collection_exclude = {}
    _render_times = []           # Durées mesurées des rendus individuels
    _render_start_time = None    # Timestamp de début du rendu courant

    # ── Poll ────────────────────────────────────────────────────────────
    @classmethod
    def poll(cls, context):
        rp = context.scene.batch_render_props
        if rp.is_running:
            return False
        return any(c.name.startswith("Batch_3D_") for c in bpy.data.collections)

    # ── Invoke → prépare puis lance le modal ────────────────────────────
    def invoke(self, context, event):
        scene = context.scene
        rp = scene.batch_render_props

        # Nettoyer un éventuel preview pour repartir des rotations d'origine
        BatchRenderPreview._cleanup_preview(context)

        # Validation du chemin de sortie
        self._output_dir = bpy.path.abspath(rp.output_path)
        if not self._output_dir:
            self.report({"ERROR"}, "Spécifiez un dossier de sortie")
            return {"CANCELLED"}
        os.makedirs(self._output_dir, exist_ok=True)

        # Collecter et trier tous les objets mesh dans les collections Batch_3D_*
        # Tri : (nom de collection, nom d'objet) → ordre alphanumérique stable et prévisible
        raw_objects = []
        for collection in sorted(bpy.data.collections, key=lambda c: c.name):
            if collection.name.startswith("Batch_3D_"):
                for obj in sorted(collection.objects, key=_batch_sort_key):
                    if obj.type == 'MESH':
                        raw_objects.append(obj)

        if not raw_objects:
            self.report({"WARNING"}, "Aucun objet trouvé dans les collections Batch_3D_*")
            return {"CANCELLED"}

        # Conserver la liste complète pour masquer les objets hors-intervalle
        self._all_batch_objects = raw_objects

        # ── Filtrage par intervalle (ex: "5:8" → modèles 5 à 8 inclus, 1-indexé) ──
        range_str = rp.render_range.strip()
        if range_str:
            try:
                parts = range_str.split(":")
                if len(parts) != 2:
                    raise ValueError("Format attendu : N:M")
                idx_start = int(parts[0].strip()) - 1  # Convertir en 0-indexé
                idx_end = int(parts[1].strip())         # Inclus → slice exclusif OK
                n_total = len(raw_objects)
                if idx_start < 0 or idx_end > n_total or idx_start >= idx_end:
                    self.report({"ERROR"}, f"Intervalle '{range_str}' invalide — plage autorisée : 1:{n_total}")
                    return {"CANCELLED"}
                self._batch_objects = raw_objects[idx_start:idx_end]
                print(f"  ↳ Intervalle actif : modèles {idx_start + 1} à {idx_end} "
                      f"({len(self._batch_objects)}/{n_total} objets)")
            except (ValueError, IndexError) as e:
                self.report({"ERROR"}, f"Format d'intervalle invalide : '{range_str}' — {e}")
                return {"CANCELLED"}
        else:
            self._batch_objects = raw_objects

        total = len(self._batch_objects)
        self._current_index = 0
        self._rendered = 0

        # Nettoyage du preview si actif
        BatchRenderPreview._cleanup_preview(context)

        print(f"\n{'='*60}")
        print(f"BATCH RENDER : {total} objets à rendre")
        print(f"Dossier : {self._output_dir}")
        print(f"{'='*60}")

        # ── Sauvegarder l'état original ──────────────────────────────────
        self._orig = self._save_render_state(scene)

        # ── Configurer Cycles ────────────────────────────────────────────
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = rp.render_samples
        scene.cycles.use_denoising = rp.use_denoising
        scene.render.resolution_x = rp.render_resolution_x
        scene.render.resolution_y = rp.render_resolution_y
        scene.render.image_settings.file_format = rp.output_format
        if rp.output_format == 'PNG':
            scene.render.image_settings.color_mode = 'RGBA'
        if rp.transparent_background and rp.output_format in ('PNG', 'OPEN_EXR'):
            scene.render.film_transparent = True

        # ── Créer caméra temporaire ──────────────────────────────────────
        self._cam_data = bpy.data.cameras.new("_BatchRender_Cam")
        self._cam_data.lens = rp.camera_focal_length
        self._cam_obj = bpy.data.objects.new("_BatchRender_Cam", self._cam_data)
        scene.collection.objects.link(self._cam_obj)
        scene.camera = self._cam_obj

        # ── Créer l'éclairage temporaire ─────────────────────────────────
        self._lights = self._create_lights(scene, rp)

        # ── Configurer HDRI si demandé ───────────────────────────────────
        self._orig_world = scene.world
        if rp.use_hdri and rp.hdri_path:
            self._setup_hdri(scene, rp.hdri_path, rp.hdri_strength)

        # ── Créer le shadow catcher si demandé ─────────────────────────
        self._shadow_plane = None
        self._shadow_plane_data = None
        if rp.use_shadow_catcher:
            self._shadow_plane_data = bpy.data.meshes.new("_BatchRender_ShadowPlane")
            import bmesh as _bm
            tmp = _bm.new()
            _bm.ops.create_grid(tmp, x_segments=1, y_segments=1, size=1.0)
            tmp.to_mesh(self._shadow_plane_data)
            tmp.free()
            self._shadow_plane = bpy.data.objects.new("_BatchRender_ShadowPlane", self._shadow_plane_data)
            scene.collection.objects.link(self._shadow_plane)
            self._shadow_plane.is_shadow_catcher = True
            # Rendre le plan invisible au viewport mais visible au rendu
            self._shadow_plane.display_type = 'WIRE'

        # ── S'assurer que toutes les collections Batch_3D_* sont incluses dans le view layer ──
        # (une collection exclue rend ses objets invisibles au rendu même avec hide_render=False)
        self._orig_collection_exclude = {}
        for layer_coll in context.view_layer.layer_collection.children:
            if layer_coll.name.startswith("Batch_3D_"):
                self._orig_collection_exclude[layer_coll.name] = layer_coll.exclude
                if layer_coll.exclude:
                    layer_coll.exclude = False
                    print(f"  ↳ Collection '{layer_coll.name}' réactivée dans le view layer")

        # ── Forcer hide_render=False sur tous les objets batch (réinitialisation robuste) ──
        # Évite la corruption d'état si un run précédent n'a pas restauré correctement
        for obj in raw_objects:
            obj.hide_render = False

        # ── Sauvegarder la visibilité originale de TOUS les objets batch ──
        self._orig_hide_render = {obj.name: False for obj in self._all_batch_objects}

        # ── Masquer immédiatement tous les objets hors-intervalle ────────
        rendered_names = {obj.name for obj in self._batch_objects}
        for obj in self._all_batch_objects:
            if obj.name not in rendered_names:
                obj.hide_render = True

        # ── Sauvegarder les rotations originales des modèles (tous) ────────
        self._orig_rotations = {obj.name: obj.rotation_euler.copy() for obj in self._all_batch_objects}
        if self._shadow_plane:
            self._orig_shadow_rotation = self._shadow_plane.rotation_euler.copy()

        # ── Calcul des angles d'orbite (rotation des modèles) ────────────
        self._orbit_angles = []
        if rp.orbit_angle_neg90:
            self._orbit_angles.append(math.radians(-90))
        if rp.orbit_angle_neg60:
            self._orbit_angles.append(math.radians(-60))
        if rp.orbit_angle_neg45:
            self._orbit_angles.append(math.radians(-45))
        if rp.orbit_angle_neg30:
            self._orbit_angles.append(math.radians(-30))
        if rp.orbit_angle_0:
            self._orbit_angles.append(0.0)
        if rp.orbit_angle_30:
            self._orbit_angles.append(math.radians(30))
        if rp.orbit_angle_45:
            self._orbit_angles.append(math.radians(45))
        if rp.orbit_angle_60:
            self._orbit_angles.append(math.radians(60))
        if rp.orbit_angle_90:
            self._orbit_angles.append(math.radians(90))
        
        # Si aucun angle n'est coché, inclure 0° par défaut
        if not self._orbit_angles:
            self._orbit_angles = [0.0]
        
        self._current_orbit_step = 0
        total_renders = total * len(self._orbit_angles)
        self._render_times = []   # Réinitialiser les mesures de temps

        # ── Mettre à jour les propriétés de progression ──────────────────
        rp.is_running = True
        rp.progress_current = 0
        rp.progress_total = total_renders
        rp.current_object_name = ""

        # ── Sauvegarder le type d'affichage du rendu ─────────────────────
        self._orig_display_type = bpy.context.preferences.view.render_display_type

        # ── Lancer le modal avec un timer ────────────────────────────────
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    # ── Modal → traite un objet par tick, gère ESC ─────────────────────
    def modal(self, context, event):
        scene = context.scene
        rp = scene.batch_render_props

        # ── Annulation par ESC ───────────────────────────────────────────
        if event.type == 'ESC':
            self._finish(context, cancelled=True)
            return {"CANCELLED"}

        # ── Timer tick → rendre le prochain objet/angle ──────────────────
        if event.type == 'TIMER':
            if self._current_index >= len(self._batch_objects):
                self._finish(context, cancelled=False)
                return {"FINISHED"}

            obj = self._batch_objects[self._current_index]
            total_objs = len(self._batch_objects)
            obj_i = self._current_index + 1
            orbit_step = self._current_orbit_step
            num_angles = len(self._orbit_angles)
            render_num = self._current_index * num_angles + orbit_step + 1
            total_renders = rp.progress_total

            # Mettre à jour la progression dans les props (pour l'UI)
            rp.progress_current = render_num
            if num_angles > 1:
                angle_deg = int(math.degrees(self._orbit_angles[orbit_step]))
                rp.current_object_name = f"{obj.name} ({angle_deg}°)"
            else:
                rp.current_object_name = obj.name

            # Mettre à jour le header de la fenêtre
            context.area.header_text_set(
                f"Batch Render [{render_num}/{total_renders}] — « {rp.current_object_name} »  |  ESC pour annuler"
            )

            print(f"\n[{render_num}/{total_renders}] Rendu de « {rp.current_object_name} »...")

            # Isoler : cacher tous les autres objets du batch
            for other in self._batch_objects:
                other.hide_render = (other is not obj)

            # ── Appliquer la rotation d'orbite au modèle ───────────────────
            orbit_angle = self._orbit_angles[orbit_step]
            # Toujours repartir de la rotation originale
            orig_rot = self._orig_rotations[obj.name]
            new_rot = orig_rot.copy()
            if orbit_angle != 0.0:
                # Appliquer la rotation selon l'axe choisi
                if rp.orbit_rotation_axis == 'X':
                    new_rot.x += orbit_angle
                elif rp.orbit_rotation_axis == 'Y':
                    new_rot.y += orbit_angle
                elif rp.orbit_rotation_axis == 'Z':
                    new_rot.z += orbit_angle
            obj.rotation_euler = new_rot

            # Forcer la mise à jour de matrix_world avant _get_bbox_info
            # (sans cela, matrix_world est périmé → bounding box fausse → caméra décalée
            # → images vides, surtout pour les modèles avec Z important comme P10/P15)
            bpy.context.view_layer.update()

            # ── Positionner caméra et lumières (sans orbite) ────────────────
            bbox_center, bbox_size = self._get_bbox_info(obj)

            # La caméra ne bouge plus — elle est fixe
            self._position_camera(self._cam_obj, bbox_center, bbox_size, rp, orbit_angle=0.0)
            self._position_lights(self._lights, bbox_center, bbox_size, rp, orbit_angle=0.0)

            # ── Auto-scale énergie lumineuse selon la taille du modèle ──────
            if rp.auto_scale_energy and rp.reference_model_dim > 0:
                max_dim = max(bbox_size.x, bbox_size.y, bbox_size.z)
                scale = (max_dim / rp.reference_model_dim) ** rp.energy_scale_exponent
                for i, (lobj, ldata) in enumerate(self._lights):
                    if i == 0:
                        ldata.energy = rp.light_energy * scale
                    elif i == 1:
                        ldata.energy = rp.light_energy * 0.3 * scale
                    elif i == 2:
                        ldata.energy = rp.light_energy * 0.6 * scale

            # Positionner le shadow catcher plane si actif
            # On travaille en espace LOCAL du modèle pour que shadow_plane_offset
            # soit toujours exact (la bbox monde grossit diagonalement lors des
            # rotations et fausse le calcul du bas).
            # Le plan reçoit la même rotation que le modèle (parallèle à sa base).
            if self._shadow_plane:
                _lc = [Vector(c) for c in obj.bound_box]
                _lxs = [v.x for v in _lc]; _lys = [v.y for v in _lc]; _lzs = [v.z for v in _lc]
                _local_cx = (min(_lxs) + max(_lxs)) / 2
                _local_cy = (min(_lys) + max(_lys)) / 2
                _local_min_z = min(_lzs)
                _local_max_dim = max(max(_lxs) - min(_lxs), max(_lys) - min(_lys), max(_lzs) - min(_lzs))
                # Point bas-centre en local → transformé en monde (rotation + échelle incluses)
                _local_pt = Vector((_local_cx, _local_cy, _local_min_z + rp.shadow_plane_offset))
                _world_pt = obj.matrix_world @ _local_pt
                plane_scale = _local_max_dim * rp.shadow_plane_size
                self._shadow_plane.location = _world_pt
                self._shadow_plane.scale = (plane_scale, plane_scale, 1.0)
                self._shadow_plane.rotation_euler = obj.rotation_euler.copy()

            # Chemin de sortie
            ext = self._FORMAT_EXT.get(rp.output_format, '.png')
            safe_name = obj.name.replace("/", "_").replace("\\", "_")
            if num_angles > 1:
                angle_deg = int(math.degrees(self._orbit_angles[orbit_step]))
                sign = "n" if angle_deg < 0 else "p" if angle_deg > 0 else ""
                scene.render.filepath = os.path.join(
                    self._output_dir, f"{safe_name}_{sign}{abs(angle_deg)}deg{ext}"
                )
            else:
                scene.render.filepath = os.path.join(self._output_dir, f"{safe_name}{ext}")

            # Rendu avec estimation de progression
            try:
                # Appliquer le type d'affichage selon la préférence
                bpy.context.preferences.view.render_display_type = (
                    'WINDOW' if rp.show_render_preview else 'NONE'
                )
                
                self._render_start_time = time.time()
                print(f"    🎬 Cycles rendering ({rp.render_samples} samples)...")
                
                bpy.ops.render.render(write_still=True)
                
                _elapsed = time.time() - self._render_start_time
                self._render_times.append(_elapsed)
                rp.last_render_time_per_image = sum(self._render_times) / len(self._render_times)
                
                # Calculer stats
                samples_per_sec = rp.render_samples / _elapsed if _elapsed > 0 else 0
                print(f"  ✅ Sauvegardé : {scene.render.filepath}")
                print(f"     ⏱️  {_elapsed:.1f}s ({samples_per_sec:.1f} samples/s)")
                self._rendered += 1
                
            except Exception as e:
                print(f"  ❌ Erreur : {e}")
                self.report({"WARNING"}, f"Échec du rendu pour {obj.name}: {e}")

            # Avancer : prochain angle d'orbite ou prochain objet
            self._current_orbit_step += 1
            if self._current_orbit_step >= len(self._orbit_angles):
                self._current_orbit_step = 0
                self._current_index += 1

            # Forcer le rafraîchissement de l'interface
            for area in context.screen.areas:
                area.tag_redraw()

        return {"RUNNING_MODAL"}

    # ── Fin (normale ou annulation) ─────────────────────────────────────
    def _finish(self, context, cancelled=False):
        scene = context.scene
        rp = scene.batch_render_props

        # Arrêter le timer
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None

        # Restaurer la visibilité de TOUS les objets batch
        for obj in self._all_batch_objects:
            if obj.name in self._orig_hide_render:
                obj.hide_render = self._orig_hide_render[obj.name]

        # Restaurer l'état d'exclusion des collections Batch_3D_* dans le view layer
        if hasattr(self, '_orig_collection_exclude'):
            for layer_coll in context.view_layer.layer_collection.children:
                if layer_coll.name in self._orig_collection_exclude:
                    layer_coll.exclude = self._orig_collection_exclude[layer_coll.name]

        # Restaurer les rotations des modèles
        if self._orig_rotations:
            for obj in self._all_batch_objects:
                orig_rot = self._orig_rotations.get(obj.name)
                if orig_rot:
                    obj.rotation_euler = orig_rot
        if self._shadow_plane and self._orig_shadow_rotation:
            self._shadow_plane.rotation_euler = self._orig_shadow_rotation

        # Supprimer caméra et lumières temporaires
        if self._cam_obj:
            bpy.data.objects.remove(self._cam_obj, do_unlink=True)
        if self._cam_data:
            bpy.data.cameras.remove(self._cam_data)
        for lobj, ldata in self._lights:
            bpy.data.objects.remove(lobj, do_unlink=True)
            bpy.data.lights.remove(ldata)

        # Supprimer le shadow catcher plane
        if self._shadow_plane:
            bpy.data.objects.remove(self._shadow_plane, do_unlink=True)
        if self._shadow_plane_data:
            bpy.data.meshes.remove(self._shadow_plane_data)

        # Restaurer le world si modifié
        if rp.use_hdri and rp.hdri_path and self._orig_world:
            scene.world = self._orig_world

        # Restaurer le type d'affichage du rendu
        if self._orig_display_type is not None:
            bpy.context.preferences.view.render_display_type = self._orig_display_type

        # Restaurer l'état de rendu original
        if self._orig:
            self._restore_render_state(scene, self._orig)

        # Restaurer le header
        context.area.header_text_set(None)

        # Remettre l'état de progression
        rp.is_running = False
        rp.current_object_name = ""

        total = len(self._batch_objects)
        if cancelled:
            print(f"\n{'='*60}")
            print(f"⛔ Batch Render annulé après {self._rendered}/{total} images")
            print(f"{'='*60}\n")
            self.report({"WARNING"}, f"Batch Render annulé — {self._rendered}/{total} images rendues dans {self._output_dir}")
        else:
            print(f"\n{'='*60}")
            print(f"✅ Batch Render terminé : {self._rendered}/{total} images générées")
            print(f"{'='*60}\n")
            self.report({"INFO"}, f"Batch Render terminé : {self._rendered} images dans {self._output_dir}")

        # Forcer le rafraîchissement de l'UI
        for area in context.screen.areas:
            area.tag_redraw()

    # ── Helpers privés ──────────────────────────────────────────────────

    def _save_render_state(self, scene):
        """Sauvegarde les paramètres de rendu actuels"""
        return {
            'engine': scene.render.engine,
            'samples': scene.cycles.samples if hasattr(scene.cycles, 'samples') else 128,
            'use_denoising': scene.cycles.use_denoising if hasattr(scene.cycles, 'use_denoising') else True,
            'resolution_x': scene.render.resolution_x,
            'resolution_y': scene.render.resolution_y,
            'file_format': scene.render.image_settings.file_format,
            'color_mode': scene.render.image_settings.color_mode,
            'filepath': scene.render.filepath,
            'camera': scene.camera,
            'film_transparent': scene.render.film_transparent,
        }

    def _restore_render_state(self, scene, orig):
        """Restaure les paramètres de rendu originaux"""
        scene.render.engine = orig['engine']
        if orig['engine'] == 'CYCLES' or scene.render.engine == 'CYCLES':
            scene.cycles.samples = orig['samples']
            scene.cycles.use_denoising = orig['use_denoising']
        scene.render.resolution_x = orig['resolution_x']
        scene.render.resolution_y = orig['resolution_y']
        scene.render.image_settings.file_format = orig['file_format']
        scene.render.image_settings.color_mode = orig['color_mode']
        scene.render.filepath = orig['filepath']
        scene.camera = orig['camera']
        scene.render.film_transparent = orig['film_transparent']

    def _get_bbox_info(self, obj):
        """Retourne le centre et la taille de la bounding box en coordonnées monde"""
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        xs = [v.x for v in bbox_corners]
        ys = [v.y for v in bbox_corners]
        zs = [v.z for v in bbox_corners]
        min_corner = Vector((min(xs), min(ys), min(zs)))
        max_corner = Vector((max(xs), max(ys), max(zs)))
        center = (min_corner + max_corner) / 2
        size = max_corner - min_corner
        return center, size

    def _position_camera(self, cam_obj, target_center, target_size, rp, orbit_angle=0.0):
        """Positionne la caméra en coordonnées sphériques autour de l'objet,
        puis applique une rotation autour de l'axe choisi pour les vues multi-angles.

        orbit_angle : angle en radians de rotation
        rp.orbit_rotation_axis : 'X', 'Y' ou 'Z' (axe de rotation)
        """
        max_dim = max(target_size.x, target_size.y, target_size.z)
        fov = cam_obj.data.angle
        frame_distance = (max_dim / 2) / math.tan(fov / 2) if fov > 0 else max_dim * 2
        distance = frame_distance * 1.4 + rp.camera_distance

        elev = rp.camera_elevation
        azim = rp.camera_azimuth

        # Position de base (coordonnées sphériques)
        offset_x = distance * math.cos(elev) * math.cos(azim)
        offset_y = distance * math.cos(elev) * math.sin(azim)
        offset_z = distance * math.sin(elev)

        # Rotation de l'offset autour de l'axe choisi
        if orbit_angle != 0.0:
            cos_a = math.cos(orbit_angle)
            sin_a = math.sin(orbit_angle)

            if rp.orbit_rotation_axis == 'X':
                # Rotation autour de X : new_y = y·cos(θ) - z·sin(θ)
                #                        new_z = y·sin(θ) + z·cos(θ)
                new_y = offset_y * cos_a - offset_z * sin_a
                new_z = offset_y * sin_a + offset_z * cos_a
                offset_y = new_y
                offset_z = new_z
            elif rp.orbit_rotation_axis == 'Y':
                # Rotation autour de Y : new_x = x·cos(θ) + z·sin(θ)
                #                        new_z = -x·sin(θ) + z·cos(θ)
                new_x = offset_x * cos_a + offset_z * sin_a
                new_z = -offset_x * sin_a + offset_z * cos_a
                offset_x = new_x
                offset_z = new_z
            elif rp.orbit_rotation_axis == 'Z':
                # Rotation autour de Z : new_x = x·cos(θ) - y·sin(θ)
                #                        new_y = x·sin(θ) + y·cos(θ)
                new_x = offset_x * cos_a - offset_y * sin_a
                new_y = offset_x * sin_a + offset_y * cos_a
                offset_x = new_x
                offset_y = new_y

        cam_obj.location = Vector((
            target_center.x + offset_x,
            target_center.y + offset_y,
            target_center.z + offset_z,
        ))

        direction = target_center - cam_obj.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        cam_obj.rotation_euler = rot_quat.to_euler()

    def _create_lights(self, scene, rp):
        """Crée les lumières temporaires et retourne une liste de (object, data)"""
        lights = []

        key_data = bpy.data.lights.new("_BatchRender_Key", 'AREA')
        key_data.energy = rp.light_energy
        key_data.size = 2.0
        key_obj = bpy.data.objects.new("_BatchRender_Key", key_data)
        scene.collection.objects.link(key_obj)
        lights.append((key_obj, key_data))

        if rp.use_three_point:
            fill_data = bpy.data.lights.new("_BatchRender_Fill", 'AREA')
            fill_data.energy = rp.light_energy * 0.3
            fill_data.size = 3.0
            fill_obj = bpy.data.objects.new("_BatchRender_Fill", fill_data)
            scene.collection.objects.link(fill_obj)
            lights.append((fill_obj, fill_data))

            rim_data = bpy.data.lights.new("_BatchRender_Rim", 'AREA')
            rim_data.energy = rp.light_energy * 0.6
            rim_data.size = 1.5
            rim_obj = bpy.data.objects.new("_BatchRender_Rim", rim_data)
            scene.collection.objects.link(rim_obj)
            lights.append((rim_obj, rim_data))

        return lights

    def _position_lights(self, lights, bbox_center, bbox_size, rp, orbit_angle=0.0):
        """Positionne les lumières autour de l'objet, avec rotation si multi-angles"""
        max_dim = max(bbox_size.x, bbox_size.y, bbox_size.z)
        dist = max_dim * 2.5
        azim = rp.camera_azimuth

        cos_a = math.cos(orbit_angle) if orbit_angle != 0.0 else 1.0
        sin_a = math.sin(orbit_angle) if orbit_angle != 0.0 else 0.0

        for idx, (lobj, _) in enumerate(lights):
            if idx == 0:
                key_azim = azim + math.radians(30)
                offset_x = dist * math.cos(key_azim)
                offset_y = dist * math.sin(key_azim)
                offset_z = dist * 0.8
            elif idx == 1:
                fill_azim = azim - math.radians(60)
                offset_x = dist * 0.8 * math.cos(fill_azim)
                offset_y = dist * 0.8 * math.sin(fill_azim)
                offset_z = dist * 0.3
            elif idx == 2:
                rim_azim = azim + math.radians(180)
                offset_x = dist * 0.6 * math.cos(rim_azim)
                offset_y = dist * 0.6 * math.sin(rim_azim)
                offset_z = dist * 0.6
            else:
                continue

            # Rotation autour de l'axe choisi
            if orbit_angle != 0.0:
                if rp.orbit_rotation_axis == 'X':
                    new_y = offset_y * cos_a - offset_z * sin_a
                    new_z = offset_y * sin_a + offset_z * cos_a
                    offset_y = new_y
                    offset_z = new_z
                elif rp.orbit_rotation_axis == 'Y':
                    new_x = offset_x * cos_a + offset_z * sin_a
                    new_z = -offset_x * sin_a + offset_z * cos_a
                    offset_x = new_x
                    offset_z = new_z
                elif rp.orbit_rotation_axis == 'Z':
                    new_x = offset_x * cos_a - offset_y * sin_a
                    new_y = offset_x * sin_a + offset_y * cos_a
                    offset_x = new_x
                    offset_y = new_y

            lobj.location = Vector((
                bbox_center.x + offset_x,
                bbox_center.y + offset_y,
                bbox_center.z + offset_z,
            ))

            direction = bbox_center - lobj.location
            rot_quat = direction.to_track_quat('-Z', 'Y')
            lobj.rotation_euler = rot_quat.to_euler()

    def _setup_hdri(self, scene, hdri_path, strength):
        """Configure un éclairage HDRI dans un nouveau World temporaire"""
        hdri_full_path = bpy.path.abspath(hdri_path)
        if not os.path.exists(hdri_full_path):
            print(f"  ⚠️ HDRI introuvable : {hdri_full_path}")
            return

        world = bpy.data.worlds.new("_BatchRender_World")
        scene.world = world
        world.use_nodes = True

        nodes = world.node_tree.nodes
        links = world.node_tree.links
        nodes.clear()

        node_output = nodes.new(type='ShaderNodeOutputWorld')
        node_output.location = (400, 0)

        node_bg = nodes.new(type='ShaderNodeBackground')
        node_bg.location = (200, 0)
        node_bg.inputs['Strength'].default_value = strength

        node_env = nodes.new(type='ShaderNodeTexEnvironment')
        node_env.location = (0, 0)
        node_env.image = bpy.data.images.load(hdri_full_path)

        links.new(node_env.outputs['Color'], node_bg.inputs['Color'])
        links.new(node_bg.outputs['Background'], node_output.inputs['Surface'])
        print(f"  ✅ HDRI chargé : {hdri_path}")


class BatchRenderPreview(bpy.types.Operator):
    """Place une caméra et des lumières de preview sur le premier objet du batch,
    puis bascule en vue caméra avec le shading Material Preview pour
    visualiser le cadrage et l'éclairage sans lancer de rendu complet"""
    bl_idname = "render.batch_render_preview"
    bl_label = "Preview Batch Render"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        rp = context.scene.batch_render_props
        if rp.is_running:
            return False
        return any(c.name.startswith("Batch_3D_") for c in bpy.data.collections)

    def execute(self, context):
        scene = context.scene
        rp = scene.batch_render_props

        # Nettoyer un éventuel preview précédent
        # (restaure les rotations originales depuis preview_orig_rotations_json)
        self._cleanup_preview(context)

        # Collecter et trier les objets mesh du batch
        # Tri identique au batch render : collections par nom, puis objets par nom
        batch_objs = []
        for collection in sorted(bpy.data.collections, key=lambda c: c.name):
            if collection.name.startswith("Batch_3D_"):
                for obj in sorted(collection.objects, key=_batch_sort_key):
                    if obj.type == 'MESH':
                        batch_objs.append(obj)

        if not batch_objs:
            self.report({"WARNING"}, "Aucun objet trouvé dans les collections Batch_3D_*")
            return {"CANCELLED"}

        # Sélectionner le modèle cible via l'index (navigation)
        n = len(batch_objs)
        rp.preview_object_index = rp.preview_object_index % n
        idx = rp.preview_object_index
        target_obj = batch_objs[idx]

        # ── Isoler le modèle cible : masquer tous les autres dans le viewport ─
        for obj in batch_objs:
            obj.hide_viewport = (obj is not target_obj)

        # ── Sauvegarder les rotations originales dans le JSON persistant ────────
        # Utiliser une StringProperty (pas un attribut Python dynamique) pour que
        # la sauvegarde survive aux undo-steps Blender (qui recrée le wrapper Python
        # du PropertyGroup et efface les attributs dynamiques → accumulation sinon).
        import json as _json
        orig_rots_dict = {
            obj.name: {"rot": list(obj.rotation_euler), "order": obj.rotation_mode}
            for obj in batch_objs
        }
        rp.preview_orig_rotations_json = _json.dumps(orig_rots_dict)

        # ── Appliquer l'angle d'orbite (ABSOLU depuis les originaux JSON) ────────
        orbit_angle = math.radians(rp.preview_orbit_angle)
        if orbit_angle != 0.0:
            rot_data = orig_rots_dict[target_obj.name]
            from mathutils import Euler as _Euler
            orig_rot = _Euler(rot_data["rot"], rot_data["order"])
            new_rot = orig_rot.copy()
            if rp.orbit_rotation_axis == 'X':
                new_rot.x += orbit_angle
            elif rp.orbit_rotation_axis == 'Y':
                new_rot.y += orbit_angle
            elif rp.orbit_rotation_axis == 'Z':
                new_rot.z += orbit_angle
            target_obj.rotation_euler = new_rot

        # ── Forcer la mise à jour de matrix_world (même précaution que le batch render)
        # Sans cela, _get_bbox_info lit une matrix_world périmée → caméra, lumières
        # et shadow plane décalés par rapport au modèle tourné.
        bpy.context.view_layer.update()

        # ── Créer la caméra preview ──────────────────────────────────────
        cam_data = bpy.data.cameras.new("_BatchPreview_Cam")
        cam_data.lens = rp.camera_focal_length
        cam_data.display_size = 0.5
        cam_data.show_limits = True
        cam_obj = bpy.data.objects.new("_BatchPreview_Cam", cam_data)
        scene.collection.objects.link(cam_obj)
        scene.camera = cam_obj

        # ── Positionner la caméra sur le modèle cible ────────────────────
        bbox_center, bbox_size = BatchRender._get_bbox_info(None, target_obj)
        BatchRender._position_camera(None, cam_obj, bbox_center, bbox_size, rp, orbit_angle=0.0)

        # ── Calculer l'énergie lumineuse (avec auto-scale selon taille) ──
        actual_energy = rp.light_energy
        if rp.auto_scale_energy and rp.reference_model_dim > 0:
            max_dim = max(bbox_size.x, bbox_size.y, bbox_size.z)
            scale = (max_dim / rp.reference_model_dim) ** rp.energy_scale_exponent
            actual_energy = rp.light_energy * scale

        # ── Créer les lumières preview ───────────────────────────────────
        lights_created = []

        key_data = bpy.data.lights.new("_BatchPreview_Key", 'AREA')
        key_data.energy = actual_energy
        key_data.size = 2.0
        key_obj = bpy.data.objects.new("_BatchPreview_Key", key_data)
        scene.collection.objects.link(key_obj)
        lights_created.append((key_obj, key_data))

        if rp.use_three_point:
            fill_data = bpy.data.lights.new("_BatchPreview_Fill", 'AREA')
            fill_data.energy = actual_energy * 0.3
            fill_data.size = 3.0
            fill_obj = bpy.data.objects.new("_BatchPreview_Fill", fill_data)
            scene.collection.objects.link(fill_obj)
            lights_created.append((fill_obj, fill_data))

            rim_data = bpy.data.lights.new("_BatchPreview_Rim", 'AREA')
            rim_data.energy = actual_energy * 0.6
            rim_data.size = 1.5
            rim_obj = bpy.data.objects.new("_BatchPreview_Rim", rim_data)
            scene.collection.objects.link(rim_obj)
            lights_created.append((rim_obj, rim_data))

        # Positionner les lumières (fixes, les modèles tournent)
        BatchRender._position_lights(None, lights_created, bbox_center, bbox_size, rp, orbit_angle=0.0)

        # ── Créer le shadow catcher plane si activé ──────────────────────
        if rp.use_shadow_catcher:
            import bmesh as _bm
            plane_data = bpy.data.meshes.new("_BatchPreview_ShadowPlane")
            tmp = _bm.new()
            _bm.ops.create_grid(tmp, x_segments=1, y_segments=1, size=1.0)
            tmp.to_mesh(plane_data)
            tmp.free()
            plane_obj = bpy.data.objects.new("_BatchPreview_ShadowPlane", plane_data)
            scene.collection.objects.link(plane_obj)
            plane_obj.is_shadow_catcher = True
            plane_obj.display_type = 'WIRE'
            # Calcul en espace LOCAL du modèle → shadow_plane_offset toujours exact,
            # indépendamment de la rotation (la bbox monde grossit diagonalement).
            # Le plan reçoit la même rotation que le modèle (parallèle à sa base).
            _lc = [Vector(c) for c in target_obj.bound_box]
            _lxs = [v.x for v in _lc]; _lys = [v.y for v in _lc]; _lzs = [v.z for v in _lc]
            _local_cx = (min(_lxs) + max(_lxs)) / 2
            _local_cy = (min(_lys) + max(_lys)) / 2
            _local_min_z = min(_lzs)
            _local_max_dim = max(max(_lxs) - min(_lxs), max(_lys) - min(_lys), max(_lzs) - min(_lzs))
            _local_pt = Vector((_local_cx, _local_cy, _local_min_z + rp.shadow_plane_offset))
            _world_pt = target_obj.matrix_world @ _local_pt
            plane_scale = _local_max_dim * rp.shadow_plane_size
            plane_obj.location = _world_pt
            plane_obj.scale = (plane_scale, plane_scale, 1.0)
            plane_obj.rotation_euler = target_obj.rotation_euler.copy()

        # ── Basculer en vue caméra + Material Preview ────────────────────
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.region_3d.view_perspective = 'CAMERA'
                        space.shading.type = 'MATERIAL'
                        break
                break

        # ── Mettre à jour l'info du modèle courant ───────────────────────
        sx = bbox_size.x * 1000
        sy = bbox_size.y * 1000
        sz = bbox_size.z * 1000
        energy_info = f"  | énergie ×{(actual_energy / max(rp.light_energy, 0.001)):.2f}" if rp.auto_scale_energy else ""
        rp.preview_current_info = f"{target_obj.name}  ({sx:.0f}×{sy:.0f}×{sz:.0f} mm){energy_info}"

        # ── Synchroniser preview_flat_index avec la position courante ────
        # (permet à la navigation de repartir du bon endroit après un preview manuel)
        _adeg = []
        if rp.orbit_angle_neg90: _adeg.append(-90)
        if rp.orbit_angle_neg60: _adeg.append(-60)
        if rp.orbit_angle_neg45: _adeg.append(-45)
        if rp.orbit_angle_neg30: _adeg.append(-30)
        if rp.orbit_angle_0:     _adeg.append(0)
        if rp.orbit_angle_30:    _adeg.append(30)
        if rp.orbit_angle_45:    _adeg.append(45)
        if rp.orbit_angle_60:    _adeg.append(60)
        if rp.orbit_angle_90:    _adeg.append(90)
        if not _adeg: _adeg = [0]
        _aidx = _adeg.index(rp.preview_orbit_angle) if rp.preview_orbit_angle in _adeg else 0
        rp.preview_flat_index = idx * len(_adeg) + _aidx

        rp.is_preview_active = True
        self.report({"INFO"}, f"Preview {idx + 1}/{n} — « {target_obj.name} »  ({sx:.0f}×{sy:.0f}×{sz:.0f} mm)")
        return {"FINISHED"}

    @staticmethod
    def _cleanup_preview(context):
        """Supprime tous les objets de preview _BatchPreview_* et restaure l'état original.

        La restauration des rotations utilise preview_orig_rotations_json (StringProperty
        persistante) plutôt que des attributs Python dynamiques, qui seraient perdus
        lors des undo-steps Blender (le wrapper Python du PropertyGroup est recréé).
        """
        scene = context.scene
        rp = scene.batch_render_props

        # Restaurer les rotations originales depuis le JSON persistant
        if rp.preview_orig_rotations_json:
            try:
                import json as _json
                from mathutils import Euler as _Euler
                orig_rots = _json.loads(rp.preview_orig_rotations_json)
                for name, rot_data in orig_rots.items():
                    obj = bpy.data.objects.get(name)
                    if obj:
                        obj.rotation_euler = _Euler(rot_data["rot"], rot_data["order"])
            except Exception as e:
                print(f"[BatchPreview] Erreur restauration rotations : {e}")
            rp.preview_orig_rotations_json = ""

        # Rétablir la visibilité de tous les objets batch
        # (on les montre tous — ils sont tous visibles par défaut dans les collections Batch_3D_*)
        for collection in bpy.data.collections:
            if collection.name.startswith("Batch_3D_"):
                for obj in collection.objects:
                    if obj.type == 'MESH':
                        obj.hide_viewport = False

        # Supprimer les objets preview
        to_remove = [obj for obj in bpy.data.objects if obj.name.startswith("_BatchPreview_")]
        for obj in to_remove:
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            # Supprimer la donnée associée (caméra, lumière ou mesh)
            if data:
                if isinstance(data, bpy.types.Camera):
                    bpy.data.cameras.remove(data)
                elif isinstance(data, bpy.types.Light):
                    bpy.data.lights.remove(data)
                elif isinstance(data, bpy.types.Mesh):
                    bpy.data.meshes.remove(data)

        rp.is_preview_active = False


class BatchRenderCleanPreview(bpy.types.Operator):
    """Supprime la caméra et les lumières de preview du batch render"""
    bl_idname = "render.batch_render_clean_preview"
    bl_label = "Supprimer Preview"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.batch_render_props.is_preview_active

    def execute(self, context):
        BatchRenderPreview._cleanup_preview(context)

        # Remettre l'angle de preview à 0 pour repartir de la rotation initiale
        context.scene.batch_render_props.preview_orbit_angle = 0

        # Revenir en vue perspective
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.region_3d.view_perspective = 'PERSP'
                        space.shading.type = 'SOLID'
                        break
                break

        self.report({"INFO"}, "Preview nettoyé")
        return {"FINISHED"}


class BatchRenderPreviewResetAngle(bpy.types.Operator):
    """Réinitialise l'angle de preview à 0° et restaure la rotation d'origine"""
    bl_idname = "render.batch_render_preview_reset_angle"
    bl_label = "Reset angle preview"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # Bouton actif même hors preview pour remettre le slider à 0
        return True

    def execute(self, context):
        scene = context.scene
        rp = scene.batch_render_props

        # Remettre le slider à 0
        rp.preview_orbit_angle = 0

        # Restaurer les rotations originales depuis le JSON persistant
        if rp.preview_orig_rotations_json:
            try:
                import json as _json
                from mathutils import Euler as _Euler
                orig_rots = _json.loads(rp.preview_orig_rotations_json)
                for name, rot_data in orig_rots.items():
                    obj = bpy.data.objects.get(name)
                    if obj:
                        obj.rotation_euler = _Euler(rot_data["rot"], rot_data["order"])
            except Exception as e:
                print(f"[BatchPreview] Erreur restauration rotations (reset) : {e}")

        # Rafraîchir la vue 3D
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({"INFO"}, "Angle preview remis à 0°")
        return {"FINISHED"}


class BatchRenderPreviewNavigate(bpy.types.Operator):
    """Navigue vers le modèle suivant ou précédent dans le preview"""
    bl_idname = "render.batch_render_preview_navigate"
    bl_label = "Naviguer preview"
    bl_options = {"REGISTER", "UNDO"}

    direction: bpy.props.EnumProperty(
        name="Direction",
        items=[
            ('NEXT', "Suivant", "Passer au modèle suivant", 'TRIA_RIGHT', 0),
            ('PREV', "Précédent", "Revenir au modèle précédent", 'TRIA_LEFT', 1),
        ],
        default='NEXT',
    )

    @classmethod
    def poll(cls, context):
        return context.scene.batch_render_props.is_preview_active

    def execute(self, context):
        rp = context.scene.batch_render_props

        # Objets batch (même ordre que le batch render)
        batch_objs = [
            obj
            for collection in sorted(bpy.data.collections, key=lambda c: c.name)
            if collection.name.startswith("Batch_3D_")
            for obj in sorted(collection.objects, key=_batch_sort_key)
            if obj.type == 'MESH'
        ]

        if not batch_objs:
            return {"CANCELLED"}

        # Angles d'orbite actifs (même ordre que le batch render)
        orbit_angles_deg = []
        if rp.orbit_angle_neg90: orbit_angles_deg.append(-90)
        if rp.orbit_angle_neg60: orbit_angles_deg.append(-60)
        if rp.orbit_angle_neg45: orbit_angles_deg.append(-45)
        if rp.orbit_angle_neg30: orbit_angles_deg.append(-30)
        if rp.orbit_angle_0:     orbit_angles_deg.append(0)
        if rp.orbit_angle_30:    orbit_angles_deg.append(30)
        if rp.orbit_angle_45:    orbit_angles_deg.append(45)
        if rp.orbit_angle_60:    orbit_angles_deg.append(60)
        if rp.orbit_angle_90:    orbit_angles_deg.append(90)
        if not orbit_angles_deg:
            orbit_angles_deg = [0]

        n_models = len(batch_objs)
        n_angles = len(orbit_angles_deg)
        total = n_models * n_angles

        if self.direction == 'NEXT':
            rp.preview_flat_index = (rp.preview_flat_index + 1) % total
        else:
            rp.preview_flat_index = (rp.preview_flat_index - 1) % total

        # Dériver index modèle et angle depuis le flat index (même séquence que le batch render)
        rp.preview_object_index = rp.preview_flat_index // n_angles
        rp.preview_orbit_angle  = orbit_angles_deg[rp.preview_flat_index % n_angles]

        return bpy.ops.render.batch_render_preview('EXEC_DEFAULT')


classes = [
    AddCadreMortaise,
    AddCadreTenon,
    AddCarreau,
    AddPeigneCourt,
    AddPeigneLong,
    AddCadreCentral,
    AddAccroche,
    AddCadreAvant,
    AddDiffuseur,
    AddAccrocheInverse,
    AddAbsorbeur,
    PrepareToCam,
    PickPosition,
    AddMoule,
    AddFondMoule,
    AddPilierMoule,
    AddContrePilierMoule,
    AddCadreMoule,
    AddCadreTissuCourt,
    AddCadreTissuLong,
    AddList,
    RemoveList,
    AddCadreMouleLong,
    AddColle,
    Add3DModel,
    SetArrayOffset,
    NoOverlap,
    SetRecommendedArray,
    UpdateAddonOperator,
    CheckUpdateOperator,
    AddonInfoOperator,
    GitDiagnosticOperator,
    PositionSelected,
    Batch3DGenerate,
    ClearBatch3D,
    AddBatchPreset,
    RemoveBatchPreset,
    LoadBatchPreset,
    SaveBatchPreset,
    BatchRender,
    BatchRenderPreview,
    BatchRenderCleanPreview,
    BatchRenderPreviewResetAngle,
    BatchRenderPreviewNavigate,
]


def register():
    print("🔧 [DEBUG] Enregistrement des opérateurs...")
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
            if "ContrePilier" in cls.__name__:
                print(f"✅ [DEBUG] Opérateur contre-pilier enregistré: {cls.__name__} -> {cls.bl_idname}")
        except Exception as e:
            print(f"❌ [DEBUG] Erreur enregistrement {cls.__name__}: {e}")
    register_keymaps()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    unregister_keymaps()