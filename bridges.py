""" Début de Script pour l'ajout de bridges personnalisé """


import bpy
import mathutils

def create_empty_at_location(location, name, parent):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    empty = bpy.context.object
    empty.name = name
    empty.parent = parent

def place_empties_on_bounding_box(obj):
    if obj.type != 'MESH':
        print("L'objet sélectionné n'est pas un mesh.")
        return

    # Mettre à jour les données du mesh pour s'assurer que le bounding box est correct
    obj.update_from_editmode()
    
    # Récupérer les coordonnées du bounding box
    bbox = obj.bound_box

    # Utiliser un ensemble pour éviter les doublons
    local_corners = set()
    for corner in bbox:
        corner_vector = mathutils.Vector(corner)
        local_corners.add((corner_vector.x, corner_vector.y, corner_vector.z))

    # Convertir les coordonnées locales en coordonnées mondiales
    world_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in local_corners]

    # Calcule les positions médianes de chaque côté du bounding box
    midpoints = []
    for i in range(len(world_corners)):
        start_vertex = world_corners[i]
        end_vertex = world_corners[(i + 1) % len(world_corners)]
        midpoint = (start_vertex + end_vertex) / 2
        midpoints.append(midpoint)
    
    # Crée un empty à chaque position médiane
    for i, midpoint in enumerate(midpoints):
        create_empty_at_location(midpoint, f"Empty_{i + 1}", obj)