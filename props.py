import bpy
import math


from bpy.props import (
    FloatProperty,
    BoolProperty,
    IntProperty,
    FloatVectorProperty,
    EnumProperty,
    StringProperty,
)

productType = (
    ("0", "Diffuseur 2D", ""),
    ("1", "Diffuseur 1D", ""),
    ("2", "Absorbeur", ""),
    ("3", "Moule", ""),
)


class UIProductProps(bpy.types.PropertyGroup):
    product_type: EnumProperty(items=productType)
    motif_display: EnumProperty(
        name="Vue",
        description="Choisissez un affichage",
        items=[
            ("depth", "Depth", "Profondeur devant les cellules"),
            ("height", "Height", "Hauteur derrière les cellules"),
            ("ratio", "Ratio", "Ratio"),
        ],
        default="depth",
    )


class Usinageprops(bpy.types.PropertyGroup):
    fraise: FloatProperty(
        name="Fraise diametre",
        description="Diametre de la fraise",
        default=0.005,
        step=0.001,
        unit="LENGTH",
        precision=4,
        min=0.001,
        max=0.030,
    )
    offset: EnumProperty(
        name="Offset %",
        items=(
            ("0", "Aucune", ""),
            ("0.05", "5%", ""),
            ("0.10", "10%", ""),
            ("0.20", "20%", ""),
            ("0.30", "30%", ""),
            ("0.50", "50%", ""),
        ),
    )

    def getOffset(self):
        offset = float(self.offset) * float(self.fraise)
        return round(offset, 4)

    def listAttributes(self):
        return [
            "fraise",
            "offset",
            "offset_peigne",
        ]


class DevisProps(bpy.types.PropertyGroup):
    qtyDif: IntProperty(
        name="Quantité",
        description="Quantité de diffuseurs",
        min=1,
        default=1,
    )
    panelx: FloatProperty(
        name="x",
        description="Longueur du panneau",
        default=1.250,
        step=0.001,
        unit="LENGTH",
        precision=3,
    )
    panely: FloatProperty(
        name="y",
        description="Largeur du panneau",
        default=1.220,
        step=0.001,
        unit="LENGTH",
        precision=3,
    )
    panelPrice: FloatProperty(
        name="Prix panneau",
        description="Le prix du panneau",
        default=33,
        step=0.001,
        unit="NONE",
        precision=2,
    )
    marge: FloatProperty(
        name="Bénéfice par marge globale",
        description="La marge du produit (ratio)",
        default=50,
        precision=0,  # Nombre de décimales
        subtype="PERCENTAGE",
        max=200,
        min=0,
    )
    priceByPiece: FloatProperty(
        name="Bénéfice par pièce (€)",
        description="Benefice par pièce pour estimer le temps de travail",
        default=0.10,
        step=1,
        precision=2,  # Nombre de décimales
    )
    urssaf: FloatProperty(
        name="Taxe de l'Urssaf",
        description="La taxe de l'urssaf",
        default=12.3,
        precision=1,  # Nombre de décimales
        subtype="PERCENTAGE",
    )
    alea: FloatProperty(
        name="Aléa",
        description="Le pourcentage de perte courant",
        default=10,
        precision=0,  # Nombre de décimales
        subtype="PERCENTAGE",
        min=0,
        max=50,
    )
    consommable: IntProperty(
        name="Consommable/Diffuseur (€)",
        description="Le prix de la colle, ponçage, fraises, electricité...",
        default=3,
    )

    def getTTCPiece(self, nbPieces, qtyPanel):
        return (
            (self.panelPrice * qtyPanel + self.consommable * self.qtyDif) * (1 + self.alea / 100)
            + nbPieces * self.priceByPiece * self.qtyDif
        ) * (1 + self.urssaf / 100)

    def getTTCMarge(self, qtyPanel):
        return (
            (self.panelPrice * qtyPanel + self.consommable * self.qtyDif)
            * (1 + self.alea / 100)
            * (1 + self.marge / 100)
            * (1 + self.urssaf / 100)
        )

    def getBenefMarge(self, qtyPanel):
        return (self.panelPrice * qtyPanel + self.consommable * self.qtyDif) * (1 + self.alea / 100) * self.marge / 100

    def getBenefPiece(self, nbPieces):
        return nbPieces * self.priceByPiece * self.qtyDif

    def getPriceMP(self, qtyPanel):
        return (self.panelPrice * qtyPanel + self.consommable * self.qtyDif) * (1 + self.alea / 100)


class DevisList(bpy.types.PropertyGroup):
    listDif: StringProperty()


