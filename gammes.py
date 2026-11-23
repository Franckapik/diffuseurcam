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
    ("5", "Trapik", "Bass trap d'angle polycylindrique à tasseaux"),
    ("6", "Mobilik", "Mobilik (placeholder sur base Organik)"),
    ("7", "Cloudik", "Cloud acoustique suspendu au plafond"),
)
GAMME_NAMES = {identifier: name for identifier, name, _description in GAMMES}

DIFFUSEURS = frozenset({"0", "1"})
# Gammes construites sur le cadre + tissu Organik (largeur, longueur, profondeur).
FAMILLE_ORGANIK = frozenset({"2", "4", "6", "7"})
# Gammes dont les pièces CAM sont exactement celles d'Organik. Cloudik (épaisseur de
# cadre propre), Trapik (pièces propres) et Mobilik (placeholder) n'ont pas encore de pièces CAM.
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


def trapik_reference(cote_m, hauteur_m, gap=None):
    """Référence Trapik : T0A42B42H120G50.

    A = B = côté contre les murs et H = hauteur hors tout, en cm ; G = % de vide visé.
    """
    cote = _part(cote_m * 100)
    reference = f"T0A{cote}B{cote}H{_part(hauteur_m * 100)}"
    if gap is not None:
        reference += f"G{_part(gap)}"
    return reference


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


# ── Trapik ────────────────────────────────────────────────────────────────
# Repère du plan : coin de la pièce à l'origine, côté A contre le mur y = 0, côté B
# contre le mur x = 0, hauteur selon z. Les deux côtés sont égaux (A = B).
TRAPIK_JEU_TISSU = 0.001          # recul des cerces derrière le tissu (évite le z-fighting)
TRAPIK_PAS_DOIGTS = 0.17          # pas visé des doigts de l'assemblage d'angle des côtés
TRAPIK_VIDE_MIN = 0.002           # vide minimal entre deux tasseaux, mesuré au tissu
TRAPIK_PAS_ARC = math.radians(3)  # pas angulaire maximal des arcs facettés


def _arc_angles(start, end, step=TRAPIK_PAS_ARC):
    """Angles régulièrement espacés de ``start`` à ``end``, bornes comprises."""
    count = max(1, math.ceil(abs(end - start) / step - 1e-9))
    return [start + (end - start) * i / count for i in range(count + 1)]


def _arc(center, radius, start, end):
    return [(center[0] + radius * math.cos(a), center[1] + radius * math.sin(a))
            for a in _arc_angles(start, end)]


def _dedupe(points, tolerance=1e-9):
    """Retire les points consécutifs confondus (et la fermeture explicite du contour)."""
    result = []
    for point in points:
        if not result or math.dist(point, result[-1]) > tolerance:
            result.append(point)
    if len(result) > 1 and math.dist(result[0], result[-1]) <= tolerance:
        result.pop()
    return result


