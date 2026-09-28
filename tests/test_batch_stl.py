"""À lancer avec : blender -b --factory-startup --python-exit-code 1 --python tests/test_batch_stl.py"""

import struct
import sys
import tempfile
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props  # noqa: E402


def stl_bounds(path):
    data = path.read_bytes()
    triangle_count = struct.unpack_from('<I', data, 80)[0]
    assert len(data) == 84 + triangle_count * 50
    vertices = [
        struct.unpack_from('<fff', data, 84 + i * 50 + 12 + vertex * 12)
        for i in range(triangle_count)
        for vertex in range(3)
    ]
    return tuple((min(p[axis] for p in vertices), max(p[axis] for p in vertices)) for axis in range(3))


class BatchSTLTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        bpy.utils.register_class(ops.ExportBatch3DSTL)

    @classmethod
    def tearDownClass(cls):
        bpy.utils.unregister_class(ops.ExportBatch3DSTL)
        props.unregister()

    def test_one_stl_per_batch_object_in_mm_without_grid_offset(self):
        scene = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        collections = []
        for name, location in (("Batch_3D_1x", (10, 0, 0)), ("Batch_3D_1x.001", (20, 0, 0))):
            collection = bpy.data.collections.new(name)
            scene.collection.children.link(collection)
            collections.append(collection)
            bpy.ops.mesh.primitive_cube_add(size=1, location=location)
            obj = bpy.context.object
            obj.name = "D1N7W50P5L1E5" if location[0] == 10 else "D2N7W50P5L1E5"
            for source in list(obj.users_collection):
                source.objects.unlink(obj)
            collection.objects.link(obj)
            if location[0] == 20:
                obj.hide_set(True)

        bpy.ops.mesh.primitive_cube_add(location=(30, 0, 0))
        unrelated = bpy.context.object
        with tempfile.TemporaryDirectory() as directory:
            scene.batch_3d_props.batch_stl_directory = directory
            result = bpy.ops.mesh.export_batch_3d_stl()
            self.assertEqual(result, {'FINISHED'})
            paths = sorted(Path(directory).glob('*.stl'))
            self.assertEqual([path.stem for path in paths], ["D1N7W50P5L1E5", "D2N7W50P5L1E5"])
            for path in paths:
                for actual, expected in zip(stl_bounds(path), ((-500, 500), (-500, 500), (-500, 500))):
                    self.assertAlmostEqual(actual[0], expected[0], places=3)
                    self.assertAlmostEqual(actual[1], expected[1], places=3)

        self.assertEqual(bpy.context.view_layer.objects.active, unrelated)
        self.assertEqual(set(bpy.context.selected_objects), {unrelated})
        self.assertEqual(len([obj for obj in bpy.data.objects if obj.name.startswith('D')]), 2)
        self.assertEqual(collections[0].objects[0].location.x, 10)
        self.assertEqual(collections[1].objects[0].location.x, 20)
        self.assertTrue(collections[1].objects[0].hide_get())
        for collection in collections:
            bpy.data.collections.remove(collection)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