class DiffuseurProps(bpy.types.PropertyGroup):
    epaisseur: FloatProperty(
        name="Epaisseur modèle",
        description="Box epaisseur",
        default=0.003,
        step=0.001,
        unit="LENGTH",
        precision=4,
    )

    type: IntProperty(
        name="Type",
        description="Type du diffuseur",
        min=6,
        max=13,
        default=7,
    )

    profondeur: FloatProperty(
        name="Profondeur",
        description="Box profondeur",
        min=0.05,
        max=0.5,
        default=0.1,
        unit="LENGTH",
        precision=4,
    )
    bord_cadre: FloatProperty(
        name="Bord cadre",
        description="Box bord_cadre",
        min=0.01,
        max=0.5,
        default=0.015,
        unit="LENGTH",
        precision=4,
    )
    largeur_diffuseur: FloatProperty(
        name="Largeur",
        description="Box largeur_diffuseur",
        min=0.05,
        max=5,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )
    tenon_cadre: FloatProperty(
        name="Tenon_cadre",
        description="Box tenon_cadre",
        min=0.01,
        max=0.1,
        default=0.05,
        unit="LENGTH",
        precision=4,
    )
    tenon_accroche: FloatProperty(
        name="Tenon_accroche",
        description="Box tenon_accroche",
        min=0.01,
        max=0.1,
        default=0.05,
        unit="LENGTH",
        precision=4,
    )

    tenon_peigne: FloatProperty(
        name="Tenon peigne",
        description="Box tenon_peigne",
        min=0.01,
        max=0.05,
        default=0.01,
        unit="LENGTH",
        precision=4,
    )

    longueur_diffuseur: FloatProperty(
        name="Longueur",
        description="Box longueur",
        min=0.5,
        max=2,
        default=1,
        step=25,
    )

    longueur_absorbeur: FloatProperty(
        name="Longueur",
        description="Longueur absorbeur",
        min=0.05,
        max=5,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )

    largeur_accroche: FloatProperty(
        name="Largeur accroche",
        description="Box largeur_accroche",
        min=0.05,
        max=1,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )
    largeur_renfort_central: FloatProperty(
        name="Largeur Renfort central",
        description="Box largeur Renfort central",
        min=0.05,
        max=1,
        default=0.5,
        unit="LENGTH",
        precision=4,
    )

    type_tenon_peigne: EnumProperty(
        name="Interface Peigne/Cadre",
        items=(
            ("0", "Pas de tenon", ""),
            ("1", "Double Tenon mi-traversant", ""),
            ("2", "Double Tenon entier", ""),
            ("3", "Mono Tenon mi-traversant", ""),
        ),
    )

    type_tenon_cadre: EnumProperty(
        name="Interface Cadre/Cadre",
        items=(
            ("0", "Pas de tenon", ""),
            ("1", "Tenon mortaise", ""),
        ),
    )

    epaisseur_moule: FloatProperty(
        name="Epaisseur_moule",
        description="Epaisseur du moule",
        min=0.005,
        max=1,
        default=0.01,
        unit="LENGTH",
        precision=4,
    )
    moule_type: EnumProperty(name="Type de Moule", items=(("2d", "2D", ""), ("1d", "1D", "")))

    socle_monopilier: FloatProperty(
        name="Hauteur socle",
        description="Socle additionnel sur les piliers",
        min=0.010,
        max=0.1,
        default=0.030,
        unit="LENGTH",
        precision=3,
    )

    epaisseur_pilier: FloatProperty(
        name="Epaisseur_pilier",
        description="Epaisseur des piliers",
        min=0.003,
        max=1,
        default=0.003,
        unit="LENGTH",
        precision=4,
    )

    pilier_reduction: EnumProperty(
        name="Reduction des piliers",
        items=(
            ("0", "Aucune", ""),
            ("0.05", "5%", ""),
            ("0.10", "10%", ""),
            ("0.20", "20%", ""),
            ("0.30", "30%", ""),
            ("0.50", "50%", ""),
        ),
    )

    pilier_pyramidal: BoolProperty(
        name="Réduction pyramidale",
        description="Applique la réduction seulement sur le haut des piliers pour créer une forme pyramidale",
        default=True,
    )

    pilier_encoches: BoolProperty(
        name="Encoches sur piliers",
        description="Active les encoches au sommet des piliers (recommandé pour les diffuseurs 2D)",
        default=True,
    )

    monopilier_mortaise_reduction: EnumProperty(
        name="Réduction mortaises mono-pilier",
        description="Réduit l'espacement des mortaises du moule mono-pilier",
        items=(
            ("0", "Aucune", ""),
            ("0.05", "5%", ""),
            ("0.10", "10%", ""),
            ("0.20", "20%", ""),
            ("0.30", "30%", ""),
            ("0.50", "50%", ""),
        ),
        default="0",
    )

    decalage_h: IntProperty(
        name="Horizontal",
        description="Décalage",
        min=0,
        max=13,
        default=0,
    )

    decalage_v: IntProperty(
        name="Vertical",
        description="Décalage",
        min=0,
        max=13,
        default=0,
    )

    type_moule: EnumProperty(
        name="Type de moule",
        items=(
            ("stable", "Stable - 2 epaisseurs", ""),
            ("eco", "Eco - 1 epaisseur", ""),
            ("mono", "Mono-Pilier", ""),
        ),
    )
    renfort_central: EnumProperty(
        name="Renfort central",
        items=(
            ("none", "Aucun", ""),
            ("front", "Avant", ""),
            ("back", "Arrière", ""),
            ("both", "Avant/Arrière", ""),
        ),
    )
    renfort_angle: EnumProperty(
        name="Renfort angle",
        items=(
            ("none", "Aucun", ""),
            ("front", "Avant", ""),
            ("back", "Arrière", ""),
            ("both", "Avant/Arrière", ""),
        ),
    )

    qrd_optimization: EnumProperty(
        name="Optimisation QRD 1D",
        description="Mode d'optimisation pour la couverture des ratios en 1D",
        items=(
            ("none", "Aucune", "Utilise la logique initiale sans modification"),
            ("strict", "QRD Strict (QRDude)", "Utilise la formule QRD standard sans modification"),
            ("coverage", "Couverture Optimisée", "Optimise pour une couverture complète des ratios"),
        ),
        default="none"
    )

    offset_peigne: IntProperty(
        name="Offset peigne %",
        description="Offset sur les peignes en %",
        min=0,
        max=10,
        default=0,
    )

    vis: IntProperty(
        name="Diamètre vis accroche",
        description="Le diamètre max pour les vis d'accroche",
        min=4,
        max=12,
        default=6,
    )

    puits_serrage: BoolProperty(
        name="Puits de serrage",
        description="Trou pour le serrage via cales",
    )

    split: FloatProperty(
        name="Split",
        description="Coupe une pièce en deux si depasse cette longueur de martyr",
        min=0,
        max=5,
        default=0,
        unit="LENGTH",
        precision=4,
    )

    def getOffsetPeigne(self):
        offset = float(self.offset_peigne / 100) * float(self.epaisseur)
        return round(offset, 4)

    def getDifName(self):
        dif_name = (
            "N"
            + str(self.type)
            + "W"
            + str(round(self.largeur_diffuseur * 100))
            + "P"
            + str(round(self.profondeur * 100))
            + "L"
            + str(round(self.longueur_diffuseur))
            + "E"
            + str(round(self.epaisseur * 1000))
        )
        return dif_name

    def getRang(self):
        rang = (self.largeur_diffuseur - self.epaisseur) / self.type
        return round(rang, 4)

    def getHauteurTenon(self):
        match self.type_tenon_peigne:
            case "0":
                """Pas de tenons"""
                return 0
            case "1":
                return self.epaisseur / 2
            case "2":
                return self.epaisseur
            case "3":
                """Mono tenon mi traversant"""
                return self.epaisseur / 2

    def getLongueur(self):
        longueurTotale = round(self.type * self.longueur_diffuseur) * self.getRang() + self.epaisseur
        return longueurTotale

    def getLargeurPilier(self):
        if (hasattr(self, 'pilier_pyramidal') and self.pilier_pyramidal and 
            hasattr(self, 'type_moule') and self.type_moule == "mono"):
            # Mode pyramidal uniquement pour mono : retourner la largeur de base (non réduite)
            largeur_pilier = self.getRang() - self.epaisseur
        else:
            # Mode classique : appliquer la réduction uniformément
            largeur_pilier = self.getRang() - self.epaisseur - self.getRang() * float(self.pilier_reduction)
        return round(largeur_pilier, 4)
    
    def getLargeurPilierHaut(self):
        """Retourne la largeur du pilier au sommet (utile pour le mode pyramidal)"""
        if (hasattr(self, 'pilier_pyramidal') and self.pilier_pyramidal and 
            hasattr(self, 'type_moule') and self.type_moule == "mono"):
            # Mode pyramidal uniquement pour mono : largeur réduite au sommet
            largeur_base = self.getRang() - self.epaisseur
            largeur_haut = largeur_base * (1 - float(self.pilier_reduction))
            return round(largeur_haut, 4)
        else:
            # Mode classique : même largeur que la base
            return self.getLargeurPilier()
    
    def getMonopilierMortaiseSpacing(self):
        """Retourne l'espacement entre les centres des mortaises du moule mono-pilier.
        Cette valeur reste constante (largeur_monopilier / 5) pour conserver les positions.
        """
        rang = self.getRang()
        type_count = self.type
        epaisseur = self.epaisseur
        largeur_monopilier = rang * type_count - epaisseur
        
        return largeur_monopilier / 5
    
    def getMonopilierMortaiseLargeur(self):
        """Retourne la largeur des mortaises du moule mono-pilier,
        réduite selon monopilier_mortaise_reduction.
        """
        espacement = self.getMonopilierMortaiseSpacing()
        reduction = float(self.monopilier_mortaise_reduction)
        
        return espacement * (1 - reduction)

    def _find_best_insertion_position(self, sequence, value, type_size):
        """Trouve la meilleure position pour insérer une valeur manquante"""
        if not sequence:
            return 0
        ideal_pos = int((value / type_size) * len(sequence))
        return min(ideal_pos, len(sequence))
    
    def _optimize_1d_coverage(self, base_sequence, target_size):
        """Optimise la couverture d'une séquence QRD 1D"""
        from collections import Counter
        
        all_values = set(range(target_size))
        present_values = set(base_sequence)
        missing_values = sorted(list(all_values - present_values))
        
        if not missing_values:
            return base_sequence
        
        optimized_sequence = base_sequence.copy()
        counts = Counter(optimized_sequence)
        duplicates = [val for val, count in counts.items() if count > 1]
        
        for missing_val in missing_values:
            if duplicates:
                for i, val in enumerate(optimized_sequence):
                    if val in duplicates and counts[val] > 1:
                        optimized_sequence[i] = missing_val
                        counts[val] -= 1
                        if counts[val] <= 1:
                            duplicates.remove(val)
                        break
            else:
                best_pos = self._find_best_insertion_position(
                    optimized_sequence, missing_val, target_size
                )
                if len(optimized_sequence) < target_size:
                    optimized_sequence.insert(best_pos, missing_val)
                else:
                    optimized_sequence[best_pos % len(optimized_sequence)] = missing_val
        
        return optimized_sequence[:target_size]

    def getMotif(self, display):
        ratio = []
        for k in range(0, self.type * round(self.type * self.longueur_diffuseur)):
            n = k % self.type
            m = math.floor(k / self.type)
            an = int(
                (math.pow(n + self.decalage_h, 2) + math.pow(m + self.decalage_v, 2)) % self.type
            )  # phase shifted = 1 on qrdude
            ratio.append(an / 1000)

        # Gestion des trois modes d'optimisation pour les diffuseurs 1D
        if self.moule_type == "1d" and hasattr(self, 'qrd_optimization'):
            if self.qrd_optimization == "coverage":
                # Mode optimisation complète - améliore la couverture
                base_sequence_1d = [int(r * 1000) for r in ratio[:self.type]]
                optimized_sequence = self._optimize_1d_coverage(base_sequence_1d, self.type)
                ratio_1d_optimized = [x / 1000 for x in optimized_sequence]
                
                # Répéter la séquence optimisée si nécessaire
                total_elements = self.type * round(self.type * self.longueur_diffuseur)
                ratio = ratio_1d_optimized * round(self.type * self.longueur_diffuseur)
                ratio = ratio[:total_elements]
            elif self.qrd_optimization == "strict":
                # Mode QRD strict - utilise la formule QRD standard sans modification
                # C'est déjà le comportement par défaut, donc rien à changer
                pass
            elif self.qrd_optimization == "none":
                # Mode aucune optimisation - utilise la logique initiale de base
                # C'est déjà le comportement par défaut, donc rien à changer
                pass

        # Correction importante: amax doit être calculé uniquement sur les éléments utilisés
        # Pour les diffuseurs 1D, seuls les self.type premiers éléments sont utilisés
        if self.moule_type == "1d":
            amax = max(ratio[0:self.type]) if len(ratio) >= self.type else max(ratio)
        else:
            amax = max(ratio)

        depth = []
        for k in range(0, len(ratio)):
            y = (ratio[k] * self.profondeur) / amax
            # Soustraire l'épaisseur pour le pilier ayant la hauteur max
            # Cela permet d'éviter que le pilier ne dépasse du moule
            if ratio[k] == amax:
                y = y - self.epaisseur
            depth.append(round(y, 3))

        height = [self.profondeur - x for x in depth]

        if display == "ratio":
            if self.moule_type == "1d":
                return ratio[0 : self.type]
            else:
                return ratio

        if display == "height":
            if self.moule_type == "1d":
                return height[0 : self.type]
            else:
                return height

        if display == "depth":
            if self.moule_type == "1d":
                return depth[0 : self.type]
            else:
                return depth

    def getArea(self):
        area = (
            self.getLongueur() * self.profondeur * (self.type + 1)
            + self.largeur_diffuseur * self.profondeur * (self.type + 1)
            + len(self.getMotif("depth")) * self.getRang() * self.getRang()
        )
        print(self.largeur_diffuseur)
        return area

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                    "epaisseur",
                    "type",
                    "profondeur",
                    "bord_cadre",
                    "largeur_diffuseur",
                    "tenon_cadre",
                    "tenon_peigne",
                    "longueur_diffuseur",
                    "vis",
                    "type_tenon_peigne",
                    "type_tenon_cadre",
                ]
            case "1":
                return [
                    "epaisseur",
                    "type",
                    "profondeur",
                    "bord_cadre",
                    "largeur_diffuseur",
                    "tenon_cadre",
                    "tenon_peigne",
                    "longueur_diffuseur",
                    "vis",
                    "type_tenon_peigne",
                    "type_tenon_cadre",
                ]
            case "2":
                return [
                    "epaisseur",
                    "profondeur",
                    "largeur_diffuseur",
                    "longueur_absorbeur",
                    "tenon_cadre",
                    "tenon_accroche",
                    "largeur_accroche",
                    "largeur_renfort_central",
                    "split",
                    "vis",
                    "renfort_central",
                    "renfort_angle",
                    "type_tenon_cadre",
                    "puits_serrage",
                ]
            case "3":
                attributes = [
                    "type_moule",
                    "epaisseur",
                    "epaisseur_moule",
                    "pilier_reduction",
                    "type",
                    "profondeur",
                    "largeur_diffuseur",
                    "longueur_diffuseur",
                    "socle_monopilier",
                ]

                # Réduction pyramidale uniquement pour mono-piliers
                if self.type_moule == "mono":
                    attributes.append("pilier_pyramidal")

                # Encoches pour stable et mono seulement (pas eco)
                if self.type_moule == "stable" or self.type_moule == "mono":
                    attributes.append("pilier_encoches")
                
                # Réduction mortaises pour mono-piliers uniquement
                if self.type_moule == "mono":
                    attributes.append("monopilier_mortaise_reduction")

                # Épaisseur pilier pour stable et mono
                if self.type_moule == "stable" or self.type_moule == "mono":
                    attributes.append("epaisseur_pilier")

                return attributes

            case _:
                return


