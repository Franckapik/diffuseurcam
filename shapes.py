import bpy

def add_cadre_mortaise(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    offset_mortaise_interne = difprops.offset_mortaise_interne
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    diffuseur_type_is2D = difprops.diffuseur_type_is2D

    N = difprops.type

    rang = difprops.getRang()
    longueurTotale = N * longueur_diffuseur * rang

    vertsCadre = [
        (0, 0, 0),
        (0, longueurTotale, 0),
        ((profondeur / 2 - tenon_cadre / 2), longueurTotale, 0),
        ((profondeur / 2 - tenon_cadre / 2), longueurTotale - epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), longueurTotale - epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), longueurTotale, 0),
        ((profondeur), longueurTotale, 0),
        ((profondeur), 0, 0),
        ((profondeur / 2 + tenon_cadre / 2), 0, 0),
        ((profondeur / 2 + tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), 0, 0),
    ]

    vertsMortaisesInt = []

    for k in range(1, round(N * longueur_diffuseur)):
        if diffuseur_type_is2D:
            vertsMortaisesInt += [
                (bord_cadre, rang * k, 0),
                (bord_cadre + tenon_peigne + offset_mortaise_interne, rang * k, 0),
                (
                    bord_cadre + tenon_peigne + offset_mortaise_interne,
                    rang * k - epaisseur,
                    0,
                ),
                (bord_cadre, rang * k - epaisseur, 0),
                (profondeur - bord_cadre, rang * k - epaisseur, 0),
                (profondeur - bord_cadre, rang * k, 0),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    rang * k,
                    0,
                ),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    rang * k - epaisseur,
                    0,
                ),
            ]

    edgesMortaisesInt = []

    i = 0

    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsMortaisesInt)):
        i += 1
        if i == 4 or k == len(vertsCadre):
            i = 0
            edgesMortaisesInt += [
                (k, k + 1),
                (k + 1, k + 2),
                (k + 2, k + 3),
                (k + 3, k),
            ]

    edgesCadre = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 11),
        (11, 0),
    ]

    verts = [*list(vertsCadre), *list(vertsMortaisesInt)]
    edges = [*list(edgesCadre), *list(edgesMortaisesInt)]

    return verts, edges


def add_cadre_tenon(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    offset_mortaise_interne = difprops.offset_mortaise_interne
    tenon_peigne = difprops.tenon_peigne

    N = difprops.type

    rang = difprops.getRang()

    vertsCadre = [
        (0, epaisseur, 0),
        (0, largeur_diffuseur - epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), largeur_diffuseur - epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), largeur_diffuseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), largeur_diffuseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), largeur_diffuseur - epaisseur, 0),
        ((profondeur), largeur_diffuseur - epaisseur, 0),
        ((profondeur), epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), 0, 0),
        ((profondeur / 2 - tenon_cadre / 2), 0, 0),
        ((profondeur / 2 - tenon_cadre / 2), epaisseur, 0),
    ]

    vertsMortaisesInt = []

    for k in range(1, N):
        vertsMortaisesInt += [
            (bord_cadre, rang * k, 0),
            (bord_cadre + tenon_peigne + offset_mortaise_interne, rang * k, 0),
            (
                bord_cadre + tenon_peigne + offset_mortaise_interne,
                rang * k - epaisseur,
                0,
            ),
            (bord_cadre, rang * k - epaisseur, 0),
            (profondeur - bord_cadre, rang * k - epaisseur, 0),
            (profondeur - bord_cadre, rang * k, 0),
            (
                profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                rang * k,
                0,
            ),
            (
                profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                rang * k - epaisseur,
                0,
            ),
        ]

    edgesMortaisesInt = []

    i = 0

    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsMortaisesInt)):
        i += 1
        if i == 4 or k == len(vertsCadre):
            i = 0
            edgesMortaisesInt += [
                (k, k + 1),
                (k + 1, k + 2),
                (k + 2, k + 3),
                (k + 3, k),
            ]

    edgesCadre = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 11),
        (11, 0),
    ]

    verts = [*list(vertsCadre), *list(vertsMortaisesInt)]
    edges = [*list(edgesCadre), *list(edgesMortaisesInt)]

    return verts, edges


