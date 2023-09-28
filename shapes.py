from .pattern import *


def add_cadre_mortaise(difprops, productprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    bord_cadre = difprops.bord_cadre
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    largeur_accroche = difprops.largeur_accroche
    cadre_avant = difprops.cadre_avant
    cadre_central = difprops.cadre_central
    product_type = productprops.product_type
    startup = epaisseur / 2
    N = difprops.type
    rang = difprops.getRang()
    longueurTotale = difprops.getLongueur()

    edgesCadre = []
    vertsMortaisesInt = []
    edgesMortaisesInt = []

    if product_type == "0" or product_type == "1":
        vertsCadre = [
            (0, 0, 0),
            (0, longueurTotale, 0),
            *mortaiseHaut((profondeur / 2 - tenon_cadre / 2), longueurTotale, difprops),
            ((profondeur), longueurTotale, 0),
            ((profondeur), 0, 0),
            *mortaiseBas((profondeur / 2 + tenon_cadre / 2), 0, difprops),
        ]

        for k in range(1, round(N * longueur_diffuseur)):
            if product_type == "0":
                vertsMortaisesInt += [
                    *mortaiseInt(bord_cadre, (startup + rang * k), difprops),
                    *mortaiseInt(
                        profondeur - bord_cadre - tenon_peigne,
                        (startup + rang * k),
                        difprops,
                    ),
                ]

    if product_type == "2":
        vertsCadre = [
            (0, 0, 0),
            *mortaiseGauche(0, (largeur_accroche / 2 - tenon_cadre / 2), difprops),
            *mortaiseGauche(
                0,
                (longueurTotale - largeur_accroche / 2 - tenon_cadre / 2),
                difprops,
            ),
            (0, longueurTotale, 0),
            *mortaiseHaut((profondeur / 2 - tenon_cadre / 2), longueurTotale, difprops),
            ((profondeur), longueurTotale, 0),
            *(
                a
                for a in mortaiseDroite(
                    profondeur,
                    longueurTotale - largeur_accroche / 2 + tenon_cadre / 2,
                    difprops,
                )
                if cadre_avant == True
            ),
            *(
                a
                for a in mortaiseDroite(
                    profondeur, longueurTotale / 2 + tenon_cadre / 2, difprops
                )
                if cadre_central == True
            ),
            *(
                a
                for a in mortaiseDroite(
                    profondeur, largeur_accroche / 2 + tenon_cadre / 2, difprops
                )
                if cadre_avant == True
            ),
            ((profondeur), 0, 0),
            *mortaiseBas((profondeur / 2 + tenon_cadre / 2), 0, difprops),
        ]

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

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    verts = [*list(vertsCadre), *list(vertsMortaisesInt)]
    edges = [*list(edgesCadre), *list(edgesMortaisesInt)]

    return verts, edges, "Cadre mortaise"


def add_cadre_tenon(difprops, productprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_peigne = difprops.tenon_peigne
    startup = epaisseur / 2
    product_type = productprops.product_type
    largeur_accroche = difprops.largeur_accroche
    cadre_avant = difprops.cadre_avant

    N = difprops.type

    rang = difprops.getRang()

    edgesCadre = []
    vertsMortaisesInt = []
    edgesMortaisesInt = []

    if product_type == "0" or product_type == "1":
        vertsCadre = [
            (0, epaisseur, 0),
            (0, largeur_diffuseur - epaisseur, 0),
            *tenonHaut(
                (profondeur / 2 - tenon_cadre / 2),
                largeur_diffuseur - epaisseur,
                difprops,
            ),
            ((profondeur), largeur_diffuseur - epaisseur, 0),
            ((profondeur), epaisseur, 0),
            *tenonBas((profondeur / 2 + tenon_cadre / 2), epaisseur, difprops),
        ]

        for k in range(1, round(N)):
            vertsMortaisesInt += [
                *mortaiseInt(bord_cadre, (startup + rang * k), difprops),
                *mortaiseInt(
                    profondeur - bord_cadre - tenon_peigne,
                    (startup + rang * k),
                    difprops,
                ),
            ]

    if product_type == "2":
        vertsCadre = [
            (0, epaisseur, 0),
            *mortaiseGauche(0, largeur_accroche / 2 - tenon_cadre / 2, difprops),
            *mortaiseGauche(
                0, largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2, difprops
            ),
            (0, largeur_diffuseur - epaisseur, 0),
            *tenonHaut(
                (profondeur / 2 - tenon_cadre / 2),
                largeur_diffuseur - epaisseur,
                difprops,
            ),
            ((profondeur), largeur_diffuseur - epaisseur, 0),
            *(
                a
                for a in mortaiseDroite(
                    profondeur,
                    largeur_diffuseur - largeur_accroche / 2 + tenon_cadre / 2,
                    difprops,
                )
                if cadre_avant == True
            ),
            *(
                a
                for a in mortaiseDroite(
                    profondeur, largeur_accroche / 2 + tenon_cadre / 2, difprops
                )
                if cadre_avant == True
            ),
            ((profondeur), epaisseur, 0),
            *tenonBas((profondeur / 2 + tenon_cadre / 2), epaisseur, difprops),
        ]

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

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    verts = [*list(vertsCadre), *list(vertsMortaisesInt)]
    edges = [*list(edgesCadre), *list(edgesMortaisesInt)]

    return verts, edges, "Cadre tenon"


def add_peigne_court(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_peigne = difprops.tenon_peigne
    offset = difprops.offset

    N = difprops.type

    rang = difprops.getRang()

    peignes = []
    for k in range(1, N):
        peignes += [
            (profondeur, largeur_diffuseur - rang * k + offset, 0),
            (profondeur / 2 - 0.005, largeur_diffuseur - rang * k + offset, 0),
            (
                profondeur / 2 - 0.005,
                largeur_diffuseur - rang * k - epaisseur - offset,
                0,
            ),
            (profondeur, largeur_diffuseur - rang * k - epaisseur - offset, 0),
        ]

    vertsCadre = [
        (0, epaisseur, 0),
        (0, largeur_diffuseur - epaisseur, 0),
        *tenonPeigneHaut(bord_cadre, largeur_diffuseur - epaisseur, difprops),
        *tenonPeigneHaut(
            profondeur - bord_cadre - tenon_peigne,
            largeur_diffuseur - epaisseur,
            difprops,
        ),
        (profondeur, largeur_diffuseur - epaisseur, 0),
        # peignes
        *list(peignes),
        (profondeur, epaisseur, 0),
        *tenonPeigneBas(profondeur - bord_cadre, epaisseur, difprops),
        *tenonPeigneBas(bord_cadre + tenon_peigne, epaisseur, difprops),
        (0, epaisseur, 0),
    ]

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre, "Peigne court"


def add_peigne_long(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    bord_cadre = difprops.bord_cadre
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    product_type = difprops.product_type
    offset = difprops.offset

    N = difprops.type

    rang = difprops.getRang()
    longueurTotale = difprops.getLongueur()

    edgesCadre = []
    peignes = []

    for k in range(1, round(N * longueur_diffuseur)):
        peignes += [
            (profondeur, longueurTotale - rang * k + offset, 0),
            (profondeur / 2 - 0.005, longueurTotale - rang * k + offset, 0),
            (
                profondeur / 2 - 0.005,
                longueurTotale - rang * k - epaisseur - offset,
                0,
            ),
            (profondeur, longueurTotale - rang * k - epaisseur - offset, 0),
        ]

    vertsCadre = [
        (0, epaisseur, 0),
        (0, longueurTotale - epaisseur, 0),
        *tenonPeigneHaut(bord_cadre, longueurTotale - epaisseur, difprops),
        *tenonPeigneHaut(
            profondeur - bord_cadre - tenon_peigne,
            longueurTotale - epaisseur,
            difprops,
        ),
        (profondeur, longueurTotale - epaisseur, 0),
        # peignes
        *[x for x in peignes if product_type == "0"],
        (profondeur, epaisseur, 0),
        *tenonPeigneBas(profondeur - bord_cadre, epaisseur, difprops),
        *tenonPeigneBas(bord_cadre + tenon_peigne, epaisseur, difprops),
        (0, epaisseur, 0),
    ]

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre, "Peigne long"


def add_carreau(difprops):
    product_type = difprops.product_type
    epaisseur = difprops.epaisseur

    N = difprops.type
    rang = difprops.getRang()

    longueurTotale = difprops.getLongueur()

    if product_type == "0":
        vertsCadre = [
            (0, 0, 0),
            (0, rang - epaisseur, 0),
            (rang - epaisseur, rang - epaisseur, 0),
            (rang - epaisseur, 0, 0),
            (0, 0, 0),
        ]
    else:
        vertsCadre = [
            (0, 0, 0),
            (0, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, 0, 0),
            (0, 0, 0),
        ]

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre, "Carreau"


def add_cadre_central(difprops):
    largeur_cadre_central = difprops.largeur_cadre_central
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre
    epaisseur = difprops.epaisseur

    vertsCadre = [
        (epaisseur, 0, 0),
        *tenonGauche(epaisseur, largeur_cadre_central / 2 - tenon_cadre / 2, difprops),
        (epaisseur, largeur_cadre_central, 0),
        (
            (largeur_diffuseur - epaisseur) / 6,
            largeur_cadre_central - largeur_cadre_central / 4,
            0,
        ),
        (
            (largeur_diffuseur - epaisseur) - (largeur_diffuseur - epaisseur) / 6,
            largeur_cadre_central - largeur_cadre_central / 4,
            0,
        ),
        (largeur_diffuseur - epaisseur, largeur_cadre_central, 0),
        *tenonDroit(
            largeur_diffuseur - epaisseur,
            largeur_cadre_central / 2 + tenon_cadre / 2,
            difprops,
        ),
        (largeur_diffuseur - epaisseur, 0, 0),
        (
            (largeur_diffuseur - epaisseur) - (largeur_diffuseur - epaisseur) / 6,
            largeur_cadre_central / 4,
            0,
        ),
        ((largeur_diffuseur - epaisseur) / 6, largeur_cadre_central / 4, 0),
    ]

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    return vertsCadre, edgesCadre, "Cadre central"


def add_accroche(difprops, productprops):
    product_type = productprops.product_type
    rang = difprops.getRang()
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre

    longueurTotale = difprops.getLongueur()
    division = (rang - epaisseur) / 12

    vertsAccroche = []
    vertsAccroche2 = []

    if product_type == "0":
        vertsCadre = [
            (0, 0, 0),
            (0, rang - epaisseur, 0),
            (rang - epaisseur, rang - epaisseur, 0),
            (rang - epaisseur, 0, 0),
        ]

        vertsAccroche = trou_accroche(division * 6, division * 4, division)

    elif product_type == "1":
        vertsCadre = [
            (0, 0, 0),
            (0, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, 0, 0),
        ]

        vertsAccroche = trou_accroche(division * 6, division * 4, division)
        vertsAccroche2 = trou_accroche(
            division * 6, longueurTotale - division * 10, division
        )

    elif product_type == "2":
        vertsCadre = [
            (epaisseur, 0, 0),
            *tenonGauche(
                epaisseur,
                epaisseur + (largeur_accroche / 2 - tenon_cadre / 2),
                difprops,
            ),
            (epaisseur, largeur_accroche, 0),
            *tenonHaut(
                (largeur_accroche / 2 - tenon_cadre / 2), largeur_accroche, difprops
            ),
            *tenonHaut(
                (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
                largeur_accroche,
                difprops,
            ),
            (largeur_diffuseur - epaisseur, largeur_accroche, 0),
            *tenonDroit(
                largeur_diffuseur - epaisseur,
                epaisseur + (largeur_accroche / 2 + tenon_cadre / 2),
                difprops,
            ),
            (largeur_diffuseur - epaisseur, 0, 0),
            (largeur_diffuseur - epaisseur - largeur_diffuseur / 8, 0, 0),
            (
                largeur_diffuseur
                - epaisseur
                - largeur_diffuseur / 8
                - largeur_diffuseur / 8,
                largeur_accroche / 3,
                0,
            ),
            (
                largeur_diffuseur / 8 + largeur_diffuseur / 8 + largeur_diffuseur / 8,
                largeur_accroche / 3,
                0,
            ),
            (
                largeur_diffuseur / 8 + largeur_diffuseur / 8,
                largeur_accroche / 3,
                0,
            ),
            (largeur_diffuseur / 8, 0, 0),
        ]

        vertsAccroche = trou_accroche(
            largeur_diffuseur / 12, epaisseur + largeur_accroche / 4, division
        )
        vertsAccroche2 = trou_accroche(
            largeur_diffuseur - largeur_diffuseur / 12,
            epaisseur + largeur_accroche / 4,
            division,
        )

    edgesCadre = []
    edgesAccroche = []
    edgesAccroche2 = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsAccroche) - 1):
        edgesAccroche += [
            (k, k + 1),
        ]
    edgesAccroche += [
        (len(vertsCadre), len(vertsCadre) + len(vertsAccroche) - 1),
    ]

    if product_type == "1" or product_type == "2":
        for k in range(
            len(vertsCadre) + len(vertsAccroche),
            len(vertsCadre) + len(vertsAccroche) + len(vertsAccroche2) - 1,
        ):
            edgesAccroche2 += [
                (k, k + 1),
            ]

        edgesAccroche2 += [
            (
                len(vertsCadre) + len(vertsAccroche),
                len(vertsCadre) + len(vertsAccroche) + len(vertsAccroche2) - 1,
            ),
        ]

    verts = [*list(vertsCadre), *list(vertsAccroche), *list(vertsAccroche2)]
    edges = [*list(edgesCadre), *list(edgesAccroche), *list(edgesAccroche2)]

    return verts, edges, "Accroche"


def add_accroche_inverse(difprops, productprops):
    product_type = productprops.product_type
    rang = difprops.getRang()
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre

    longueurTotale = difprops.getLongueur()
    division = (rang - epaisseur) / 12

    vertsAccroche = []
    vertsAccroche2 = []

    vertsCadre = [
        (epaisseur, 0, 0),
        *tenonGauche(
            epaisseur,
            epaisseur + (largeur_accroche / 2 - tenon_cadre / 2),
            difprops,
        ),
        (epaisseur, largeur_accroche, 0),
        *tenonHaut(
            (largeur_accroche / 2 - tenon_cadre / 2), largeur_accroche, difprops
        ),
        *tenonHaut(
            (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
            largeur_accroche,
            difprops,
        ),
        (largeur_diffuseur - epaisseur, largeur_accroche, 0),
        *tenonDroit(
            largeur_diffuseur - epaisseur,
            epaisseur + (largeur_accroche / 2 + tenon_cadre / 2),
            difprops,
        ),
        (largeur_diffuseur - epaisseur, 0, 0),
        (largeur_diffuseur - epaisseur - largeur_diffuseur / 8, 0, 0),
        (
            largeur_diffuseur
            - epaisseur
            - largeur_diffuseur / 8
            - largeur_diffuseur / 8,
            largeur_accroche / 3,
            0,
        ),
        (
            largeur_diffuseur / 8 + largeur_diffuseur / 8 + largeur_diffuseur / 8,
            largeur_accroche / 3,
            0,
        ),
        (
            largeur_diffuseur / 8 + largeur_diffuseur / 8,
            largeur_accroche / 3,
            0,
        ),
        (largeur_diffuseur / 8, 0, 0),
    ]
    vertsAccroche = trou_accroche_inverse(
        largeur_diffuseur / 12, epaisseur + largeur_accroche / 4, division
    )
    vertsAccroche2 = trou_accroche_inverse(
        largeur_diffuseur - largeur_diffuseur / 12,
        epaisseur + largeur_accroche / 4,
        division,
    )

    # bpy.ops.mesh.bevel(offset=0.003, offset_pct=0, segments=3, profile=0.987013, affect='VERTICES', release_confirm=True)

    edgesCadre = []
    edgesAccroche = []
    edgesAccroche2 = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsAccroche) - 1):
        edgesAccroche += [
            (k, k + 1),
        ]
    edgesAccroche += [
        (len(vertsCadre), len(vertsCadre) + len(vertsAccroche) - 1),
    ]

    if product_type == "1" or product_type == "2":
        for k in range(
            len(vertsCadre) + len(vertsAccroche),
            len(vertsCadre) + len(vertsAccroche) + len(vertsAccroche2) - 1,
        ):
            edgesAccroche2 += [
                (k, k + 1),
            ]

        edgesAccroche2 += [
            (
                len(vertsCadre) + len(vertsAccroche),
                len(vertsCadre) + len(vertsAccroche) + len(vertsAccroche2) - 1,
            ),
        ]

    verts = [*list(vertsCadre), *list(vertsAccroche), *list(vertsAccroche2)]
    edges = [*list(edgesCadre), *list(edgesAccroche), *list(edgesAccroche2)]

    return verts, edges, "Accroche"


def add_cadre_avant(difprops, productprops):
    product_type = productprops.product_type
    rang = difprops.getRang()
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre

    longueurTotale = difprops.getLongueur()
    division = (rang - epaisseur) / 12

    if product_type == "2":
        vertsCadre = [
            (epaisseur, 0, 0),
            *tenonGauche(
                epaisseur,
                epaisseur + (largeur_accroche / 2 - tenon_cadre / 2),
                difprops,
            ),
            (epaisseur, largeur_accroche, 0),
            *tenonHaut(
                (largeur_accroche / 2 - tenon_cadre / 2), largeur_accroche, difprops
            ),
            *tenonHaut(
                (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
                largeur_accroche,
                difprops,
            ),
            (largeur_diffuseur - epaisseur, largeur_accroche, 0),
            *tenonDroit(
                largeur_diffuseur - epaisseur,
                epaisseur + (largeur_accroche / 2 + tenon_cadre / 2),
                difprops,
            ),
            (largeur_diffuseur - epaisseur, 0, 0),
            (largeur_diffuseur - epaisseur - largeur_diffuseur / 8, 0, 0),
            (
                largeur_diffuseur
                - epaisseur
                - largeur_diffuseur / 8
                - largeur_diffuseur / 8,
                largeur_accroche / 3,
                0,
            ),
            (
                largeur_diffuseur / 8 + largeur_diffuseur / 8 + largeur_diffuseur / 8,
                largeur_accroche / 3,
                0,
            ),
            (
                largeur_diffuseur / 8 + largeur_diffuseur / 8,
                largeur_accroche / 3,
                0,
            ),
            (largeur_diffuseur / 8, 0, 0),
        ]

    # bpy.ops.mesh.bevel(offset=0.003, offset_pct=0, segments=3, profile=0.987013, affect='VERTICES', release_confirm=True)

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    verts = [*list(vertsCadre)]
    edges = [*list(edgesCadre)]

    return verts, edges, "Cadre Avant"


def add_fond_moule(difprops, productprops):
    product_type = productprops.product_type
    rang = difprops.getRang()
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre
    rang = difprops.getRang()

    longueurTotale = difprops.getLongueur()
    N = difprops.type

    if product_type == "3":
        mortaises_pilier = []
        b = 0
        for k in range(0, round(N * N)):
            c = k % N
            if c == 0 : 
                b += 1
            print(c, b)

            mortaises_pilier += [
                 *mortaise_pilier_fond_moule(rang * (c+1),rang*b,difprops) # epaisseur à prendre en compte ? 
            ]

        vertsCadre = [
            *mortaise_bas_fond_moule(0, 0, difprops),
            *mortaise_droite_fond_moule(
                largeur_diffuseur + 2 * epaisseur, epaisseur, difprops
            ),
            *mortaise_haut_fond_moule(
                largeur_diffuseur + epaisseur,
                largeur_diffuseur + 2 * epaisseur,
                difprops,
            ),
            *mortaise_gauche_fond_moule(
                0,
                largeur_diffuseur + epaisseur,
                difprops,
            ),
            *mortaises_pilier

        ]

    

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    verts = [*list(vertsCadre)]
    edges = [*list(edgesCadre)]

    return verts, edges, "Fond moule"


