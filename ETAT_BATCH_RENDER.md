# État des lieux — Batch Render, Preview, Caméra, Intervalle

_Document généré le 2026-05-05 — aide au diagnostic et aux pistes de correction_

---

## 1. Architecture générale

### Nomenclature des objets

Format : `N{type}W{largeur_cm}P{profondeur_cm}L{longueur}E{epaisseur_mm}`  
Exemple : `N7W50P5L1E5`

- `N7` → ordre QRD 7
- `W50` → largeur 500 mm
- `P5` → profondeur 50 mm
- `L1` → ratio longueur 1
- `E5` → épaisseur 5 mm

### Collections Blender

Les modèles sont groupés dans des collections dont le nom commence par `Batch_3D_`.  
Exemple : `Batch_3D_12x` pour un batch de 12 modèles.

---

## 2. Génération du Batch — `Batch3DGenerate.execute()`

**Fichier** : `ops.py`, classe `Batch3DGenerate` (~ligne 1771)

### Ordre de génération

```python
combinations = list(iterproduct(product_types, types, profondeurs, longueurs))
```

Ordre des boucles :

1. **product_types** (ex : `["0", "1"]` ou `["0"]`)
2. **types** (ordre QRD, ex : `[7, 11]`)
3. **profondeurs** (ex : `[0.05, 0.10, 0.15]`)
4. **longueurs** (ex : `[1.0]`)

Exemple pour types=[7,11], profondeurs=[5,10,15]mm, longueurs=[1] :

```
i=0  → N7W50P5L1E5
i=1  → N7W50P10L1E5
i=2  → N7W50P15L1E5
i=3  → N11W50P5L1E5
i=4  → N11W50P10L1E5
i=5  → N11W50P15L1E5
```

Les objets générés sont stockés dans `generated_objects` (liste Python) dans cet ordre.  
Tous les objets vont dans **la même collection** `Batch_3D_Nx`.

---

## 3. Collecte des objets pour le Batch Render — `BatchRender.invoke()`

**Fichier** : `ops.py`, ~ligne 2348

```python
raw_objects = []
for collection in sorted(bpy.data.collections, key=lambda c: c.name):
    if collection.name.startswith("Batch_3D_"):
        for obj in sorted(collection.objects, key=lambda o: o.name):
            if obj.type == 'MESH':
                raw_objects.append(obj)
```

L'ordre est donc : **tri alphanumérique sur les noms d'objets** (Python str sort).

### ⚠️ Problème connu : tri alphanumérique vs tri numérique

Le tri `sorted(..., key=lambda o: o.name)` est **alphabétique**, pas numérique.  
Exemples de noms : `N7W50P10L1E5`, `N7W50P15L1E5`, `N7W50P5L1E5`

Tri alphabétique Python :

```
N7W50P10L1E5   ← "P10" < "P15" < "P5" alphabétiquement
N7W50P15L1E5
N7W50P5L1E5    ← "P5" vient APRÈS "P10" et "P15"
```

**Le premier rendu serait donc `N7W50P10L1E5` et non `N7W50P5L1E5` comme attendu.**

Cette inversion explique le constat utilisateur : _"le rendu DEVRAIT commencer par N7W50P5L1E5"_.

---

## 4. Collecte des objets pour le Preview — `BatchRenderPreview.execute()`

**Fichier** : `ops.py`, ~ligne 2966

```python
batch_objs = []
for collection in sorted(bpy.data.collections, key=lambda c: c.name):
    if collection.name.startswith("Batch_3D_"):
        for obj in sorted(collection.objects, key=lambda o: o.name):
            if obj.type == 'MESH':
                batch_objs.append(obj)
```

Même logique que le batch render (corrigé dans la session en cours).  
**Même bug de tri alphabétique → mêmes conséquences sur l'index affiché.**

---

## 5. Navigation Preview — `BatchRenderPreviewNavigate.execute()`

**Fichier** : `ops.py`, ~ligne 3232

```python
batch_objs = [
    obj
    for collection in sorted(bpy.data.collections, key=lambda c: c.name)
    if collection.name.startswith("Batch_3D_")
    for obj in sorted(collection.objects, key=lambda o: o.name)
    if obj.type == 'MESH'
]
```

Même logique (corrigé dans la session). L'index `rp.preview_object_index` est incrémenté/décrémenté puis passe à `BatchRenderPreview.execute()` → cohérence OK tant que le tri est identique dans les deux.

---

## 6. Positionnement de la caméra — `_position_camera()`

**Fichier** : `ops.py`, ~ligne 2762

```python
max_dim = max(target_size.x, target_size.y, target_size.z)
fov = cam_obj.data.angle
frame_distance = (max_dim / 2) / math.tan(fov / 2) if fov > 0 else max_dim * 2
distance = frame_distance * 1.4 + rp.camera_distance
```

