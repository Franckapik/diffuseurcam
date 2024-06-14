import bpy
from mathutils import Vector

def get_bounding_box_size(obj):
    bbox = obj.bound_box
    x_size = max([v[0] for v in bbox]) - min([v[0] for v in bbox])
    y_size = max([v[1] for v in bbox]) - min([v[1] for v in bbox])
    z_size = max([v[2] for v in bbox]) - min([v[2] for v in bbox])
    return x_size, y_size, z_size

def pack_objects(objects, bin_width):
    positions = []
    current_x = 0
    current_y = 0
    max_row_height = 0

    for obj in objects:
        x_size, y_size, z_size = get_bounding_box_size(obj)

        if current_x + x_size > bin_width:
            current_x = 0
            current_y += max_row_height
            max_row_height = 0

        positions.append((current_x + x_size / 2, current_y + y_size / 2))
        current_x += x_size
        max_row_height = max(max_row_height, y_size)

    return positions

def place_selected_objects_no_overlap(bin_width):
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    positions = pack_objects(selected_objects, bin_width)

    for obj, (x, y) in zip(selected_objects, positions):
        obj.location = (x, y, 0)

    print("Placement terminé")