def mortaiseHaut(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def mortaiseBas(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def mortaiseGauche(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def mortaiseDroite(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def mortaiseInt(x, y, difprops, usinageprops):
    tenon_peigne = difprops.tenon_peigne
    offset = usinageprops.getOffset()
    epaisseur = difprops.epaisseur
    hauteurTenonPeigne = difprops.getHauteurTenon()

    if hauteurTenonPeigne != 0 :
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
    else:
        return []


def tenonHaut(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def tenonGauche(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def tenonDroit(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def tenonBas(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
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


def tenonPeigneHaut(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
    hauteurTenonPeigne = difprops.getHauteurTenon()
    tenon_peigne = difprops.tenon_peigne

    if hauteurTenonPeigne != 0: 
        return [
            (x + offset, y, 0),
            (
                x,
                y + hauteurTenonPeigne,
                0,
            ),
            (
                x + tenon_peigne,
                y + hauteurTenonPeigne,
                0,
            ),
            (
                x + tenon_peigne - offset,
                y,
                0,
            ),
        ]
    else : #pas de tenons
        return [
            
        ]


def tenonPeigneBas(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
    hauteurTenonPeigne = difprops.getHauteurTenon()
    tenon_peigne = difprops.tenon_peigne

    if hauteurTenonPeigne != 0:
        return [
            (x - offset, y, 0),
            (
                x,
                y - hauteurTenonPeigne,
                0,
            ),
            (
                x - tenon_peigne,
                y - hauteurTenonPeigne,
                0,
            ),
            (
                x - tenon_peigne + offset,
                y,
                0,
            ),
        ]
    else : #pas de tenons
        return [
            
        ]


def trou_accroche(x, y, division):
    return [
        (x - division * 2, y, 0),
        (x - division * 2, y + division * 2, 0),
        (x - division, y + division * 3, 0),
        (x - 0.0025, y + division * 6, 0),
        (x + 0.0025, y + division * 6, 0),
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


def mortaise_bas_fond_moule(x, y, difprops, usinageprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = largeur_diffuseur / 8

    return [
        (x + epaisseur_moule + tenon_cadre, y, 0),
        (x + epaisseur_moule + tenon_cadre, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 2, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 2, y, 0),
        (x + epaisseur_moule + tenon_cadre * 3, y, 0),
        (x + epaisseur_moule + tenon_cadre * 3, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 5, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 5, y, 0),
        (x + epaisseur_moule + tenon_cadre * 6, y, 0),
        (x + epaisseur_moule + tenon_cadre * 6, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 7, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 7, y, 0),
    ]

def mortaise_bas_fond_moule_long(x, y, difprops, usinageprops):
    epaisseur_moule = difprops.epaisseur_moule
    longueurTotale = difprops.getLongueur()
    tenon_cadre = longueurTotale / 8

    return [
        (x + epaisseur_moule + tenon_cadre, y, 0),
        (x + epaisseur_moule + tenon_cadre, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 2, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 2, y, 0),
        (x + epaisseur_moule + tenon_cadre * 3, y, 0),
        (x + epaisseur_moule + tenon_cadre * 3, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 5, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 5, y, 0),
        (x + epaisseur_moule + tenon_cadre * 6, y, 0),
        (x + epaisseur_moule + tenon_cadre * 6, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 7, y + epaisseur_moule, 0),
        (x + epaisseur_moule + tenon_cadre * 7, y, 0),
    ]


def mortaise_droite_fond_moule(x, y, difprops, usinageprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    longueurTotale = difprops.getLongueur()

    tenon_cadre = longueurTotale / 8


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


def mortaise_haut_fond_moule(x, y, difprops, usinageprops):
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


def mortaise_gauche_fond_moule(x, y, difprops, usinageprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    longueurTotale = difprops.getLongueur()
    tenon_cadre = longueurTotale / 8

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


def mortaise_pilier_fond_moule_eco(x, y, difprops, usinageprops):
    epaisseur_moule = difprops.epaisseur_moule
    epaisseur_pilier = difprops.epaisseur_pilier
    offset = usinageprops.getOffset()

    return [
        (x - epaisseur_pilier / 2 , y - epaisseur_moule / 2 , 0),
        (x + epaisseur_pilier / 2 , y - epaisseur_moule / 2 , 0),
        (x + epaisseur_pilier / 2 , y + epaisseur_moule / 2 , 0),
        (x - epaisseur_pilier / 2 , y + epaisseur_moule / 2 , 0),
    ]

def mortaise_pilier_fond_moule_stable(x, y, difprops, usinageprops):
    epaisseur_pilier = difprops.epaisseur_pilier
    largeur_pilier = difprops.getLargeurPilier()

    return [
        (x - epaisseur_pilier / 2, y - largeur_pilier / 2, 0),
        (x - epaisseur_pilier / 2, y - epaisseur_pilier / 2, 0),
        (x - largeur_pilier / 2, y - epaisseur_pilier / 2, 0),
        (x - largeur_pilier / 2, y + epaisseur_pilier / 2, 0),
        (x - epaisseur_pilier / 2, y + epaisseur_pilier / 2, 0),
        (x - epaisseur_pilier / 2, y + largeur_pilier / 2, 0),
        (x + epaisseur_pilier / 2, y + largeur_pilier / 2, 0),
        (x + epaisseur_pilier / 2, y + epaisseur_pilier / 2, 0),
        (x + largeur_pilier / 2, y + epaisseur_pilier / 2, 0),
        (x + largeur_pilier / 2, y - epaisseur_pilier / 2, 0),
        (x + epaisseur_pilier / 2, y -   epaisseur_pilier / 2, 0),
        (x + epaisseur_pilier / 2, y -largeur_pilier / 2, 0),
    ]
