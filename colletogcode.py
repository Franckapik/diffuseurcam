import bpy

# Sélectionnez la courbe que vous souhaitez exporter
curve = bpy.context.active_object

if curve and curve.type == 'CURVE':
    gcode_lines = []
    gcode_lines.append("G21 ; Set units to millimeters")
    gcode_lines.append("G90 ; Absolute positioning")

    for spline in curve.data.splines:
        if spline.type == 'BEZIER':
            for point in spline.bezier_points:
                x = point.co.x *100
                y = point.co.y * 100
                z = point.co.z *100
                gcode_lines.append(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f}")

        elif spline.type == 'NURBS' or spline.type == 'POLY':
            for point in spline.points:
                x, y, z, w = point.co
                x1 = x*100
                y1 = y*100
                z1=z*100
                gcode_lines.append(f"G1 X{x1:.2f} Y{y1:.2f} Z{z1:.2f}")

    gcode_lines.append("M30 ; End of program")

    # Sauvegarder le G-code dans un fichier
    with open("/home/fanch/output.gcode", 'w') as f:
        for line in gcode_lines:
            f.write(line + "\n")

    print("G-code exporté avec succès.")