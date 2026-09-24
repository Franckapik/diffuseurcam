"""À lancer avec : blender -b --factory-startup --python-exit-code 1 --python tests/test_precision.py"""

import csv
import sys
import tempfile
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import props  # noqa: E402
from diffuseurcam.cutlist import build_cutlist, write_cutlist_csv  # noqa: E402


class PrecisionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()

    def setUp(self):
        self.scene = bpy.context.scene
        self.dif = self.scene.dif_props
        self.dif.type = 11
        self.dif.largeur_diffuseur = 0.6
        self.dif.epaisseur = 0.005
        self.dif.cadre_epais = False
        self.dif.epaisseur_cadre = 0.015
        self.dif.profondeur = 0.15
        self.dif.longueur_diffuseur = 1

    def test_width_and_square_tiles(self):
        for product in ("0", "1"):
            with self.subTest(product=product):
                self.scene.product_props.product_type = product
                self.assertAlmostEqual(self.dif.getLongueur(), self.dif.largeur_diffuseur, places=6)
                rows = build_cutlist(self.scene)
                frame = next(row for row in rows if row[1] == "Cadre mortaise")
                tile = next(row for row in rows if row[1] == "Carreau")
                self.assertEqual(frame[2], 600)
                self.assertEqual(tile[3], 49.09)
                self.assertEqual(tile[2], 49.09 if product == "0" else 590)

    def test_thick_frame_and_long_product(self):
        self.scene.product_props.product_type = "0"
        self.dif.cadre_epais = True
        self.assertAlmostEqual(self.dif.getLongueur(), 0.6, places=6)
        self.assertEqual(next(row for row in build_cutlist(self.scene) if row[1] == "Carreau")[2:4], (47.27, 47.27))
        self.dif.longueur_diffuseur = 2
        self.assertAlmostEqual(self.dif.getLongueur(), 1.175, places=6)

    def test_width_576_does_not_shrink(self):
        self.scene.product_props.product_type = "1"
        self.dif.largeur_diffuseur = 0.576
        self.assertAlmostEqual(self.dif.getLongueur(), 0.576, places=6)
        rows = build_cutlist(self.scene)
        frame = next(row for row in rows if row[1] == "Cadre mortaise")
        tile = next(row for row in rows if row[1] == "Carreau")
        self.assertEqual(frame[2], 576)
        self.assertEqual(tile[2:4], (566, 46.91))

    def test_csv_keeps_hundredth_millimetre(self):
        self.scene.product_props.product_type = "0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "debit.csv"
            write_cutlist_csv(path, build_cutlist(self.scene))
            with path.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream, delimiter=";"))
        tile = next(row for row in rows if row[1] == "Carreau")
        self.assertEqual(tile[2:5], ["49,09", "49,09", "5"])


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
