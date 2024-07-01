Trouve rle moyen d'avoir un gcode clair sur ncviewer avec cette histoire de difprops.profondeur.

La génération d'une curve est possible mais le chemin ne semble pas clair alors qu'un fichier gcode est finalement facile a generer depuis python. IL faut travailler en ce sens pour avoir un fichier générer a la base du fichier blend avec les instructions gocde inspirées des fichiers blendercam.

Verifier si les 5mm traversants pour le fond du moule ne devrait pas etre compensés par la hauteur des piliers: si besoin faire une option.

Erreur avec mono tenon mi traversant et overcuts : 

TypeError: 'MultiPolygon' object is not subscriptable
Location: /home/fanch/.apps/blender402/4.0/scripts/modules/bpy/ops.py:109

ajouter modele 3d dans une collection

retravailler sur l'erreur du bouton colle suite probablement à un merge de deux branches peu coherent.


ajouter le moyen de supprimer ou de faire un reset des items de la liste
ici : https://blender.stackexchange.com/questions/16511/how-can-i-store-and-retrieve-a-custom-list-in-a-blend-file

affiner l'affichage de l'ui et verifier dans l'ops si tout est bien ecris pour le add_list

- script qui permet d'assembler les carreaux selon 40cm si necessaité de poncer à la calibreuse.
- génération de bridges via un autre script que blendercam pour pouvoir parenter, faire un bridge sur mesure selon la pièce. 

- overcuts non necessaires sur les stries du peigne
- overcuts non necessaires sur les trous du fond du moule 

proposer un array recommandé.
proposer une option : generer pour la premiere fois. positions sans superpositions