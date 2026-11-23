"""À lancer avec : blender -b --factory-startup --python-exit-code 1 --python tests/test_contrepilier_eco.py"""

import sys
import unittest
from collections import defaultdict
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props, shapes  # noqa: E402


def component_sizes(vertex_count, edges):
    neighbors = defaultdict(list)
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    seen = set()
    sizes = []
    for start in range(vertex_count):
        if start in seen:
            continue
        pending = [start]
        seen.add(start)
        size = 0
        while pending:
            index = pending.pop()
            size += 1
            for neighbor in neighbors[index]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    pending.append(neighbor)
        sizes.append(size)
    return sizes


class ContrepilierEcoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        bpy.utils.register_class(ops.AddContrePilierMoule)

    @classmethod
    def tearDownClass(cls):
        bpy.utils.unregister_class(ops.AddContrePilierMoule)
        props.unregister()

    def setUp(self):
        scene = bpy.context.scene
        self.dif = scene.dif_props
        self.product = scene.product_props
        self.usinage = scene.usinage_props
        self.array = scene.array_props
        self.product.product_type = "1"
        self.dif.type_moule = "mono_v2"
        self.dif.contrepilier_eco = True
        self.dif.contrepilier_eco_fente_assemblage = True
        self.dif.moule_type = "1d"
        self.dif.type = 11
        self.dif.largeur_diffuseur = 0.6
        self.dif.longueur_diffuseur = 1
        self.dif.profondeur = 0.2
        self.dif.epaisseur = 0.005
        self.dif.epaisseur_moule = 0.01
        self.dif.epaisseur_pilier = 0.005
        self.dif.pilier_reduction = "0.20"
        self.dif.decalage_h = 6
        self.dif.decalage_v = 0
        self.dif.center_pattern = False
        self.dif.qrd_optimization = "none"
        self.dif.cadre_epais = False
        self.array.array_offset = 0.01

    def generated(self):
        return shapes.add_contre_pilier_moule(
            self.dif, self.product, self.usinage, self.array
        )

    def test_reference_outline_and_slot(self):
        vertices, edges, name = self.generated()
        self.assertEqual(name, "Contre-Piliers Eco")
        self.assertEqual(len(vertices), 56)
        self.assertEqual(len(edges), 56)
        self.assertEqual(component_sizes(len(vertices), edges), [56])
        self.assertAlmostEqual(min(v[0] for v in vertices), 0)
        self.assertAlmostEqual(max(v[0] for v in vertices), 0.670)
        self.assertAlmostEqual(min(v[1] for v in vertices), 0)
        self.assertAlmostEqual(max(v[1] for v in vertices), 0.060)
        self.assertTrue(all(v[2] == 0 for v in vertices))
        self.assertEqual(len([v for v in vertices if abs(v[1] - 0.035) < 1e-7]), 2)
        bottom = sorted(v[0] for v in vertices if abs(v[1] - 0.035) < 1e-7)
        self.assertAlmostEqual(bottom[1] - bottom[0], 0.005004, places=6)
        self.assertAlmostEqual((bottom[0] + bottom[1]) / 2 - 0.335, 0.008634, places=5)
        # Deux cellules de ratio maximal sont affleurantes au niveau des fentes.
        self.assertTrue(any(abs(v[0] - 0.1431818) < 2e-6 and abs(v[1] - 0.030) < 1e-7
                            for v in vertices))
        self.assertIn("contrepilier_eco", self.dif.listMouleAttributes())
        self.assertIn("contrepilier_eco_fente_assemblage", self.dif.listMouleAttributes())
        self.dif.type_moule = "eco"
        self.assertIn("epaisseur_pilier", self.dif.listMouleAttributes())

    def test_assembly_slot_can_be_disabled_without_changing_other_features(self):
        with_slot, with_edges, _ = self.generated()
        self.dif.contrepilier_eco_fente_assemblage = False
        without_slot, without_edges, _ = self.generated()
        self.assertEqual(len(without_slot), len(with_slot) - 4)
        self.assertEqual(len(without_edges), len(with_edges) - 4)
        self.assertTrue(set(without_slot).issubset(set(with_slot)))
        removed = set(with_slot) - set(without_slot)
        self.assertEqual(len(removed), 4)
        self.assertTrue(all(abs(v[0] - 0.335) < self.dif.getRang() / 2 for v in removed))
        self.assertEqual(component_sizes(len(without_slot), without_edges), [52])
        self.dif.contrepilier_eco = False
        self.assertNotIn("contrepilier_eco_fente_assemblage", self.dif.listMouleAttributes())

        # Un jeu trop épais ne bloque plus le profil quand la fente est absente.
        self.dif.contrepilier_eco = True
        self.dif.epaisseur_pilier = 0.080
        without_slot, _, _ = self.generated()
        self.assertEqual(len(without_slot), 52)

    def test_option_replaces_shape_and_preserves_existing_piece_count(self):
        for mold_type in ("stable", "eco", "mono", "mono_v2"):
            for dimension in ("1d", "2d"):
                with self.subTest(mold_type=mold_type, dimension=dimension):
                    self.dif.type_moule = mold_type
                    self.dif.moule_type = dimension
                    self.dif.contrepilier_eco = False
                    legacy_vertices, legacy_edges, _ = self.generated()
                    expected = len(component_sizes(len(legacy_vertices), legacy_edges))
                    self.dif.contrepilier_eco = True
                    vertices, edges, _ = self.generated()
                    self.assertEqual(len(component_sizes(len(vertices), edges)), expected)
                    self.assertEqual(len(vertices), len(edges))
                    self.assertTrue(all(abs(v[2]) < 1e-8 for v in vertices))

    def test_width_and_regular_slots_follow_model_thickness(self):
        self.dif.largeur_diffuseur = 0.8
        self.dif.epaisseur = 0.006
        vertices, _, _ = self.generated()
        self.assertAlmostEqual(max(v[0] for v in vertices), 0.870, places=6)
        self.assertAlmostEqual(max(v[1] for v in vertices), 0.060, places=6)
        baseline = sorted(v[0] for v in vertices if abs(v[1] - 0.030) < 1e-7)
        regular_gaps = [b - a for a, b in zip(baseline[::2], baseline[1::2])]
        self.assertIn(0.0065, [round(gap, 4) for gap in regular_gaps])

    def test_center_slot_follows_the_cell_and_pillar_thickness(self):
        self.dif.type = 13
        self.dif.epaisseur_pilier = 0.007
        vertices, _, _ = self.generated()
        bottom = [v for v in vertices if abs(v[1] - 0.037) < 1e-7]
        self.assertEqual(len(bottom), 2)
        self.assertAlmostEqual(abs(bottom[1][0] - bottom[0][0]), 0.005004, places=6)
        bottom_index = vertices.index(bottom[0])
        key_top_right = vertices[bottom_index + 2]
        cell_top_right = vertices[bottom_index + 3]
        center_height = self.dif.getMotif("height")[self.dif.type // 2]
        expected_top = 0.030 + min(0.030, center_height - self.dif.epaisseur)
        self.assertAlmostEqual(key_top_right[1], expected_top, places=6)
        self.assertAlmostEqual(cell_top_right[0] - key_top_right[0], 0.008, places=6)

    def test_operator_creates_profile_and_uses_its_bounds_for_array_spacing(self):
        self.array.contre_pilier_moule_x = 2
        before = set(bpy.data.objects)
        self.assertEqual(bpy.ops.mesh.contre_pilier_moule(), {"FINISHED"})
        created = list(set(bpy.data.objects) - before)
        self.assertEqual(len(created), 1)
        obj = created[0]
        try:
            self.assertEqual(obj.type, "MESH")
            self.assertEqual(len(obj.data.vertices), 56)
            array_x = next(modifier for modifier in obj.modifiers
                           if modifier.type == "ARRAY" and modifier.count == 2)
            self.assertAlmostEqual(array_x.constant_offset_displace[0], 0.680, places=6)
        finally:
            bpy.data.objects.remove(obj, do_unlink=True)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
