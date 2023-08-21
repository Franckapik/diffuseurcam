def mortaiseHaut(x, y, difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x - offset,
            y - epaisseur,
            0,
        ),
        (
            x + offset + tenon_cadre,
            y - epaisseur,
            0,
        ),
        (
            x + tenon_cadre,
            y,
            0,
        ),
    ]


def mortaiseBas(x, y, difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x + offset,
            y + epaisseur,
            0,
        ),
        (
            x - offset - tenon_cadre,
            y + epaisseur,
            0,
        ),
        (
            x - tenon_cadre,
            y,
            0,
        ),
    ]


def mortaiseGauche(x, y, difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x + epaisseur,
            y - offset,
            0,
        ),
        (
            x + epaisseur,
            y + offset + tenon_cadre,
            0,
        ),
        (
            x,
            y + tenon_cadre,
            0,
        ),
    ]


def mortaiseDroite(x, y, difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x - epaisseur,
            y + offset,
            0,
        ),
        (
            x - epaisseur,
            y - offset - tenon_cadre,
            0,
        ),
        (
            x,
            y - tenon_cadre,
            0,
        ),
    ]


def mortaiseInt(x, y, difprops):
    tenon_peigne = difprops.tenon_peigne
    offset = difprops.offset
    epaisseur = difprops.epaisseur

    return [
        (
            x - offset,
            y + epaisseur / 2 + offset,
            0,
        ),
        (
            x + tenon_peigne + offset,
            y + epaisseur / 2 + offset,
            0,
        ),
        (
            x + tenon_peigne + offset,
            y - epaisseur / 2 - offset,
            0,
        ),
        (
            x - offset,
            y - epaisseur / 2 - offset,
            0,
        ),
    ]

def tenonHaut(x,y,difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x + offset, y, 0),
        (
            x,
            y + epaisseur,
            0,
        ),
        (
            x + tenon_cadre,
            y + epaisseur,
            0,
        ),
        (
            x - offset + tenon_cadre,
            y,
            0,
        ),
    ]

def tenonGauche(x,y,difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y + offset, 0),
        (
            x - epaisseur,
            y ,
            0,
        ),
        (
            x - epaisseur,
            y + tenon_cadre ,
            0,
        ),
        (
            x,
            y + tenon_cadre - offset ,
            0,
        ),
    ]

def tenonDroit(x,y,difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y - offset, 0),
        (
            x + epaisseur,
            y ,
            0,
        ),
        (
            x + epaisseur,
            y - tenon_cadre ,
            0,
        ),
        (
            x,
            y - tenon_cadre + offset ,
            0,
        ),
    ]

def tenonBas(x,y,difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x - offset, y, 0),
        (
            x ,
            y - epaisseur,
            0,
        ),
        (
            x - tenon_cadre,
            y - epaisseur,
            0,
        ),
        (
            x +offset -  tenon_cadre,
            y,
            0,
        ),
    ]

def tenonPeigneHaut(x,y,difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_peigne = difprops.tenon_peigne

    return [
        (x + offset, y, 0),
        (
            x,
            y + epaisseur,
            0,
        ),
        (
            x + tenon_peigne ,
            y + epaisseur,
            0,
        ),
        (
            x + tenon_peigne - offset,
            y,
            0,
        ),
    ]

def tenonPeigneBas(x,y,difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_peigne = difprops.tenon_peigne

    return [
        (x - offset, y, 0),
        (
            x,
            y - epaisseur,
            0,
        ),
        (
            x - tenon_peigne ,
            y - epaisseur,
            0,
        ),
        (
            x - tenon_peigne + offset,
            y,
            0,
        ),
    ]

def trou_accroche(x,y,division):
    return [
            (x, y, 0),
            (x, y + division * 2, 0),
            (x + division * 2, y + division * 4, 0),
            (x + division * 4, y + division * 2, 0),
            (x + division * 4, y  , 0),
            
    ]