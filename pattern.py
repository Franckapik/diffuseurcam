def mortaiseHaut(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x - offset,
            y - ec,
            0,
        ),
        (
            x + offset + tenon_cadre,
            y - ec,
            0,
        ),
        (
            x + tenon_cadre,
            y,
            0,
        ),
    ]

def papillonHaut(x, y, difprops, usinageprops):
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

def papillonDroit(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
    tenon_accroche = difprops.tenon_accroche

    return [
        (x, y, 0),
        (
            x - 0.03,
            y  + tenon_accroche/6,
            0,
        ),
        (
            x - 0.03,
            y  - tenon_accroche - tenon_accroche/6,
            0,
        ),
        (
            x,
            y - tenon_accroche,
            0,
        ),
    ]


def mortaiseBas(x, y, difprops, usinageprops):
    offset = usinageprops.getOffset()
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x + offset,
            y + ec,
            0,
        ),
        (
            x - offset - tenon_cadre,
            y + ec,
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
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x + ec,
            y - offset,
            0,
        ),
        (
            x + ec,
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
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y, 0),
        (
            x - ec,
            y + offset,
            0,
        ),
        (
            x - ec,
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
    
def puits(x, y, width, height):
        return [
            (
                x-width/2 ,
                y + height / 2  ,
                0,
            ),
            (
                x + width/2  ,
                y + height / 2  ,
                0,
            ),
            (
                x + width/2  ,
                y - height / 2  ,
                0,
            ),
            (
                x - width/2 ,
                y - height / 2  ,
                0,
            ),
        ]


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
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x + offset, y, 0),
        (
            x,
            y + ec,
            0,
        ),
        (
            x + tenon_cadre,
            y + ec,
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
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y + offset, 0),
        (
            x - ec,
            y,
            0,
        ),
        (
            x - ec,
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
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x, y - offset, 0),
        (
            x + ec,
            y,
            0,
        ),
        (
            x + ec,
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
    ec = difprops.getEpaisseurCadre()
    tenon_cadre = difprops.tenon_cadre

    return [
        (x - offset, y, 0),
        (
            x,
            y - ec,
            0,
        ),
        (
            x - tenon_cadre,
            y - ec,
            0,
        ),
        (
            x + offset - tenon_cadre,
            y,
            0,
        ),
    ]


def _queues_droites_layout(profondeur, t):
    """Calcule n (nombre de sections, forcé impair) et la marge de centrage.
    n impair garantit que le profil commence et finit par un tenon (symétrie).
    La marge est garantie >= t ou == 0 pour éviter des restes trop petits."""
    n = max(1, int(profondeur / t))
    if n % 2 == 0:
        n -= 1
    margin = (profondeur - n * t) / 2
    if 0 < margin < t:
        n = max(1, n - 2)
        margin = (profondeur - n * t) / 2
    return n, margin


def queuesDroitesHaut(profondeur, y, difprops, usinageprops):
    """Mortaises multiples (queues droites) sur le bord haut, de gauche à droite."""
    offset = usinageprops.getOffset()
    ec = difprops.getEpaisseurCadre()
    t = difprops.tenon_cadre
    n, margin = _queues_droites_layout(profondeur, t)
    verts = []
    for i in range(0, n, 2):
        x_l = margin + i * t
        x_r = x_l + t
        verts += [
            (x_l, y, 0),
            (x_l - offset, y - ec, 0),
            (x_r + offset, y - ec, 0),
            (x_r, y, 0),
        ]
    return verts


def queuesDroitesBas(profondeur, y, difprops, usinageprops):
    """Mortaises multiples (queues droites) sur le bord bas, de droite à gauche."""
    offset = usinageprops.getOffset()
    ec = difprops.getEpaisseurCadre()
    t = difprops.tenon_cadre
    n, margin = _queues_droites_layout(profondeur, t)
    verts = []
    for i in reversed(range(0, n, 2)):
        x_l = margin + i * t
        x_r = x_l + t
        verts += [
            (x_r, y, 0),
            (x_r + offset, y + ec, 0),
            (x_l - offset, y + ec, 0),
            (x_l, y, 0),
        ]
    return verts


def queuesDroitesTenonHaut(profondeur, y, difprops, usinageprops):
    """Tenons multiples (queues droites) sur le bord haut, de gauche à droite."""
    offset = usinageprops.getOffset()
    ec = difprops.getEpaisseurCadre()
    t = difprops.tenon_cadre
    n, margin = _queues_droites_layout(profondeur, t)
    verts = []
    for i in range(0, n, 2):
        x_l = margin + i * t
        x_r = x_l + t
        verts += [
            (x_l + offset, y, 0),
            (x_l, y + ec, 0),
            (x_r, y + ec, 0),
            (x_r - offset, y, 0),
        ]
    return verts


def queuesDroitesTenonBas(profondeur, y, difprops, usinageprops):
    """Tenons multiples (queues droites) sur le bord bas, de droite à gauche."""
    offset = usinageprops.getOffset()
    ec = difprops.getEpaisseurCadre()
    t = difprops.tenon_cadre
    n, margin = _queues_droites_layout(profondeur, t)
    verts = []
    for i in reversed(range(0, n, 2)):
        x_l = margin + i * t
        x_r = x_l + t
        verts += [
            (x_r - offset, y, 0),
            (x_r, y - ec, 0),
            (x_l, y - ec, 0),
            (x_l + offset, y, 0),
        ]
    return verts


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


def mortaise_pilier_fond_moule_mono(x, y, difprops, distanceMortaises, apply_reduction=True):
    epaisseur_pilier = difprops.epaisseur_pilier
    largeur_pilier = difprops.getLargeurPilier()
    rang = difprops.getRang()
    
    # Obtenir la largeur de la mortaise (réduite ou non selon le paramètre)
    if apply_reduction:
        largeur_mortaise = difprops.getMonopilierMortaiseLargeur()
    else:
        # Sans réduction : la mortaise a la même largeur que l'espacement
        largeur_mortaise = distanceMortaises
    
    # Calculer le décalage pour centrer la mortaise
    decalage_centrage = (distanceMortaises - largeur_mortaise) / 2
    
    return [
        (x + distanceMortaises + decalage_centrage, y - epaisseur_pilier / 2, 0),
        (x + distanceMortaises + decalage_centrage, y + epaisseur_pilier / 2, 0),
        (x + distanceMortaises + decalage_centrage + largeur_mortaise, y + epaisseur_pilier / 2, 0),
        (x + distanceMortaises + decalage_centrage + largeur_mortaise, y - epaisseur_pilier / 2, 0),
    ]


def monopilier_profondeurs(x, y, difprops, colonne, cross_monopilier_min):
    ratios = difprops.getMotif("depth")
    # getMotif() retourne déjà les profondeurs ajustées (épaisseur soustraite pour le max)
    amax = max(ratios)
    epaisseur = difprops.epaisseur
    epaisseur_pilier = difprops.epaisseur_pilier
    profondeur = difprops.profondeur
    
    # Calcul des dimensions respectant toutes les contraintes
    largeur_diffuseur = difprops.largeur_diffuseur
    reduction_ratio = float(difprops.pilier_reduction)
    # La logique pyramidale est disponible pour cette fonction (mono uniquement)
    pyramidal = difprops.pilier_pyramidal if hasattr(difprops, 'pilier_pyramidal') else False
    encoches = difprops.pilier_encoches if hasattr(difprops, 'pilier_encoches') else True
    
    # largeur_monopilier = rang * type - epaisseur = largeur_diffuseur - 2*ec
    ec = difprops.getEpaisseurCadre()
    largeur_monopilier = largeur_diffuseur - 2 * ec

    # La largeur nominale d'un sous-pilier = largeur de cellule du diffuseur (rang - e).
    # Cela garantit l'alignement exact avec le modèle 3D :
    #   N * (rang - e) + (N-1) * e = N*rang - e = largeur_monopilier
    rang = difprops.getRang()
    largeur_pilier_base = rang - epaisseur

    if pyramidal:
        largeur_pilier_base_finale = largeur_pilier_base
        largeur_pilier_haut = largeur_pilier_base * (1 - reduction_ratio)
    else:
        largeur_pilier_base_finale = largeur_pilier_base * (1 - reduction_ratio)
        largeur_pilier_haut = largeur_pilier_base_finale

    largeur_pilier_pour_positionnement = largeur_pilier_base_finale

    if difprops.type > 1:
        # Pas centre-à-centre = rang (période des cellules, identique au modèle 3D)
        espacement_entre_centres = rang
        # Premier sous-pilier : bord gauche à x (face intérieure du cadre gauche),
        # centre à x + (rang - e) / 2
        x_premier_pilier = x + largeur_pilier_base / 2
    else:
        # Un seul pilier, centré dans l'intérieur du moule
        espacement_entre_centres = 0
        x_premier_pilier = x + largeur_monopilier / 2
    
    x0, y0 = x, y  # Initialisation des coordonnées de départ
    result = []

    for i in range(difprops.type):
        index = colonne * difprops.type + i
        if(ratios[index]) : # if not pilier 0
            # Position du centre de ce pilier
            centre_pilier_x = x_premier_pilier + i * espacement_entre_centres
            
            # Calcul des positions du pilier selon le mode
            if pyramidal:
                # Mode pyramidal : base large, haut réduit
                pilier_base_start = centre_pilier_x - largeur_pilier_base_finale / 2
                pilier_base_end = centre_pilier_x + largeur_pilier_base_finale / 2
                pilier_haut_start = centre_pilier_x - largeur_pilier_haut / 2
                pilier_haut_end = centre_pilier_x + largeur_pilier_haut / 2
            else:
                # Mode classique : largeur uniforme
                pilier_base_start = centre_pilier_x - largeur_pilier_pour_positionnement / 2
                pilier_base_end = centre_pilier_x + largeur_pilier_pour_positionnement / 2
                pilier_haut_start = pilier_base_start
                pilier_haut_end = pilier_base_end
            
            # getMotif() retourne déjà les hauteurs ajustées
            hauteur_pilier = ratios[index]
            
            if encoches:
                # Avec encoches (logique originale)
                result.extend(
                    [
                        (pilier_base_start, y0, 0),
                        (pilier_base_start, y0 + hauteur_pilier, 0),
                        (
                            pilier_haut_start + (largeur_pilier_haut - epaisseur_pilier) / 2,
                            y0 + hauteur_pilier,
                            0,
                        ),
                        (
                            pilier_haut_start + (largeur_pilier_haut - epaisseur_pilier) / 2,
                            y0 + hauteur_pilier - cross_monopilier_min / 2 - epaisseur_pilier/2, # epaisseur_pilier/2 à confirmer selon overcuts ou non . Différence avec stable qui s'équilibre car il touche le fond
                            0,
                        ),
                        (
                            pilier_haut_start + (largeur_pilier_haut + epaisseur_pilier) / 2,
                            y0 + hauteur_pilier - cross_monopilier_min / 2 - epaisseur_pilier/2,
                            0,
                        ),
                        (
                            pilier_haut_start + (largeur_pilier_haut + epaisseur_pilier) / 2,
                            y0 + hauteur_pilier,
                            0,
                        ),
                        (pilier_haut_end, y0 + hauteur_pilier, 0),
                        (pilier_base_end, y0, 0),
                    ]
                )
            else:
                # Sans encoches : forme simple rectangulaire ou pyramidale
                if pyramidal:
                    # Forme pyramidale sans encoches
                    result.extend(
                        [
                            (pilier_base_start, y0, 0),
                            (pilier_haut_start, y0 + hauteur_pilier, 0),
                            (pilier_haut_end, y0 + hauteur_pilier, 0),
                            (pilier_base_end, y0, 0),
                        ]
                    )
                else:
                    # Forme rectangulaire classique sans encoches
                    result.extend(
                        [
                            (pilier_base_start, y0, 0),
                            (pilier_base_start, y0 + hauteur_pilier, 0),
                            (pilier_base_end, y0 + hauteur_pilier, 0),
                            (pilier_base_end, y0, 0),
                        ]
                    )

    return result


def contremonopilier_hauteurs(x, y, difprops):
    ratios = difprops.getMotif("height")
    # getMotif() retourne déjà les hauteurs ajustées (épaisseur soustraite pour le max)
    amax = max(ratios)
    epaisseur = difprops.epaisseur
    profondeur = difprops.profondeur
    
    # Calcul des dimensions respectant toutes les contraintes (même logique que monopilier_profondeurs)
    largeur_diffuseur = difprops.largeur_diffuseur
    reduction_ratio = float(difprops.pilier_reduction)
    # La logique pyramidale est disponible pour cette fonction (mono uniquement)
    pyramidal = difprops.pilier_pyramidal if hasattr(difprops, 'pilier_pyramidal') else False
    
    # largeur_monopilier = rang * type - epaisseur = largeur_diffuseur - 2*ec
    ec = difprops.getEpaisseurCadre()
    largeur_monopilier = largeur_diffuseur - 2 * ec

    # Largeur nominale d'un sous-pilier = largeur de cellule du diffuseur (rang - e),
    # identique à monopilier_profondeurs pour garantir l'alignement avec le modèle 3D.
    rang = difprops.getRang()
    largeur_pilier_base = rang - epaisseur

    if pyramidal:
        largeur_pilier_base_finale = largeur_pilier_base
        largeur_pilier_haut = largeur_pilier_base * (1 - reduction_ratio)
    else:
        largeur_pilier_base_finale = largeur_pilier_base * (1 - reduction_ratio)
        largeur_pilier_haut = largeur_pilier_base_finale

    largeur_pilier_pour_positionnement = largeur_pilier_base_finale

    if difprops.type > 1:
        espacement_entre_centres = rang
        x_premier_pilier = x + largeur_pilier_base / 2
    else:
        espacement_entre_centres = 0
        x_premier_pilier = x + largeur_monopilier / 2

    x0, y0 = x, y  # Initialisation des coordonnées de départ
    result = []

    for i in range(difprops.type):
        # Position du centre de ce pilier (même logique que monopilier_profondeurs)
        centre_pilier_x = x_premier_pilier + i * espacement_entre_centres
        
        # Calcul des positions du contrepilier selon le mode
        if pyramidal:
            # Mode pyramidal : base large, haut réduit
            pilier_base_start = centre_pilier_x - largeur_pilier_base_finale / 2
            pilier_base_end = centre_pilier_x + largeur_pilier_base_finale / 2
            pilier_haut_start = centre_pilier_x - largeur_pilier_haut / 2
            pilier_haut_end = centre_pilier_x + largeur_pilier_haut / 2
        else:
            # Mode classique : largeur uniforme
            pilier_base_start = centre_pilier_x - largeur_pilier_pour_positionnement / 2
            pilier_base_end = centre_pilier_x + largeur_pilier_pour_positionnement / 2
            pilier_haut_start = pilier_base_start
            pilier_haut_end = pilier_base_end
        
        # getMotif() retourne déjà les hauteurs ajustées
        h = ratios[i]
        if h is None:
            continue
        if h <= 0:
            # hmin=0 : pas de contre-pilier du tout
            continue
        
        # Utiliser directement la valeur de getMotif()
        hauteur_pilier = max(0.0, h)
        
        if pyramidal:
            # Forme pyramidale pour les contrepiliers
            result.extend(
                [
                    (pilier_base_start, y0, 0),
                    (pilier_haut_start, y0 + hauteur_pilier, 0),
                    (pilier_haut_end, y0 + hauteur_pilier, 0),
                    (pilier_base_end, y0, 0),
                ]
            )
        else:
            # Forme rectangulaire classique pour les contrepiliers
            result.extend(
                [
                    (pilier_base_start, y0, 0),
                    (pilier_base_start, y0 + hauteur_pilier, 0),
                    (pilier_base_end, y0 + hauteur_pilier, 0),
                    (pilier_base_end, y0, 0),
                ]
            )

    return result
