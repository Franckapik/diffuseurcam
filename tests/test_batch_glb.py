"""À lancer avec : blender -b --factory-startup --python-exit-code 1 --python tests/test_batch_glb.py"""

import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from diffuseurcam import ops, props  # noqa: E402


def read_glb(path):
    data = path.read_bytes()
    magic, version, total_length = struct.unpack_from('<4sII', data)
    assert (magic, version, total_length) == (b'glTF', 2, len(data))
    chunk_length, chunk_type = struct.unpack_from('<I4s', data, 12)
    assert chunk_type == b'JSON'
    return json.loads(data[20:20 + chunk_length].decode('utf-8'))


class BatchGLBTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        props.register()
        bpy.utils.register_class(ops.ExportBatch3DGLB)

    @classmethod
    def tearDownClass(cls):
        bpy.utils.unregister_class(ops.ExportBatch3DGLB)
        props.unregister()

    def test_one_glb_per_batch_object_with_material_and_no_grid_offset(self):
        scene = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        collections = []
        material_names = ("Batch Rouge", "Batch Vert")
        for name, location, material_name, color in (
            ("Batch_3D_1x", (10, 0, 0), material_names[0], (0.8, 0.1, 0.1, 1)),
            ("Batch_3D_1x.001", (20, 0, 0), material_names[1], (0.1, 0.8, 0.1, 1)),
        ):
            collection = bpy.data.collections.new(name)
            scene.collection.children.link(collection)
            collections.append(collection)
            bpy.ops.mesh.primitive_cube_add(size=1, location=location)
            obj = bpy.context.object
            obj.name = "D1N7W50P5L1E5" if location[0] == 10 else "D2N7W50P5L1E5"
            material = bpy.data.materials.new(material_name)
            material.use_nodes = True
            material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value = color
            obj.data.materials.append(material)
            for source in list(obj.users_collection):
                source.objects.unlink(obj)
            collection.objects.link(obj)
            if location[0] == 20:
                obj.hide_set(True)

        bpy.ops.mesh.primitive_cube_add(location=(30, 0, 0))
        unrelated = bpy.context.object
        with tempfile.TemporaryDirectory() as directory:
            scene.batch_3d_props.batch_stl_directory = directory
            self.assertEqual(bpy.ops.mesh.export_batch_3d_glb(), {'FINISHED'})
            paths = sorted(Path(directory).glob('*.glb'))
            self.assertEqual([path.stem for path in paths], ["D1N7W50P5L1E5", "D2N7W50P5L1E5"])
            for path, material_name in zip(paths, material_names):
                glb = read_glb(path)
                self.assertEqual(len(glb['meshes']), 1)
                self.assertEqual([mat['name'] for mat in glb['materials']], [material_name])
                self.assertEqual(glb['meshes'][0]['primitives'][0]['material'], 0)
                self.assertTrue(all(all(abs(value) < 1e-5 for value in node.get('translation', (0, 0, 0)))
                                    for node in glb['nodes']))

        self.assertEqual(bpy.context.view_layer.objects.active, unrelated)
        self.assertEqual(set(bpy.context.selected_objects), {unrelated})
        self.assertEqual(collections[0].objects[0].location.x, 10)
        self.assertEqual(collections[1].objects[0].location.x, 20)
        self.assertTrue(collections[1].objects[0].hide_get())
        for collection in collections:
            bpy.data.collections.remove(collection)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]])