La distance est calculée à partir de **la plus grande des 3 dimensions**.

### ⚠️ Problème avec les modèles profonds (P10, P15)

| Modèle | X (largeur) | Y (longueur) | Z (profondeur) | max_dim |
| ------ | ----------- | ------------ | -------------- | ------- |
| P5     | ~500mm      | ~500mm       | 50mm           | ~500mm  |
| P10    | ~500mm      | ~500mm       | 100mm          | ~500mm  |
| P15    | ~500mm      | ~500mm       | 150mm          | ~500mm  |

Pour les valeurs ci-dessus, `max_dim` reste X ou Y → pas de problème.  
**Mais si `largeur < profondeur` (diffuseurs petits ou profonds), Z devient max_dim → distance excessive.**

---

## 7. Calcul de la bounding box — `_get_bbox_info()`

**Fichier** : `ops.py`, ~ligne 2749

```python
bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
```

Utilise `matrix_world` de l'objet. Ce champ n'est mis à jour par Blender qu'au prochain cycle du dépsgraphe.

### ⚠️ Problème : matrix_world périmé après rotation

Lorsque le modal fait :

```python
obj.rotation_euler = new_rot
# puis immédiatement :
bbox_center, bbox_size = self._get_bbox_info(obj)
```

`matrix_world` n'a pas encore été recalculé → la bounding box est calculée avec l'ancienne rotation.

Le correctif ajouté dans la session précédente :

```python
bpy.context.view_layer.update()
```

**Ce correctif est présent dans le code actuel (ligne ~2563).**  
Cependant son efficacité dépend du contexte Blender : pendant un rendu modal, `view_layer.update()` peut ne pas déclencher une réévaluation complète du dépsgraphe.

---

## 8. Gestion de la visibilité (`hide_render`) — Modal

Dans le modal, **à chaque tick** :

```python
for other in self._batch_objects:
    other.hide_render = (other is not obj)
```

Puis à la fin (`_finish`) :

```python
for obj in self._all_batch_objects:
    if obj.name in self._orig_hide_render:
        obj.hide_render = self._orig_hide_render[obj.name]
```

### ⚠️ Bug potentiel : `_batch_objects` ≠ `_all_batch_objects` avec intervalle

Quand un intervalle est défini :

