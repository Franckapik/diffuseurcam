"""À lancer avec Blender 5.1 : ~/.app/blender510/blender -b --factory-startup --python-exit-code 1 --python tests/test_quadraroom_glb.py"""

import tempfile
import sys
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props  # noqa: E402
from diffuseurcam.quadraroom_glb import product_stem, read_glb  # noqa: E402


class QuadraRoomGLBTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        bpy.utils.register_class(ops.ExportBatch3DQuadraRoomGLB)

    @classmethod
    def tearDownClass(cls):
        bpy.utils.unregister_class(ops.ExportBatch3DQuadraRoomGLB)
        props.unregister()

    def setUp(self):
        self.scene = bpy.context.scene
        self.scene.dif_props.epaisseur = 0.005

        self.collection = bpy.data.collections.new("Batch_3D_1x")
        self.scene.collection.children.link(self.collection)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(10, 0, 0))
        self.product = bpy.context.object
        self.product.name = "D1N7W50P5L1"
        self.product.scale = (0.6, 1.2, 0.15)
        for vertex in self.product.data.vertices:
            vertex.co.x += 1
            vertex.co.y += 2
            vertex.co.z += 3
        for collection in list(self.product.users_collection):
            collection.objects.unlink(self.product)
        self.collection.objects.link(self.product)
        self.source_materials = []
        for name in ("wood", "fabric"):
            material = bpy.data.materials.new(name)
            material.use_nodes = True
            self.product.data.materials.append(material)
            self.source_materials.append(material)
        for index, face in enumerate(self.product.data.polygons):
            face.material_index = 0 if index < 3 else 1
        self.assertTrue(self.product.data.uv_layers)

        # Un maillage auxiliaire dans la collection batch ne doit pas être exporté.
        bpy.ops.mesh.primitive_cube_add(location=(30, 0, 0))
        self.helper = bpy.context.object
        self.helper.name = "Helper"
        for collection in list(self.helper.users_collection):
            collection.objects.unlink(self.helper)
        self.collection.objects.link(self.helper)
        bpy.ops.mesh.primitive_cube_add(location=(40, 0, 0))
        self.unrelated = bpy.context.object

    def tearDown(self):
        bpy.data.collections.remove(self.collection)
        meshes = [obj.data for obj in (self.product, self.helper, self.unrelated)]
        for obj in (self.product, self.helper, self.unrelated):
            bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        for material in self.source_materials:
            if material.users == 0:
                bpy.data.materials.remove(material)

    def test_export_keeps_groups_uv_normals_and_axes_without_images(self):
        source_mesh = self.product.data
        source_materials = [material.name for material in source_mesh.materials]
        with tempfile.TemporaryDirectory() as directory:
            self.scene.batch_3d_props.quadra_glb_directory = directory
            self.assertEqual(bpy.ops.mesh.export_batch_3d_quadraroom_glb(), {'FINISHED'})
            files = list(Path(directory).glob('*.glb'))
            self.assertEqual([path.name for path in files], ["D1N7W50P5L1E5.glb"])
            document, _ = read_glb(files[0])
            self.assertFalse(document.get('images'))
            self.assertFalse(document.get('textures'))
            self.assertEqual({material['name'] for material in document['materials']},
                             {'wood', 'fabric'})
            counts = {}
            positions = []
            for primitive in document['meshes'][0]['primitives']:
                material = document['materials'][primitive['material']]['name']
                self.assertIn('TEXCOORD_0', primitive['attributes'])
                self.assertIn('NORMAL', primitive['attributes'])
                counts[material] = document['accessors'][primitive['indices']]['count']
                positions.append(document['accessors'][primitive['attributes']['POSITION']])
            self.assertEqual(counts, {'wood': 18, 'fabric': 18})
            node = next(node for node in document['nodes'] if 'mesh' in node)
            scale = node.get('scale', (1, 1, 1))
            translation = node.get('translation', (0, 0, 0))
            for axis, expected in enumerate((0.6, 1.2, 0.15)):
                bounds = [value * scale[axis] + translation[axis]
                          for accessor in positions
                          for value in (accessor['min'][axis], accessor['max'][axis])]
                lower, upper = min(bounds), max(bounds)
                self.assertAlmostEqual(lower, -expected / 2, places=5)
                self.assertAlmostEqual(upper, expected / 2, places=5)
            self.assertLess(files[0].stat().st_size, 50000)

        self.assertEqual(self.product.data.as_pointer(), source_mesh.as_pointer())
        self.assertEqual([material.name for material in source_mesh.materials], source_materials)
        self.assertEqual(self.product.location.x, 10)
        self.assertEqual(bpy.context.view_layer.objects.active, self.unrelated)
        self.assertEqual(set(bpy.context.selected_objects), {self.unrelated})

    def test_unknown_face_material_refuses_entire_export(self):
        self.product.data.materials[1].name = "Non associé"
        allowed = ops._QUADRAROOM_MATERIALS
        with self.assertRaisesRegex(ValueError, 'face 3.*Non associé'):
            ops._quadraroom_face_materials(self.product, allowed, bpy.context.evaluated_depsgraph_get())
        with tempfile.TemporaryDirectory() as directory:
            self.scene.batch_3d_props.quadra_glb_directory = directory
            with self.assertRaisesRegex(RuntimeError, 'Non associé'):
                bpy.ops.mesh.export_batch_3d_quadraroom_glb()
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_catalog_suffix_is_added_once(self):
        self.assertEqual(product_stem('D1N7W50P5L1', 0.005), 'D1N7W50P5L1E5')
        self.assertEqual(product_stem('D1N7W50P5L1E5', 0.005), 'D1N7W50P5L1E5')
        self.assertEqual(product_stem('D1N7W50P5L1E5.001', 0.005), 'D1N7W50P5L1E5')

    def test_only_direct_material_names_are_accepted(self):
        self.assertEqual(ops._QUADRAROOM_MATERIALS, {'wood', 'fabric'})

    def test_old_fallback_material_is_refused(self):
        self.product.data.materials[0].name = 'DIF_Cadre'
        with tempfile.TemporaryDirectory() as directory:
            self.scene.batch_3d_props.quadra_glb_directory = directory
            with self.assertRaisesRegex(RuntimeError, 'DIF_Cadre'):
                bpy.ops.mesh.export_batch_3d_quadraroom_glb()
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_duplicate_catalog_reference_refuses_export(self):
        duplicate = self.product.copy()
        self.collection.objects.link(duplicate)
        duplicate.name = 'D1N7W50P5L1E5'
        try:
            with tempfile.TemporaryDirectory() as directory:
                self.scene.batch_3d_props.quadra_glb_directory = directory
                with self.assertRaisesRegex(RuntimeError, 'Référence produit présente plusieurs fois'):
                    bpy.ops.mesh.export_batch_3d_quadraroom_glb()
                self.assertEqual(list(Path(directory).iterdir()), [])
        finally:
            bpy.data.objects.remove(duplicate, do_unlink=True)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
