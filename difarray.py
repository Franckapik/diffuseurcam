import bpy


def difArray(mesh_obj, array_offset, count_x, count_y, x_offset, y_offset):
    arrx = bpy.data.objects[mesh_obj.name].modifiers.new(
        name=mesh_obj.name + " X", type="ARRAY"
    )
    arrx.use_relative_offset = False
    arrx.use_constant_offset = True
    arrx.constant_offset_displace[0] = x_offset + array_offset
    arrx.constant_offset_displace[1] = 0
    arrx.count = count_x

    arry = bpy.data.objects[mesh_obj.name].modifiers.new(
        name=mesh_obj.name + " Y", type="ARRAY"
    )
    arry.use_relative_offset = False
    arry.use_constant_offset = True
    arry.constant_offset_displace[0] = 0
    arry.constant_offset_displace[1] = y_offset / 2 + array_offset
    arry.count = count_y
