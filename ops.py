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
from mathutils import Vector


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
    bl_idname = "mesh.simulation"
    bl_label = "Ajouter Modele 3D"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props

        depth = difprops.getMotif("depth")
        print(depth)

        # Calculer le nombre de lignes en tenant compte de la longueur du diffuseur
        num_rows = 1 if difprops.moule_type == "1d" else round(difprops.type * difprops.longueur_diffuseur)
        
        for i in range(num_rows):
            y = i * difprops.getRang()
            for k in range(difprops.type):
                index = i * difprops.type + k
                x = k * difprops.getRang()
                z = depth[index]
                vertex, edges, name = add_carreau(scene.dif_props, scene.product_props, scene.usinage_props)

                # create a bmesh
                bm = bmesh.new()

                # Create new mesh data.
                mesh = bpy.data.meshes.new(name)
                mesh.from_pydata(vertex, edges, [])

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

                # Positionning according to position props
                mesh_obj.location = (x, y, z)

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

            for obj in [o for o in bpy.data.objects if "_cam" in o.name]:
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # apply modifier
                bpy.ops.object.convert(target="CURVE")
                bpy.ops.object.convert(target="MESH")

        # convert to curve
        if prepprops.isConvertToCurve_prepare:
            bpy.ops.object.convert(target="CURVE")

            # remove double if curve
            if prepprops.isCRemove_prepare:
                bpy.ops.object.curve_remove_doubles()

        # join selected object
        if prepprops.isJoin_prepare:
            bpy.ops.object.join()
            bpy.context.object.name = difprops.getDifName()
            if prepprops.isConvertToCurve_prepare and prepprops.isOvercuts:
                bpy.ops.object.curve_overcuts(diameter=usinageprops.fraise, threshold=1.569)

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