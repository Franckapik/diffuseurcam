"""Débit des pièces du produit courant, avant l'usinage des contours."""

import csv
import re
import unicodedata
from collections import defaultdict

from . import shapes


# Le nom vient de la même fonction que celle utilisée par les opérateurs de génération.
PRODUCT_PARTS = {
    "0": (
        ("cadre_mortaise", shapes.add_cadre_mortaise),
        ("cadre_tenon", shapes.add_cadre_tenon),
        ("peigne_court", shapes.add_peigne_court),
        ("peigne_long", shapes.add_peigne_long),
        ("carreau", shapes.add_carreau),
        ("accroche", shapes.add_accroche),
    ),
    "1": (
        ("cadre_mortaise", shapes.add_cadre_mortaise),
        ("cadre_tenon", shapes.add_cadre_tenon),
        ("peigne_long", shapes.add_peigne_long),
        ("carreau", shapes.add_carreau),
        ("accroche", shapes.add_accroche),
    ),
    "2": (
        ("cadre_mortaise", shapes.add_cadre_mortaise),
        ("cadre_tenon", shapes.add_cadre_tenon),
        ("accroche", shapes.add_accroche),
        ("accroche_inverse", shapes.add_accroche),
        ("renfort_central", shapes.add_renfort_central),
        ("renfort_angle", shapes.add_renfort_angle),
        ("cadre_tissu_court", shapes.add_cadre_tissu_court),
        ("cadre_tissu_long", shapes.add_cadre_tissu_long),
    ),
}


def _millimetres(metres):
    """Arrondit à 0,01 mm pour éliminer le bruit des nombres flottants."""
    return round(metres * 1000, 2)


def _number(value, decimal_separator=","):
    return f"{value:.2f}".rstrip("0").rstrip(".").replace(".", decimal_separator)


def _label(name, profondeur):
    words = re.findall(r"[A-Za-zÀ-ÿ]+", name)
    initials = "".join(
        unicodedata.normalize("NFKD", word)[0].upper() for word in words
    )
    # Même convention que l'exemple : 150 mm de profondeur donne le suffixe 15.
    return initials + _number(_millimetres(profondeur) / 10, ".")


def _part_geometry(part_key, generator, scene):
    args = (scene.dif_props, scene.product_props, scene.usinage_props)
    if part_key in {"cadre_tissu_court", "cadre_tissu_long"}:
        return generator(*args, scene.array_props)
    if part_key in {"accroche", "accroche_inverse"}:
        return generator(*args, part_key == "accroche_inverse")
    return generator(*args)


def build_cutlist(scene):
    """Retourne (label, nom, longueur_mm, largeur_mm, épaisseur_mm, quantité)."""
    product = scene.product_props.product_type
    if product not in PRODUCT_PARTS:
        raise ValueError("Type de produit non pris en charge")

    rows = defaultdict(int)
    for part_key, generator in PRODUCT_PARTS[product]:
        counts = (
            getattr(scene.array_props, part_key + "_x"),
            getattr(scene.array_props, part_key + "_y"),
        )
        quantity = counts[0] * counts[1] * scene.devis_props.qtyDif
        if quantity == 0:
            continue

        vertices, _edges, name = _part_geometry(part_key, generator, scene)
        if not vertices:
            raise ValueError(f"Aucune géométrie pour {name}")
        size_x = _millimetres(max(v[0] for v in vertices) - min(v[0] for v in vertices))
        size_y = _millimetres(max(v[1] for v in vertices) - min(v[1] for v in vertices))
        length, width = sorted((size_x, size_y), reverse=True)
        if width <= 0:
            raise ValueError(f"Dimensions invalides pour {name}")
        thickness = (
            scene.dif_props.getEpaisseurCadre()
            if part_key in {"cadre_mortaise", "cadre_tenon"}
            else scene.dif_props.epaisseur
        )
        key = (_label(name, scene.dif_props.profondeur), name, length, width, _millimetres(thickness))
        rows[key] += quantity

    return [(*key, quantity) for key, quantity in rows.items()]


def write_cutlist_csv(path, rows):
    # BOM UTF-8 : Excel reconnaît directement les accents. Le point-virgule et la
    # virgule décimale correspondent aux paramètres habituels d'un tableur FR.
    with open(path, "w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerow((
            "Label", "Nom de la pièce", "Longueur (mm)", "Largeur (mm)",
            "Épaisseur (mm)", "Quantité",
        ))
        for label, name, length, width, thickness, quantity in rows:
            writer.writerow((label, name, _number(length), _number(width), _number(thickness), quantity))
