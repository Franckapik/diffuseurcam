"""Contrôles du conteneur GLB destiné à QuadraRoom."""

import json
import math
import re
import struct


_PRODUCT_NAME = re.compile(
    r"(?:D[12]N\d+W\d+(?:p\d+)?P\d+(?:p\d+)?L\d+(?:p\d+)?"
    r"|A\d+W\d+(?:p\d+)?P\d+(?:p\d+)?L\d+(?:p\d+)?)"
    r"(?:E\d+(?:p\d+)?)?"
)


def is_product_reference(name):
    base = re.sub(r"\.\d{3}$", "", name)
    return _PRODUCT_NAME.fullmatch(base) is not None


def product_stem(name, thickness_m):
    """Ajoute E{épaisseur mm} aux références qui n'en disposent pas encore."""
    match = re.fullmatch(r"(.+?)(\.\d{3})?", name)
    base, _duplicate_suffix = match.groups()
    if not _PRODUCT_NAME.fullmatch(base):
        return None
    if not re.search(r"E\d+(?:p\d+)?$", base):
        thickness_mm = thickness_m * 1000
        if not math.isfinite(thickness_mm) or thickness_mm <= 0:
            raise ValueError("Épaisseur invalide pour compléter la référence produit")
        thickness = f"{thickness_mm:.3f}".rstrip("0").rstrip(".").replace(".", "p")
        base += "E" + thickness
    return base


def read_glb(path):
    """Lit le JSON et conserve à l'identique les blocs binaires du GLB."""
    data = path.read_bytes()
    if len(data) < 20:
        raise ValueError("GLB incomplet")
    magic, version, declared_length = struct.unpack_from("<4sII", data)
    if magic != b"glTF" or version != 2 or declared_length != len(data):
        raise ValueError("En-tête GLB invalide")
    json_length, chunk_type = struct.unpack_from("<I4s", data, 12)
    if chunk_type != b"JSON" or 20 + json_length > len(data):
        raise ValueError("Bloc JSON GLB invalide")
    document = json.loads(data[20:20 + json_length].decode("utf-8"))
    return document, data[20 + json_length:]


def validate_quadraroom_glb(document, expected_materials):
    """Vérifie la structure requise par les textures chargées dans QuadraRoom."""
    if document.get("images") or document.get("textures"):
        raise ValueError("Le GLB contient encore des images ou des textures")

    materials = document.get("materials", [])
    material_names = [material.get("name") for material in materials]
    if len(material_names) != len(set(material_names)):
        raise ValueError("Le GLB contient des noms de matériaux en double")
    if set(material_names) != set(expected_materials):
        raise ValueError(f"Matériaux GLB inattendus : {material_names}")

    used_materials = set()
    meshes = document.get("meshes", [])
    if not meshes:
        raise ValueError("Le GLB ne contient aucun maillage")
    for mesh in meshes:
        for primitive in mesh.get("primitives", []):
            index = primitive.get("material")
            if not isinstance(index, int) or not 0 <= index < len(materials):
                raise ValueError("Une primitive GLB a perdu son affectation de matériau")
            used_materials.add(material_names[index])
            attributes = primitive.get("attributes", {})
            for attribute in ("POSITION", "NORMAL", "TEXCOORD_0"):
                if attribute not in attributes:
                    raise ValueError(f"La primitive {material_names[index]} n'a pas {attribute}")
    if used_materials != set(expected_materials):
        raise ValueError("Les groupes de faces par matériau ne correspondent pas à la scène")

