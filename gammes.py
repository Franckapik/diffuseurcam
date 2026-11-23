"""Catalogue des gammes de produits et calculs géométriques purs (sans bpy).

Chaque gamme correspond à une valeur de ``product_props.product_type``.
La valeur "3" reste réservée au moule des diffuseurs.
"""

import math


# (identifiant interne, nom commercial, description). L'ordre est celui des onglets.
GAMMES = (
    ("1", "Indik", "Diffuseur 1D"),
    ("0", "Woodik", "Diffuseur 2D"),
    ("2", "Organik", "Absorbeur : cadre bois et tissu"),
    ("4", "Stratik", "Organik avec tasseaux en façade"),
    ("5", "Trapik", "Bass trap d'angle (placeholder)"),
    ("6", "Mobilik", "Mobilik (placeholder sur base Organik)"),
    ("7", "Cloudik", "Cloud acoustique suspendu au plafond"),
)
GAMME_NAMES = {identifier: name for identifier, name, _description in GAMMES}

DIFFUSEURS = frozenset({"0", "1"})
# Gammes construites sur le cadre + tissu Organik (largeur, longueur, profondeur).
FAMILLE_ORGANIK = frozenset({"2", "4", "6", "7"})
# Gammes dont les pièces CAM sont exactement celles d'Organik. Cloudik (épaisseur de
# cadre propre), Trapik et Mobilik (placeholders) n'ont pas encore de pièces CAM.
CAM_ORGANIK = frozenset({"2", "4"})

# Lettre de référence catalogue de chaque gamme hors diffuseurs (D1/D2).
PREFIXES = {"2": "A", "4": "S", "5": "T", "6": "K", "7": "C"}


def cam_product_type(product_type):
    """Type utilisé par les pièces CAM, ou None si la gamme n'en a pas encore."""
    if product_type in DIFFUSEURS:
        return product_type
    if product_type in CAM_ORGANIK:
        return "2"
    return None


def _part(value):
    """Nombre de la nomenclature : 60 → '60', 60.5 → '60p5'."""
    return f"{value:.4f}".rstrip("0").rstrip(".").replace(".", "p")


def panel_reference(product_type, width_m, depth_m, ratio, gap=None):
    """Référence d'un panneau de la famille Organik : A0W60P10L2, S0W60P10L2G30…

    W et P en cm, L = longueur / largeur, G = % de vide visé (Stratik).
    """
    reference = (
        f"{PREFIXES[product_type]}0W{_part(width_m * 100)}"
        f"P{_part(depth_m * 100)}L{_part(ratio)}"
    )
    if gap is not None:
        reference += f"G{_part(gap)}"
    return reference


def trapik_reference(a_m, b_m, h_m):
    """Référence Trapik : T0A30B30H120 (côtés et hauteur en cm)."""
    return f"T0A{_part(a_m * 100)}B{_part(b_m * 100)}H{_part(h_m * 100)}"


def stratik_layout(span, largeur, pourcentage, nombre_force=0):
    """Répartit les tasseaux sur ``span`` avec un tasseau affleurant chaque bord.

    pourcentage : part de vide visée en façade (0–100).
    nombre_force : si > 0, impose le nombre de tasseaux au lieu du pourcentage.
    Retourne n, le vide entre deux tasseaux, le % de vide obtenu et la position
    du bord de chaque tasseau depuis l'origine.
    """
    if not (math.isfinite(span) and math.isfinite(largeur) and span > 0 and largeur > 0):
        raise ValueError("Dimensions des tasseaux invalides")
    n_max = math.floor(span / largeur + 1e-9)
    if n_max < 2:
        raise ValueError(
            f"{span * 1000:.0f} mm ne suffisent pas pour deux tasseaux de {largeur * 1000:.0f} mm"
        )
    if nombre_force:
        n = int(nombre_force)
    else:
        n = math.floor((1 - pourcentage / 100) * span / largeur + 0.5)
    n = max(2, min(n_max, n))
    vide = (span - n * largeur) / (n - 1)
    return {
        "n": n,
        "vide": vide,
        "ajoure": 100 * (span - n * largeur) / span,
        "positions": [k * (largeur + vide) for k in range(n)],
    }


def trapik_section(a, b):
    """Section du prisme d'angle dont les côtés a et b sont contre les murs.

    Retourne (c, h, xc) : largeur de la face avant (hypoténuse), profondeur
    du coin à la face avant, et abscisse du coin projeté sur la face avant.
    """
    if not (a > 0 and b > 0):
        raise ValueError("Côtés du Trapik invalides")
    c = math.hypot(a, b)
    return c, a * b / c, a * a / c