class ArrayProps(bpy.types.PropertyGroup):
    array_offset: FloatProperty(
        name="Offset Array",
        description="Espace entre les pièces",
        min=0.000,
        default=0.01,
        unit="LENGTH",
        precision=4,
    )

    peigne_court_x: IntProperty(
        name="Peigne court",
        default=1,
        min=0,
    )

    peigne_court_y: IntProperty(
        name="Peigne court",
        default=1,
        min=0,
    )

    peigne_long_x: IntProperty(
        name="Peigne long",
        default=1,
        min=0,
    )

    peigne_long_y: IntProperty(
        name="Peigne long",
        default=1,
        min=0,
    )
    cadre_mortaise_x: IntProperty(
        name="Cadre mortaise",
        default=1,
        min=0,
    )

    cadre_mortaise_y: IntProperty(
        name="Cadre mortaise",
        default=1,
        min=0,
    )

    cadre_tenon_x: IntProperty(
        name="Cadre tenon",
        default=1,
        min=0,
    )

    cadre_tenon_y: IntProperty(
        name="Cadre tenon",
        default=1,
        min=0,
    )
    carreau_x: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )

    carreau_y: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )
    carreau_x: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )

    carreau_y: IntProperty(
        name="Carreau",
        default=1,
        min=0,
    )
    accroche_x: IntProperty(
        name="Accroche",
        default=1,
        min=0,
    )

    accroche_y: IntProperty(
        name="Accroche",
        default=1,
        min=0,
    )
    accroche_inverse_x: IntProperty(
        name="Accroche Inverse",
        default=1,
        min=0,
    )

    accroche_inverse_y: IntProperty(
        name="Accroche Invserse",
        default=1,
        min=0,
    )
    renfort_central_x: IntProperty(
        name="Renfort central",
        default=1,
        min=0,
    )

    renfort_central_y: IntProperty(
        name="Renfort central",
        default=1,
        min=0,
    )
    renfort_angle_x: IntProperty(
        name="Renfort angle",
        default=1,
        min=0,
    )

    renfort_angle_y: IntProperty(
        name="Renfort angle",
        default=1,
        min=0,
    )

    fond_moule_x: IntProperty(
        name="Fond Moule",
        default=1,
        min=0,
    )
    fond_moule_y: IntProperty(
        name="Fond Moule",
        default=1,
        min=0,
    )
    cadre_moule_x: IntProperty(
        name="Cadre Moule",
        default=1,
        min=0,
    )
    cadre_moule_y: IntProperty(
        name="Cadre Moule",
        default=1,
        min=0,
    )
    cadre_moule_long_x: IntProperty(
        name="Cadre Moule Long",
        default=1,
        min=0,
    )
    cadre_moule_long_y: IntProperty(
        name="Cadre Moule Long",
        default=1,
        min=0,
    )
    pilier_moule_x: IntProperty(
        name="Piliers Moule",
        default=1,
        min=0,
    )
    pilier_moule_y: IntProperty(
        name="Piliers Moule",
        default=1,
        min=0,
    )
    contre_pilier_moule_x: IntProperty(
        name="Contre Piliers Moule",
        default=1,
        min=0,
    )
    contre_pilier_moule_y: IntProperty(
        name="Contre Piliers Moule",
        default=1,
        min=0,
    )
    cadre_tissu_court_x: IntProperty(
        name="Cadre tissu court",
        default=1,
        min=0,
    )
    cadre_tissu_court_y: IntProperty(
        name="Cadre tissu court",
        default=1,
        min=0,
    )
    cadre_tissu_long_x: IntProperty(
        name="Cadre tissu long",
        default=1,
        min=0,
    )
    cadre_tissu_long_y: IntProperty(
        name="Cadre tissu long",
        default=1,
        min=0,
    )

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                    "peigne_court_x",
                    "peigne_court_y",
                    "peigne_long_x",
                    "peigne_long_y",
                    "cadre_mortaise_x",
                    "cadre_mortaise_y",
                    "cadre_tenon_x",
                    "cadre_tenon_y",
                    "carreau_x",
                    "carreau_y",
                    "accroche_x",
                    "accroche_y",
                ]
            case "1":
                return [
                    "peigne_long_x",
                    "peigne_long_y",
                    "cadre_mortaise_x",
                    "cadre_mortaise_y",
                    "cadre_tenon_x",
                    "cadre_tenon_y",
                    "carreau_x",
                    "carreau_y",
                    "accroche_x",
                    "accroche_y",
                ]
            case "2":
                return [
                    "cadre_mortaise_x",
                    "cadre_mortaise_y",
                    "cadre_tenon_x",
                    "cadre_tenon_y",
                    "accroche_x",
                    "accroche_y",
                    "accroche_inverse_x",
                    "accroche_inverse_y",
                    "renfort_central_x",
                    "renfort_central_y",
                    "renfort_angle_x",
                    "renfort_angle_y",
                    "cadre_tissu_court_x",
                    "cadre_tissu_court_y",
                    "cadre_tissu_long_x",
                    "cadre_tissu_long_y",
                ]
            case "3":
                return [
                    "fond_moule_x",
                    "fond_moule_y",
                    "cadre_moule_x",
                    "cadre_moule_y",
                    "cadre_moule_long_x",
                    "cadre_moule_long_y",
                    "pilier_moule_x",
                    "pilier_moule_y",
                    "contre_pilier_moule_x",
                    "contre_pilier_moule_y",
                ]
            case _:
                return

    def nbPieces(self, product):
        match product:
            case "0":
                return (
                    self.peigne_court_x * self.peigne_court_y
                    + self.peigne_long_x * self.peigne_long_y
                    + self.cadre_mortaise_x * self.cadre_mortaise_y
                    + self.cadre_tenon_x * self.cadre_tenon_y
                    + self.carreau_x * self.carreau_y
                    + self.accroche_x * self.accroche_y
                )

            case "1":
                return (
                    self.peigne_court_x * self.peigne_court_y
                    + self.peigne_long_x * self.peigne_long_y
                    + self.cadre_mortaise_x * self.cadre_mortaise_y
                    + self.cadre_tenon_x * self.cadre_tenon_y
                    + self.carreau_x * self.carreau_y
                    + self.accroche_x * self.accroche_y
                )

            case "2":
                return (
                    self.cadre_mortaise_x * self.cadre_mortaise_y
                    + self.cadre_tenon_x * self.cadre_tenon_y
                    + self.accroche_x * self.accroche_y
                    + self.accroche_inverse_x * self.accroche_inverse_y
                    + self.renfort_central_x * self.renfort_central_y
                    + self.renfort_angle_x * self.renfort_angle_y
                    + self.cadre_tissu_court_x * self.cadre_tissu_court_y
                    + self.cadre_tissu_long_x * self.cadre_tissu_long_y
                )

            case "3":
                return (
                    self.fond_moule_x * self.fond_moule_y
                    + self.cadre_moule_x * self.cadre_moule_y
                    + self.cadre_moule_long_x * self.cadre_moule_long_y
                    + self.pilier_moule_x * self.pilier_moule_y
                    + self.contre_pilier_moule_x * self.contre_pilier_moule_y
                )

            case _:
                return


