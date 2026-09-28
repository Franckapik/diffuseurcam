"""À lancer avec Blender 5.1 : blender -b --factory-startup --python-exit-code 1 --python tests/test_material_asset.py"""

import sys
import unittest
from pathlib import Path

import bpy


ASSET = Path(__file__).resolve().parents[1] / "materials.blend"


class MaterialAssetTest(unittest.TestCase):
    def test_only_shared_wood_and_fabric_are_packed(self):
        bpy.ops.wm.open_mainfile(filepath=str(ASSET))
        self.assertEqual(set(bpy.data.materials.keys()), {"wood", "fabric"})
        self.assertEqual(len(bpy.data.objects), 0)

        wood = bpy.data.materials["wood"]
        fabric = bpy.data.materials["fabric"]
        self.assertTrue(wood.use_fake_user)
        self.assertTrue(fabric.use_fake_user)
        wood_images = {node.image for node in wood.node_tree.nodes
                       if node.type == "TEX_IMAGE" and node.image is not None}
        self.assertEqual(len(wood_images), 4)
        self.assertEqual({image for image in bpy.data.images if image.source == "FILE"}, wood_images)
        self.assertTrue(all(image.packed_file is not None for image in wood_images))
        self.assertFalse(any(node.type == "TEX_IMAGE" for node in fabric.node_tree.nodes))


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
