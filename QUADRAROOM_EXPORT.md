# Export GLB QuadraRoom

Dans **Modèle 3D → Batch 3D → GLB QuadraRoom (sans textures)** :

1. Générer les produits du batch.
2. Choisir le dossier QuadraRoom.
3. Cliquer sur **Exporter GLB QuadraRoom**.

Les matériaux Blender portent directement les identifiants utilisés par QuadraRoom :

| Matériau Blender | Identifiant exporté |
| --- | --- |
| `wood` | `wood` |
| `fabric` | `fabric` |

Les deux matériaux sont chargés depuis `materials.blend` une seule fois puis partagés entre les produits générés. Le fichier contient uniquement `wood` et `fabric` et les quatre images utilisées par le bois, toutes emballées dans le fichier Blender. Le matériau `fabric` ne dépend d'aucune image. Si le fichier est absent ou incomplet, la génération s'arrête avec un message d'erreur. Une face utilisant un autre matériau bloque l'export ; le message précise l'objet, la face et le matériau concernés.

Chaque référence reconnue dans une collection `Batch_3D_*` produit un GLB autonome. Le suffixe d'épaisseur `E...` est conservé ou ajouté s'il manque ; un suffixe Blender tel que `.001` est retiré. Deux objets avec la même référence bloquent l'export. Les objets auxiliaires sans nom de référence sont ignorés. Le contenu GLB garde les normales, `TEXCOORD_0` et l'affectation des primitives à `wood` ou `fabric`. Aucune image ni texture n'est embarquée. Le produit est centré sur sa boîte englobante, en mètres, avec X = largeur, Y = hauteur, Z = profondeur dans QuadraRoom. L'export utilise une copie temporaire du maillage ; la scène et les matériaux restent intacts.

La version cible de l'addon est **Blender 5.1.0**. Son exporteur glTF propose `export_materials='VIEWPORT'` et `export_image_format='NONE'`. L'addon exporte une copie temporaire du maillage avec les matériaux d'origine puis vérifie le GLB obtenu. Les noms des matériaux ne sont pas réécrits. Si les UV ou les normales manquent, ou si une image ou une texture est présente, le fichier est refusé.
