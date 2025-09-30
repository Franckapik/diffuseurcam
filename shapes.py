from .pattern import *
import math


def add_cadre_mortaise(difprops, productprops, usinageprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    type_tenon_cadre = difprops.type_tenon_cadre
    bord_cadre = difprops.bord_cadre
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    largeur_accroche = difprops.largeur_accroche
    product_type = productprops.product_type
    startup = epaisseur / 2
    N = difprops.type
    rang = difprops.getRang()
    longueurTotale = difprops.getLongueur()
    type_tenon_peigne = difprops.type_tenon_peigne
    split = difprops.split
    longueur_absorbeur = difprops.longueur_absorbeur
    is_splitted = True if longueur_absorbeur > split and split != 0 else False
    renfort_central = difprops.renfort_central
    renfort_angle = difprops.renfort_angle

    edgesCadre = []
    vertsMortaisesInt = []
    edgesMortaisesInt = []

    if product_type == "0" or product_type == "1":
        if type_tenon_cadre == "1":
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
        else:
            vertsCadre = [
                (0, 0, 0),
                (0, longueurTotale, 0),
                ((profondeur), longueurTotale, 0),
                ((profondeur), 0, 0),
            ]

        for k in range(1, round(N * longueur_diffuseur)):
            if product_type == "0":
                if type_tenon_peigne == "3":
                    vertsMortaisesInt += [
                        *mortaiseIntTraversante(0, (startup + rang * k), difprops, usinageprops),
                    ]
                else:
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
        longueur_absorbeur = longueur_absorbeur / 2 if is_splitted else longueur_absorbeur
        if type_tenon_cadre == "1":
            vertsCadre = [
                (0, 0, 0),
                *(
                    mortaiseGauche(0, (largeur_accroche / 2 - tenon_cadre / 2), difprops, usinageprops)
                    if renfort_angle == "back" or renfort_angle == "both"
                    else []
                ),
                *(
                    mortaiseGauche(
                        0,
                        (longueur_absorbeur - largeur_accroche / 2 - tenon_cadre / 2),
                        difprops,
                        usinageprops,
                    )
                    if (renfort_angle == "back" or renfort_angle == "both") and not is_splitted
                    else []
                ),
                *(
                    mortaiseGauche(
                        0,
                        longueur_absorbeur / 2 - tenon_cadre / 2,
                        difprops,
                        usinageprops,
                    )
                    if renfort_central == "back" or renfort_central == "both"
                    else []
                ),
                (0, longueur_absorbeur, 0),
                *(
                    mortaiseHaut(
                        (profondeur / 2 - tenon_cadre / 2),
                        longueur_absorbeur,
                        difprops,
                        usinageprops,
                    )
                    if not is_splitted
                    else papillonHaut(
                        (profondeur / 2 - tenon_cadre / 2),
                        longueur_absorbeur,
                        difprops,
                        usinageprops,
                    )
                ),
                ((profondeur), longueur_absorbeur, 0),
                *(
                    mortaiseDroite(
                        profondeur,
                        longueur_absorbeur - largeur_accroche / 2 + tenon_cadre / 2,
                        difprops,
                        usinageprops,
                    )
                    if (renfort_angle == "front" or renfort_angle == "both") and not is_splitted
                    else []
                ),
                *(
                    mortaiseDroite(
                        profondeur,
                        longueur_absorbeur / 2 + tenon_cadre / 2,
                        difprops,
                        usinageprops,
                    )
                    if renfort_central == "front" or renfort_central == "both"
                    else []
                ),
                *(
                    mortaiseDroite(
                        profondeur,
                        largeur_accroche / 2 + tenon_cadre / 2,
                        difprops,
                        usinageprops,
                    )
                    if renfort_angle == "front" or renfort_angle == "both"
                    else []
                ),
                ((profondeur), 0, 0),
                *mortaiseBas((profondeur / 2 + tenon_cadre / 2), 0, difprops, usinageprops),
            ]
        else:
            vertsCadre = [
                (0, 0, 0),
                (0, longueur_absorbeur, 0),
                ((profondeur), longueur_absorbeur, 0),
                ((profondeur), 0, 0),
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
    type_tenon_cadre = difprops.type_tenon_cadre
    type_tenon_peigne = difprops.type_tenon_peigne
    split = difprops.split
    is_splitted = True if largeur_diffuseur > split and split != 0 else False
    renfort_angle = difprops.renfort_angle

    N = difprops.type

    rang = difprops.getRang()

    edgesCadre = []
    vertsMortaisesInt = []
    edgesMortaisesInt = []

    if product_type == "0" or product_type == "1":
        if type_tenon_cadre == "1":
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
                    (profondeur / 2 + tenon_cadre / 2),
                    epaisseur,
                    difprops,
                    usinageprops,
                ),
            ]
        else:
            vertsCadre = [
                (0, epaisseur, 0),
                (0, largeur_diffuseur - epaisseur, 0),
                ((profondeur), largeur_diffuseur - epaisseur, 0),
                ((profondeur), epaisseur, 0),
            ]

        for k in range(1, round(N)):
            if type_tenon_peigne == "3":
                vertsMortaisesInt += [
                    *mortaiseIntTraversante(0, (startup + rang * k), difprops, usinageprops),
                ]
            else:
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
        largeur_diffuseur = largeur_diffuseur / 2 if is_splitted else largeur_diffuseur
        if type_tenon_cadre == "1":
            vertsCadre = [
                (0, epaisseur, 0),
                *(
                    mortaiseGauche(0, largeur_accroche / 2 - tenon_cadre / 2, difprops, usinageprops)
                    if (renfort_angle == "back" or renfort_angle == "both")
                    else []
                ),
                *(
                    mortaiseGauche(
                        0,
                        largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2,
                        difprops,
                        usinageprops,
                    )
                    if (renfort_angle == "back" or renfort_angle == "both") and not is_splitted
                    else []
                ),
                (0, largeur_diffuseur - epaisseur, 0),
                *(
                    tenonHaut(
                        (profondeur / 2 - tenon_cadre / 2),
                        largeur_diffuseur - epaisseur,
                        difprops,
                        usinageprops,
                    )
                    if not is_splitted
                    else papillonHaut(
                        (profondeur / 2 - tenon_cadre / 2),
                        largeur_diffuseur - epaisseur,
                        difprops,
                        usinageprops,
                    )
                ),
                ((profondeur), largeur_diffuseur - epaisseur, 0),
                *(
                    mortaiseDroite(
                        profondeur,
                        largeur_diffuseur - largeur_accroche / 2 + tenon_cadre / 2,
                        difprops,
                        usinageprops,
                    )
                    if (renfort_angle == "front" or renfort_angle == "both") and not is_splitted
                    else []
                ),
                *(
                    mortaiseDroite(
                        profondeur,
                        largeur_accroche / 2 + tenon_cadre / 2,
                        difprops,
                        usinageprops,
                    )
                    if renfort_angle == "front" or renfort_angle == "both"
                    else []
                ),
                ((profondeur), epaisseur, 0),
                *tenonBas(
                    (profondeur / 2 + tenon_cadre / 2),
                    epaisseur,
                    difprops,
                    usinageprops,
                ),
            ]
        else:
            vertsCadre = [
                (0, epaisseur, 0),
                (0, largeur_diffuseur - epaisseur, 0),
                ((profondeur), largeur_diffuseur - epaisseur, 0),
                ((profondeur), epaisseur, 0),
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
    type_tenon_peigne = difprops.type_tenon_peigne
    offset = usinageprops.getOffset()
    offset_peigne = difprops.getOffsetPeigne()
    rainure_offset = 0.0005

    N = difprops.type

    rang = difprops.getRang()

    peignes = []
    for k in range(1, N):
        peignes += [
            (profondeur, largeur_diffuseur - rang * k + offset_peigne, 0),
            (
                profondeur / 2 - rainure_offset,
                largeur_diffuseur - rang * k + offset_peigne,
                0,
            ),
            (
                profondeur / 2 - rainure_offset,
                largeur_diffuseur - rang * k - epaisseur - offset_peigne,
                0,
            ),
            (profondeur, largeur_diffuseur - rang * k - epaisseur - offset_peigne, 0),
        ]

    if type_tenon_peigne == "3":
        vertsCadre = [
            (0, epaisseur / 2, 0),
            (0, largeur_diffuseur - epaisseur / 2, 0),
            (profondeur, largeur_diffuseur - epaisseur / 2, 0),
            # peignes
            *list(peignes),
            (profondeur, epaisseur / 2, 0),
            (0, epaisseur / 2, 0),
        ]
    else:
        vertsCadre = [
            (0, epaisseur, 0),
            (0, largeur_diffuseur - epaisseur, 0),
            *tenonPeigneHaut(bord_cadre, largeur_diffuseur - epaisseur, difprops, usinageprops),
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
    offset_peigne = difprops.getOffsetPeigne()
    type_tenon_peigne = difprops.type_tenon_peigne
    rainure_offset = 0.0005

    N = difprops.type

    rang = difprops.getRang()
    longueurTotale = difprops.getLongueur()

    edgesCadre = []
    peignes = []

    for k in range(1, round(N * longueur_diffuseur)):
        peignes += [
            (profondeur, longueurTotale - rang * k + offset_peigne, 0),
            (profondeur / 2 - rainure_offset, longueurTotale - rang * k + offset_peigne, 0),
            (
                profondeur / 2 - rainure_offset,
                longueurTotale - rang * k - epaisseur - offset_peigne,
                0,
            ),
            (profondeur, longueurTotale - rang * k - epaisseur - offset_peigne, 0),
        ]

    if type_tenon_peigne == "3":
        vertsCadre = [
            (0, epaisseur / 2, 0),
            (0, longueurTotale - epaisseur / 2, 0),
            (profondeur, longueurTotale - epaisseur / 2, 0),
            # peignes
            *list(peignes),
            (profondeur, epaisseur / 2, 0),
            (0, epaisseur / 2, 0),
        ]
    else:
        vertsCadre = [
            (0, epaisseur, 0),
            (0, longueurTotale - epaisseur, 0),
            *tenonPeigneHaut(bord_cadre, longueurTotale - epaisseur, difprops, usinageprops),
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


def add_renfort_central(difprops, productprops, usinageprops):
    largeur_renfort_central = difprops.largeur_renfort_central
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre
    epaisseur = difprops.epaisseur
    split = difprops.split
    puitsSerrage = difprops.puits_serrage
    is_splitted = True if largeur_diffuseur > split and split != 0 else False
    largeur_diffuseur = (
        largeur_diffuseur / 2 + epaisseur if is_splitted else largeur_diffuseur
    )  # epaisseur ajoutée sans comprendre ni verifier

    vertsCadre = [
        (epaisseur, 0, 0),
        *tenonGauche(
            epaisseur,
            largeur_renfort_central / 2 - tenon_cadre / 2,
            difprops,
            usinageprops,
        ),
        (epaisseur, largeur_renfort_central, 0),
        (
            (largeur_diffuseur - epaisseur) / 6,
            largeur_renfort_central - largeur_renfort_central / 4,
            0,
        ),
        (
            (largeur_diffuseur - epaisseur) - (largeur_diffuseur - epaisseur) / 6,
            largeur_renfort_central - largeur_renfort_central / 4,
            0,
        ),
        (largeur_diffuseur - epaisseur, largeur_renfort_central, 0),
        *(
            tenonDroit(
                largeur_diffuseur - epaisseur,
                largeur_renfort_central / 2 + tenon_cadre / 2,
                difprops,
                usinageprops,
            )
            if not is_splitted
            else []
        ),
        *(
            papillonDroit(
                largeur_diffuseur - epaisseur,
                largeur_renfort_central / 2 + tenon_cadre / 2,
                difprops,
                usinageprops,
            )
            if is_splitted
            else []
        ),
        (largeur_diffuseur - epaisseur, 0, 0),
        (
            (largeur_diffuseur - epaisseur) - (largeur_diffuseur - epaisseur) / 6,
            largeur_renfort_central / 4,
            0,
        ),
        ((largeur_diffuseur - epaisseur) / 6, largeur_renfort_central / 4, 0),
    ]

    vertsPuits = []

    if puitsSerrage:
        vertsPuits += [
            *puits(epaisseur * 3, largeur_renfort_central / 6, 0.005, 0.008),
            *puits(epaisseur * 3, largeur_renfort_central - largeur_renfort_central / 6, 0.005, 0.008),
            *(
                puits(largeur_diffuseur - epaisseur * 3, largeur_renfort_central / 6, 0.005, 0.008)
                if not is_splitted
                else []
            ),
            *(
                puits(
                    largeur_diffuseur - epaisseur * 3,
                    largeur_renfort_central - largeur_renfort_central / 6,
                    0.005,
                    0.008,
                )
                if not is_splitted
                else []
            ),
        ]

    edgesCadre = []
    edgesPuits = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    i = 0

    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsPuits)):
        i += 1
        if i == 4 or k == len(vertsCadre):
            i = 0
            edgesPuits += [
                (k, k + 1),
                (k + 1, k + 2),
                (k + 2, k + 3),
                (k + 3, k),
            ]

    verts = [*list(vertsCadre), *list(vertsPuits)]
    edges = [*list(edgesCadre), *list(edgesPuits)]

    return verts, edges, "Renfort central"


def add_accroche(difprops, productprops, usinageprops, invert):
    product_type = productprops.product_type
    rang = difprops.getRang()
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_accroche = difprops.tenon_accroche
    vis = difprops.vis
    puitsSerrage = difprops.puits_serrage

    longueurTotale = difprops.getLongueur()
    division = (rang - epaisseur) / 12

    vertsAccroche = []
    vertsAccroche2 = []

    split = difprops.split
    is_splitted = True if largeur_diffuseur > split and split != 0 else False

    if product_type == "0":
        vertsCadre = [
            (0, 0, 0),
            (0, rang - epaisseur, 0),
            (rang - epaisseur, rang - epaisseur, 0),
            (rang - epaisseur, 0, 0),
        ]

        vertsAccroche = trou_accroche(division * 6, division * 3, vis / 1000)

    elif product_type == "1":
        vertsCadre = [
            (0, 0, 0),
            (0, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, 0, 0),
        ]

        vertsAccroche = trou_accroche(division * 6, division * 3, vis / 1000)
        vertsAccroche2 = trou_accroche(division * 6, longueurTotale - division * 11, vis / 1000)

    elif product_type == "2":
        largeur_diffuseur = largeur_diffuseur / 2 if is_splitted else largeur_diffuseur
        vertsCadre = [
            (epaisseur, 0, 0),
            *tenonGauche(
                epaisseur,
                epaisseur + (largeur_accroche / 2 - tenon_accroche / 2),
                difprops,
                usinageprops,
            ),
            (epaisseur, largeur_accroche, 0),
            *tenonHaut(
                (largeur_accroche / 2 - tenon_accroche / 2),
                largeur_accroche,
                difprops,
                usinageprops,
            ),
            *(
                tenonHaut(
                    (largeur_diffuseur - largeur_accroche / 2 - tenon_accroche / 2),
                    largeur_accroche,
                    difprops,
                    usinageprops,
                )
                if not is_splitted
                else []
            ),
            (largeur_diffuseur - epaisseur, largeur_accroche, 0),
            *(
                tenonDroit(
                    largeur_diffuseur - epaisseur,
                    epaisseur + (largeur_accroche / 2 + tenon_accroche / 2),
                    difprops,
                    usinageprops,
                )
                if not is_splitted
                else []
            ),
            *(
                papillonDroit(
                    largeur_diffuseur - epaisseur,
                    largeur_accroche / 2 + tenon_accroche / 2,
                    difprops,
                    usinageprops,
                )
                if is_splitted
                else []
            ),
            (largeur_diffuseur - epaisseur, 0, 0),
            (largeur_diffuseur - epaisseur - largeur_diffuseur / 8, 0, 0),
            (
                largeur_diffuseur - epaisseur - largeur_diffuseur / 8 - largeur_diffuseur / 8,
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

        def miroir_sur_y_centre(vertices):
            # Calculer le centre sur Y
            y_centre = sum(y for _, y, _ in vertices) / len(vertices)

            # Appliquer le miroir sur Y par rapport au centre
            mirrored_vertices = [(x, 2 * y_centre - y, z) for x, y, z in vertices]

            return mirrored_vertices

        vertsEndroit = trou_accroche(largeur_diffuseur / 12, epaisseur + largeur_accroche / 4, vis / 1000)
        vertsEndroit2 = (
            trou_accroche(
                largeur_diffuseur - largeur_diffuseur / 12,
                epaisseur + largeur_accroche / 4,
                vis / 1000,
            )
            if not is_splitted
            else []
        )

        vertsAccroche += miroir_sur_y_centre(vertsEndroit) if invert else vertsEndroit
        if not is_splitted:
            vertsAccroche2 += miroir_sur_y_centre(vertsEndroit2) if invert else vertsEndroit2

        vertsPuits = []

        if puitsSerrage:
            vertsPuits += [
                *puits(epaisseur * 3, largeur_accroche / 6, 0.005, 0.008),
                *puits(epaisseur * 3, largeur_accroche - largeur_accroche / 6, 0.005, 0.008),
                *(
                    puits(largeur_diffuseur - epaisseur * 3, largeur_accroche / 6, 0.005, 0.008)
                    if not is_splitted
                    else []
                ),
                *(
                    puits(largeur_diffuseur - epaisseur * 3, largeur_accroche - largeur_accroche / 6, 0.005, 0.008)
                    if not is_splitted
                    else []
                ),
            ]

        edgesCadre = []
        edgesAccroche = []
        edgesAccroche2 = []
        edgesPuits = []

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
        if is_splitted is not True:
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

    if product_type == "2":
        i = 0

    for k in range(
        len(vertsCadre) + len(vertsAccroche) + len(vertsAccroche2),
        len(vertsCadre) + len(vertsAccroche) + len(vertsAccroche2) + len(vertsPuits),
    ):
        i += 1
        if i == 4 or k == (len(vertsCadre) + len(vertsAccroche) + len(vertsAccroche2)):
            i = 0
            edgesPuits += [
                (k, k + 1),
                (k + 1, k + 2),
                (k + 2, k + 3),
                (k + 3, k),
            ]

    verts = [*list(vertsCadre), *list(vertsAccroche), *list(vertsAccroche2), *list(vertsPuits)]
    edges = [*list(edgesCadre), *list(edgesAccroche), *list(edgesAccroche2), *list(edgesPuits)]

    return verts, edges, "Accroche inverse" if invert else "Accroche"


def add_renfort_angle(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = difprops.tenon_cadre
    split = difprops.split
    is_splitted = True if largeur_diffuseur > split and split != 0 else False
    puitsSerrage = difprops.puits_serrage

    if product_type == "2":
        largeur_diffuseur = (
            largeur_diffuseur / 2 + epaisseur if is_splitted else largeur_diffuseur
        )  # epaisseur ajoutée sans comprendre ni verifier
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
            *(
                tenonHaut(
                    (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
                    largeur_accroche,
                    difprops,
                    usinageprops,
                )
                if not is_splitted
                else []
            ),
            (largeur_diffuseur - epaisseur, largeur_accroche, 0),
            *(
                tenonDroit(
                    largeur_diffuseur - epaisseur,
                    epaisseur + (largeur_accroche / 2 + tenon_cadre / 2),
                    difprops,
                    usinageprops,
                )
                if not is_splitted
                else []
            ),
            *(
                papillonDroit(
                    largeur_diffuseur - epaisseur,
                    largeur_accroche / 2 + tenon_cadre / 2,
                    difprops,
                    usinageprops,
                )
                if is_splitted
                else []
            ),
            (largeur_diffuseur - epaisseur, 0, 0),
            (largeur_diffuseur - epaisseur - largeur_diffuseur / 8, 0, 0),
            (
                largeur_diffuseur - epaisseur - largeur_diffuseur / 8 - largeur_diffuseur / 8,
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

    vertsPuits = []

    if puitsSerrage:
        vertsPuits += [
            *puits(epaisseur * 3, largeur_accroche / 6, 0.005, 0.008),
            *puits(epaisseur * 3, largeur_accroche - largeur_accroche / 6, 0.005, 0.008),
            *(puits(largeur_diffuseur - epaisseur * 3, largeur_accroche / 6, 0.005, 0.008) if not is_splitted else []),
            *(
                puits(largeur_diffuseur - epaisseur * 3, largeur_accroche - largeur_accroche / 6, 0.005, 0.008)
                if not is_splitted
                else []
            ),
        ]

    edgesCadre = []
    edgesPuits = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    edgesCadre += [
        (len(vertsCadre) - 1, 0),
    ]

    i = 0

    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsPuits)):
        i += 1
        if i == 4 or k == len(vertsCadre):
            i = 0
            edgesPuits += [
                (k, k + 1),
                (k + 1, k + 2),
                (k + 2, k + 3),
                (k + 3, k),
            ]

    verts = [*list(vertsCadre), *list(vertsPuits)]
    edges = [*list(edgesCadre), *list(edgesPuits)]

    return verts, edges, "Renfort angle"


def add_fond_moule(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    rang = difprops.getRang()
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    longueur_diffuseur = difprops.longueur_diffuseur
    tenon_cadre = largeur_diffuseur / 8
    longueurTotale = difprops.getLongueur()
    debord_moule = 0.010
    type = difprops.type
    largeur_monopilier = rang * type - epaisseur
    ratio = difprops.getMotif("ratio")

    N = difprops.type
    rang2 = rang - epaisseur

    edgesCadre = []
    vertsMortaisesInt = []
    edgesMortaisesInt = []
    vertsMortaiseCadre = []
    edgesMortaiseCadre = []

    if product_type == "3":
        """depart bas/haut"""
        y0 = rang2 / 2 + epaisseur + epaisseur_moule + debord_moule
        """ depart gauche/droite """
        x0 = rang2 / 2 + epaisseur + epaisseur_moule + debord_moule

        for k in range(0, round(N * round(N * longueur_diffuseur))):
            if k % N == 0 and k != 0:
                y0 += rang2 + epaisseur
                x0 = rang2 / 2 + epaisseur + epaisseur_moule + debord_moule

            if difprops.type_moule == "eco":
                if ratio[k] != 0:
                    vertsMortaisesInt += [*mortaise_pilier_fond_moule_eco(x0, y0, difprops, usinageprops)]

                x0 += rang2 + epaisseur

            if difprops.type_moule == "stable":
                if ratio[k] != 0:
                    vertsMortaisesInt += [*mortaise_pilier_fond_moule_stable(x0, y0, difprops, usinageprops)]

                x0 += rang2 + epaisseur

        if difprops.type_moule == "mono":
            """depart bas/haut"""
            y0 = rang2 / 2 + epaisseur + epaisseur_moule + debord_moule
            """ depart gauche/droite """
            x0 = epaisseur + epaisseur_moule + debord_moule

            for k in range(0, round(N * longueur_diffuseur * 2)):
                if k % (round(N * longueur_diffuseur)) == 0 and k != 0:
                    x0 += largeur_monopilier / 5 * 2
                    y0 = rang2 / 2 + epaisseur + epaisseur_moule + debord_moule

                vertsMortaisesInt += [*mortaise_pilier_fond_moule_mono(x0, y0, difprops, largeur_monopilier / 5)]

                y0 += rang2 + epaisseur

        vertsCadre = [
            (0, 0, 0),
            (
                epaisseur_moule + debord_moule * 2 + epaisseur_moule + tenon_cadre * 8,
                0,
                0,
            ),
            (
                epaisseur_moule + debord_moule * 2 + epaisseur_moule + tenon_cadre * 8,
                longueurTotale + epaisseur_moule * 2 + debord_moule * 2,
                0,
            ),
            (
                0,
                longueurTotale + epaisseur_moule * 2 + debord_moule * 2,
                0,
            ),
        ]

        vertsMortaiseCadre = [
            *mortaise_bas_fond_moule(
                debord_moule,
                debord_moule,
                difprops,
                usinageprops,
            ),
            *mortaise_droite_fond_moule(
                epaisseur_moule + debord_moule + epaisseur_moule + tenon_cadre * 8,
                debord_moule + epaisseur_moule,
                difprops,
                usinageprops,
            ),
            *mortaise_haut_fond_moule(
                largeur_diffuseur + epaisseur_moule + debord_moule,
                longueurTotale + 2 * epaisseur_moule + debord_moule,
                difprops,
                usinageprops,
            ),
            *mortaise_gauche_fond_moule(
                debord_moule,
                longueurTotale + epaisseur_moule + debord_moule,
                difprops,
                usinageprops,
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
        if difprops.type_moule == "eco" or difprops.type_moule == "mono":
            i += 1
            if i == 4 or k == len(vertsCadre):
                i = 0
                edgesMortaisesInt += [
                    (k, k + 1),
                    (k + 1, k + 2),
                    (k + 2, k + 3),
                    (k + 3, k),
                ]
        if difprops.type_moule == "stable":
            i += 1
            if i == 12 or k == len(vertsCadre):
                i = 0
                edgesMortaisesInt += [
                    (k, k + 1),
                    (k + 1, k + 2),
                    (k + 2, k + 3),
                    (k + 3, k + 4),
                    (k + 4, k + 5),
                    (k + 5, k + 6),
                    (k + 6, k + 7),
                    (k + 7, k + 8),
                    (k + 8, k + 9),
                    (k + 9, k + 10),
                    (k + 10, k + 11),
                    (k + 11, k),
                ]

    i = 0

    for k in range(
        len(vertsCadre) + len(vertsMortaisesInt),
        len(vertsCadre) + len(vertsMortaisesInt) + len(vertsMortaiseCadre),
    ):
        i += 1
        if i == 4 or k == len(vertsCadre) + len(vertsMortaisesInt):
            i = 0
            edgesMortaiseCadre += [
                (k, k + 1),
                (k + 1, k + 2),
                (k + 2, k + 3),
                (k + 3, k),
            ]

    verts = [*list(vertsCadre), *list(vertsMortaisesInt), *list(vertsMortaiseCadre)]
    edges = [*list(edgesCadre), *list(edgesMortaisesInt), *list(edgesMortaiseCadre)]

    return verts, edges, "Fond moule"


def add_cadre_moule(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    rang = difprops.getRang()
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    debord_moule = 0.050

    N = difprops.type

    edgesCadre = []

    if product_type == "3":
        vertsCadre = [
            (-debord_moule, 0, 0),
            (0, 0, 0),
            (0, -profondeur / 2 - 0.005, 0),
            (epaisseur_moule, -profondeur / 2 - 0.005, 0),
            (epaisseur_moule, 0, 0),
            *mortaise_bas_fond_moule(0, 0, difprops, usinageprops),
            (largeur_diffuseur + epaisseur_moule, 0, 0),
            (largeur_diffuseur + epaisseur_moule, -profondeur / 2 - 0.005, 0),
            (largeur_diffuseur + epaisseur_moule * 2, -profondeur / 2 - 0.005, 0),
            (largeur_diffuseur + epaisseur_moule * 2, 0, 0),
            (largeur_diffuseur + epaisseur_moule * 2 + debord_moule, 0, 0),
            (largeur_diffuseur + epaisseur_moule * 2 + debord_moule, -profondeur, 0),
            (largeur_diffuseur + epaisseur_moule * 2 + debord_moule, -profondeur, 0),
            (-debord_moule, -profondeur, 0),
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


def add_cadre_moule_long(difprops, productprops, usinageprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    rang = difprops.getRang()
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    longueurTotale = difprops.getLongueur()
    debord_moule = 0.050

    N = difprops.type

    edgesCadre = []

    if product_type == "3":
        vertsCadre = [
            (-debord_moule - epaisseur_moule, 0, 0),
            *mortaise_bas_fond_moule_long(-epaisseur_moule, 0, difprops, usinageprops),
            (longueurTotale + epaisseur_moule + debord_moule, 0, 0),
            (longueurTotale + epaisseur_moule + debord_moule, -profondeur, 0),
            (longueurTotale + epaisseur_moule, -profondeur, 0),
            (longueurTotale + epaisseur_moule, -profondeur / 2 + 0.005, 0),
            (longueurTotale, -profondeur / 2 + 0.005, 0),
            (longueurTotale, -profondeur, 0),
            (0, -profondeur, 0),
            (0, -profondeur / 2 + 0.005, 0),
            (-epaisseur_moule, -profondeur / 2 + 0.005, 0),
            (-epaisseur_moule, -profondeur, 0),
            (-debord_moule - epaisseur_moule, -profondeur, 0),
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

    return verts, edges, "Cadre moule Long"


def add_pilier_moule(difprops, productprops, usinageprops, arrayprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    epaisseur_pilier = difprops.epaisseur_pilier
    socle_monopilier = difprops.socle_monopilier
    epaisseur_moule = difprops.epaisseur_moule
    array_offset = arrayprops.array_offset
    rang = difprops.getRang()
    type = difprops.type

    N = difprops.type
    largeur_pilier = difprops.getLargeurPilier()

    edgesCadre = []

    vertsCadre = []

    ratios = difprops.getMotif("depth")

    amax = max(ratios)
    amin = min([x for x in ratios if x > 0])
    cross_monopilier_min = amin + socle_monopilier
    a = []

    for k in ratios:
        a.append((k, ratios.count(k)))

    ratio = list(dict.fromkeys(a))  # remove duplicates items

    if product_type == "3":
        y0 = 0
        x0 = 0
        if difprops.type_moule == "eco":
            # Mode eco : logique classique sans pyramidal ni encoches
            reduction_ratio = float(difprops.pilier_reduction)
            
            for i in range(len(ratio)):
                if ratio[i][0] != 0:  # delete hauteur = 0
                    if ratio[i][0] == amax:
                        y = ((ratio[i][0] * profondeur) / amax) - epaisseur
                    else:
                        y = (ratio[i][0] * profondeur) / amax

                    for k in range(ratio[i][1]):
                        # Mode classique avec réduction uniforme
                        largeur_reduite = largeur_pilier * (1 - reduction_ratio)
                        decalage_reduction = (largeur_pilier - largeur_reduite) / 2
                        
                        vertsCadre += [
                            (x0 + decalage_reduction, y0 + y + epaisseur_moule, 0),
                            (x0 + decalage_reduction + largeur_reduite, y0 + y + epaisseur_moule, 0),
                            (x0 + decalage_reduction + largeur_reduite, y0 + epaisseur_moule, 0),
                            (
                                x0 + largeur_pilier / 2 + epaisseur_moule / 2,
                                y0 + epaisseur_moule,
                                0,
                            ),
                            (
                                x0 + largeur_pilier / 2 + epaisseur_moule / 2,
                                y0,
                                0,
                            ),
                            (
                                x0 + largeur_pilier / 2 - epaisseur_moule / 2,
                                y0,
                                0,
                            ),
                            (
                                x0 + largeur_pilier / 2 - epaisseur_moule / 2,
                                y0 + epaisseur_moule,
                                0,
                            ),
                            (x0 + decalage_reduction, y0 + epaisseur_moule, 0),
                        ]
                        x0 += largeur_pilier + array_offset

                    x0 = 0
                    y0 += y + array_offset + epaisseur_moule

            # Génération des edges (8 vertices par pilier en mode eco)
            for i in range(0, len(vertsCadre), 8):
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

        if difprops.type_moule == "stable":
            # Mode stable : logique classique avec possibilité d'encoches
            reduction_ratio = float(difprops.pilier_reduction)
            encoches = difprops.pilier_encoches if hasattr(difprops, 'pilier_encoches') else True
            
            for i in range(len(ratio)):
                if ratio[i][0] != 0:  # delete hauteur = 0
                    if ratio[i][0] == amax:
                        y = ((ratio[i][0] * profondeur) / amax) - epaisseur
                    else:
                        y = (ratio[i][0] * profondeur) / amax

                    for k in range(ratio[i][1]):
                        # Mode classique avec réduction uniforme
                        largeur_reduite = largeur_pilier * (1 - reduction_ratio)
                        decalage_reduction = (largeur_pilier - largeur_reduite) / 2
                        
                        if encoches:
                            # Avec encoches (logique originale modifiée)
                            vertsCadre += [
                                (x0 + decalage_reduction, y0 + y, 0),
                                (x0 + decalage_reduction + largeur_reduite, y0 + y, 0),
                                (x0 + decalage_reduction + largeur_reduite, y0, 0),
                                (x0 + largeur_pilier / 2 + epaisseur_pilier / 2, y0, 0),
                                (
                                    x0 + largeur_pilier / 2 + epaisseur_pilier / 2,
                                    y0 + y / 2 + epaisseur_pilier / 2,
                                    0,
                                ),
                                (
                                    x0 + largeur_pilier / 2 - epaisseur_pilier / 2,
                                    y0 + y / 2 + epaisseur_pilier / 2,
                                    0,
                                ),
                                (x0 + largeur_pilier / 2 - epaisseur_pilier / 2, y0, 0),
                                (x0 + decalage_reduction, y0, 0),
                            ]
                        else:
                            # Sans encoches : forme rectangulaire simple
                            vertsCadre += [
                                (x0 + decalage_reduction, y0, 0),
                                (x0 + decalage_reduction, y0 + y, 0),
                                (x0 + decalage_reduction + largeur_reduite, y0 + y, 0),
                                (x0 + decalage_reduction + largeur_reduite, y0, 0),
                            ]
                        x0 += largeur_pilier + array_offset

                    x0 = 0
                    y0 += y + array_offset

            # Génération des edges selon le mode d'encoches
            vertices_per_pillar = 8 if encoches else 4
            for i in range(0, len(vertsCadre), vertices_per_pillar):
                if encoches:
                    # Mode avec encoches : 8 vertices par pilier
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
                else:
                    # Mode sans encoches : 4 vertices par pilier
                    edgesCadre += [
                        (i, i + 1),
                        (i + 1, i + 2),
                        (i + 2, i + 3),
                        (i + 3, i),
                    ]

        if difprops.type_moule == "mono":
            y0 = 0
            largeur_monopilier = rang * type - epaisseur
            rangee_end_indices = []  # Pour tracker les fins de rangées
            
            for i in range(len(ratio)):
                if (difprops.moule_type == "1d" and i < 1) or difprops.moule_type == "2d":
                    start_idx = len(vertsCadre)  # Index de début de cette rangée
                    
                    vertsCadre += [
                        (x0 - epaisseur, y0, 0),
                        (x0 - epaisseur, y0 + socle_monopilier, 0),
                        *monopilier_profondeurs(x0, y0 + socle_monopilier, difprops, i, cross_monopilier_min),
                        (largeur_monopilier + epaisseur, y0 + socle_monopilier, 0),
                        (largeur_monopilier + epaisseur, y0, 0),
                        (largeur_monopilier - largeur_monopilier / 5, y0, 0),
                        (largeur_monopilier - largeur_monopilier / 5, y0 - epaisseur_moule, 0),
                        (largeur_monopilier - 2 * largeur_monopilier / 5, y0 - epaisseur_moule, 0),
                        (largeur_monopilier - 2 * largeur_monopilier / 5, y0, 0),
                        (largeur_monopilier - 3 * largeur_monopilier / 5, y0, 0),
                        (largeur_monopilier - 3 * largeur_monopilier / 5, y0 - epaisseur_moule, 0),
                        (largeur_monopilier - 4 * largeur_monopilier / 5, y0 - epaisseur_moule, 0),
                        (largeur_monopilier - 4 * largeur_monopilier / 5, y0, 0),
                        (x0 - epaisseur, y0, 0),
                    ]
                    
                    rangee_end_indices.append(len(vertsCadre) - 1)  # Marquer la fin de cette rangée

                    y0 += amax + array_offset + socle_monopilier

            # Génération des edges par rangée pour éviter les connexions inter-rangées
            rangee_start = 0
            for rangee_end in rangee_end_indices:
                # Créer les edges pour cette rangée seulement
                for k in range(rangee_start, rangee_end):
                    edgesCadre += [(k, k + 1)]
                
                # Fermer le contour de cette rangée
                edgesCadre += [(rangee_end, rangee_start)]
                
                # Préparer pour la rangée suivante
                rangee_start = rangee_end + 1

    verts = [*list(vertsCadre)]
    edges = [*list(edgesCadre)]

    return verts, edges, "Piliers"


# creer des cercles pour reconnaitre les monopiliers. Chatgpt proposition pour le dessin d'un cercle.

""" def create_circle(name, diameter, segments): 
    # Calculer le rayon
    radius = diameter / 2.0

    # Générer les vertices pour un cercle
    vertices = []
    edges = []

    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, y, 0))  # Cercle dans le plan XY

    # Générer les edges reliant les vertices
    for i in range(segments):
        edges.append((i, (i + 1) % segments))  # Relier chaque vertex au suivant

    # Créer le bmesh
    bm = bmesh.new()

    # Ajouter les vertices
    for v in vertices:
        bm.verts.new(v)

    # Mettre à jour le bmesh
    bm.verts.ensure_lookup_table()

    # Ajouter les edges
    for e in edges:
        bm.edges.new((bm.verts[e[0]], bm.verts[e[1]]))

    # Créer une nouvelle mesh et lui attribuer le bmesh
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()

    # Créer un nouvel objet pour afficher la mesh
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

# Créer un cercle de diamètre 5 mm et 32 segments
create_circle("MyCircle", diameter=5, segments=32) """


def add_contre_pilier_moule(difprops, productprops, usinageprops, arrayprops):
    product_type = productprops.product_type
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    epaisseur_pilier = difprops.epaisseur_pilier
    socle_contrepiliers = 0.05
    epaisseur_moule = difprops.epaisseur_moule
    array_offset = arrayprops.array_offset
    rang = difprops.getRang()
    type = difprops.type
    double_epaisseur = epaisseur_moule + epaisseur

    N = difprops.type
    largeur_pilier = difprops.getLargeurPilier()

    edgesCadre = []
    vertsCadre = []

    # Utiliser les hauteurs (height) pour les contre-piliers au lieu des profondeurs (depth)
    ratios = difprops.getMotif("height")

    amax = max(ratios)
    amin = min([x for x in ratios if x > 0])
    a = []

    for k in ratios:
        a.append((k, ratios.count(k)))

    ratio = list(dict.fromkeys(a))  # remove duplicates items

    if product_type == "3":
        y0 = 0
        x0 = 0

        if difprops.type_moule in ["eco", "stable"]:
            # Pour eco et stable, utiliser la fonction contremonopilier_hauteurs
            for i in range(len(ratio)):
                if ratio[i][0] != 0:  # delete hauteur = 0
                    for k in range(ratio[i][1]):
                        contre_pilier_verts = contremonopilier_hauteurs(x0, y0, difprops)
                        vertsCadre += contre_pilier_verts
                        x0 += largeur_pilier + array_offset

                    x0 = 0
                    # Logique standard : pas de correction d'épaisseur ici car elle se fait dans contremonopilier_hauteurs
                    if difprops.type_moule == "eco":
                        y0 += (ratio[i][0] * profondeur) / amax + array_offset + epaisseur_moule
                    else:  # stable
                        y0 += (ratio[i][0] * profondeur) / amax + array_offset

            # Génération des edges (4 vertices par contre-pilier avec la fonction originale)
            num_pillars_per_row = difprops.type  # Nombre de piliers par rangée
            for i in range(0, len(vertsCadre), 4 * num_pillars_per_row):
                # Pour chaque rangée de piliers
                for j in range(num_pillars_per_row):
                    pillar_start = i + j * 4
                    if pillar_start + 3 < len(vertsCadre):
                        edgesCadre += [
                            (pillar_start, pillar_start + 1),
                            (pillar_start + 1, pillar_start + 2),
                            (pillar_start + 2, pillar_start + 3),
                            (pillar_start + 3, pillar_start),
                        ]

        elif difprops.type_moule == "mono":
            largeur_monopilier = rang * type - epaisseur
            rangee_end_indices = []  # Pour tracker les fins de rangées

            for i in range(len(ratio)):
                if (difprops.moule_type == "1d" and i < 1) or difprops.moule_type == "2d":
                    start_idx = len(vertsCadre)  # Index de début de cette rangée
                    
                    vertsCadre += [
                        (x0, y0, 0),
                        (x0, y0 + socle_contrepiliers + profondeur, 0),
                        (x0 + 0.05, y0 + socle_contrepiliers + profondeur, 0),
                        (x0 + 0.05, y0 + socle_contrepiliers, 0),
                        (x0 + 0.05 + double_epaisseur, y0 + socle_contrepiliers, 0),
                        *contremonopilier_hauteurs(x0 + 0.05 + double_epaisseur, y0 + socle_contrepiliers, difprops),
                        (x0 + 0.05 + double_epaisseur + largeur_monopilier + double_epaisseur, y0 + socle_contrepiliers, 0),
                        (
                            x0 + 0.05 + double_epaisseur + largeur_monopilier + double_epaisseur,
                            y0 + socle_contrepiliers + profondeur,
                            0,
                        ),
                        (
                            x0 + 0.05 + double_epaisseur + largeur_monopilier + double_epaisseur + 0.05,
                            y0 + socle_contrepiliers + profondeur,
                            0,
                        ),
                        (x0 + 0.05 + double_epaisseur + largeur_monopilier + double_epaisseur + 0.05, y0, 0),
                    ]
                    
                    rangee_end_indices.append(len(vertsCadre) - 1)  # Marquer la fin de cette rangée

                    y0 += amax + array_offset + socle_contrepiliers

            # Génération des edges par rangée pour éviter les connexions inter-rangées
            rangee_start = 0
            for rangee_end in rangee_end_indices:
                # Créer les edges pour cette rangée seulement
                for k in range(rangee_start, rangee_end):
                    edgesCadre += [(k, k + 1)]
                
                # Fermer le contour de cette rangée
                edgesCadre += [(rangee_end, rangee_start)]
                
                # Préparer pour la rangée suivante
                rangee_start = rangee_end + 1

    verts = [*list(vertsCadre)]
    edges = [*list(edgesCadre)]

    return verts, edges, "Contre-Piliers"


def add_colle(difprops, productprops, usinageprops, arrayprops):

    vertsCadre = []

    epaisseur = difprops.epaisseur

    ratio = difprops.getMotif("depth")

    for i in range(difprops.type):
        y = i * difprops.getRang() + (difprops.getRang() - epaisseur) / 2
        for k in range(difprops.type):
            index = i * difprops.type + k
            x = k * difprops.getRang() + (difprops.getRang() - epaisseur) / 2
            z = ratio[index]
            vertsCadre += [(x, y, z)]

    verts = [*list(vertsCadre)]
    edges = []

    return verts, edges, "Colle"


def add_cadre_tissu_long(difprops, productprops, usinageprops, arrayprops):
    product_type = productprops.product_type
    split = difprops.split
    epaisseur = difprops.epaisseur
    is_splitted = True if difprops.longueur_absorbeur > split and split != 0 else False
    longueurAbsorbeur = (difprops.longueur_absorbeur - 2 * epaisseur) if not is_splitted else (difprops.longueur_absorbeur - 2 * epaisseur) / 2

    edgesCadre = []

    if product_type == "2":
        vertsCadre = [
            (0, 0, 0),
            (0.03, 0, 0),
            (0.03, longueurAbsorbeur, 0),
            (0, longueurAbsorbeur, 0),
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

    return verts, edges, "Cadre tissu long"


def add_cadre_tissu_court(difprops, productprops, usinageprops, arrayprops):
    product_type = productprops.product_type
    split = difprops.split
    largeur_diffuseur = difprops.largeur_diffuseur
    is_splitted = True if largeur_diffuseur > split and split != 0 else False
    epaisseur = difprops.epaisseur
    largeurAbsorbeur = (
        (difprops.largeur_diffuseur - 2 * epaisseur)
        if not is_splitted
        else (difprops.largeur_diffuseur - 2 * epaisseur) / 2
    )

    edgesCadre = []

    if product_type == "2":
        vertsCadre = [
            (0, 0, 0),
            (0.03, 0, 0),
            (0.03, largeurAbsorbeur, 0),
            (0, largeurAbsorbeur, 0),
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

    return verts, edges, "Cadre tissu court"
