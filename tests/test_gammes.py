"""À lancer avec : ~/.app/blender510/blender -b --factory-startup --python-exit-code 1 --python tests/test_gammes.py"""

import math
import sys
import tempfile
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import gammes, ops, props, ui  # noqa: E402
from diffuseurcam.quadraroom_glb import is_product_reference, product_stem, read_glb  # noqa: E402


def _clear_batches():
    for collection in list(bpy.data.collections):
        if collection.name.startswith('Batch_3D_'):
            for obj in list(collection.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(collection)


def _batch_objects():
    return [obj for collection in bpy.data.collections if collection.name.startswith('Batch_3D_')
            for obj in collection.objects]


class PureCalculationsTest(unittest.TestCase):
    def test_stratik_layout_from_percentage(self):
        layout = gammes.stratik_layout(0.6, 0.025, 30)
        self.assertEqual(layout['n'], 17)          # 0.7 × 600 / 25 = 16.8 → 17
        self.assertAlmostEqual(layout['vide'], (0.6 - 17 * 0.025) / 16)
        self.assertAlmostEqual(layout['ajoure'], 100 * (0.6 - 17 * 0.025) / 0.6)
        self.assertAlmostEqual(layout['positions'][0], 0)
        self.assertAlmostEqual(layout['positions'][-1] + 0.025, 0.6)   # affleure les deux bords

    def test_stratik_layout_forced_and_clamped(self):
        self.assertEqual(gammes.stratik_layout(0.6, 0.025, 30, nombre_force=5)['n'], 5)
        self.assertEqual(gammes.stratik_layout(0.6, 0.025, 90)['n'], 2)       # au moins deux
        self.assertEqual(gammes.stratik_layout(0.6, 0.025, 0)['n'], 24)       # plein
        self.assertEqual(gammes.stratik_layout(0.6, 0.025, 0, nombre_force=99)['n'], 24)
        with self.assertRaisesRegex(ValueError, 'deux tasseaux'):
            gammes.stratik_layout(0.04, 0.025, 30)

    def test_trapik_section(self):
        c, h, xc = gammes.trapik_section(0.3, 0.4)
        self.assertAlmostEqual(c, 0.5)
        self.assertAlmostEqual(h, 0.24)
        self.assertAlmostEqual(math.hypot(xc, h), 0.3)
        self.assertAlmostEqual(math.hypot(c - xc, h), 0.4)

    def test_references(self):
        self.assertEqual(gammes.panel_reference('4', 0.5, 0.1, 1, 30), 'S0W50P10L1G30')
        self.assertEqual(gammes.panel_reference('6', 1.2, 0.1, 1), 'K0W120P10L1')
        self.assertEqual(gammes.panel_reference('7', 0.5, 0.1, 1), 'C0W50P10L1')
        self.assertEqual(gammes.panel_reference('2', 0.605, 0.155, 1.5), 'A0W60p5P15p5L1p5')
        self.assertEqual(gammes.trapik_reference(0.3, 0.3, 1.2), 'T0A30B30H120')
        for name in ('S0W50P10L1G30', 'K0W120P10L1', 'C0W50P10L1E10', 'T0A30B30H120', 'A0W60P10L2'):
            self.assertTrue(is_product_reference(name), name)
        self.assertFalse(is_product_reference('T0W50P10L1'))
        self.assertEqual(product_stem('S0W50P10L1G30.001', 0.015), 'S0W50P10L1G30E15')

    def test_cam_mapping(self):
        self.assertEqual(gammes.cam_product_type('4'), '2')
        self.assertEqual(gammes.cam_product_type('0'), '0')
        for product in ('5', '6', '7'):
            self.assertIsNone(gammes.cam_product_type(product))


class GammesBlenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        cls.operators = (
            ops.Add3DModel, ops.Batch3DGenerate, ops.AddBatchPreset, ops.LoadBatchPreset,
            ops.SaveBatchPreset, ops.ExportBatch3DQuadraRoomGLB, ops.ExportBatch3DGLB,
        )
        for operator in cls.operators:
            bpy.utils.register_class(operator)

    @classmethod
    def tearDownClass(cls):
        _clear_batches()
        for operator in reversed(cls.operators):
            bpy.utils.unregister_class(operator)
        props.unregister()

    def setUp(self):
        self.scene = bpy.context.scene
        self.dif = self.scene.dif_props
        self.batch = self.scene.batch_3d_props
        self.stratik = self.scene.stratik_props
        self.cloudik = self.scene.cloudik_props
        self.trapik = self.scene.trapik_props
        self.dif.epaisseur = 0.015
        self.dif.largeur_diffuseur = 0.6
        self.dif.longueur_absorbeur = 1.2
        self.dif.profondeur = 0.1
        self.stratik.orientation = 'V'
        self.stratik.nombre_manuel = False
        self.stratik.pourcentage_ajoure = 30
        for group in (self.stratik, self.cloudik, self.trapik):
            for name in ('largeur_tasseau', 'saillie_tasseau', 'gousset_taille', 'gousset_epaisseur',
                         'oeillet_diametre', 'oeillet_fil', 'epaisseur_cadre', 'cote_a', 'cote_b',
                         'hauteur'):
                if name in group.bl_rna.properties:
                    group.property_unset(name)

    def tearDown(self):
        _clear_batches()
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in list(bpy.data.meshes):
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        self.scene.batch_presets.clear()

    def _generate(self, product):
        self.scene.product_props.product_type = product
        self.assertEqual(bpy.ops.mesh.simulation(), {'FINISHED'})
        return bpy.context.active_object

    def test_tabs_order_and_stored_values(self):
        items = props.UIProductProps.bl_rna.properties['product_type'].enum_items
        self.assertEqual([item.name for item in items],
                         ['Indik', 'Woodik', 'Organik', 'Stratik', 'Trapik', 'Mobilik', 'Cloudik'])
        # Valeurs stockées inchangées pour les fichiers .blend existants.
        self.assertEqual({item.identifier: item.value for item in items},
                         {'0': 0, '1': 1, '2': 2, '4': 4, '5': 5, '6': 6, '7': 7})

    def test_stratik_vertical_model(self):
        obj = self._generate('4')
        self.assertEqual(obj.name, '3D_S0W60P10L2G30')
        self.assertAlmostEqual(obj.dimensions.x, 0.6, places=5)
        self.assertAlmostEqual(obj.dimensions.y, 1.2, places=5)
        self.assertAlmostEqual(obj.dimensions.z, 0.1 + 0.04, places=5)
        front = [v.co for v in obj.data.vertices if v.co.z > max(v.co.z for v in obj.data.vertices) - 1e-6]
        # 17 tasseaux × 4 coins sur la face avant.
        self.assertEqual(len(front), 17 * 4)
        self.assertEqual([m.name for m in obj.data.materials], ['wood', 'fabric'])

    def test_stratik_horizontal_forced_count(self):
        self.stratik.orientation = 'H'
        self.stratik.nombre_manuel = True
        self.stratik.nombre_tasseaux = 10
        obj = self._generate('4')
        layout = self.stratik.layout(self.dif)
        self.assertEqual(layout['n'], 10)
        self.assertEqual(obj.name, f"3D_S0W60P10L2G{round(layout['ajoure'])}")
        top = max(v.co.z for v in obj.data.vertices)
        ys = sorted({round(v.co.y, 5) for v in obj.data.vertices if abs(v.co.z - top) < 1e-6})
        self.assertEqual(len(ys), 20)   # deux arêtes par tasseau horizontal

    def test_cloudik_model_and_quadraroom_export(self):
        self.batch.batch_product_type = '7'
        self.batch.batch_profondeurs = '100'
        self.batch.batch_longueurs = '1'
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        obj, = _batch_objects()
        self.assertEqual(obj.name, 'C0W60P10L1')
        self.assertEqual([m.name for m in obj.data.materials], ['wood', 'fabric', 'metal'])
        self.assertAlmostEqual(obj.dimensions.x, 0.6, places=5)
        major = self.cloudik.oeillet_diametre / 2 - self.cloudik.oeillet_fil / 2
        expected_z = 0.1 + self.cloudik.gousset_epaisseur + 2 * major + self.cloudik.oeillet_fil / 2
        self.assertAlmostEqual(obj.dimensions.z, expected_z, places=4)
        # Planches de 10 mm : arêtes intérieures du cadre à 10 mm des bords.
        xs = [v.co.x for v in obj.data.vertices]
        self.assertTrue(any(abs(x - min(xs) - 0.010) < 1e-5 for x in xs))
        metal_faces = [f for f in obj.data.polygons if f.material_index == 2]
        self.assertGreater(len(metal_faces), 4 * 5)
        with tempfile.TemporaryDirectory() as directory:
            self.batch.quadra_glb_directory = directory
            self.assertEqual(bpy.ops.mesh.export_batch_3d_quadraroom_glb(), {'FINISHED'})
            document, _ = read_glb(Path(directory) / 'C0W60P10L1E10.glb')
            self.assertFalse(document.get('images'))
            self.assertEqual({m['name'] for m in document['materials']}, {'wood', 'fabric', 'metal'})

    def test_trapik_placeholder(self):
        self.trapik.cote_a = 0.3
        self.trapik.cote_b = 0.4
        self.trapik.hauteur = 1.2
        obj = self._generate('5')
        self.assertEqual(obj.name, '3D_T0A30B40H120')
        self.assertAlmostEqual(obj.dimensions.x, 0.5, places=5)
        self.assertAlmostEqual(obj.dimensions.y, 1.2, places=5)
        self.assertAlmostEqual(obj.dimensions.z, 0.24, places=5)
        fabric, = [f for f in obj.data.polygons if f.material_index == 1]
        self.assertAlmostEqual(fabric.normal.z, 1.0, places=5)
        self.assertAlmostEqual(fabric.area, (0.5 - 0.03) * (1.2 - 0.03), places=5)

    def test_mobilik_placeholder(self):
        obj = self._generate('6')
        self.assertEqual(obj.name, '3D_K0W60P10L2')
        self.assertEqual(len(obj.data.materials), 2)
        self.assertAlmostEqual(obj.dimensions.z, 0.1, places=5)

    def test_stratik_batch_names_order_and_restoration(self):
        self.scene.product_props.product_type = '1'
        self.stratik.nombre_manuel = True
        self.stratik.pourcentage_ajoure = 25
        self.batch.batch_product_type = '4'
        self.batch.batch_profondeurs = '150,100'
        self.batch.batch_longueurs = '1'
        self.batch.batch_ajoures = '40,20'
        self.assertEqual(ops.batch_3d_configuration(self.batch, self.dif)['count'], 4)
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        names = [obj.name for obj in sorted(_batch_objects(), key=ops._batch_sort_key)]
        self.assertEqual(names, ['S0W60P10L1G20', 'S0W60P10L1G40', 'S0W60P15L1G20', 'S0W60P15L1G40'])
        for obj in _batch_objects():
            self.assertAlmostEqual(obj.dimensions.z * 1000, int(obj.name.split('P')[1].split('L')[0]) * 10 + 40,
                                   places=2)
        self.assertEqual(self.scene.product_props.product_type, '1')
        self.assertTrue(self.stratik.nombre_manuel)
        self.assertAlmostEqual(self.stratik.pourcentage_ajoure, 25)

    def test_trapik_batch_and_mixed_sort(self):
        self.batch.batch_product_type = '5'
        self.batch.batch_trapik_a = '300'
        self.batch.batch_trapik_b = '300,400'
        self.batch.batch_trapik_h = '1200'
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        self.batch.batch_product_type = '3'
        self.batch.batch_profondeurs = '100'
        self.batch.batch_longueurs = '1'
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        names = [obj.name for obj in sorted(_batch_objects(), key=ops._batch_sort_key)]
        self.assertEqual(names, ['A0W60P10L1', 'T0A30B30H120', 'T0A30B40H120'])
        self.assertAlmostEqual(self.trapik.cote_b, 0.3)   # valeur d'origine restaurée

    def test_invalid_batches(self):
        self.batch.batch_product_type = '7'
        self.batch.batch_profondeurs = '100'
        self.batch.batch_longueurs = '1'
        self.cloudik.gousset_taille = 0.35
        with self.assertRaisesRegex(ValueError, 'Goussets'):
            ops.batch_3d_configuration(self.batch, self.dif)
        self.cloudik.gousset_taille = 0.1
        self.batch.batch_product_type = '4'
        self.batch.batch_ajoures = '30'
        self.stratik.largeur_tasseau = 0.2
        self.dif.largeur_diffuseur = 0.3
        with self.assertRaisesRegex(ValueError, 'deux tasseaux'):
            ops.batch_3d_configuration(self.batch, self.dif)
        self.dif.largeur_diffuseur = 0.6
        self.batch.batch_ajoures = '95'
        with self.assertRaisesRegex(ValueError, 'hors plage'):
            ops.batch_3d_configuration(self.batch, self.dif)

    def test_preset_round_trip_new_fields(self):
        self.batch.batch_product_type = '4'
        self.batch.batch_ajoures = '15,35'
        self.batch.batch_trapik_h = '900'
        self.assertEqual(bpy.ops.mesh.add_batch_preset(), {'FINISHED'})
        self.batch.batch_product_type = '0'
        self.batch.batch_ajoures = '50'
        self.batch.batch_trapik_h = '1000'
        self.assertEqual(bpy.ops.mesh.load_batch_preset(), {'FINISHED'})
        self.assertEqual(self.batch.batch_product_type, '4')
        self.assertEqual(self.batch.batch_ajoures, '15,35')
        self.assertEqual(self.batch.batch_trapik_h, '900')


class _FakeLayout:
    """Layout factice : vérifie que chaque propriété dessinée existe."""

    def __init__(self, test):
        self.test = test

    def __getattr__(self, name):
        return self._child

    def _child(self, *args, **kwargs):
        return self

    def prop(self, data, attribute, **kwargs):
        self.test.assertIn(attribute, data.bl_rna.properties, f"{data} n'a pas {attribute}")
        return self

    def operator(self, *args, **kwargs):
        return type('Op', (), {})()

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


class PanelDrawTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()

    @classmethod
    def tearDownClass(cls):
        props.unregister()

    def test_panel_draws_for_every_product(self):
        scene = bpy.context.scene
        for batch_product in ('0', '3', '4', '5', '7'):
            scene.batch_3d_props.batch_product_type = batch_product
            for identifier, _name, _description in gammes.GAMMES:
                scene.product_props.product_type = identifier
                panel = type('Panel', (), {'layout': _FakeLayout(self)})()
                ui.Diffuseur_SideBar.draw(panel, bpy.context)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
