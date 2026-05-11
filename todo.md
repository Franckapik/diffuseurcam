Les dimensions d'un produits sont externes.
Or, depuis la mise ne place de la fonctionnalité "cadre epais", il est possible que les dimensions internes ne soient plus respectées. Par exemple, un modèle de 600x1200 doit préservé ces dimensions à l'extérieur, et tout le coeur du systeme : les peignes, carreaux, etc... doivent prendre en compte l'épaisseur du cadre : les longueurs de peignes et de carreaux sont ainsi diminuées, et les acluls des largeur de carreaux doivent permettre des dimensions uniformes.Actuellement, si je genere un modèle 3D, je vois que les carreaux externes seulement sont rognés et qu'une re-répartition est necessaire pour atteindre un équilibre. Lorsque le cadre_epais n'est pas coché, la dimension de ce cadre est naturellement celle du modèle par defaut.
Peut tu tout d'abord analyser le code actuel, vérifier les éléments qui entre en contradiction vis à vis de ce que je souhaite, planifier une refonte dans tous les calculs qui permette ce changement. ENfin, peut tu, avec tes mots plus justes/techniques, me décrire ce que je souhaite, afin de m'assurer que ma demande est bien comprise.

ajouter nombre panneaux superposés pour faire des comptes (ex : dp123) et agencer tout de meme selon un array different
pré-remplir : le nombre de carreaux doit etre ajusté si modele double!
Pré-remplir pour l'abs en prenant en compte le is-splitted pour faire x2.
Travailler les accroches pour avoir un motif plus adapté si besoin.
Puis de serrage parametrable en terme de dimensions
travailler les position array pour cadre tissu court et long dans ops car copier coller d'un autre sans modif
verifier que le rechargement du script s'effectue bien après update (bl info issue).
ajouter une possibilité d'alignement positif/negatif selon la touche shift + fleche pressée pour position selected et de pouvoir selctionner pusieurs objets pour réaliser les dpclmts.

Moule 1D sans les inserts de croix ?

travailler sur les edges entres les mono piliers du 2D.
faire coincider reduction des piliers avec la variable existante pour le 2d stable a la base.
Pouvoir faire des cercles pour recconiatre les piliers de 1 à 13 par ex.

meiulleur affichage a faire du nombre d'occurences des piliers.
prendre en consideration la profondeur du moule pour la hauteur des piliers qui s'enfonce dans le moule
avoir un perimetre decouper autours d'une selection de pieces pour permetre le poncage groupé a la calibreuse

Attention : a faire, mono pilier et contrepilier lorsque il existe une reduction des piliers !
mono pilier/contre si stable ou eco ? (code supprimé en attendant)
debord moule réglé à 5cm => en faire une variable ?
hide old modele apres overcut

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

IL Y A TOUJOURS UN CONFLIT AVEC LES EMBASES DES MONO PILIERS ET LES PLAQUES DE MOULES . Les embases sont trop longues, il faudrait réduire de 5mm de chaque coté.

Corriger le comportement des encoches sur piliers 2D + piramide .