def add_carreau(difprops):
    epaisseur = difprops.epaisseur
    largeur_diffuseur = difprops.largeur_diffuseur
    longueur_diffuseur = difprops.longueur_diffuseur
    diffuseur_type_is2D = difprops.diffuseur_type_is2D
    is_accroche = difprops.is_accroche
    N = difprops.type
    rang = difprops.getRang()

    longueurTotale = N * longueur_diffuseur * rang

    if diffuseur_type_is2D:
        vertsCadre = [(0, 0, 0), (0, rang, 0), (rang, rang, 0), (rang, 0, 0), (0, 0, 0)]
    else:
        vertsCadre = [
            (0, 0, 0),
            (0, longueurTotale, 0),
            (rang, longueurTotale, 0),
            (rang, 0, 0),
            (0, 0, 0),
        ]

    if is_accroche and diffuseur_type_is2D:
        bpy.ops.mesh.primitive_circle_add(
            radius=0.01,
            enter_editmode=True,
            align="WORLD",
            location=(rang / 2, rang / 2, 0),
            scale=(1, 1, 1),
        )

    if is_accroche and not diffuseur_type_is2D:
        bpy.ops.mesh.primitive_circle_add(
            radius=0.01,
            enter_editmode=True,
            align="WORLD",
            location=(rang / 2, longueurTotale / 5, 0),
            scale=(1, 1, 1),
        )
        bpy.ops.mesh.primitive_circle_add(
            radius=0.01,
            enter_editmode=True,
            align="WORLD",
            location=(rang / 2, longueurTotale / 5 * 4, 0),
            scale=(1, 1, 1),
        )

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre


def add_peigne_court(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_peigne = difprops.tenon_peigne

    N = difprops.type

    rang = difprops.getRang()

    peignes = []
    for k in range(1, N):
        peignes += [
            (profondeur, largeur_diffuseur - epaisseur - rang * k, 0),
            (profondeur / 2, largeur_diffuseur - epaisseur - rang * k, 0),
            (profondeur / 2, largeur_diffuseur - epaisseur - rang * k - epaisseur, 0),
            (profondeur, largeur_diffuseur - epaisseur - rang * k - epaisseur, 0),
        ]

    vertsCadre = [
        (0, epaisseur, 0),
        (0, largeur_diffuseur - epaisseur, 0),
        (bord_cadre, largeur_diffuseur - epaisseur, 0),
        (bord_cadre, largeur_diffuseur, 0),
        (bord_cadre + tenon_peigne, largeur_diffuseur, 0),
        (bord_cadre + tenon_peigne, largeur_diffuseur - epaisseur, 0),
        (profondeur - bord_cadre - tenon_peigne, largeur_diffuseur - epaisseur, 0),
        (profondeur - bord_cadre - tenon_peigne, largeur_diffuseur, 0),
        (profondeur - bord_cadre, largeur_diffuseur, 0),
        (profondeur - bord_cadre, largeur_diffuseur - epaisseur, 0),
        (profondeur, largeur_diffuseur - epaisseur, 0),
        # peignes
        *list(peignes),
        (profondeur, epaisseur, 0),
        (profondeur - bord_cadre, epaisseur, 0),
        (profondeur - bord_cadre, 0, 0),
        (profondeur - bord_cadre - tenon_peigne, 0, 0),
        (profondeur - bord_cadre - tenon_peigne, epaisseur, 0),
        (bord_cadre + tenon_peigne, epaisseur, 0),
        (bord_cadre + tenon_peigne, 0, 0),
        (bord_cadre, 0, 0),
        (bord_cadre, epaisseur, 0),
        (0, epaisseur, 0),
    ]

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre


def add_peigne_long(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    diffuseur_type_is2D = difprops.diffuseur_type_is2D


    N = difprops.type

    rang = difprops.getRang()
    longueurTotale = N * longueur_diffuseur * rang

    peignes = []
    for k in range(1, round(N * longueur_diffuseur)):
        peignes += [
            (profondeur, longueurTotale - epaisseur - rang * k, 0),
            (profondeur / 2, longueurTotale - epaisseur - rang * k, 0),
            (profondeur / 2, longueurTotale - epaisseur - rang * k - epaisseur, 0),
            (profondeur, longueurTotale - epaisseur - rang * k - epaisseur, 0),
        ]


    vertsCadre = [
        (0, epaisseur, 0),
        (0, longueurTotale - epaisseur, 0),
        (bord_cadre, longueurTotale - epaisseur, 0),
        (bord_cadre, longueurTotale, 0),
        (bord_cadre + tenon_peigne, longueurTotale, 0),
        (bord_cadre + tenon_peigne, longueurTotale - epaisseur, 0),
        (profondeur - bord_cadre - tenon_peigne, longueurTotale - epaisseur, 0),
        (profondeur - bord_cadre - tenon_peigne, longueurTotale, 0),
        (profondeur - bord_cadre, longueurTotale, 0),
        (profondeur - bord_cadre, longueurTotale - epaisseur, 0),
        (profondeur, longueurTotale - epaisseur, 0),
        # peignes
        *[x for x in peignes if diffuseur_type_is2D == True],
        (profondeur, epaisseur, 0),
        (profondeur - bord_cadre, epaisseur, 0),
        (profondeur - bord_cadre, 0, 0),
        (profondeur - bord_cadre - tenon_peigne, 0, 0),
        (profondeur - bord_cadre - tenon_peigne, epaisseur, 0),
        (bord_cadre + tenon_peigne, epaisseur, 0),
        (bord_cadre + tenon_peigne, 0, 0),
        (bord_cadre, 0, 0),
        (bord_cadre, epaisseur, 0),
        (0, epaisseur, 0),
    ]

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre
