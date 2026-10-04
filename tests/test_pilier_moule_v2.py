"""À lancer avec : blender -b --factory-startup --python-exit-code 1 --python tests/test_pilier_moule_v2.py"""

import sys
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props, shapes  # noqa: E402


class PilierMouleV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        bpy.utils.register_class(ops.AddPilierMoule)

    @classmethod
    def tearDownClass(cls):
        bpy.utils.unregister_class(ops.AddPilierMoule)
        props.unregister()

    def setUp(self):
        scene = bpy.context.scene
        self.dif = scene.dif_props
        self.product = scene.product_props
        self.usinage = scene.usinage_props
        self.array = scene.array_props
        self.product.product_type = "1"
        self.dif.moule_type = "1d"
        self.dif.type = 11
        self.dif.epaisseur = 0.005
        self.dif.epaisseur_moule = 0.01
        self.dif.socle_monopilier = 0.03
        self.dif.pilier_reduction = "0.20"
        self.dif.pilier_pyramidal = True
        self.dif.monopilier_mortaise_reduction = "0"
        self.dif.cadre_epais = False
        self.dif.decalage_h = 6
        self.dif.decalage_v = 0
        self.dif.center_pattern = False
        self.dif.qrd_optimization = "none"
        self.dif.longueur_diffuseur = 1

    def generated(self, width, depth, mode):
        self.dif.largeur_diffuseur = width
        self.dif.profondeur = depth
        self.dif.type_moule = mode
        return shapes.add_pilier_moule(self.dif, self.product, self.usinage, self.array)

    def test_three_reference_profiles_keep_their_tops_and_gain_two_steps(self):
        for width, depth, expected_top in ((0.6, 0.2, 0.225),
                                           (0.576, 0.15, 0.175),
                                           (0.576, 0.095, 0.120)):
            with self.subTest(width=width, depth=depth):
                old_vertices, _, _ = self.generated(width, depth, "mono")
                vertices, edges, _ = self.generated(width, depth, "mono_v2")
                self.assertEqual(len(vertices), len(edges))
                self.assertEqual({v for v in old_vertices if v[1] > 0},
                                 {v for v in vertices if v[1] > 0})
                self.assertAlmostEqual(max(v[1] for v in vertices), expected_top, places=5)
                self.assertEqual({round(v[1], 6) for v in vertices if v[1] < 0},
                                 {-0.012, -0.022})
                self.assertTrue(all(v[2] == 0 for v in vertices))

                # Mesure relative au bord gauche : deux entailles de même
                # largeur, chacune décalée de 20 mm par rapport au mono.
                x_min = min(v[0] for v in vertices)
                spacing = (width - 2 * self.dif.getEpaisseurCadre()) / 5
                expected_deep_x = sorted((self.dif.getEpaisseurCadre() + spacing - 0.020,
                                          self.dif.getEpaisseurCadre() + 2 * spacing - 0.020,
                                          self.dif.getEpaisseurCadre() + 3 * spacing - 0.020,
                                          self.dif.getEpaisseurCadre() + 4 * spacing - 0.020))
                actual_deep_x = sorted(v[0] - x_min for v in vertices if abs(v[1] + 0.022) < 1e-7)
                self.assertEqual(len(actual_deep_x), 4)
                for actual, expected in zip(actual_deep_x, expected_deep_x):
                    self.assertAlmostEqual(actual, expected, places=5)

    def test_step_depth_and_width_match_the_fond_mortises(self):
        self.dif.epaisseur_moule = 0.012
        self.dif.monopilier_mortaise_reduction = "0.20"
        self.dif.type_moule = "mono_v2"
        self.assertNotIn("monopilier_mortaise_reduction", self.dif.listMouleAttributes())
        for width, expected_mm in ((0.6, 118.0), (0.576, 113.2)):
            with self.subTest(width=width):
                vertices, _, _ = self.generated(width, 0.15, "mono_v2")
                self.assertEqual({round(v[1], 6) for v in vertices if v[1] < 0},
                                 {-0.014, -0.026})
                deep_x = sorted(v[0] for v in vertices if abs(v[1] + 0.026) < 1e-7)
                fond_vertices, _, _ = shapes.add_fond_moule(self.dif, self.product, self.usinage)
                fond_mortaise = fond_vertices[4:8]
                fond_width = max(v[0] for v in fond_mortaise) - min(v[0] for v in fond_mortaise)
                self.assertAlmostEqual(fond_width * 1000, expected_mm, places=3)
                self.assertAlmostEqual(deep_x[1] - deep_x[0], fond_width, places=5)
                self.assertAlmostEqual(deep_x[3] - deep_x[2], fond_width, places=5)

    def test_operator_creates_a_planar_pillar_with_the_new_base(self):
        self.dif.largeur_diffuseur = 0.6
        self.dif.profondeur = 0.2
        self.dif.type_moule = "mono_v2"
        self.dif.pilier_codage = False
        before = set(bpy.data.objects)
        self.assertEqual(bpy.ops.mesh.pilier_moule(), {"FINISHED"})
        created = list(set(bpy.data.objects) - before)
        self.assertEqual(len(created), 1)
        obj = created[0]
        try:
            self.assertEqual(obj.type, "MESH")
            self.assertAlmostEqual(min(v.co.y for v in obj.data.vertices), -0.022, places=6)
            self.assertTrue(all(abs(v.co.z) < 1e-8 for v in obj.data.vertices))
        finally:
            bpy.data.objects.remove(obj, do_unlink=True)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
