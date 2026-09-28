"""Reconstruit materials.blend avec Blender 5.1, sans objets ni données inutilisées.

Exécution : blender -b --factory-startup --python tools/rebuild_materials.py
Le résultat est écrit dans materials.optimized.blend pour vérification avant remplacement.
"""

from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "materials.blend"
OUTPUT = ROOT / "materials.optimized.blend"

with bpy.data.libraries.load(str(SOURCE)) as (available, loaded):
    wood_name = "wood" if "wood" in available.materials else "ctp"
    if wood_name not in available.materials:
        raise RuntimeError("Le fichier source ne contient ni wood ni ctp")
    loaded.materials = [wood_name] + (["fabric"] if "fabric" in available.materials else [])

wood = bpy.data.materials[wood_name]
wood.name = "wood"
wood.use_fake_user = True

fabric = bpy.data.materials.get("fabric")
if fabric is None:
    fabric = bpy.data.materials.new("fabric")
    fabric.use_nodes = True
    bsdf = fabric.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Sheen Weight"].default_value = 0.3
    fabric.diffuse_color = (0.02, 0.02, 0.02, 1.0)
fabric.use_fake_user = True

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
bpy.data.orphans_purge(do_recursive=True)
bpy.ops.file.pack_all()

assert {material.name for material in bpy.data.materials} == {"wood", "fabric"}
assert all(image.packed_file is not None for image in bpy.data.images if image.source == "FILE")

bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT), check_existing=False, compress=True)
print(f"Matériaux nettoyés : {OUTPUT} ({OUTPUT.stat().st_size} octets)")
