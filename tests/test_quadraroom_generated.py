"""Validation avec un véritable absorbeur : ~/.app/blender510/blender -b --factory-startup --python-exit-code 1 --python tests/test_quadraroom_generated.py"""

import sys
import tempfile
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props  # noqa: E402
from diffuseurcam.quadraroom_glb import read_glb  # noqa: E402


class GeneratedAbsorberTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        cls.operators = (ops.Add3DModel, ops.Batch3DGenerate, ops.ExportBatch3DQuadraRoomGLB)
        for operator in cls.operators:
            bpy.utils.register_class(operator)

    @classmethod
    def tearDownClass(cls):
        for collection in list(bpy.data.collections):
            if collection.name.startswith('Batch_3D_'):
                for obj in list(collection.objects):
                    bpy.data.objects.remove(obj, do_unlink=True)
                bpy.data.collections.remove(collection)
        for operator in reversed(cls.operators):
            bpy.utils.unregister_class(operator)
        props.unregister()

    def test_generated_absorber_has_two_materials_and_correct_axes(self):
        scene = bpy.context.scene
        batch = scene.batch_3d_props
        batch.batch_product_type = '3'
        batch.batch_profondeurs = '150'
        batch.batch_longueurs = '2'
        scene.dif_props.largeur_diffuseur = 0.6
        scene.dif_props.epaisseur = 0.015
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        product = next(obj for collection in scene.collection.children_recursive
                       if collection.name.startswith('Batch_3D_') for obj in collection.objects)
        source_materials = [material.name for material in product.data.materials]
        self.assertEqual(source_materials, ['wood', 'fabric'])
        fabric_faces = [face for face in product.data.polygons if face.material_index == 1]
        self.assertEqual(len(fabric_faces), 2)
        for face, expected_z, expected_normal in zip(
                sorted(fabric_faces, key=lambda face: face.center.z),
                (-0.075, 0.075), (-1.0, 1.0)):
            self.assertAlmostEqual(face.center.z, expected_z, places=5)
            self.assertAlmostEqual(face.normal.z, expected_normal, places=5)
            self.assertEqual(len(face.vertices), 4)

        with tempfile.TemporaryDirectory() as directory:
            batch.quadra_glb_directory = directory
            self.assertEqual(bpy.ops.mesh.export_batch_3d_quadraroom_glb(), {'FINISHED'})
            glb_path = Path(directory) / 'A0W60P15L2E15.glb'
            self.assertTrue(glb_path.exists())
            document, _ = read_glb(glb_path)
            self.assertFalse(document.get('images'))
            self.assertFalse(document.get('textures'))
            self.assertEqual({material['name'] for material in document['materials']},
                             {'wood', 'fabric'})
            self.assertEqual({document['materials'][primitive['material']]['name']
                              for primitive in document['meshes'][0]['primitives']},
                             {'wood', 'fabric'})
            positions = []
            for primitive in document['meshes'][0]['primitives']:
                self.assertIn('TEXCOORD_0', primitive['attributes'])
                self.assertIn('NORMAL', primitive['attributes'])
                positions.append(document['accessors'][primitive['attributes']['POSITION']])
            for axis, expected in enumerate((0.6, 1.2, 0.15)):
                self.assertAlmostEqual(min(item['min'][axis] for item in positions), -expected / 2, places=5)
                self.assertAlmostEqual(max(item['max'][axis] for item in positions), expected / 2, places=5)

            stl_path = Path(directory) / (product.name + '.stl')
            self.assertEqual(bpy.ops.wm.stl_export(
                filepath=str(stl_path), export_selected_objects=True,
                global_scale=1000.0, use_scene_unit=False,
                apply_modifiers=True, ascii_format=False, use_batch=False,
            ), {'FINISHED'})
            print(f"TAILLES : GLB QuadraRoom {glb_path.stat().st_size} octets ; "
                  f"STL {stl_path.stat().st_size} octets")
        self.assertEqual([material.name for material in product.data.materials], source_materials)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
