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
    
    # Dans le contexte du moule mono, la largeur disponible est largeur_monopilier
    # largeur_monopilier = rang * type - epaisseur = (largeur_diffuseur - epaisseur) - epaisseur = largeur_diffuseur - 2*epaisseur
    largeur_monopilier = largeur_diffuseur - 2 * epaisseur
    # Zone utile pour les piliers : on laisse epaisseur de marge à droite
    largeur_utile = largeur_monopilier - epaisseur
    
    # Calcul de l'espace théorique par pilier dans la zone utile
    if difprops.type > 0:
        espace_theorique_par_pilier = largeur_utile / difprops.type
    else:
        espace_theorique_par_pilier = largeur_utile
    
    # Calcul de la largeur des piliers selon le mode pyramidal
    largeur_pilier_base = espace_theorique_par_pilier - epaisseur  # Espace pour le pilier moins l'épaisseur de séparation
    
    if pyramidal:
        # Mode pyramidal : la base garde la largeur originale, seul le haut est réduit
        largeur_pilier_base_finale = largeur_pilier_base  # Base non réduite
        largeur_pilier_haut = largeur_pilier_base * (1 - reduction_ratio)  # Haut réduit
    else:
        # Mode classique : réduction uniforme sur toute la hauteur
        largeur_pilier_base_finale = largeur_pilier_base * (1 - reduction_ratio)
        largeur_pilier_haut = largeur_pilier_base_finale
    
    # Pour centrer l'ensemble des piliers : utiliser la largeur de base pour le positionnement
    largeur_pilier_pour_positionnement = largeur_pilier_base_finale
    
    if difprops.type > 1:
        # Calcul de l'espace total occupé par tous les piliers (base)
        espace_total_piliers = difprops.type * largeur_pilier_pour_positionnement
        # Espace restant à répartir entre les intervalles (type-1 intervalles)
        espace_pour_intervalles = largeur_utile - espace_total_piliers
        # Intervalle uniforme entre les piliers
        intervalle_entre_piliers = espace_pour_intervalles / (difprops.type - 1)
        # Espacement entre centres = largeur pilier + intervalle
        espacement_entre_centres = largeur_pilier_pour_positionnement + intervalle_entre_piliers
        
        # Position du premier pilier : centré dans la largeur complète du moule
        # Le moule va de (x - epaisseur) à (largeur_monopilier + epaisseur)
        # Nous devons centrer l'ensemble des piliers dans cette largeur totale
        largeur_totale_moule = largeur_monopilier + 2 * epaisseur  # = largeur_diffuseur
        largeur_ensemble_total = (difprops.type - 1) * espacement_entre_centres + largeur_pilier_pour_positionnement
        marge_centrage_moule = (largeur_totale_moule - largeur_ensemble_total) / 2
        x_premier_pilier = (x - epaisseur) + marge_centrage_moule + largeur_pilier_pour_positionnement / 2
        
        # Calculons les positions réelles des piliers par rapport au moule complet
        positions_piliers = []
        for i in range(difprops.type):
            centre_pilier = x_premier_pilier + i * espacement_entre_centres
            debut_pilier = centre_pilier - largeur_pilier_pour_positionnement / 2
            fin_pilier = centre_pilier + largeur_pilier_pour_positionnement / 2
            positions_piliers.append((debut_pilier, fin_pilier))
        
        premier_debut = positions_piliers[0][0]
        dernier_fin = positions_piliers[-1][1]
        # Les marges sont calculées par rapport aux limites du moule
        marge_gauche_moule = premier_debut - (x - epaisseur)  # Distance depuis le début du moule
        marge_droite_moule = (largeur_monopilier + epaisseur) - dernier_fin  # Distance jusqu'à la fin du moule
        # Les marges utiles (par rapport à la zone de piliers)
        marge_gauche_utile = premier_debut - (x + epaisseur)
        marge_droite_utile = (x + epaisseur + largeur_utile) - dernier_fin
    else:
        # Un seul pilier, centré parfaitement dans le moule complet
        espacement_entre_centres = 0
        largeur_totale_moule = largeur_monopilier + 2 * epaisseur
        x_premier_pilier = (x - epaisseur) + largeur_totale_moule / 2
    
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
    
    # Dans le contexte du moule mono, la largeur disponible est largeur_monopilier
    # largeur_monopilier = rang * type - epaisseur = (largeur_diffuseur - epaisseur) - epaisseur = largeur_diffuseur - 2*epaisseur
    largeur_monopilier = largeur_diffuseur - 2 * epaisseur
    # Zone utile pour les piliers : on laisse epaisseur de marge à droite
    largeur_utile = largeur_monopilier - epaisseur
    
    # Calcul de l'espace théorique par pilier dans la zone utile
    if difprops.type > 0:
        espace_theorique_par_pilier = largeur_utile / difprops.type
    else:
        espace_theorique_par_pilier = largeur_utile
    
    # Calcul de la largeur des contrepiliers selon le mode pyramidal
    largeur_pilier_base = espace_theorique_par_pilier - epaisseur  # Espace pour le pilier moins l'épaisseur de séparation
    
    if pyramidal:
        # Mode pyramidal : la base garde la largeur originale, seul le haut est réduit
        largeur_pilier_base_finale = largeur_pilier_base  # Base non réduite
        largeur_pilier_haut = largeur_pilier_base * (1 - reduction_ratio)  # Haut réduit
    else:
        # Mode classique : réduction uniforme sur toute la hauteur
        largeur_pilier_base_finale = largeur_pilier_base * (1 - reduction_ratio)
        largeur_pilier_haut = largeur_pilier_base_finale
    
    # Pour centrer l'ensemble des piliers : utiliser la largeur de base pour le positionnement
    largeur_pilier_pour_positionnement = largeur_pilier_base_finale
    
    if difprops.type > 1:
        # Calcul de l'espace total occupé par tous les piliers (base)
        espace_total_piliers = difprops.type * largeur_pilier_pour_positionnement
        # Espace restant à répartir entre les intervalles (type-1 intervalles)
        espace_pour_intervalles = largeur_utile - espace_total_piliers
        # Intervalle uniforme entre les piliers
        intervalle_entre_piliers = espace_pour_intervalles / (difprops.type - 1)
        # Espacement entre centres = largeur pilier + intervalle
        espacement_entre_centres = largeur_pilier_pour_positionnement + intervalle_entre_piliers
        
        # Position du premier pilier : centré dans la largeur complète du moule
        # (même logique que monopilier_profondeurs)
        largeur_totale_moule = largeur_monopilier + 2 * epaisseur  # = largeur_diffuseur
        largeur_ensemble_total = (difprops.type - 1) * espacement_entre_centres + largeur_pilier_pour_positionnement
        marge_centrage_moule = (largeur_totale_moule - largeur_ensemble_total) / 2
        x_premier_pilier = (x - epaisseur) + marge_centrage_moule + largeur_pilier_pour_positionnement / 2
    else:
        # Un seul pilier, centré parfaitement dans le moule complet
        espacement_entre_centres = 0
        largeur_totale_moule = largeur_monopilier + 2 * epaisseur
        x_premier_pilier = (x - epaisseur) + largeur_totale_moule / 2

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
