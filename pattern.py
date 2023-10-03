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


def tenonHaut(x, y, difprops):
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


def tenonGauche(x, y, difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y + offset, 0),
        (
            x - epaisseur,
            y,
            0,
        ),
        (
            x - epaisseur,
            y + tenon_cadre,
            0,
        ),
        (
            x,
            y + tenon_cadre - offset,
            0,
        ),
    ]


def tenonDroit(x, y, difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y - offset, 0),
        (
            x + epaisseur,
            y,
            0,
        ),
        (
            x + epaisseur,
            y - tenon_cadre,
            0,
        ),
        (
            x,
            y - tenon_cadre + offset,
            0,
        ),
    ]


def tenonBas(x, y, difprops):
    offset = difprops.offset
    epaisseur = difprops.epaisseur
    tenon_cadre = difprops.tenon_cadre

    return [
        (x - offset, y, 0),
        (
            x,
            y - epaisseur,
            0,
        ),
        (
            x - tenon_cadre,
            y - epaisseur,
            0,
        ),
        (
            x + offset - tenon_cadre,
            y,
            0,
        ),
    ]


def tenonPeigneHaut(x, y, difprops):
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
            x + tenon_peigne,
            y + epaisseur,
            0,
        ),
        (
            x + tenon_peigne - offset,
            y,
            0,
        ),
    ]


def tenonPeigneBas(x, y, difprops):
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
            x - tenon_peigne,
            y - epaisseur,
            0,
        ),
        (
            x - tenon_peigne + offset,
            y,
            0,
        ),
    ]


def trou_accroche(x, y, division):
    return [
        (x - division * 2, y, 0),
        (x - division * 2, y + division * 2, 0),
        (x - division, y + division * 3, 0),
        (x - division / 3, y + division * 5, 0),
        (x + division / 3, y + division * 5, 0),
        (x + division, y + division * 3, 0),
        (x + division * 2, y + division * 2, 0),
        (x + division * 2, y, 0),
    ]


def trou_accroche_inverse(x, y, division):
    return [
        (x - division / 3, y, 0),
        (x - division, y + division * 2, 0),
        (x - division * 2, y + division * 3, 0),
        (x - division * 2, y + division * 5, 0),
        (x + division * 2, y + division * 5, 0),
        (x + division * 2, y + division * 3, 0),
        (x + division, y + division * 2, 0),
        (x + division / 3, y, 0),
    ]


def mortaise_bas_fond_moule(x, y, difprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = largeur_diffuseur / 8

    return [
        (x, y, 0),
        (x + epaisseur_moule, 0, 0),
        (x + epaisseur_moule + tenon_cadre, y + 0, 0),
        (x + epaisseur_moule + tenon_cadre, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 2, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 2, y + 0, 0),
        (x + epaisseur_moule + tenon_cadre * 3, y + 0, 0),
        (x + epaisseur_moule + tenon_cadre * 3, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 5, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 5, y + 0, 0),
        (x + epaisseur_moule + tenon_cadre * 6, y + 0, 0),
        (x + epaisseur_moule + tenon_cadre * 6, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 7, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 7, y + 0, 0),
        (x + epaisseur_moule * 2 + tenon_cadre * 8, y + 0, 0),
    ]


def mortaise_droite_fond_moule(x, y, difprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = largeur_diffuseur / 8

    return [
        (x, y, 0),
        (x, y + tenon_cadre, 0),
        (x - epaisseur_moule, y + tenon_cadre, 0),
        (x - epaisseur_moule, y + tenon_cadre * 2, 0),
        (x, y + tenon_cadre * 2, 0),
        (x, y + tenon_cadre * 3, 0),
        (x - epaisseur_moule, y + tenon_cadre * 3, 0),
        (x - epaisseur_moule, y + tenon_cadre * 5, 0),
        (x, y + tenon_cadre * 5, 0),
        (x, y + tenon_cadre * 6, 0),
        (x - epaisseur_moule, y + tenon_cadre * 6, 0),
        (x - epaisseur_moule, y + tenon_cadre * 7, 0),
        (x, y + tenon_cadre * 7, 0),
        (x, y + tenon_cadre * 8, 0),
        (x, y + tenon_cadre * 8 + epaisseur_moule, 0),
    ]


def mortaise_haut_fond_moule(x, y, difprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = largeur_diffuseur / 8

    return [
        (x, y, 0),
        (x - tenon_cadre, y, 0),
        (x - tenon_cadre, y - epaisseur_moule, 0),
        (x - tenon_cadre * 2, y - epaisseur_moule, 0),
        (x - tenon_cadre * 2, y, 0),
        (x - tenon_cadre * 3, y, 0),
        (x - tenon_cadre * 3, y - epaisseur_moule, 0),
        (x - tenon_cadre * 5, y - epaisseur_moule, 0),
        (x - tenon_cadre * 5, y, 0),
        (x - tenon_cadre * 6, y, 0),
        (x - tenon_cadre * 6, y - epaisseur_moule, 0),
        (x - tenon_cadre * 7, y - epaisseur_moule, 0),
        (x - tenon_cadre * 7, y, 0),
        (x - tenon_cadre * 8, y, 0),
        (x - tenon_cadre * 8 - epaisseur_moule, y, 0),
    ]


def mortaise_gauche_fond_moule(x, y, difprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = largeur_diffuseur / 8

    return [
        (x, y, 0),
        (x, y - tenon_cadre, 0),
        (x + epaisseur_moule, y - tenon_cadre, 0),
        (x + epaisseur_moule, y - tenon_cadre * 2, 0),
        (x, y - tenon_cadre * 2, 0),
        (x, y - tenon_cadre * 3, 0),
        (x + epaisseur_moule, y - tenon_cadre * 3, 0),
        (x + epaisseur_moule, y - tenon_cadre * 5, 0),
        (x, y - tenon_cadre * 5, 0),
        (x, y - tenon_cadre * 6, 0),
        (x + epaisseur_moule, y - tenon_cadre * 6, 0),
        (x + epaisseur_moule, y - tenon_cadre * 7, 0),
        (x, y - tenon_cadre * 7, 0),
    ]


def mortaise_pilier_fond_moule(x, y, difprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_pilier = difprops.tenon_pilier
    offset = difprops.offset


    return [
        (x-tenon_pilier/2 - offset, y-epaisseur_moule/2 - offset, 0),
        (x+ tenon_pilier/2 + offset, y-epaisseur_moule/2 - offset, 0),
        (x+ tenon_pilier/2 + offset, y + epaisseur_moule/2 + offset, 0),
        (x- tenon_pilier/2 - offset, y + epaisseur_moule/2 + offset, 0),
    ]
