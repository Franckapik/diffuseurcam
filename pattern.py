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

def papillonIn(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x -tenon_cadre/6,
            y - 0.03,
            0,
        ),
        (
            x +  tenon_cadre+ tenon_cadre/6,
            y - 0.03,
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

    if hauteurTenonPeigne != 0:
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


def mortaiseIntTraversante(x, y, difprops, usinageprops):
    tenon_peigne = difprops.tenon_peigne
    offset = usinageprops.getOffset()
    epaisseur = difprops.epaisseur
    hauteurTenonPeigne = difprops.getHauteurTenon()
    profondeur = difprops.profondeur

    if hauteurTenonPeigne != 0:
        return [
            (
                x - offset,
                y + epaisseur / 2 + offset,
                0,
            ),
            (
                x + profondeur + offset,
                y + epaisseur / 2 + offset,
                0,
            ),
            (
                x + profondeur + offset,
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
    else:  # pas de tenons
        return []


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
    else:  # pas de tenons
        return []


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
    ]


def mortaise_haut_fond_moule(x, y, difprops, usinageprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    tenon_cadre = largeur_diffuseur / 8

    return [
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
    ]


def mortaise_gauche_fond_moule(x, y, difprops, usinageprops):
    epaisseur_moule = difprops.epaisseur_moule
    largeur_diffuseur = difprops.largeur_diffuseur
    longueurTotale = difprops.getLongueur()
    tenon_cadre = longueurTotale / 8

    return [
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
        (x - epaisseur_pilier / 2, y - epaisseur_moule / 2, 0),
        (x + epaisseur_pilier / 2, y - epaisseur_moule / 2, 0),
        (x + epaisseur_pilier / 2, y + epaisseur_moule / 2, 0),
        (x - epaisseur_pilier / 2, y + epaisseur_moule / 2, 0),
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
        (x + epaisseur_pilier / 2, y - epaisseur_pilier / 2, 0),
        (x + epaisseur_pilier / 2, y - largeur_pilier / 2, 0),
    ]


def mortaise_pilier_fond_moule_mono(x, y, difprops, distanceMortaises):
    epaisseur_pilier = difprops.epaisseur_pilier
    largeur_pilier = difprops.getLargeurPilier()
    rang = difprops.getRang()

    return [
        (x + distanceMortaises, y - epaisseur_pilier / 2, 0),
        (x + distanceMortaises, y + epaisseur_pilier / 2, 0),
        (x + 2 * distanceMortaises, y + epaisseur_pilier / 2, 0),
        (x + 2 * distanceMortaises, y - epaisseur_pilier / 2, 0),
    ]


def monopilier_profondeurs(x, y, difprops, colonne, cross_monopilier_min):
    ratios = difprops.getMotif("depth")
    amax = max(ratios)
    epaisseur = difprops.epaisseur
    epaisseur_pilier = difprops.epaisseur_pilier
    profondeur = difprops.profondeur
    largeur_pilier = round(difprops.getLargeurPilier(), 4)
    reduction = 0.2 * largeur_pilier

    x0, y0 = x, y  # Initialisation des coordonnées de départ
    array_offset = 0  # Remplacez par la valeur appropriée pour l'offset
    result = []

    for i in range(difprops.type):
        index = colonne * difprops.type + i
        if(ratios[index]) : # if not pilier 0
            result.extend(
                [
                    (x0, y0, 0),
                    (x0 + reduction, y0 + ratios[index], 0),
                    (
                        x0 + reduction + (largeur_pilier - reduction * 2 - epaisseur_pilier ) / 2,
                        y0 + ratios[index],
                        0,
                    ),
                    (
                        x0 + reduction + (largeur_pilier - reduction * 2 - epaisseur_pilier ) / 2,
                        y0 + ratios[index] - cross_monopilier_min / 2 - epaisseur_pilier/2, # epaisseur_pilier/2 à confirmer selon overcuts ou non . Différence avec stable qui s'équilibre car il touche le fond
                        0,
                    ),
                    (
                        x0 + reduction + (largeur_pilier - reduction * 2 + epaisseur_pilier ) / 2,
                        y0 + ratios[index] - cross_monopilier_min / 2 - epaisseur_pilier/2,
                        0,
                    ),
                    (
                        x0 + reduction + (largeur_pilier - reduction * 2 + epaisseur_pilier ) / 2,
                        y0 + ratios[index],
                        0,
                    ),
                    (x0 + largeur_pilier - reduction, y0 + ratios[index], 0),
                    (x0 + largeur_pilier, y0, 0),
                ]
            )

        x0 += largeur_pilier + epaisseur
    print("|")

    return result


def contremonopilier_hauteurs(x, y, difprops):
    ratios = difprops.getMotif("height")
    amax = max(ratios)
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    largeur_pilier = round(difprops.getLargeurPilier(), 4)
    reduction = 0.008

    x0, y0 = x, y  # Initialisation des coordonnées de départ
    array_offset = 0  # Remplacez par la valeur appropriée pour l'offset
    result = []

    for i in range(difprops.type):
        result.extend(
            [
                (x0, y0, 0),
                (x0 + reduction, y0 + ratios[i] - epaisseur, 0),
                (x0 + largeur_pilier - reduction, y0 + ratios[i] - epaisseur, 0),
                (x0 + largeur_pilier, y0, 0),
            ]
        )

        x0 += largeur_pilier + epaisseur

    return result
