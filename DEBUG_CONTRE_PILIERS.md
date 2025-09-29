# Debug des Contre-Piliers - Instructions

## 🔧 Système de debug mis en place

### Logs ajoutés
Un système de debug complet a été ajouté pour tracer la génération des contre-piliers :

#### Dans `ops.py` - Opérateur `AddContrePilierMoule`
- Vérification du `product_type` (doit être "3" pour moule)
- Affichage du `type_moule` (eco/stable/mono)
- Vérification que des vertices sont générés
- Gestion d'erreurs avec traceback complet

#### Dans `shapes.py` - Fonction `add_contre_pilier_moule`
- Trace de tous les paramètres d'entrée
- Vérification des ratios (motifs height)
- Suivi du traitement pour chaque type de moule
- Comptage des vertices et edges générés

#### Dans `pattern.py` - Fonctions de génération
- `contremonopilier_hauteurs_stable()` : Debug des calculs de hauteur
- `contremonopilier_hauteurs_eco()` : Debug des calculs de hauteur

## 🧪 Comment tester

### 1. Configuration dans Blender
```
Product Type: "3" (Moule)
Type de moule: "stable" ou "eco" ou "mono"
```

### 2. Observation des logs
Après avoir cliqué sur le bouton "Contre Pilier Moule", consultez la **console Blender** :
- `Window > Toggle System Console` (Windows)
- Ou regardez le terminal où Blender a été lancé (Linux/Mac)

### 3. Messages attendus
```
🔧 [DEBUG CONTRE-PILIERS] === DÉBUT GÉNÉRATION ===
🔧 [DEBUG] product_type: 3
🔧 [DEBUG] type_moule: stable
🔧 [DEBUG] type: 4
🔧 [DEBUG] profondeur: 0.06
🔧 [DEBUG] Appel de add_contre_pilier_moule...
🔧 [DEBUG SHAPES] === DÉBUT add_contre_pilier_moule ===
...
✅ [DEBUG] Objet créé: Piliers
🔧 [DEBUG CONTRE-PILIERS] === FIN GÉNÉRATION ===
```

## 🔍 Diagnostic possible

### Si aucun log n'apparaît
- L'opérateur n'est pas appelé → Vérifier l'UI
- Problème de chargement de l'addon → Vérifier `bl_info`

### Si les logs s'arrêtent à un endroit précis
- Erreur de syntaxe → Le debug montrera l'exception
- Paramètres incorrects → Les valeurs seront affichées

### Si "Aucun vertex généré!"
- Problème dans la logique de génération
- Ratios vides ou malformés
- Type de moule non reconnu

## 🎯 Prochaines étapes

1. **Tester** la génération avec le debug activé
2. **Copier** les logs de la console
3. **Identifier** où le processus s'arrête ou échoue
4. **Corriger** le problème identifié

Les logs permettront de voir exactement ce qui se passe et où le problème se situe.
