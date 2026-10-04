"""À lancer avec : blender -b --factory-startup --python-exit-code 1 --python tests/test_fond_moule_v2.py"""

import sys
import unittest
from collections import Counter, defaultdict
from math import hypot
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props, shapes  # noqa: E402


def connected_contours(vertices, edges):
    neighbors = defaultdict(list)
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)

    seen = set()
    contours = []
    for start in range(len(vertices)):
        if start in seen:
            continue
        pending = [start]
        seen.add(start)
        contour = []
        while pending:
            vertex = pending.pop()
            contour.append(vertex)
            for neighbor in neighbors[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    pending.append(neighbor)
        contours.append([vertices[i] for i in contour])
    return contours


class FondMouleV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        bpy.utils.register_class(ops.AddFondMoule)

    @classmethod
    def tearDownClass(cls):
        bpy.utils.unregister_class(ops.AddFondMoule)
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
        self.dif.largeur_diffuseur = 0.6
        self.dif.longueur_diffuseur = 1
        self.dif.epaisseur = 0.005
        self.dif.epaisseur_moule = 0.01
        self.dif.epaisseur_pilier = 0.005
        self.dif.cadre_epais = False
        self.dif.monopilier_mortaise_reduction = "0.20"

    def test_fond_and_pillar_base_change_but_contre_pillars_do_not(self):
        self.dif.type_moule = "mono"
        original_fond = shapes.add_fond_moule(self.dif, self.product, self.usinage)
        original_piliers = shapes.add_pilier_moule(self.dif, self.product, self.usinage, self.array)
        original_contre_piliers = shapes.add_contre_pilier_moule(self.dif, self.product, self.usinage, self.array)

        self.dif.type_moule = "mono_v2"
        new_fond = shapes.add_fond_moule(self.dif, self.product, self.usinage)
        new_piliers = shapes.add_pilier_moule(self.dif, self.product, self.usinage, self.array)
        self.assertNotEqual(original_piliers, new_piliers)
        self.assertEqual({vertex for vertex in original_piliers[0] if vertex[1] > 0},
                         {vertex for vertex in new_piliers[0] if vertex[1] > 0})
        self.assertEqual(original_contre_piliers, shapes.add_contre_pilier_moule(self.dif, self.product, self.usinage, self.array))

        original_contours = connected_contours(*original_fond[:2])
        new_contours = connected_contours(*new_fond[:2])
        self.assertEqual(Counter(map(len, original_contours)), {4: 35})
        self.assertEqual(Counter(map(len, new_contours)), {4: 23, 32: 16})
        self.assertTrue(all(abs(vertex[2]) < 1e-8 for vertex in new_fond[0]))

        outer = next(contour for contour in new_contours if len(contour) == 4 and
                     max(v[0] for v in contour) - min(v[0] for v in contour) > 0.5)
        self.assertAlmostEqual(max(v[0] for v in outer) - min(v[0] for v in outer), 0.62, places=5)
        self.assertAlmostEqual(max(v[1] for v in outer) - min(v[1] for v in outer), 0.62, places=5)

        slots = [contour for contour in new_contours if len(contour) == 4 and contour is not outer]
        self.assertEqual(len(slots), 22)
        self.assertTrue(all(abs(max(v[1] for v in slot) - min(v[1] for v in slot) - 0.005) < 1e-6
                            for slot in slots))

    def test_hole_diameter_and_edge_distances_do_not_scale(self):
        for width, length_ratio in ((0.6, 1), (0.8, 2)):
            with self.subTest(width=width, length_ratio=length_ratio):
                self.dif.largeur_diffuseur = width
                self.dif.longueur_diffuseur = length_ratio
                self.dif.type_moule = "mono_v2"
                vertices, edges, _ = shapes.add_fond_moule(self.dif, self.product, self.usinage)
                contours = connected_contours(vertices, edges)
                outer = next(c for c in contours if len(c) == 4 and
                             max(v[0] for v in c) - min(v[0] for v in c) > 0.5)
                x_max = max(v[0] for v in outer)
                y_max = max(v[1] for v in outer)
                circles = [c for c in contours if len(c) == 32]
                self.assertEqual(len(circles), 16)

                centers = []
                for circle in circles:
                    cx = sum(v[0] for v in circle) / 32
                    cy = sum(v[1] for v in circle) / 32
                    self.assertTrue(all(abs(hypot(v[0] - cx, v[1] - cy) - 0.004) < 1e-7
                                        for v in circle))
                    centers.append((cx, cy))

                for expected in ((0.03578, 0.03578),
                                 (x_max - 0.03578, y_max - 0.03578),
                                 (0.03505, y_max / 2),
                                 (x_max / 2, y_max - 0.03505),
                                 (0.00877, 0.06001),
                                 (x_max - 0.06001, y_max - 0.00877)):
                    self.assertTrue(any(hypot(cx - expected[0], cy - expected[1]) < 1e-6
                                        for cx, cy in centers), expected)

    def test_operator_creates_the_new_fond(self):
        self.dif.type_moule = "mono_v2"
        before = set(bpy.data.objects)
        self.assertEqual(bpy.ops.mesh.fond_moule(), {"FINISHED"})
        created = list(set(bpy.data.objects) - before)
        self.assertEqual(len(created), 1)
        obj = created[0]
        try:
            self.assertEqual(obj.type, "MESH")
            self.assertEqual(len(obj.data.vertices), 604)
            self.assertTrue(all(abs(v.co.z) < 1e-8 for v in obj.data.vertices))
        finally:
            bpy.data.objects.remove(obj, do_unlink=True)

    def test_too_small_fond_is_rejected_without_creating_an_object(self):
        self.dif.type_moule = "mono_v2"
        self.dif.largeur_diffuseur = 0.1
        before = set(bpy.data.objects)
        with self.assertRaisesRegex(RuntimeError, "trop petit"):
            bpy.ops.mesh.fond_moule()
        self.assertEqual(set(bpy.data.objects), before)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
