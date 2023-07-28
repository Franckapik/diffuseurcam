import bpy

def add_cadre_mortaise(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset_mortaise_interne,
    tenon_peigne,
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    largeurTotale = largeur_diffuseur + 2 * epaisseur
    longueurArray = largeurTotale - 2 * correction
    bloc = longueurArray / N

    vertsCadre = [
        (0, 0, 0),
        (0, largeur_diffuseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), largeur_diffuseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), largeur_diffuseur - epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), largeur_diffuseur - epaisseur, 0),
        ((profondeur / 2 + tenon_cadre / 2), largeur_diffuseur , 0),
        ((profondeur), largeur_diffuseur, 0),
        ((profondeur), 0, 0),
        ((profondeur / 2 + tenon_cadre / 2), 0, 0),
        ((profondeur / 2 + tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), epaisseur, 0),
        ((profondeur / 2 - tenon_cadre / 2), 0, 0),
    ]

    vertsMortaisesInt = []

    for k in range(1, N):
        vertsMortaisesInt += [
            (bord_cadre, bloc * k, 0),
            (bord_cadre + tenon_peigne + offset_mortaise_interne, bloc * k, 0),
            (
                bord_cadre + tenon_peigne + offset_mortaise_interne,
                bloc * k - epaisseur,
                0,
            ),
            (bord_cadre, bloc * k - epaisseur, 0),
            (profondeur - bord_cadre, bloc * k - epaisseur, 0),
            (profondeur - bord_cadre, bloc * k, 0),
            (
                profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                bloc * k,
                0,
            ),
            (
                profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                bloc * k - epaisseur,
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

def add_cadre_long_mortaise(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset_mortaise_interne,
    tenon_peigne,
    longueur_diffuseur,
    diffuseur_type_is2D
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    largeurTotale = largeur_diffuseur + 2 * epaisseur
    longueurArray = largeurTotale - 2 * correction
    bloc = longueurArray / N
    longueurTotale = N * longueur_diffuseur * bloc

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
        if diffuseur_type_is2D : 
            vertsMortaisesInt += [
                (bord_cadre, bloc * k, 0),
                (bord_cadre + tenon_peigne + offset_mortaise_interne, bloc * k, 0),
                (
                    bord_cadre + tenon_peigne + offset_mortaise_interne,
                    bloc * k - epaisseur,
                    0,
                ),
                (bord_cadre, bloc * k - epaisseur, 0),
                (profondeur - bord_cadre, bloc * k - epaisseur, 0),
                (profondeur - bord_cadre, bloc * k, 0),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    bloc * k,
                    0,
                ),
                (
                    profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                    bloc * k - epaisseur,
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

def add_cadre_tenon(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset_mortaise_interne,
    tenon_peigne,
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    largeurTotale = largeur_diffuseur + 2 * epaisseur
    longueurArray = largeurTotale - 2 * correction
    bloc = longueurArray / N

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
            (bord_cadre, bloc * k, 0),
            (bord_cadre + tenon_peigne + offset_mortaise_interne, bloc * k, 0),
            (
                bord_cadre + tenon_peigne + offset_mortaise_interne,
                bloc * k - epaisseur,
                0,
            ),
            (bord_cadre, bloc * k - epaisseur, 0),
            (profondeur - bord_cadre, bloc * k - epaisseur, 0),
            (profondeur - bord_cadre, bloc * k, 0),
            (
                profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                bloc * k,
                0,
            ),
            (
                profondeur - bord_cadre - tenon_peigne - offset_mortaise_interne,
                bloc * k - epaisseur,
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

def add_carreau(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset_mortaise_interne,
    tenon_peigne,
    longueur_diffuseur,
    diffuseur_type_is2D,
    is_accroche
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    largeurTotale = largeur_diffuseur + 2 * epaisseur
    longueurArray = largeurTotale - 2 * correction
    bloc = longueurArray / N
    longueurTotale = N * longueur_diffuseur * bloc

    if diffuseur_type_is2D:
        vertsCadre = [(0, 0, 0), (0, bloc, 0), (bloc, bloc, 0), (bloc, 0, 0), (0, 0, 0)]
    else:
        vertsCadre = [(0, 0, 0), (0, longueurTotale, 0), (bloc, longueurTotale, 0), (bloc, 0, 0), (0, 0, 0)]

    if is_accroche and diffuseur_type_is2D:
        bpy.ops.mesh.primitive_circle_add(radius=0.01, enter_editmode=True, align='WORLD', location= (bloc/2,bloc/2, 0), scale=(1, 1, 1))
        
    if is_accroche and not diffuseur_type_is2D :    
        bpy.ops.mesh.primitive_circle_add(radius=0.01, enter_editmode=True, align='WORLD', location= (bloc/2,longueurTotale/5, 0), scale=(1, 1, 1))
        bpy.ops.mesh.primitive_circle_add(radius=0.01, enter_editmode=True, align='WORLD', location= (bloc/2,longueurTotale/5 * 4, 0), scale=(1, 1, 1))


    edgesCadre = []

    for k in range(0, len(vertsCadre) - 1):
        edgesCadre += [
            (k, k + 1),
        ]

    return vertsCadre, edgesCadre

def add_peigne_court(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset_mortaise_interne,
    tenon_peigne,
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    largeurTotale = largeur_diffuseur + 2 * epaisseur
    longueurArray = largeurTotale - 2 * correction
    bloc = longueurArray / N

    peignes = []
    for k in range(1, N):
        peignes += [
            (profondeur, largeur_diffuseur - epaisseur - bloc * k, 0),
            (profondeur/2, largeur_diffuseur - epaisseur - bloc * k, 0),
            (profondeur/2, largeur_diffuseur - epaisseur - bloc * k - epaisseur, 0),
            (profondeur, largeur_diffuseur - epaisseur - bloc * k - epaisseur, 0),
            
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

    for k in range(0, len(vertsCadre)-1):
            edgesCadre += [
                (k, k + 1),
            ]   



    return vertsCadre, edgesCadre

def add_peigne_long(
    epaisseur,
    profondeur,
    tenon_cadre,
    bord_cadre,
    largeur_diffuseur,
    offset_mortaise_interne,
    tenon_peigne,
    longueur_diffuseur
):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    N = 7
    correction = 0.00235
    largeurTotale = largeur_diffuseur + 2 * epaisseur
    longueurArray = largeurTotale - 2 * correction
    bloc = longueurArray / N
    longueurTotale = N * longueur_diffuseur * bloc

    peignes = []
    for k in range(1, round(N * longueur_diffuseur)):
        peignes += [
            (profondeur, longueurTotale - epaisseur - bloc * k, 0),
            (profondeur/2, longueurTotale - epaisseur - bloc * k, 0),
            (profondeur/2, longueurTotale - epaisseur - bloc * k - epaisseur, 0),
            (profondeur, longueurTotale - epaisseur - bloc * k - epaisseur, 0),
            
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

    for k in range(0, len(vertsCadre)-1):
            edgesCadre += [
                (k, k + 1),
            ]   



    return vertsCadre, edgesCadre