def trapik_layout(cote, hauteur, *, largeur_tasseau, epaisseur_tasseau, pourcentage,
                  nombre_force=0, epaisseur_cote, epaisseur_plateau, epaisseur_finition,
                  epaisseur_cerce, largeur_cerce, nombre_cerces):
    """Géométrie complète d'un Trapik dans le repère du plan (voir plus haut).

    Façade : arc de centre (c, c), avec c = largeur_tasseau / 2, et de rayon
    ``rayon_tissu`` = cote - c. Les tasseaux d'extrémité sont centrés à 0° et 90° et
    couvrent le chant des côtés. Le tissu suit cet arc, derrière les tasseaux, et le
    % ajouré se mesure le long de l'arc du tissu.

    Verticalement (hauteur hors tout) : finition tissu, plateau crénelé, intérieur
    (côtés, cerces, tissu), plateau crénelé, finition tissu. Les tasseaux traversent
    les plateaux et vont d'une finition à l'autre.

    Plateaux : dents jusqu'au rayon de façade entre les tasseaux, et mortaises ouvertes
    de la section exacte des tasseaux, où ceux-ci s'encastrent. Les finitions sont des
    quarts de disque lisses de même rayon qui couvrent le plateau et les bouts de tasseaux.

    Les cerces sont réparties sur l'intérieur, les deux extrêmes contre les plateaux.
    Chaque bout de cerce porte un tenon (tiers central) qui traverse le côté. Les deux
    côtés s'assemblent dans l'angle par des doigts alternés (nombre impair).
    """
    w, t = largeur_tasseau, epaisseur_tasseau
    e_c, e_p, e_f = epaisseur_cote, epaisseur_plateau, epaisseur_finition
    e_r, l_r = epaisseur_cerce, largeur_cerce
    dimensions = (cote, hauteur, w, t, e_c, e_p, e_f, e_r, l_r)
    if not all(math.isfinite(value) and value > 0 for value in dimensions):
        raise ValueError("Dimensions du Trapik invalides")
    if int(nombre_cerces) < 2:
        raise ValueError("Il faut au moins deux cerces")

    c = w / 2
    r_tissu = cote - c
    if r_tissu <= w:
        raise ValueError("Côté trop petit pour la largeur des tasseaux")
    r_facade = r_tissu + t

    # ── Tasseaux : répartition le long de l'arc du tissu ──────────────────
    span = math.pi / 2 * r_tissu + w
    n_max = math.floor((span + TRAPIK_VIDE_MIN) / (w + TRAPIK_VIDE_MIN) + 1e-9)
    if n_max < 2:
        raise ValueError("Façade trop courte pour deux tasseaux")
    tasseaux = stratik_layout(span, w, pourcentage, nombre_force)
    if tasseaux["n"] > n_max:
        tasseaux = stratik_layout(span, w, pourcentage, n_max)
    angles = [position / r_tissu for position in tasseaux["positions"]]
    # Demi-ouverture angulaire d'un tasseau sur l'arc du tissu.
    phi = math.asin(c / r_tissu)
    if angles[1] - angles[0] <= 2 * phi:
        raise ValueError("Tasseaux jointifs : augmentez le % ajouré")

    def corner(theta, radius, side):
        """Coin d'un tasseau : ``radius`` le long de l'axe, ``side`` = ±1 de part et d'autre."""
        cos, sin = math.cos(theta), math.sin(theta)
        return (c + radius * cos - side * c * sin, c + radius * sin + side * c * cos)

    slats = [[corner(a, r_tissu, -1), corner(a, r_facade, -1),
              corner(a, r_facade, 1), corner(a, r_tissu, 1)] for a in angles]
    vide_facade = math.dist(corner(angles[0], r_facade, 1), corner(angles[1], r_facade, -1))

    # Tissu : arc continu derrière les tasseaux, avec des sommets aux bords de chaque tasseau.
    tissu_angles = [angles[0]]
    for k in range(1, len(angles)):
        tissu_angles += _arc_angles(angles[k - 1] + phi, angles[k] - phi) + [angles[k]]
    tissu = [(c + r_tissu * math.cos(a), c + r_tissu * math.sin(a)) for a in tissu_angles]

    # Plateau : dents en arc de rayon r_facade entre les tasseaux, mortaise au droit de
    # chacun (joues le long des flancs du tasseau, fond contre son dos).
    psi = math.asin(c / r_facade)
    plateau = [(0.0, 0.0)]
    for k, theta in enumerate(angles):
        if k:
            plateau += _arc((c, c), r_facade, angles[k - 1] + psi, theta - psi)
        plateau += [corner(theta, r_tissu, -1), corner(theta, r_tissu, 1)]
    finition = [(0.0, 0.0), (cote + t, 0.0)] + _arc((c, c), r_facade, 0, math.pi / 2) + [(0.0, cote + t)]

    # ── Niveaux ───────────────────────────────────────────────────────────
    z0 = e_f + e_p
    z1 = hauteur - z0
    interieur = z1 - z0
    nombre_cerces = int(nombre_cerces)
    pas_cerces = (interieur - e_r) / (nombre_cerces - 1)
    if pas_cerces <= e_r:
        raise ValueError("Hauteur insuffisante pour les plateaux et les cerces")
    cerces = [(z0 + k * pas_cerces, z0 + k * pas_cerces + e_r) for k in range(nombre_cerces)]
    nombre_doigts = max(3, round(interieur / TRAPIK_PAS_DOIGTS))
    if nombre_doigts % 2 == 0:
        nombre_doigts += 1
    doigts = [(z0 + interieur * i / nombre_doigts, z0 + interieur * (i + 1) / nombre_doigts,
               "A" if i % 2 == 0 else "B") for i in range(nombre_doigts)]

    # ── Cerce : arc extérieur sous le tissu, arc intérieur centré sur le coin ──
    r_ext = r_tissu - TRAPIK_JEU_TISSU
    r_int = cote - l_r
    if l_r <= TRAPIK_JEU_TISSU or r_int <= e_c * math.sqrt(2):
        raise ValueError("Largeur de cerce incompatible avec le côté")
    x_int = math.sqrt(r_int ** 2 - e_c ** 2)
    if c >= e_c:
        x_ext = c + r_ext
        contour_ext = [(x_ext, e_c)] + _arc((c, c), r_ext, 0, math.pi / 2) + [(e_c, x_ext)]
    else:
        start = math.asin((e_c - c) / r_ext)
        x_ext = c + r_ext * math.cos(start)
        contour_ext = _arc((c, c), r_ext, start, math.pi / 2 - start)
    if x_ext - x_int < 0.015:
        raise ValueError("Cerces trop étroites pour leurs tenons")
    t0 = x_int + (x_ext - x_int) / 3
    t1 = x_int + 2 * (x_ext - x_int) / 3
    cerce = ([(x_int, e_c), (t0, e_c), (t0, 0.0), (t1, 0.0), (t1, e_c)] + contour_ext
             + [(e_c, t1), (0.0, t1), (0.0, t0), (e_c, t0), (e_c, x_int)]
             + _arc((0.0, 0.0), r_int, math.atan2(x_int, e_c), math.atan2(e_c, x_int))[1:-1])

    plateau, finition, cerce = _dedupe(plateau), _dedupe(finition), _dedupe(cerce)
    return {
        "cote": cote,
        "hauteur": hauteur,
        "centre": c,
        "rayon_tissu": r_tissu,
        "rayon_facade": r_facade,
        "n": tasseaux["n"],
        "vide": tasseaux["vide"],
        "vide_facade": vide_facade,
        "ajoure": tasseaux["ajoure"],
        "angles": angles,
        "tasseaux": slats,
        "tissu": tissu,
        "plateau": plateau,
        "finition": finition,
        "cerce": cerce,
        "tenon": (t0, t1),
        "epaisseur_cote": e_c,
        "niveaux": {
            "finition_bas": (0.0, e_f),
            "plateau_bas": (e_f, z0),
            "interieur": (z0, z1),
            "plateau_haut": (z1, z1 + e_p),
            "finition_haut": (hauteur - e_f, hauteur),
            "tasseaux": (e_f, hauteur - e_f),
        },
        "cerces": cerces,
        "doigts": doigts,
        "emprise": cote + t,
        # Distance du coin à la façade, mesurée selon la bissectrice.
        "profondeur": max((x + y) / math.sqrt(2)
                          for x, y in plateau + finition + [p for slat in slats for p in slat]),
    }
