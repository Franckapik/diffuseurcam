import bpy
import bmesh
from .shapes import *
from .difarray import difArray
from .bridges import place_empties_on_bounding_box
from .pack import place_selected_objects_no_overlap
from bpy_extras.object_utils import AddObjectHelper
from bpy.props import FloatVectorProperty, StringProperty, IntProperty
import math


class AddCadreMortaise(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.cadre_mortaise"
    bl_label = "Ajouter Cadre mortaise"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_cadre_mortaise(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_cadre_tenon(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_carreau(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_accroche(
            scene.dif_props, scene.product_props, scene.usinage_props, False
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
        vertex, edges, name = add_accroche(
            scene.dif_props, scene.product_props, scene.usinage_props, True
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
        vertex, edges, name = add_renfort_angle(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_peigne_court(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_renfort_central(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_peigne_long(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_fond_moule(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_cadre_moule(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_cadre_moule_long(
            scene.dif_props, scene.product_props, scene.usinage_props
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
        vertex, edges, name = add_colle(
            scene.dif_props, scene.product_props, scene.usinage_props, scene.array_props
        )


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

        for i in range(1 if difprops.moule_type == "1d" else difprops.type):
            y = i * difprops.getRang()
            for k in range(difprops.type):
                index = i * difprops.type + k
                x = k * difprops.getRang()
                z = depth[index]
                vertex, edges, name = add_carreau(
                    scene.dif_props, scene.product_props, scene.usinage_props
                )

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
            (difprops.getLargeurPilier() + arrayprops.array_offset)
            * (difprops.type + 1),
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
        vertex, edges, name = add_contre_pilier_moule(
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
            posprops.contre_pilier_moule_position[1],
            posprops.contre_pilier_moule_position[2],
            posprops.contre_pilier_moule_position[0],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.contre_pilier_moule_x,
            arrayprops.contre_pilier_moule_y,
            (difprops.getLargeurPilier() + arrayprops.array_offset)
            * (difprops.type + 1),
            difprops.longueur_diffuseur,  # calcul à faire sur l'addition des ratios
        )

        if posprops.contre_pilier_moule_rotation:
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
        if scene.product_props.product_type == "0" : 
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

        return {"FINISHED"}


class AddMoule(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.add_moule"
    bl_label = "Generer Moule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        AddCadreMoule.execute(self, context)
        AddFondMoule.execute(self, context)
        AddPilierMoule.execute(self, context)
        AddCadreMouleLong.execute(self, context)

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
        if scene.product_props.product_type == "0" : 
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

        if scene.product_props.product_type == "1" : 
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
                bpy.ops.object.curve_overcuts(
                    diameter=usinageprops.fraise, threshold=1.569
                )

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
    AddList,
    RemoveList,
    AddCadreMouleLong,
    AddColle,
    Add3DModel,
    SetArrayOffset,
    NoOverlap,
    SetRecommendedArray
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