- `_all_batch_objects` = tous les objets (stocke l'état original)
- `_batch_objects` = sous-ensemble (ceux à rendre)

Dans le modal, seuls les objets de `_batch_objects` sont masqués/démasqués par le bloc d'isolation.  
Les objets hors-intervalle ont été masqués en `invoke()` et ne sont **pas touchés** dans le modal.

Cependant : **si un objet hors-intervalle partage la scène et son `hide_render` était `False`, il reste visible pendant tous les rendus de l'intervalle** si on a oublié de le masquer. Vérification → le code `invoke()` masque bien tous les hors-intervalle :

```python
rendered_names = {obj.name for obj in self._batch_objects}
for obj in self._all_batch_objects:
    if obj.name not in rendered_names:
        obj.hide_render = True
```

Cette partie semble correcte.

---

## 9. Historique Git — Évolution des fonctionnalités

| Commit    | Tag/Message              | État batch render                                                       |
| --------- | ------------------------ | ----------------------------------------------------------------------- |
| `42dfab5` | batch render cycle       | **Version de référence** — pas de tri, pas d'intervalle, pas de preview |
| `105ebca` | render preview           | Ajout preview, toujours sans tri                                        |
| `29a1322` | scale light              | Auto-scale énergie                                                      |
| `50cace9` | v2.6.0                   | Version stable avant modifications de session                           |
| `3d84bdb` | intermediate commit      | En cours                                                                |
| `2c8538f` | going back to good light | **HEAD actuel**                                                         |

**Dans `42dfab5` (batch render cycle) :** collecte sans `sorted()` → ordre non garanti mais probablement stable (ordre d'insertion Blender). Aucune isolation des objets autres que `_batch_objects`. Pas d'intervalle.

**Dans `105ebca` (render preview) :** idem pour le batch, preview ajouté sans tri.

**Les modifications de la session** (non commitées) ont ajouté :

- `sorted()` sur collections ET objets → introduit le bug de tri alphabétique
- `_all_batch_objects` + masquage hors-intervalle
- `view_layer.update()` avant `_get_bbox_info`

---

## 10. Symptôme rapporté

> "Sur les 58 premiers rendus, seul les deux premiers : N11W50P10L1E5 à 0° et 29° ont un rendu correct"

- Le premier rendu est `N11W50P10L1E5` au lieu de `N7W50P5L1E5` → **tri alphabétique incorrect**
- Seuls les 2 premiers rendus sont corrects → possiblement un crash/corruption après le 2ème

---

## 11. Hypothèses classées par probabilité

### H1 — Tri alphanumérique (HAUTE PROBABILITÉ — confirme le symptôme)

**Cause** : `sorted(..., key=lambda o: o.name)` est alphabétique.  
`N11W50P10L1E5` < `N7W50P5L1E5` alphabétiquement car `'1' < '7'`.

**Conséquence** : les objets N11 viennent avant N7 → ordre de rendu inversé par rapport à l'intention.

**Preuve** : l'utilisateur confirme que le premier rendu est `N11W50P10L1E5`.

**Fix proposé** : trier par extraction numérique des composants du nom.

```python
import re

def _sort_key_dif_name(obj):
    """Tri numérique sur N, W, P, L, E extraits du nom du modèle."""
    m = re.match(r'N(\d+)W(\d+)P(\d+)L(\d+)E(\d+)', obj.name)
    if m:
        return tuple(int(x) for x in m.groups())
    return (9999, 9999, 9999, 9999, 9999)
```

À utiliser partout (invoke, preview execute, navigate execute).

---

### H2 — `view_layer.update()` insuffisant dans le contexte modal (MOYENNE PROBABILITÉ)

**Cause** : `bpy.context.view_layer.update()` peut être un no-op pendant un modal render handler si le contexte Blender est en état de rendu.

**Conséquence** : `matrix_world` périmé → bounding box incorrecte → caméra positionnée par rapport à l'ancienne position → image vide ou mal cadrée pour les modèles ayant été déplacés/rotés.

**Preuve partielle** : seuls les 2 premiers rendus sont corrects (premier rendu = rotation 0 → pas de rotation appliquée → `matrix_world` valide).

**Fix proposé** : utiliser `bpy.context.evaluated_depsgraph_get()` pour obtenir la bounding box depuis l'objet évalué, sans dépendre de `matrix_world` mis à jour :

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
bbox_corners = [obj_eval.matrix_world @ Vector(corner) for corner in obj_eval.bound_box]
```

---

### H3 — Régression liée à l'ajout du tri (HAUTE PROBABILITÉ pour l'ordre)

**Cause** : Avant les modifications de la session, les objets n'étaient **pas triés** (`for obj in collection.objects`). L'ordre était celui de la collection Blender, qui correspond à l'ordre d'insertion dans `Batch3DGenerate.execute()` → ordre de génération prévisible et conforme au tableau de combinaisons.

**Conséquence** : Le tri `sorted(..., key=lambda o: o.name)` introduit au nom d'une "stabilité" est en réalité **moins correct** que l'ordre original.

**Fix proposé** : Soit revenir à l'ordre non trié (comme dans `42dfab5`), soit implémenter un tri numérique (H1).

---

### H4 — Corruption de `hide_render` en cascade (MOYENNE PROBABILITÉ)

**Cause** : Dans le modal, à chaque tick :

```python
for other in self._batch_objects:
    other.hide_render = (other is not obj)
```

Ceci met `hide_render = True` sur tous les objets sauf l'actuel.  
Si un rendu échoue (exception), `_finish()` est **appelé** mais les objets restent dans un état partiel.  
À la prochaine exécution du batch render, `_orig_hide_render` est recalculé — mais si des objets sont déjà `hide_render=True` depuis le run précédent, leur état "original" sauvegardé est `True`.

**Conséquence** : les objets pensent être cachés à l'origine → ne sont jamais remis à `False` → rendus vides à partir d'un certain index.

**Fix proposé** : Forcer `hide_render = False` pour tous les objets batch au début de `invoke()`, avant de sauvegarder l'état :

```python
# Forcer la visibilité de tous les objets batch (réinitialisation robuste)
for obj in raw_objects:
    obj.hide_render = False
# Puis sauvegarder l'état (tous à False désormais)
self._orig_hide_render = {obj.name: False for obj in self._all_batch_objects}
```

---

### H5 — Un seul objet dans une collection unique (FAIBLE PROBABILITÉ mais à vérifier)

**Cause** : Si tous les modèles sont dans une seule collection `Batch_3D_12x`, le tri par collection n'est pas le problème. Mais si plusieurs collections existent (ex: `Batch_3D_6x_A` et `Batch_3D_6x_B`), leur ordre alphabétique peut créer un interleaving inattendu.

**Fix proposé** : vérifier avec `ClearBatch3D` + régénération pour repartir d'une collection propre.

---

### H6 — Conflit avec le `_cleanup_preview()` appelé deux fois dans `invoke()` (FAIBLE PROBABILITÉ)

Dans `BatchRender.invoke()`, `_cleanup_preview()` est appelé **deux fois** :

```python
# Appel 1 — début d'invoke
BatchRenderPreview._cleanup_preview(context)
# ...
# Appel 2 — après collecte des objets
BatchRenderPreview._cleanup_preview(context)
```

Le second appel est redondant mais inoffensif — **à moins** que le premier ait restauré des rotations et que le second les re-restaure à une valeur incorrecte si `_preview_rotations` a été supprimé par le premier appel.  
Probable non-issue mais à nettoyer.

---

## 14. Analyse du log de rendu fourni (48 objets × 2 angles = 96 rendus)

```
[1/96] N11W50P10L1E5 (-29°)
[2/96] N11W50P10L1E5 (0°)
[3/96] N11W50P10L1E5.001 (-29°)   ← doublon .001
...
[25/96] N11W50P5L1E5 (-29°)       ← P5 arrive APRÈS P10, P15, P20
...
[33/96] N13W50P10L1E5 (-29°)      ← N13 après tous les N11
```

**Observations confirmées :**

1. **Tri alphabétique actif** → N11 < N13 < N7 en alpha ; P10 < P15 < P20 < P5 en alpha
2. **Doublons `.001`** → le batch a été généré 2× sans `ClearBatch3D` → 48 objets (24 × 2)
3. **Multi-angle fonctionne** → 2 angles (-29° et 0°) imbriqués correctement pour chaque objet
4. **Aucun rendu vide** dans ce log → le `view_layer.update()` ou la réinitialisation `hide_render=False` ont aidé

---

## 15. Correctifs appliqués (session actuelle)

| Correctif                                                                                                                                  | Fichier  | Lignes     |
| ------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ---------- |
| `import re` + fonction `_batch_sort_key()` (tri numérique N/W/P/L/E)                                                                       | `ops.py` | 9-26       |
| Remplacement `sorted(..., key=lambda o: o.name)` → `sorted(..., key=_batch_sort_key)` dans `invoke`, `preview execute`, `navigate execute` | `ops.py` | 3 endroits |
| Réactivation des collections `Batch_3D_*` exclues du view layer dans `invoke()`                                                            | `ops.py` | invoke     |
| `hide_render=False` forcé sur tous les objets batch avant sauvegarde état                                                                  | `ops.py` | invoke     |
| Restauration de l'état d'exclusion des collections dans `_finish()`                                                                        | `ops.py` | \_finish   |
| `_orig_collection_exclude = {}` dans les attributs de classe                                                                               | `ops.py` | attributs  |
| `view_layer.update()` avant `_get_bbox_info()` dans le modal                                                                               | `ops.py` | modal      |

**Ordre de rendu attendu après correctifs** pour types=[7,11,13], profondeurs=[5,10,15,20]mm, longueurs=[1,2] :

```
N7W50P5L1E5, N7W50P5L2E5, N7W50P10L1E5, N7W50P10L2E5, ...
N11W50P5L1E5, N11W50P5L2E5, ...
N13W50P5L1E5, ...
```

**Note sur les doublons :** utiliser `ClearBatch3D` avant chaque régénération de batch.  
Le suffixe `.001` est ajouté automatiquement par Blender quand un objet de même nom existe déjà.

### Étape 1 — Corriger le tri (résout H1 + H3)

Remplacer dans les 3 endroits (`invoke`, `preview execute`, `navigate execute`) :

```python
# AVANT
for obj in sorted(collection.objects, key=lambda o: o.name):
# APRÈS
for obj in sorted(collection.objects, key=_sort_key_dif_name):
```

Avec `_sort_key_dif_name` définie comme fonction module-level dans `ops.py`.

**Alternative plus simple** : revenir à l'ordre non trié comme dans `42dfab5` (ordre d'insertion Blender = ordre de génération `Batch3DGenerate`).

### Étape 2 — Corriger la bounding box (résout H2)

Remplacer dans `_get_bbox_info` :

```python
bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
```

par :

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
bbox_corners = [obj_eval.matrix_world @ Vector(corner) for corner in obj_eval.bound_box]
```

### Étape 3 — Réinitialisation robuste de hide_render (résout H4)

Dans `BatchRender.invoke()`, avant la sauvegarde de `_orig_hide_render` :

```python
for obj in raw_objects:
    obj.hide_render = False
```

### Étape 4 — Supprimer le double `_cleanup_preview()` (résout H6)

Supprimer le second appel redondant dans `invoke()`.

---

## 13. Vérification par git — Retour à une version stable

Pour vérifier que le problème vient bien des modifications récentes :

```bash
# Voir les diffs des modifications non commitées
git diff ops.py

# Ou revenir à la version v2.6.0 pour test
git stash
# tester avec Blender
git stash pop
```

La version `50cace9` (v2.6.0) est le dernier tag stable avant les modifications de session. Elle n'avait **pas** de `sorted()` sur les objets, pas d'intervalle, et pas de `view_layer.update()`. Les rendus fonctionnaient dans l'ordre de génération.
