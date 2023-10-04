from .pattern import *
import math


def add_cadre_mortaise(difprops, productprops, usinageprops):
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
            *mortaiseHaut(
                (profondeur / 2 - tenon_cadre / 2),
                longueurTotale,
                difprops,
                usinageprops,
            ),
            ((profondeur), longueurTotale, 0),
            ((profondeur), 0, 0),
            *mortaiseBas((profondeur / 2 + tenon_cadre / 2), 0, difprops, usinageprops),
        ]

        for k in range(1, round(N * longueur_diffuseur)):
            if product_type == "0":
                vertsMortaisesInt += [
                    *mortaiseInt(
                        bord_cadre, (startup + rang * k), difprops, usinageprops
                    ),
                    *mortaiseInt(
                        profondeur - bord_cadre - tenon_peigne,
                        (startup + rang * k),
                        difprops,
                        usinageprops,
                    ),
                ]

    if product_type == "2":
        vertsCadre = [
            (0, 0, 0),
            *mortaiseGauche(
                0, (largeur_accroche / 2 - tenon_cadre / 2), difprops, usinageprops
            ),
            *mortaiseGauche(
                0,
                (longueurTotale - largeur_accroche / 2 - tenon_cadre / 2),
                difprops,
                usinageprops,
            ),
            (0, longueurTotale, 0),
            *mortaiseHaut(
                (profondeur / 2 - tenon_cadre / 2),
                longueurTotale,
                difprops,
                usinageprops,
            ),
            ((profondeur), longueurTotale, 0),
            *(
                a
                for a in mortaiseDroite(
                    profondeur,
                    longueurTotale - largeur_accroche / 2 + tenon_cadre / 2,
                    difprops,
                    usinageprops,
                )
                if cadre_avant == True
            ),
            *(
                a
                for a in mortaiseDroite(
                    profondeur,
                    longueurTotale / 2 + tenon_cadre / 2,
                    difprops,
                    usinageprops,
                )
                if cadre_central == True
            ),
            *(
                a
                for a in mortaiseDroite(
                    profondeur,
                    largeur_accroche / 2 + tenon_cadre / 2,
                    difprops,
                    usinageprops,
                )
                if cadre_avant == True
            ),
            ((profondeur), 0, 0),
            *mortaiseBas((profondeur / 2 + tenon_cadre / 2), 0, difprops, usinageprops),
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


def add_cadre_tenon(difprops, productprops, usinageprops):
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
                usinageprops,
            ),
            ((profondeur), largeur_diffuseur - epaisseur, 0),
            ((profondeur), epaisseur, 0),
            *tenonBas(
                (profondeur / 2 + tenon_cadre / 2), epaisseur, difprops, usinageprops
            ),
        ]

        for k in range(1, round(N)):
            vertsMortaisesInt += [
                *mortaiseInt(bord_cadre, (startup + rang * k), difprops, usinageprops),
                *mortaiseInt(
                    profondeur - bord_cadre - tenon_peigne,
                    (startup + rang * k),
                    difprops,
                    usinageprops,
                ),
            ]

    if product_type == "2":
        vertsCadre = [
            (0, epaisseur, 0),
            *mortaiseGauche(
                0, largeur_accroche / 2 - tenon_cadre / 2, difprops, usinageprops
            ),
            *mortaiseGauche(
                0,
                largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2,
                difprops,
                usinageprops,
            ),
            (0, largeur_diffuseur - epaisseur, 0),
            *tenonHaut(
                (profondeur / 2 - tenon_cadre / 2),
                largeur_diffuseur - epaisseur,
                difprops,
                usinageprops,
            ),
            ((profondeur), largeur_diffuseur - epaisseur, 0),
            *(
                a
                for a in mortaiseDroite(
                    profondeur,
                    largeur_diffuseur - largeur_accroche / 2 + tenon_cadre / 2,
                    difprops,
                    usinageprops,
                )
                if cadre_avant == True
            ),
            *(
                a
                for a in mortaiseDroite(
                    profondeur,
                    largeur_accroche / 2 + tenon_cadre / 2,
                    difprops,
                    usinageprops,
                )
                if cadre_avant == True
            ),
            ((profondeur), epaisseur, 0),
            *tenonBas(
                (profondeur / 2 + tenon_cadre / 2), epaisseur, difprops, usinageprops
            ),
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


def add_peigne_court(difprops, productprops, usinageprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_peigne = difprops.tenon_peigne
    offset = usinageprops.getOffset()

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
        *tenonPeigneHaut(
            bord_cadre, largeur_diffuseur - epaisseur, difprops, usinageprops
        ),
        *tenonPeigneHaut(
            profondeur - bord_cadre - tenon_peigne,
            largeur_diffuseur - epaisseur,
            difprops,
            usinageprops,
        ),
        (profondeur, largeur_diffuseur - epaisseur, 0),
        # peignes
        *list(peignes),
        (profondeur, epaisseur, 0),
        *tenonPeigneBas(profondeur - bord_cadre, epaisseur, difprops, usinageprops),
        *tenonPeigneBas(bord_cadre + tenon_peigne, epaisseur, difprops, usinageprops),
        (0, epaisseur, 0),
    ]

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre, "Peigne court"


def add_peigne_long(difprops, productprops, usinageprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    bord_cadre = difprops.bord_cadre
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    product_type = productprops.product_type
    offset = usinageprops.getOffset()

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
        *tenonPeigneHaut(
            bord_cadre, longueurTotale - epaisseur, difprops, usinageprops
        ),
        *tenonPeigneHaut(
            profondeur - bord_cadre - tenon_peigne,
            longueurTotale - epaisseur,
            difprops,
            usinageprops,
        ),
        (profondeur, longueurTotale - epaisseur, 0),
        # peignes
        *[x for x in peignes if product_type == "0"],
        (profondeur, epaisseur, 0),
        *tenonPeigneBas(profondeur - bord_cadre, epaisseur, difprops, usinageprops),
        *tenonPeigneBas(bord_cadre + tenon_peigne, epaisseur, difprops, usinageprops),
        (0, epaisseur, 0),
    ]

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre, "Peigne long"


def add_carreau(difprops, productprops, usinageprops):
    product_type = productprops.product_type
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


def add_cadre_central(difprops, productprops, usinageprops):
    largeur_cadre_central = difprops.largeur_cadre_central
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre
    epaisseur = difprops.epaisseur

    vertsCadre = [
        (epaisseur, 0, 0),
        *tenonGauche(
            epaisseur,
            largeur_cadre_central / 2 - tenon_cadre / 2,
            difprops,
            usinageprops,
        ),
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
            usinageprops,
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


def add_accroche(difprops, productprops, usinageprops):
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
                usinageprops,
            ),
            (epaisseur, largeur_accroche, 0),
            *tenonHaut(
                (largeur_accroche / 2 - tenon_cadre / 2),
                largeur_accroche,
                difprops,
                usinageprops,
            ),
            *tenonHaut(
                (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
                largeur_accroche,
                difprops,
                usinageprops,
            ),
            (largeur_diffuseur - epaisseur, largeur_accroche, 0),
            *tenonDroit(
                largeur_diffuseur - epaisseur,
                epaisseur + (largeur_accroche / 2 + tenon_cadre / 2),
                difprops,
                usinageprops,
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


def add_accroche_inverse(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    rang = difprops.getRang()
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre

    division = (rang - epaisseur) / 12

    vertsAccroche = []
    vertsAccroche2 = []

    vertsCadre = [
        (epaisseur, 0, 0),
        *tenonGauche(
            epaisseur,
            epaisseur + (largeur_accroche / 2 - tenon_cadre / 2),
            difprops,
            usinageprops,
        ),
        (epaisseur, largeur_accroche, 0),
        *tenonHaut(
            (largeur_accroche / 2 - tenon_cadre / 2),
            largeur_accroche,
            difprops,
            usinageprops,
        ),
        *tenonHaut(
            (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
            largeur_accroche,
            difprops,
            usinageprops,
        ),
        (largeur_diffuseur - epaisseur, largeur_accroche, 0),
        *tenonDroit(
            largeur_diffuseur - epaisseur,
            epaisseur + (largeur_accroche / 2 + tenon_cadre / 2),
            difprops,
            usinageprops,
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


def add_cadre_avant(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre

    if product_type == "2":
        vertsCadre = [
            (epaisseur, 0, 0),
            *tenonGauche(
                epaisseur,
                epaisseur + (largeur_accroche / 2 - tenon_cadre / 2),
                difprops,
                usinageprops,
            ),
            (epaisseur, largeur_accroche, 0),
            *tenonHaut(
                (largeur_accroche / 2 - tenon_cadre / 2),
                largeur_accroche,
                difprops,
                usinageprops,
            ),
            *tenonHaut(
                (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
                largeur_accroche,
                difprops,
                usinageprops,
            ),
            (largeur_diffuseur - epaisseur, largeur_accroche, 0),
            *tenonDroit(
                largeur_diffuseur - epaisseur,
                epaisseur + (largeur_accroche / 2 + tenon_cadre / 2),
                difprops,
                usinageprops,
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


def add_fond_moule(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    rang = difprops.getRang()
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = largeur_diffuseur / 8

    N = difprops.type
    rang2 = rang - epaisseur / N
    print(rang, epaisseur, rang - epaisseur / N)

    edgesCadre = []
    vertsMortaisesInt = []
    edgesMortaisesInt = []

    if product_type == "3":
        y0 = rang2 / 2 + epaisseur + epaisseur_moule
        x0 = rang2 / 2 + epaisseur + epaisseur_moule

        for k in range(0, round(N * N)):
            if k % N == 0 and k != 0:
                print(k)
                y0 += rang2
                x0 = rang2 / 2 + epaisseur + epaisseur_moule

            vertsMortaisesInt += [
                *mortaise_pilier_fond_moule(x0, y0, difprops, usinageprops)
            ]

            x0 += rang2

        vertsCadre = [
            (0, 0, 0),
            (epaisseur_moule, 0, 0),
            *mortaise_bas_fond_moule(0, 0, difprops, usinageprops),
            (epaisseur_moule + tenon_cadre * 8, 0, 0),
            (epaisseur_moule + epaisseur_moule + tenon_cadre * 8, 0, 0),
            *mortaise_droite_fond_moule(
                largeur_diffuseur + 2 * epaisseur_moule,
                epaisseur_moule,
                difprops,
                usinageprops,
            ),
            *mortaise_haut_fond_moule(
                largeur_diffuseur + epaisseur_moule,
                largeur_diffuseur + 2 * epaisseur_moule,
                difprops,
                usinageprops,
            ),
            *mortaise_gauche_fond_moule(
                0, largeur_diffuseur + epaisseur_moule, difprops, usinageprops
            ),
        ]

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
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

    verts = [*list(vertsCadre), *list(vertsMortaisesInt)]
    edges = [*list(edgesCadre), *list(edgesMortaisesInt)]

    return verts, edges, "Fond moule"


def add_cadre_moule(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    rang = difprops.getRang()
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur

    N = difprops.type
    print(rang, epaisseur, rang - epaisseur / N)

    edgesCadre = []

    if product_type == "3":
        vertsCadre = [
            (epaisseur_moule * 2, 0, 0),
            *mortaise_bas_fond_moule(0, 0, difprops, usinageprops),
            (largeur_diffuseur, 0, 0),
            (largeur_diffuseur, -profondeur, 0),
            (epaisseur_moule * 2, -profondeur, 0),
        ]

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    verts = [*list(vertsCadre)]
    edges = [*list(edgesCadre)]

    return verts, edges, "Cadre moule"


def add_pilier_moule(difprops, productprops, usinageprops, arrayprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_pilier = difprops.tenon_pilier
    epaisseur_moule = difprops.epaisseur_moule
    array_offset = arrayprops.array_offset

    N = difprops.type
    largeur_pilier = difprops.getLargeurPilier()

    edgesCadre = []

    prof = []
    vertsCadre = []

    for k in range(0, N * N):
        n = k % N
        m = math.floor(k / N)
        an = int((math.pow(n, 2) + math.pow(m, 2)) % N)
        prof.append(an)

    amax = max(prof)
    a = []

    for k in prof:
        a.append((k, prof.count(k)))

    ratio = list(dict.fromkeys(a))  # remove duplicates items

    if product_type == "3":
        y0 = 0
        x0 = 0
        for i in range(len(ratio)):
            if ratio[i][0] != 0:  # delete hauteur = 0
                if ratio[i][0] == amax:
                    y = ((ratio[i][0] * profondeur) / amax) - epaisseur
                else:
                    y = (ratio[i][0] * profondeur) / amax

                for k in range(ratio[i][1]):
                    vertsCadre += [
                        (x0, y0 + y + epaisseur_moule, 0),
                        (x0 + largeur_pilier, y0 + y + epaisseur_moule, 0),
                        (x0 + largeur_pilier, y0 + epaisseur_moule, 0),
                        (
                            x0 + largeur_pilier / 2 + tenon_pilier / 2,
                            y0 + epaisseur_moule,
                            0,
                        ),
                        (
                            x0 + largeur_pilier / 2 + tenon_pilier / 2,
                            y0,
                            0,
                        ),
                        (
                            x0 + largeur_pilier / 2 - tenon_pilier / 2,
                            y0,
                            0,
                        ),
                        (
                            x0 + largeur_pilier / 2 - tenon_pilier / 2,
                            y0 + epaisseur_moule,
                            0,
                        ),
                        (x0, y0 + epaisseur_moule, 0),
                    ]
                    x0 += largeur_pilier + array_offset

                x0 = 0
                y0 += y + array_offset + epaisseur_moule

    for i in range(len(vertsCadre)):
        if i % 8 == 0:
            edgesCadre += [
                (i, i + 1),
                (i + 1, i + 2),
                (i + 2, i + 3),
                (i + 3, i + 4),
                (i + 4, i + 5),
                (i + 5, i + 6),
                (i + 6, i + 7),
                (i + 7, i),
            ]

    verts = [*list(vertsCadre)]
    edges = [*list(edgesCadre)]

    return verts, edges, "Piliers"