class PositionProps(bpy.types.PropertyGroup):
    peigne_court_position: FloatVectorProperty(
        name="Peigne court",
        unit="LENGTH",
        precision=4,
    )

    peigne_long_position: FloatVectorProperty(
        name="Peigne long",
        unit="LENGTH",
        precision=4,
    )

    cadre_mortaise_position: FloatVectorProperty(
        name="Cadre mortaise",
        unit="LENGTH",
        precision=4,
    )

    cadre_tenon_position: FloatVectorProperty(
        name="Cadre tenon",
        unit="LENGTH",
        precision=4,
    )

    carreau_position: FloatVectorProperty(
        name="Carreau",
        unit="LENGTH",
        precision=4,
    )
    accroche_position: FloatVectorProperty(
        name="Accroche",
        unit="LENGTH",
        precision=4,
    )
    accroche_inverse_position: FloatVectorProperty(
        name="Accroche inverse",
        unit="LENGTH",
        precision=4,
    )
    renfort_central_position: FloatVectorProperty(
        name="Renfort central",
        unit="LENGTH",
        precision=4,
    )
    renfort_angle_position: FloatVectorProperty(
        name="Renfort angle",
        unit="LENGTH",
        precision=4,
    )
    fond_moule_position: FloatVectorProperty(
        name="Fond Moule",
        unit="LENGTH",
        precision=4,
    )
    pilier_moule_position: FloatVectorProperty(
        name="Pilier Moule",
        unit="LENGTH",
        precision=4,
    )
    contre_pilier_moule_position: FloatVectorProperty(
        name="Contre Pilier Moule",
        unit="LENGTH",
        precision=4,
    )
    cadre_moule_position: FloatVectorProperty(
        name="Cadre Moule",
        unit="LENGTH",
        precision=4,
    )
    cadre_moule_long_position: FloatVectorProperty(
        name="Cadre Moule Long",
        unit="LENGTH",
        precision=4,
    )
    cadre_tissu_long_position: FloatVectorProperty(
        name="Cadre Tissu Long",
        unit="LENGTH",
        precision=4,
    )
    cadre_tissu_court_position: FloatVectorProperty(
        name="Cadre Tissu Court",
        unit="LENGTH",
        precision=4,
    )

    peigne_court_rotation: BoolProperty(name="Peigne court", description="Rotation")

    peigne_long_rotation: BoolProperty(name="Peigne long", description="Rotation")

    cadre_mortaise_rotation: BoolProperty(name="Cadre mortaise", description="Rotation")

    cadre_tenon_rotation: BoolProperty(name="Cadre tenon", description="Rotation")

    carreau_rotation: BoolProperty(name="Carreau", description="Rotation")
    accroche_rotation: BoolProperty(name="Accroche", description="Rotation")
    accroche_inverse_rotation: BoolProperty(name="Accroche inverse", description="Rotation")
    renfort_central_rotation: BoolProperty(name="Renfort central", description="Rotation")
    renfort_angle_rotation: BoolProperty(name="Renfort angle", description="Rotation")
    fond_moule_rotation: BoolProperty(name="Fond Moule", description="Rotation")
    pilier_moule_rotation: BoolProperty(name="Pilier Moule", description="Rotation")
    contre_pilier_moule_rotation: BoolProperty(name="Contre Pilier Moule", description="Rotation")
    cadre_moule_rotation: BoolProperty(name="Cadre Moule", description="Rotation")
    cadre_moule_long_rotation: BoolProperty(name="Cadre Moule", description="Rotation")
    cadre_tissu_long_rotation: BoolProperty(name="Cadre Tissu Long", description="Rotation")
    cadre_tissu_court_rotation: BoolProperty(name="Cadre Tissu Court", description="Rotation")

    def update(self, target, cursor):
        self[target] = cursor

    def listAttributes(self, product):
        match product:
            case "0":
                return [
                    "peigne_court_position",
                    "peigne_long_position",
                    "cadre_mortaise_position",
                    "cadre_tenon_position",
                    "carreau_position",
                    "accroche_position",
                    "peigne_court_rotation",
                    "peigne_long_rotation",
                    "cadre_mortaise_rotation",
                    "cadre_tenon_rotation",
                    "carreau_rotation",
                    "accroche_rotation",
                ]
            case "1":
                return [
                    "peigne_long_position",
                    "cadre_mortaise_position",
                    "cadre_tenon_position",
                    "carreau_position",
                    "accroche_position",
                    "peigne_long_rotation",
                    "cadre_mortaise_rotation",
                    "cadre_tenon_rotation",
                    "carreau_rotation",
                    "accroche_rotation",
                ]
            case "2":
                return [
                    "cadre_mortaise_position",
                    "cadre_tenon_position",
                    "accroche_position",
                    "accroche_inverse_position",
                    "renfort_central_position",
                    "renfort_angle_position",
                    "cadre_tissu_court_position",
                    "cadre_tissu_long_position",
                    "cadre_mortaise_rotation",
                    "cadre_tenon_rotation",
                    "accroche_rotation",
                    "accroche_inverse_rotation",
                    "renfort_central_rotation",
                    "renfort_angle_rotation",
                    "cadre_tissu_court_rotation",
                    "cadre_tissu_long_rotation",
                ]
            case "3":
                return [
                    "fond_moule_position",
                    "fond_moule_rotation",
                    "pilier_moule_position",
                    "pilier_moule_rotation",
                    "contre_pilier_moule_position",
                    "contre_pilier_moule_rotation",
                    "cadre_moule_position",
                    "cadre_moule_rotation",
                    "cadre_moule_long_position",
                    "cadre_moule_long_rotation",
                ]
            case _:
                return


