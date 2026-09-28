"""À lancer avec : blender -b --factory-startup --python-exit-code 1 --python tests/test_batch_absorber.py"""

import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props  # noqa: E402


class BatchAbsorberTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        cls.operators = (
            ops.Add3DModel, ops.Batch3DGenerate, ops.AddBatchPreset,
            ops.LoadBatchPreset, ops.SaveBatchPreset, ops.ExportBatch3DGLB,
        )
        for operator in cls.operators:
            bpy.utils.register_class(operator)

    @classmethod
    def tearDownClass(cls):
        for operator in reversed(cls.operators):
            bpy.utils.unregister_class(operator)
        props.unregister()

    def setUp(self):
        self.scene = bpy.context.scene
        self.batch = self.scene.batch_3d_props
        self.dif = self.scene.dif_props
        self.batch.batch_product_type = '3'
        self.batch.batch_profondeurs = '100,150'
        self.batch.batch_longueurs = '1,2'
        self.batch.batch_stl_directory = ''
        self.scene.product_props.product_type = '1'
        self.dif.moule_type = '1d'
        self.dif.cadre_epais = True
        self.dif.epaisseur_cadre = 0.025
        self.dif.epaisseur = 0.015
        self.dif.largeur_diffuseur = 0.6
        self.dif.longueur_absorbeur = 0.8
        self.dif.profondeur = 0.2

    def tearDown(self):
        for collection in list(bpy.data.collections):
            if collection.name.startswith('Batch_3D_'):
                for obj in list(collection.objects):
                    bpy.data.objects.remove(obj, do_unlink=True)
                bpy.data.collections.remove(collection)
        self.scene.batch_presets.clear()

    def test_absorber_combinations_geometry_and_state_restoration(self):
        self.batch.batch_types = 'unused for absorber'
        self.assertEqual(ops.batch_3d_configuration(self.batch, self.dif)['count'], 4)
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})

        collection = next(c for c in bpy.data.collections if c.name.startswith('Batch_3D_'))
        objects = list(collection.objects)
        self.assertEqual(len(objects), 4)
        self.assertEqual({o.name for o in objects}, {
            'A0W60P10L1', 'A0W60P10L2',
            'A0W60P15L1', 'A0W60P15L2',
        })
        self.assertEqual({o.data.materials[0].name for o in objects}, {'wood'})
        self.assertEqual({o.data.materials[1].name for o in objects}, {'fabric'})
        self.assertIs(objects[0].data.materials[0], objects[-1].data.materials[0])
        self.assertIs(objects[0].data.materials[1], objects[-1].data.materials[1])
        self.assertFalse(any(material.name.startswith(('wood.', 'fabric.')) for material in bpy.data.materials))
        for obj in objects:
            ratio = int(obj.name.rsplit('L', 1)[1])
            depth_mm = int(obj.name.split('P')[1].split('L')[0]) * 10
            self.assertAlmostEqual(obj.dimensions.x * 1000, 600, places=2)
            self.assertAlmostEqual(obj.dimensions.y * 1000, 600 * ratio, places=2)
            self.assertAlmostEqual(obj.dimensions.z * 1000, depth_mm, places=2)
            self.assertEqual(len(obj.data.materials), 2)
            xs = [v.co.x for v in obj.data.vertices]
            self.assertTrue(any(abs(x - min(xs) - 0.015) < 1e-5 for x in xs))

        self.assertEqual(self.scene.product_props.product_type, '1')
        self.assertEqual(self.dif.moule_type, '1d')
        self.assertTrue(self.dif.cadre_epais)
        self.assertAlmostEqual(self.dif.epaisseur_cadre, 0.025)
        self.assertAlmostEqual(self.dif.largeur_diffuseur, 0.6)
        self.assertAlmostEqual(self.dif.longueur_absorbeur, 0.8)
        self.assertAlmostEqual(self.dif.profondeur, 0.2)

    def test_invalid_ratio_does_not_create_batch(self):
        self.dif.largeur_diffuseur = 0.05
        self.batch.batch_longueurs = '0.5'
        with self.assertRaisesRegex(ValueError, 'longueur calculée'):
            ops.batch_3d_configuration(self.batch, self.dif)
        with self.assertRaisesRegex(RuntimeError, 'longueur calculée'):
            bpy.ops.mesh.batch_3d()
        self.assertFalse(any(c.name.startswith('Batch_3D_') for c in bpy.data.collections))

    def test_ratios_have_clearance_and_export(self):
        self.batch.batch_profondeurs = '150'
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        collection = next(c for c in bpy.data.collections if c.name.startswith('Batch_3D_'))
        left, right = sorted(collection.objects, key=lambda obj: obj.location.x)
        self.assertEqual([obj.name for obj in sorted(collection.objects, key=ops._batch_sort_key)],
                         ['A0W60P15L1', 'A0W60P15L2'])
        clearance = right.location.x - left.location.x - (left.dimensions.x + right.dimensions.x) / 2
        self.assertAlmostEqual(clearance, self.batch.batch_grid_gap, places=5)
        with tempfile.TemporaryDirectory() as directory:
            self.batch.batch_stl_directory = directory
            self.assertEqual(bpy.ops.mesh.export_batch_3d_glb(), {'FINISHED'})
            files = list(Path(directory).glob('*.glb'))
            self.assertEqual({p.stem for p in files}, {left.name, right.name})
            for path in files:
                data = path.read_bytes()
                chunk_length = struct.unpack_from('<I', data, 12)[0]
                glb = json.loads(data[20:20 + chunk_length].decode('utf-8'))
                self.assertEqual(len(glb['materials']), 2)
                self.assertEqual({primitive['material'] for primitive in glb['meshes'][0]['primitives']}, {0, 1})

    def test_existing_mixed_diffuser_batch(self):
        self.batch.batch_product_type = '2'
        self.batch.batch_types = '7'
        self.batch.batch_profondeurs = '100'
        self.batch.batch_longueurs = '1'
        self.assertEqual(ops.batch_3d_configuration(self.batch, self.dif)['count'], 2)
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        collection = next(c for c in bpy.data.collections if c.name.startswith('Batch_3D_'))
        self.assertEqual({obj.name for obj in collection.objects},
                         {'D1N7W60P10L1E15', 'D2N7W60P10L1E15'})

    def test_preset_round_trip_and_mixed_diffuser_count(self):
        self.batch.batch_grid_gap = 0.25
        self.batch.batch_stl_directory = '//exports/'
        self.assertEqual(bpy.ops.mesh.add_batch_preset(), {'FINISHED'})
        self.batch.batch_product_type = '2'
        self.batch.batch_types = '7,11'
        self.batch.batch_profondeurs = '50'
        self.batch.batch_longueurs = '1'
        self.assertEqual(ops.batch_3d_configuration(self.batch, self.dif)['count'], 4)
        self.assertEqual(bpy.ops.mesh.load_batch_preset(), {'FINISHED'})
        self.assertEqual(self.batch.batch_product_type, '3')
        self.assertEqual(self.batch.batch_profondeurs, '100,150')
        self.assertEqual(self.batch.batch_longueurs, '1,2')
        self.assertAlmostEqual(self.batch.batch_grid_gap, 0.25)
        self.assertEqual(self.batch.batch_stl_directory, '//exports/')
        self.batch.batch_longueurs = '0.5,1'
        self.assertEqual(bpy.ops.mesh.save_batch_preset(), {'FINISHED'})
        self.batch.batch_longueurs = '1.5'
        self.assertEqual(bpy.ops.mesh.load_batch_preset(), {'FINISHED'})
        self.assertEqual(self.batch.batch_longueurs, '0.5,1')

    def test_fractional_dimensions_keep_distinct_names(self):
        self.dif.largeur_diffuseur = 0.605
        self.batch.batch_profondeurs = '155'
        self.batch.batch_longueurs = '1.5'
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        collection = next(c for c in bpy.data.collections if c.name.startswith('Batch_3D_'))
        obj = collection.objects[0]
        self.assertEqual(obj.name, 'A0W60p5P15p5L1p5')
        self.assertAlmostEqual(obj.dimensions.y * 1000, 907.5, places=2)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
