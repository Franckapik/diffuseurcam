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


# Trapik-42 du fichier blend/Trapik-web.blend (collection « Trapik-42 »).
TRAPIK_42 = dict(largeur_tasseau=0.044, epaisseur_tasseau=0.023, pourcentage=48,
                 epaisseur_cote=0.018, epaisseur_plateau=0.020, epaisseur_finition=0.002,
                 epaisseur_cerce=0.013, largeur_cerce=0.075, nombre_cerces=4)


def _segments_cross(a, b, c, d):
    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (orient(a, b, c) * orient(a, b, d) < -1e-18
            and orient(c, d, a) * orient(c, d, b) < -1e-18)


def _is_simple(polygon):
    """Aucune arête ne coupe une arête non adjacente."""
    edges = [(polygon[k], polygon[(k + 1) % len(polygon)]) for k in range(len(polygon))]
    for i, (a, b) in enumerate(edges):
        for j in range(i + 2, len(edges)):
            if i == 0 and j == len(edges) - 1:
                continue
            if _segments_cross(a, b, *edges[j]):
                return False
    return True


def _inside(point, polygon):
    """Test pair-impair du point dans le polygone."""
    x, y = point
    inside = False
    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def _parts(obj):
    """Morceaux connexes du maillage : (indice de matériau, volume signé)."""
    mesh = obj.data
    parent = list(range(len(mesh.vertices)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for edge in mesh.edges:
        parent[find(edge.vertices[0])] = find(edge.vertices[1])
    parts = {}
    for face in mesh.polygons:
        co = [mesh.vertices[i].co for i in face.vertices]
        volume = sum(co[0].dot(co[k].cross(co[k + 1])) for k in range(1, len(co) - 1)) / 6
        material, total = parts.get(find(face.vertices[0]), (face.material_index, 0.0))
        parts[find(face.vertices[0])] = (material, total + volume)
    return list(parts.values())


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

    def test_trapik_layout_matches_reference_model(self):
        geo = gammes.trapik_layout(0.424, 1.2, **TRAPIK_42)
        c, r = geo['centre'], geo['rayon_tissu']
        self.assertAlmostEqual(c, 0.022)
        self.assertAlmostEqual(r, 0.402)
        # 8 tasseaux à pas angulaire constant, d'un mur à l'autre.
        self.assertEqual(geo['n'], 8)
        steps = [b - a for a, b in zip(geo['angles'], geo['angles'][1:])]
        for step in steps:
            self.assertAlmostEqual(step, math.pi / 2 / 7)
        self.assertAlmostEqual(geo['angles'][-1], math.pi / 2)
        span = math.pi / 2 * r + 0.044
        self.assertAlmostEqual(geo['ajoure'], 100 * (span - 8 * 0.044) / span)
        self.assertGreater(geo['vide_facade'], geo['vide'])
        # Tasseau d'extrémité : dos sur le chant du côté, joue dans le plan du mur.
        xs, ys = zip(*geo['tasseaux'][0])
        self.assertAlmostEqual(min(xs), 0.424)
        self.assertAlmostEqual(max(xs), 0.447)
        self.assertAlmostEqual(min(ys), 0)
        self.assertAlmostEqual(max(ys), 0.044)
        self.assertAlmostEqual(geo['emprise'], 0.447)
        # Tissu sur l'arc ; cerces en retrait du tissu.
        for point in geo['tissu']:
            self.assertAlmostEqual(math.dist(point, (c, c)), r)
        sector = [(x, y) for x, y in geo['cerce'] if x >= c and y >= c]
        self.assertLessEqual(max(math.dist(point, (c, c)) for point in sector),
                             r - gammes.TRAPIK_JEU_TISSU + 1e-9)
        # Hors de l'arc, la cerce reste derrière le dos des tasseaux d'extrémité.
        self.assertLessEqual(max(max(point) for point in geo['cerce']), 0.424 - gammes.TRAPIK_JEU_TISSU + 1e-9)
        for polygon in (geo['plateau'], geo['finition'], geo['cerce'], *geo['tasseaux']):
            self.assertTrue(_is_simple(polygon))
        # Plateau : mortaise ouverte au droit de chaque tasseau, dent pleine entre deux tasseaux.
        r_facade = geo['rayon_facade']
        plateau = geo['plateau']
        self.assertLessEqual(max(math.dist(point, (c, c)) for point in plateau), r_facade + 1e-9)
        for slat, theta, next_theta in zip(geo['tasseaux'], geo['angles'], geo['angles'][1:] + [None]):
            for back_corner in (slat[0], slat[3]):
                self.assertTrue(any(math.dist(back_corner, point) < 1e-9 for point in plateau))
            middle = (c + (r + 0.0115) * math.cos(theta), c + (r + 0.0115) * math.sin(theta))
            self.assertFalse(_inside(middle, plateau))
            if next_theta is not None:
                gap = (theta + next_theta) / 2
                tooth = (c + (r + 0.0115) * math.cos(gap), c + (r + 0.0115) * math.sin(gap))
                self.assertTrue(_inside(tooth, plateau))
        # Niveaux : finition 2 + plateau 20 de chaque côté, hauteur hors tout 1200.
        levels = geo['niveaux']
        self.assertEqual(levels['interieur'], (0.022, 1.2 - 0.022))
        self.assertAlmostEqual(levels['finition_haut'][1], 1.2)
        self.assertEqual(levels['tasseaux'], (0.002, 1.2 - 0.002))   # à travers les plateaux
        cerces = geo['cerces']
        self.assertEqual(len(cerces), 4)
        self.assertAlmostEqual(cerces[0][0], 0.022)
        self.assertAlmostEqual(cerces[-1][1], 1.178)
        # Doigts d'angle : nombre impair, alternés, jointifs sur toute la hauteur intérieure.
        doigts = geo['doigts']
        self.assertEqual(len(doigts), 7)
        self.assertEqual([owner for *_z, owner in doigts], list('ABABABA'))
        for (_lo, hi, _o), (lo, _hi, _o2) in zip(doigts, doigts[1:]):
            self.assertAlmostEqual(hi, lo)
        # Tenon : tiers central du bout de cerce, hors de la zone des doigts.
        t0, t1 = geo['tenon']
        self.assertLess(0.018, t0)
        self.assertLess(t1, 0.424)
        self.assertAlmostEqual(t0, 0.3734, places=4)
        self.assertAlmostEqual(t1, 0.3982, places=4)

    def test_trapik_layout_clamps_and_errors(self):
        dense = gammes.trapik_layout(0.424, 1.2, **{**TRAPIK_42, 'pourcentage': 0})
        self.assertGreaterEqual(dense['vide'], gammes.TRAPIK_VIDE_MIN - 1e-12)
        self.assertTrue(_is_simple(dense['plateau']))
        forced = gammes.trapik_layout(0.424, 1.2, nombre_force=5, **TRAPIK_42)
        self.assertEqual(forced['n'], 5)
        too_many = gammes.trapik_layout(0.424, 1.2, nombre_force=99, **TRAPIK_42)
        self.assertEqual(too_many['n'], dense['n'])
        # Tasseaux plus étroits que les côtés : la cerce démarre sur l'arc.
        narrow = gammes.trapik_layout(0.424, 1.2, **{**TRAPIK_42, 'largeur_tasseau': 0.02})
        self.assertTrue(_is_simple(narrow['cerce']))
        cases = (
            (0.05, 1.2, {}, 'Côté trop petit'),
            (0.424, 0.08, {}, 'Hauteur insuffisante'),
            (0.424, 1.2, {'largeur_cerce': 0.4}, 'Largeur de cerce'),
            (0.424, 1.2, {'nombre_cerces': 1}, 'deux cerces'),
            (0.424, 1.2, {'epaisseur_cote': 0}, 'invalides'),
        )
        for cote, hauteur, override, message in cases:
            with self.assertRaisesRegex(ValueError, message):
                gammes.trapik_layout(cote, hauteur, **{**TRAPIK_42, **override})

    def test_references(self):
        self.assertEqual(gammes.panel_reference('4', 0.5, 0.1, 1, 30), 'S0W50P10L1G30')
        self.assertEqual(gammes.panel_reference('6', 1.2, 0.1, 1), 'K0W120P10L1')
        self.assertEqual(gammes.panel_reference('7', 0.5, 0.1, 1), 'C0W50P10L1')
        self.assertEqual(gammes.panel_reference('2', 0.605, 0.155, 1.5), 'A0W60p5P15p5L1p5')
        self.assertEqual(gammes.trapik_reference(0.42, 1.2, 50), 'T0A42B42H120G50')
        self.assertEqual(gammes.trapik_reference(0.424, 1.2), 'T0A42p4B42p4H120')
        for name in ('S0W50P10L1G30', 'K0W120P10L1', 'C0W50P10L1E10', 'T0A30B30H120', 'A0W60P10L2',
                     'T0A42B42H120G50', 'T0A42B42H120G50E18'):
            self.assertTrue(is_product_reference(name), name)
        self.assertFalse(is_product_reference('T0W50P10L1'))
        self.assertEqual(product_stem('S0W50P10L1G30.001', 0.015), 'S0W50P10L1G30E15')
        self.assertEqual(product_stem('T0A42B42H120G50.001', 0.018), 'T0A42B42H120G50E18')

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
        for group in (self.stratik, self.cloudik, self.trapik):
            for prop in group.bl_rna.properties:
                if prop.identifier != 'rna_type':
                    group.property_unset(prop.identifier)
        self.dif.epaisseur = 0.015
        self.dif.largeur_diffuseur = 0.6
        self.dif.longueur_absorbeur = 1.2
        self.dif.profondeur = 0.1

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

    def test_trapik_model(self):
        obj = self._generate('5')
        geo = self.trapik.layout()
        self.assertEqual(obj.name, '3D_T0A42B42H120G50')
        self.assertEqual([m.name for m in obj.data.materials], ['wood', 'fabric'])
        self.assertAlmostEqual(obj['epaisseur_ref'], 0.018)
        # Murs à ±45° de l'axe Z : largeur = diagonale de l'emprise, profondeur selon la bissectrice.
        self.assertAlmostEqual(obj.dimensions.x, math.sqrt(2) * (0.42 + 0.023), places=5)
        self.assertAlmostEqual(obj.dimensions.y, 1.2, places=5)
        self.assertAlmostEqual(obj.dimensions.z, geo['profondeur'], places=5)
        # Bois : 2 côtés, 2 plateaux, 4 cerces, 8 tasseaux. Tissu : façade et 2 finitions.
        parts = _parts(obj)
        self.assertEqual(geo['n'], 8)
        self.assertEqual(sum(1 for material, _v in parts if material == 0), 2 + 2 + 4 + 8)
        self.assertEqual(sum(1 for material, _v in parts if material == 1), 3)
        # Pièces bois fermées et normales sortantes.
        for material, volume in parts:
            if material == 0:
                self.assertGreater(volume, 0)
        for edge_faces in self._edge_face_counts(obj, material=0).values():
            self.assertEqual(edge_faces, 2)
        # Tasseaux de finition à finition : le bois couvre toute la hauteur moins 2 × 2 mm.
        wood_y = [obj.data.vertices[i].co.y for f in obj.data.polygons if f.material_index == 0
                  for i in f.vertices]
        self.assertAlmostEqual(max(wood_y) - min(wood_y), 1.2 - 2 * 0.002, places=5)
        # Tissu de façade lissé, tourné vers la pièce.
        facade = [f for f in obj.data.polygons if f.material_index == 1 and f.use_smooth]
        self.assertEqual(len(facade), len(geo['tissu']) - 1)
        for face in facade:
            self.assertGreater(face.normal.z, 0)

    def _edge_face_counts(self, obj, material):
        counts = {}
        for face in obj.data.polygons:
            if face.material_index == material:
                for key in face.edge_keys:
                    counts[key] = counts.get(key, 0) + 1
        return counts

    def test_trapik_forced_count_reference(self):
        self.trapik.nombre_manuel = True
        self.trapik.nombre_tasseaux = 6
        obj = self._generate('5')
        geo = self.trapik.layout()
        self.assertEqual(geo['n'], 6)
        self.assertEqual(obj.name, f"3D_T0A42B42H120G{round(geo['ajoure'])}")

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
        self.trapik.nombre_manuel = True
        self.batch.batch_product_type = '5'
        self.batch.batch_trapik_cotes = '420'
        self.batch.batch_trapik_h = '1200,900'
        self.batch.batch_ajoures = '50,40'
        self.assertEqual(ops.batch_3d_configuration(self.batch, self.dif)['count'], 4)
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        self.batch.batch_product_type = '3'
        self.batch.batch_profondeurs = '100'
        self.batch.batch_longueurs = '1'
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        names = [obj.name for obj in sorted(_batch_objects(), key=ops._batch_sort_key)]
        self.assertEqual(names, ['A0W60P10L1', 'T0A42B42H90G40', 'T0A42B42H90G50',
                                 'T0A42B42H120G40', 'T0A42B42H120G50'])
        for obj in _batch_objects():
            if obj.name.startswith('T0'):
                self.assertAlmostEqual(obj.dimensions.y * 100, int(obj.name.split('H')[1].split('G')[0]),
                                       places=4)
        # Valeurs d'origine restaurées.
        self.assertTrue(self.trapik.nombre_manuel)
        self.assertAlmostEqual(self.trapik.hauteur, 1.2)
        self.assertAlmostEqual(self.trapik.pourcentage_ajoure, 50)

    def test_trapik_quadraroom_export(self):
        self.batch.batch_product_type = '5'
        self.batch.batch_trapik_cotes = '420'
        self.batch.batch_trapik_h = '1200'
        self.batch.batch_ajoures = '50'
        self.assertEqual(bpy.ops.mesh.batch_3d(), {'FINISHED'})
        with tempfile.TemporaryDirectory() as directory:
            self.batch.quadra_glb_directory = directory
            self.assertEqual(bpy.ops.mesh.export_batch_3d_quadraroom_glb(), {'FINISHED'})
            document, _ = read_glb(Path(directory) / 'T0A42B42H120G50E18.glb')
            self.assertFalse(document.get('images'))
            self.assertEqual({m['name'] for m in document['materials']}, {'wood', 'fabric'})

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
        self.batch.batch_product_type = '5'
        self.batch.batch_ajoures = '50'
        self.batch.batch_trapik_h = '1200'
        self.batch.batch_trapik_cotes = '420,100'
        with self.assertRaisesRegex(ValueError, 'cerce'):
            ops.batch_3d_configuration(self.batch, self.dif)

    def test_preset_round_trip_new_fields(self):
        self.batch.batch_product_type = '4'
        self.batch.batch_ajoures = '15,35'
        self.batch.batch_trapik_h = '900'
        self.batch.batch_trapik_cotes = '420,600'
        self.assertEqual(bpy.ops.mesh.add_batch_preset(), {'FINISHED'})
        self.batch.batch_product_type = '0'
        self.batch.batch_ajoures = '50'
        self.batch.batch_trapik_h = '1000'
        self.batch.batch_trapik_cotes = '300'
        self.assertEqual(bpy.ops.mesh.load_batch_preset(), {'FINISHED'})
        self.assertEqual(self.batch.batch_product_type, '4')
        self.assertEqual(self.batch.batch_ajoures, '15,35')
        self.assertEqual(self.batch.batch_trapik_h, '900')
        self.assertEqual(self.batch.batch_trapik_cotes, '420,600')


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