class PrepareProps(bpy.types.PropertyGroup):
    selection_prepare: EnumProperty(items=(("0", "Generated", ""), ("1", "Selected", ""), ("2", "All", "")))

    isConvertToCurve_prepare: BoolProperty(
        name="Convert to curve",
        description="Convert mesh to curve",
    )
    isCRemove_prepare: BoolProperty(
        name="Remove curve doubles",
        description="Remove curve doubles",
    )
    isOvercuts: BoolProperty(
        name="Overcuts",
        description="Add overcuts",
    )
    isJoin_prepare: BoolProperty(
        name="Join all",
        description="Join all parts to one",
    )
    isNewMesh_prepare: BoolProperty(
        name="Create new mesh",
        description="Create a copy from selection",
    )
    isDeleteOldMesh_prepare: BoolProperty(
        name="Delete old mesh",
        description="Delete old mesh",
    )
    isHidingOldMesh_prepare: BoolProperty(
        name="Hide old mesh",
        description="Hide old mesh",
    )
    
    isOffsetCarreau_prepare: BoolProperty(
        name="Offset de ponçage des carreaux",
        description="Applique un offset de 1mm aux pièces nommées 'Carreau' pour le ponçage",
        default=False,
    )

    def listAttributes(self):
        attributes = [
            a
            for a in dir(self)
            if not (
                a.startswith("__")
                or "bl_rna" in a
                or "name" in a
                or "rna_type" in a
                or "listAttributes" in a
                or "getRang" in a
                or "getLongueur" in a
                or "getDifName" in a
            )
        ]
        return attributes


