def add_cadre_mortaise(difprops, productprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    bord_cadre = difprops.bord_cadre
    offset = difprops.offset
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    largeur_accroche = difprops.largeur_accroche

    product_type = productprops.product_type
    startup = epaisseur / 2
    N = difprops.type

    rang = difprops.getRang()
    longueurTotale = difprops.getLongueur()

    if product_type == "0" or product_type == "1":
        vertsCadre = [
            (0, 0, 0),
            (0, longueurTotale, 0),
            ((profondeur / 2 - tenon_cadre / 2), longueurTotale, 0),
            (
                (profondeur / 2 - tenon_cadre / 2) - offset,
                longueurTotale - epaisseur,
                0,
            ),
            (
                (profondeur / 2 + tenon_cadre / 2) + offset,
                longueurTotale - epaisseur,
                0,
            ),
            ((profondeur / 2 + tenon_cadre / 2), longueurTotale, 0),
            ((profondeur), longueurTotale, 0),
            ((profondeur), 0, 0),
            ((profondeur / 2 + tenon_cadre / 2), 0, 0),
            ((profondeur / 2 + tenon_cadre / 2) + offset, epaisseur, 0),
            ((profondeur / 2 - tenon_cadre / 2) - offset, epaisseur, 0),
            ((profondeur / 2 - tenon_cadre / 2), 0, 0),
        ]

        vertsMortaisesInt = []

        for k in range(1, round(N * longueur_diffuseur)):
            if product_type == "0":
                vertsMortaisesInt += [
                    (
                        bord_cadre - offset,
                        startup + rang * k + epaisseur / 2 + offset,
                        0,
                    ),
                    (
                        bord_cadre + tenon_peigne + offset,
                        startup + rang * k + epaisseur / 2 + offset,
                        0,
                    ),
                    (
                        bord_cadre + tenon_peigne + offset,
                        startup + rang * k - epaisseur / 2 - offset,
                        0,
                    ),
                    (
                        bord_cadre - offset,
                        startup + rang * k - epaisseur / 2 - offset,
                        0,
                    ),
                    (
                        profondeur - bord_cadre + offset,
                        startup + rang * k + epaisseur / 2 + offset,
                        0,
                    ),
                    (
                        profondeur - bord_cadre + offset,
                        startup + rang * k - epaisseur / 2 - offset,
                        0,
                    ),
                    (
                        profondeur - bord_cadre - tenon_peigne - offset,
                        startup + rang * k - epaisseur / 2 - offset,
                        0,
                    ),
                    (
                        profondeur - bord_cadre - tenon_peigne - offset,
                        startup + rang * k + epaisseur / 2 + offset,
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

    if product_type == "2":
        vertsCadre = [
            (0, 0, 0),
            (0, largeur_accroche / 2 - tenon_cadre / 2, 0),
            (epaisseur, (largeur_accroche / 2 - tenon_cadre / 2) - offset, 0),
            (epaisseur, (largeur_accroche / 2 + tenon_cadre / 2) + offset, 0),
            (0, largeur_accroche / 2 + tenon_cadre / 2, 0),
            (0, longueurTotale - largeur_accroche / 2 - tenon_cadre / 2, 0),
            (
                epaisseur,
                (longueurTotale - largeur_accroche / 2 - tenon_cadre / 2) - offset,
                0,
            ),
            (
                epaisseur,
                (longueurTotale - largeur_accroche / 2 + tenon_cadre / 2) + offset,
                0,
            ),
            (0, longueurTotale - largeur_accroche / 2 + tenon_cadre / 2, 0),
            (0, longueurTotale, 0),
            ((profondeur / 2 - tenon_cadre / 2), longueurTotale, 0),
            (
                (profondeur / 2 - tenon_cadre / 2) - offset,
                longueurTotale - epaisseur,
                0,
            ),
            (
                (profondeur / 2 + tenon_cadre / 2) + offset,
                longueurTotale - epaisseur,
                0,
            ),
            ((profondeur / 2 + tenon_cadre / 2), longueurTotale, 0),
            ((profondeur), longueurTotale, 0),
            (profondeur, longueurTotale - largeur_accroche / 2 + tenon_cadre / 2, 0),
            (
                profondeur - epaisseur,
                (longueurTotale - largeur_accroche / 2 + tenon_cadre / 2) + offset,
                0,
            ),
            (
                profondeur - epaisseur,
                (longueurTotale - largeur_accroche / 2 - tenon_cadre / 2) - offset,
                0,
            ),
            (profondeur, longueurTotale - largeur_accroche / 2 - tenon_cadre / 2, 0),
            (profondeur, largeur_accroche / 2 + tenon_cadre / 2, 0),
            (
                profondeur - epaisseur,
                (largeur_accroche / 2 + tenon_cadre / 2) + offset,
                0,
            ),
            (
                profondeur - epaisseur,
                (largeur_accroche / 2 - tenon_cadre / 2) - offset,
                0,
            ),
            (profondeur, largeur_accroche / 2 - tenon_cadre / 2, 0),
            ((profondeur), 0, 0),
            ((profondeur / 2 + tenon_cadre / 2), 0, 0),
            ((profondeur / 2 + tenon_cadre / 2) + offset, epaisseur, 0),
            ((profondeur / 2 - tenon_cadre / 2) - offset, epaisseur, 0),
            ((profondeur / 2 - tenon_cadre / 2), 0, 0),
        ]

        vertsMortaisesInt = []

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

        edgesCadre = []

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
    offset = difprops.offset
    tenon_peigne = difprops.tenon_peigne
    startup = epaisseur / 2
    longueur_diffuseur = difprops.longueur_diffuseur
    product_type = productprops.product_type
    largeur_accroche = difprops.largeur_accroche

    N = difprops.type

    rang = difprops.getRang()

    edgesCadre = []

    if product_type == "0" or product_type == "1":
        vertsCadre = [
            (0, epaisseur, 0),
            (0, largeur_diffuseur - epaisseur, 0),
            (
                (profondeur / 2 - tenon_cadre / 2) + offset,
                largeur_diffuseur - epaisseur,
                0,
            ),
            ((profondeur / 2 - tenon_cadre / 2), largeur_diffuseur, 0),
            ((profondeur / 2 + tenon_cadre / 2), largeur_diffuseur, 0),
            (
                (profondeur / 2 + tenon_cadre / 2) - offset,
                largeur_diffuseur - epaisseur,
                0,
            ),
            ((profondeur), largeur_diffuseur - epaisseur, 0),
            ((profondeur), epaisseur, 0),
            ((profondeur / 2 + tenon_cadre / 2) - offset, epaisseur, 0),
            ((profondeur / 2 + tenon_cadre / 2), 0, 0),
            ((profondeur / 2 - tenon_cadre / 2), 0, 0),
            ((profondeur / 2 - tenon_cadre / 2) + offset, epaisseur, 0),
        ]

        vertsMortaisesInt = []

        for k in range(1, round(N * longueur_diffuseur)):
            vertsMortaisesInt += [
                (bord_cadre - offset, startup + rang * k + epaisseur / 2 + offset, 0),
                (
                    bord_cadre + tenon_peigne + offset,
                    startup + rang * k + epaisseur / 2 + offset,
                    0,
                ),
                (
                    bord_cadre + tenon_peigne + offset,
                    startup + rang * k - epaisseur / 2 - offset,
                    0,
                ),
                (bord_cadre - offset, startup + rang * k - epaisseur / 2 - offset, 0),
                (
                    profondeur - bord_cadre + offset,
                    startup + rang * k + epaisseur / 2 + offset,
                    0,
                ),
                (
                    profondeur - bord_cadre + offset,
                    startup + rang * k - epaisseur / 2 - offset,
                    0,
                ),
                (
                    profondeur - bord_cadre - tenon_peigne - offset,
                    startup + rang * k - epaisseur / 2 - offset,
                    0,
                ),
                (
                    profondeur - bord_cadre - tenon_peigne - offset,
                    startup + rang * k + epaisseur / 2 + offset,
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

    if product_type == "2":
        vertsCadre = [
            (0, epaisseur, 0),
            (0, largeur_accroche / 2 - tenon_cadre / 2, 0),
            (epaisseur, (largeur_accroche / 2 - tenon_cadre / 2) - offset, 0),
            (epaisseur, (largeur_accroche / 2 + tenon_cadre / 2) + offset, 0),
            (0, largeur_accroche / 2 + tenon_cadre / 2, 0),
            (0, largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2, 0),
            (
                epaisseur,
                (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2) - offset,
                0,
            ),
            (
                epaisseur,
                (largeur_diffuseur - largeur_accroche / 2 + tenon_cadre / 2) + offset,
                0,
            ),
            (0, largeur_diffuseur - largeur_accroche / 2 + tenon_cadre / 2, 0),
            (0, largeur_diffuseur - epaisseur, 0),
            (
                (profondeur / 2 - tenon_cadre / 2) + offset,
                largeur_diffuseur - epaisseur,
                0,
            ),
            ((profondeur / 2 - tenon_cadre / 2), largeur_diffuseur, 0),
            ((profondeur / 2 + tenon_cadre / 2), largeur_diffuseur, 0),
            (
                (profondeur / 2 + tenon_cadre / 2) - offset,
                largeur_diffuseur - epaisseur,
                0,
            ),
            ((profondeur), largeur_diffuseur - epaisseur, 0),
            ((profondeur), epaisseur, 0),
            ((profondeur / 2 + tenon_cadre / 2) - offset, epaisseur, 0),
            ((profondeur / 2 + tenon_cadre / 2), 0, 0),
            ((profondeur / 2 - tenon_cadre / 2), 0, 0),
            ((profondeur / 2 - tenon_cadre / 2) + offset, epaisseur, 0),
        ]

        vertsMortaisesInt = []

        edgesMortaisesInt = []

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
        (bord_cadre + offset, largeur_diffuseur - epaisseur, 0),
        (bord_cadre, largeur_diffuseur, 0),
        (bord_cadre + tenon_peigne, largeur_diffuseur, 0),
        (bord_cadre + tenon_peigne - offset, largeur_diffuseur - epaisseur, 0),
        (
            profondeur - bord_cadre - tenon_peigne + offset,
            largeur_diffuseur - epaisseur,
            0,
        ),
        (profondeur - bord_cadre - tenon_peigne, largeur_diffuseur, 0),
        (profondeur - bord_cadre, largeur_diffuseur, 0),
        (profondeur - bord_cadre - offset, largeur_diffuseur - epaisseur, 0),
        (profondeur, largeur_diffuseur - epaisseur, 0),
        # peignes
        *list(peignes),
        (profondeur, epaisseur, 0),
        (profondeur - bord_cadre - offset, epaisseur, 0),
        (profondeur - bord_cadre, 0, 0),
        (profondeur - bord_cadre - tenon_peigne, 0, 0),
        (profondeur - bord_cadre - tenon_peigne + offset, epaisseur, 0),
        (bord_cadre + tenon_peigne - offset, epaisseur, 0),
        (bord_cadre + tenon_peigne, 0, 0),
        (bord_cadre, 0, 0),
        (bord_cadre + offset, epaisseur, 0),
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
        (bord_cadre + offset, longueurTotale - epaisseur, 0),
        (bord_cadre, longueurTotale, 0),
        (bord_cadre + tenon_peigne, longueurTotale, 0),
        (bord_cadre + tenon_peigne - offset, longueurTotale - epaisseur, 0),
        (
            profondeur - bord_cadre - tenon_peigne + offset,
            longueurTotale - epaisseur,
            0,
        ),
        (profondeur - bord_cadre - tenon_peigne, longueurTotale, 0),
        (profondeur - bord_cadre, longueurTotale, 0),
        (profondeur - bord_cadre - offset, longueurTotale - epaisseur, 0),
        (profondeur, longueurTotale - epaisseur, 0),
        # peignes
        *[x for x in peignes if product_type == "0"],
        (profondeur, epaisseur, 0),
        (profondeur - bord_cadre - offset, epaisseur, 0),
        (profondeur - bord_cadre, 0, 0),
        (profondeur - bord_cadre - tenon_peigne, 0, 0),
        (profondeur - bord_cadre - tenon_peigne + offset, epaisseur, 0),
        (bord_cadre + tenon_peigne - offset, epaisseur, 0),
        (bord_cadre + tenon_peigne, 0, 0),
        (bord_cadre, 0, 0),
        (bord_cadre + offset, epaisseur, 0),
        (0, epaisseur, 0),
    ]

    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre, "Peigne long"


def add_carreau(difprops):
    product_type = difprops.product_type
    epaisseur = difprops.epaisseur
    offset = difprops.offset

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


def add_accroche(difprops, productprops):
    product_type = productprops.product_type
    rang = difprops.getRang()
    epaisseur = difprops.epaisseur
    largeur_accroche = difprops.largeur_accroche
    largeur_diffuseur = difprops.largeur_diffuseur
    bord_cadre = difprops.bord_cadre
    tenon_cadre = difprops.tenon_cadre
    offset = difprops.offset

    longueurTotale = difprops.getLongueur()
    division = (rang - epaisseur) / 12

    if product_type == "0":
        vertsCadre = [
            (0, 0, 0),
            (0, rang - epaisseur, 0),
            (rang - epaisseur, rang - epaisseur, 0),
            (rang - epaisseur, 0, 0),
            (0, 0, 0),
        ]
        vertsAccroche = [
            (division * 4, division * 4, 0),
            (division * 4, division * 6, 0),
            (division * 6, division * 8, 0),
            (division * 8, division * 6, 0),
            (division * 8, division * 4, 0),
        ]
    elif product_type == "1":
        vertsCadre = [
            (0, 0, 0),
            (0, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, longueurTotale - epaisseur * 2, 0),
            (rang - epaisseur, 0, 0),
            (0, 0, 0),
        ]
        vertsAccroche = [
            (division * 4, division * 4, 0),
            (division * 4, division * 6, 0),
            (division * 6, division * 8, 0),
            (division * 8, division * 6, 0),
            (division * 8, division * 4, 0),
        ]
    elif product_type == "2":
        vertsCadre = [
            (epaisseur, 0, 0),
            (epaisseur, (largeur_accroche / 2 - tenon_cadre / 2) + offset, 0),
            (0, largeur_accroche / 2 - tenon_cadre / 2, 0),
            (0, largeur_accroche / 2 + tenon_cadre / 2, 0),
            (epaisseur, largeur_accroche / 2 + tenon_cadre / 2 - offset, 0),
            (epaisseur, largeur_accroche, 0),
            ((largeur_accroche / 2 - tenon_cadre / 2), largeur_accroche, 0),
            (
                (largeur_accroche / 2 - tenon_cadre / 2) - offset,
                largeur_accroche + epaisseur,
                0,
            ),
            (
                (largeur_accroche / 2 + tenon_cadre / 2) + offset,
                largeur_accroche + epaisseur,
                0,
            ),
            ((largeur_accroche / 2 + tenon_cadre / 2), largeur_accroche, 0),
            (
                (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2),
                largeur_accroche,
                0,
            ),
            (
                (largeur_diffuseur - largeur_accroche / 2 - tenon_cadre / 2) - offset,
                largeur_accroche + epaisseur,
                0,
            ),
            (
                (largeur_diffuseur - largeur_accroche / 2 + tenon_cadre / 2) + offset,
                largeur_accroche + epaisseur,
                0,
            ),
            (
                (largeur_diffuseur - largeur_accroche / 2 + tenon_cadre / 2),
                largeur_accroche,
                0,
            ),
            (largeur_diffuseur - epaisseur, largeur_accroche, 0),
            (largeur_diffuseur - epaisseur, (largeur_accroche / 2 + tenon_cadre / 2) - offset, 0),
            (largeur_diffuseur, largeur_accroche / 2 + tenon_cadre / 2, 0),
            (largeur_diffuseur, largeur_accroche / 2 - tenon_cadre / 2, 0),
            (largeur_diffuseur - epaisseur, (largeur_accroche / 2 - tenon_cadre / 2) + offset, 0),
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
            (largeur_diffuseur / 8 + largeur_diffuseur / 8, largeur_accroche / 3, 0),
            (largeur_diffuseur / 8, 0, 0),
            (0, 0, 0),
        ]
        vertsAccroche = [
            (division * 4, division * 4, 0),
            (division * 4, division * 6, 0),
            (division * 6, division * 8, 0),
            (division * 8, division * 6, 0),
            (division * 8, division * 4, 0),
        ]

    # bpy.ops.mesh.bevel(offset=0.003, offset_pct=0, segments=3, profile=0.987013, affect='VERTICES', release_confirm=True)

    edgesCadre = []
    edgesAccroche = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]
    for k in range(len(vertsCadre), len(vertsCadre) + len(vertsAccroche) - 1):
        edgesAccroche += [
            (k, k + 1),
        ]
    edgesAccroche += [
        (len(vertsCadre), len(vertsCadre) + len(vertsAccroche) - 1),
    ]

    verts = [*list(vertsCadre), *list(vertsAccroche)]
    edges = [*list(edgesCadre), *list(edgesAccroche)]

    return verts, edges, "Accroche"
