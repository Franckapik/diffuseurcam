import bpy
import bmesh
from .shapes import *
from .difarray import difArray
from bpy_extras.object_utils import AddObjectHelper
from bpy.props import FloatVectorProperty, StringProperty
import math


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

        # Convert BMesh to mesh data, then release BMesh.
        bm.to_mesh(mesh)
        bm.free()

        # Add Object to the default collection from mesh
        mesh_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(mesh_obj)

        bpy.types.Scene.dif_parts.append(mesh_obj.name)

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
            difprops.getRang() if scene.product_props.product_type == "0" else difprops.largeur_diffuseur * difprops.longueur_diffuseur ,
            
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
        vertex, edges, name = add_accroche(scene.dif_props, scene.product_props, scene.usinage_props)
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
        vertex, edges, name = add_accroche_inverse(scene.dif_props, scene.product_props, scene.usinage_props)
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
    bl_idname = "mesh.cadre_avant"
    bl_label = "Ajouter un cadre avant"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_cadre_avant(scene.dif_props, scene.product_props, scene.usinage_props)
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
            posprops.cadre_avant_position[0],
            posprops.cadre_avant_position[1],
            posprops.cadre_avant_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_avant_x,
            arrayprops.cadre_avant_y,
            difprops.getRang(),
            difprops.getRang(),
        )
        if posprops.cadre_avant_rotation:
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
    bl_idname = "mesh.cadre_central"
    bl_label = "Ajouter Cadre Central"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        vertex, edges, name = add_cadre_central(scene.dif_props, scene.product_props, scene.usinage_props)

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
            posprops.cadre_central_position[0],
            posprops.cadre_central_position[1],
            posprops.cadre_central_position[2],
        )

        difArray(
            mesh_obj,
            arrayprops.array_offset,
            arrayprops.cadre_central_x,
            arrayprops.cadre_central_y,
            difprops.profondeur,
            difprops.longueur_diffuseur,
        )

        if posprops.cadre_central_rotation:
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


class AddPilierMoule(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.pilier_moule"
    bl_label = "Ajouter Piliers Moule"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        vertex, edges, name = add_pilier_moule(scene.dif_props, scene.product_props, scene.usinage_props, scene.array_props)

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
            difprops.longueur_diffuseur, #calcul à faire sur l'addition des ratios
        )

        if posprops.pilier_moule_rotation:
            mesh_obj.rotation_euler = [0, 0, math.radians(90)]

        return {"FINISHED"}


class AddDiffuseur(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.add_diffuseur"
    bl_label = "Generer Diffuseur"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        AddCadreMortaise.execute(self, context)
        AddCadreTenon.execute(self, context)
        AddCarreau.execute(self, context)
        AddPeigneCourt.execute(self, context)
        AddPeigneLong.execute(self, context)
        AddAccroche.execute(self, context)

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

        # copy selected mesh
        if prepprops.isNewMesh_prepare:
            C = bpy.context
            old_select_objects = C.selected_objects
            for o in C.selected_objects:
                new_obj = o.copy()
                new_obj.name += "_cam"
                C.collection.objects.link(new_obj)

            bpy.ops.object.select_all(action="DESELECT")

            if prepprops.isDeleteOldMesh_prepare:
                for obj in old_select_objects:
                    obj.select_set(True)
                    bpy.ops.object.delete()

            for obj in [o for o in bpy.data.objects if "_cam" in o.name]:
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                bpy.ops.object.convert(target="MESH")  # apply modifier

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
            if prepprops.isOvercuts:
                bpy.ops.object.curve_overcuts(diameter=usinageprops.fraise,threshold=1.5708)


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
    AddCadreMoule,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