class PositionSelectedProps(bpy.types.PropertyGroup):
    selection_position: EnumProperty(
        items=(("0", "Droite", ""), ("1", "Gauche", ""), ("2", "Haut", ""), ("3", "Bas", ""))
    )


classes = [
    DiffuseurProps,
    ArrayProps,
    PositionProps,
    PrepareProps,
    UIProductProps,
    Usinageprops,
    DevisProps,
    DevisList,
    PositionSelectedProps,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.usinage_props = bpy.props.PointerProperty(type=Usinageprops)
    bpy.types.Scene.dif_props = bpy.props.PointerProperty(type=DiffuseurProps)
    bpy.types.Scene.array_props = bpy.props.PointerProperty(type=ArrayProps)
    bpy.types.Scene.pos_props = bpy.props.PointerProperty(type=PositionProps)
    bpy.types.Scene.pos_sel_props = bpy.props.PointerProperty(type=PositionSelectedProps)
    bpy.types.Scene.prep_props = bpy.props.PointerProperty(type=PrepareProps)
    bpy.types.Scene.product_props = bpy.props.PointerProperty(type=UIProductProps)
    bpy.types.Scene.devis_props = bpy.props.PointerProperty(type=DevisProps)
    bpy.types.Scene.devis_list = bpy.props.CollectionProperty(type=DevisList)
    bpy.types.Scene.dif_parts = []


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.usinage_props
    del bpy.types.Scene.dif_props
    del bpy.types.Scene.array_props
    del bpy.types.Scene.pos_props
    del bpy.types.Scene.pos_sel_props
    del bpy.types.Scene.prep_props
    del bpy.types.Scene.dif_parts
    del bpy.types.Scene.product_props
    del bpy.types.Scene.devis_props
    del bpy.types.Scene.devis_list
