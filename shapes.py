def add_cadre_mortaise(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    bord_cadre = difprops.bord_cadre
    offset_mortaise_interne = difprops.offset_mortaise_interne
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    diffuseur_type_is2D = difprops.diffuseur_type_is2D
    startup = epaisseur / 2
    N = difprops.type

    rang = difprops.getRang()
    longueurTotale = difprops.getLongueur()

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
                (bord_cadre, startup + rang * k + epaisseur/2, 0),
                (
                    bord_cadre + tenon_peigne + offset_mortaise_interne,
                    startup + rang * k + epaisseur/2,   
                    0,
                ),
                (
                    bord_cadre + tenon_peigne + offset_mortaise_interne,
                    startup + rang * k - epaisseur/2,
                    0,
                ),
                (bord_cadre, startup + rang * k - epaisseur/2, 0),

                (profondeur - bord_cadre, startup + rang * k + epaisseur/2, 0),
                (profondeur - bord_cadre, startup + rang * k - epaisseur/2, 0),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    startup + rang * k - epaisseur/2,
                    0,
                ),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    startup + rang * k + epaisseur/2,
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

    return verts, edges, "Cadre mortaise"


def add_cadre_tenon(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    tenon_cadre = difprops.tenon_cadre
    bord_cadre = difprops.bord_cadre
    largeur_diffuseur = difprops.largeur_diffuseur
    offset_mortaise_interne = difprops.offset_mortaise_interne
    tenon_peigne = difprops.tenon_peigne
    startup = epaisseur / 2
    longueur_diffuseur = difprops.longueur_diffuseur


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

    for k in range(1, round(N * longueur_diffuseur)):
            vertsMortaisesInt += [
                (bord_cadre, startup + rang * k + epaisseur/2, 0),
                (
                    bord_cadre + tenon_peigne + offset_mortaise_interne,
                    startup + rang * k + epaisseur/2,   
                    0,
                ),
                (
                    bord_cadre + tenon_peigne + offset_mortaise_interne,
                    startup + rang * k - epaisseur/2,
                    0,
                ),
                (bord_cadre, startup + rang * k - epaisseur/2, 0),

                (profondeur - bord_cadre, startup + rang * k + epaisseur/2, 0),
                (profondeur - bord_cadre, startup + rang * k - epaisseur/2, 0),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    startup + rang * k - epaisseur/2,
                    0,
                ),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    startup + rang * k + epaisseur/2,
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

    return verts, edges, "Cadre tenon"





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
            (profondeur, largeur_diffuseur - rang * k , 0),
            (profondeur / 2, largeur_diffuseur - rang * k, 0),
            (profondeur / 2, largeur_diffuseur - rang * k - epaisseur, 0),
            (profondeur, largeur_diffuseur - rang * k - epaisseur, 0),
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

    return vertsCadre, edgesCadre, "Peigne court"


def add_peigne_long(difprops):
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    bord_cadre = difprops.bord_cadre
    tenon_peigne = difprops.tenon_peigne
    longueur_diffuseur = difprops.longueur_diffuseur
    diffuseur_type_is2D = difprops.diffuseur_type_is2D

    N = difprops.type

    rang = difprops.getRang()
    longueurTotale = difprops.getLongueur()


    peignes = []
    for k in range(1, round(N * longueur_diffuseur)):
        peignes += [
            (profondeur, longueurTotale - rang * k, 0),
            (profondeur / 2, longueurTotale - rang * k, 0),
            (profondeur / 2, longueurTotale - rang * k - epaisseur, 0),
            (profondeur, longueurTotale - rang * k - epaisseur, 0),
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

    return vertsCadre, edgesCadre, "Peigne long"

def add_carreau(difprops):
    diffuseur_type_is2D = difprops.diffuseur_type_is2D
    epaisseur = difprops.epaisseur

    N = difprops.type
    rang = difprops.getRang()

    longueurTotale = difprops.getLongueur()

    if diffuseur_type_is2D:
        vertsCadre = [(0, 0, 0), (0, rang-epaisseur, 0), (rang-epaisseur, rang-epaisseur, 0), (rang-epaisseur, 0, 0), (0, 0, 0)]
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


def add_accroche(difprops):
    longueur_diffuseur = difprops.longueur_diffuseur
    diffuseur_type_is2D = difprops.diffuseur_type_is2D
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

    vertsAccroche = [
        (rang / 3, rang / 4, 0),
        (rang / 3 * 2, rang / 4, 0),
        (rang / 3 * 2, rang / 4 * 2, 0),
        (rang / 2, rang / 4 * 3, 0),
        (rang / 3, rang / 4 * 2, 0),
    ]

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

    print(edgesAccroche)

    verts = [*list(vertsCadre), *list(vertsAccroche)]
    edges = [*list(edgesCadre), *list(edgesAccroche)]

    return verts, edges, "Accroche"