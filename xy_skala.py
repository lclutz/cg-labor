#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Punkte im RGB Farbraum
blue_rgb       = (0x00, 0x00, 0xff) # On-Punkt
blue_green_rgb = (0x00, 0xff, 0xff) # Off-Punkt
green_rgb      = (0x00, 0xff, 0x00) # On-Punkt
green_red_rgb  = (0xff, 0xff, 0x00) # Off-Punkt
red_rgb        = (0xff, 0x00, 0x00) # On-Punkt

# Vorgegebene Temperaturwerte
temp_blue  = 25
temp_green = 50
temp_red   = 75


# Berechnet für die On-Punkte p0 und p2 und den Off-Punkt p1 einen neuen
# Punkt im xy-Farbraum.
def bezier_xy(p0, p1, p2, u):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2

    # Berechnung komponentenweise weil wir keinen Vektor Datentyp haben.
    x = x0 * (1 - u)**2 + x1 * 2 * u * (1 - u) + x2 * u**2
    y = y0 * (1 - u)**2 + y1 * 2 * u * (1 - u) + y2 * u**2

    return (x, y)


# Wir verwenden die Werte aus dem ersten Aufgabenblatt als Werte der
# Gewichtsfunktionen.
def convert_rgb_to_xy(color_rgb):
    r = color_rgb[0]
    g = color_rgb[1]
    b = color_rgb[2]

    # Skalieren auf Werte zwischen 1 und 0
    r = r / 0xff
    g = g / 0xff
    b = b / 0xff

    X = r * 0.6424 + g * 0.2904 + b * 0.3362
    Y = r * 0.265  + g * 0.954  + b * 0.038
    Z = r * 0      + g * 0.0203 + b * 1.7721

    x = X/(X+Y+Z)
    y = Y/(X+Y+Z)

    return (x, y)


# Für die Konvertierung von xy nach RGB verwenden wir die Formel die wir im
# ersten Aufgabenblatt hergeleitet hatten.
def convert_xy_to_rgb(color_xy):
    x, y = color_xy
    z = 1.0 - x - y
    b = 1.0
    g = (-1.608*x-1.07371*z+1.1384)/(0.0184202*x+0.548934*z-0.0130407)
    r = (g*(0.2904-1.2647*x)+0.3362-2.1463*x)/(0.9074*x-0.6424)

    # Skalieren auf Werte zwischen 1 und 0
    skale_by = max(r, g, b)
    r = r / skale_by
    g = g / skale_by
    b = b / skale_by

    return (round(r * 0xff), round(g * 0xff), round(b * 0xff))


# save_color_scale_as_ppm speichert die Farbskala im PPM-Format
# (https://netpbm.sourceforge.net/doc/ppm.html)
#
# Wir nutzen dieses Format weil es sehr einfach ist und ohne zusätzliche
# Bibliotheken implementiert werden kann.
#
# PPM Bilder können z.B. mit GIMP geöffnet und angezeigt werden.
def save_color_scale_as_ppm(path, colors_rgb):
    width  = len(colors_rgb)
    height = int(round(width/4))
    with open(path, "wb") as f:
        f.write(f"P6\n{width} {height} 255\n".encode(encoding="ascii"))
        for _ in range(height):
            for r, g, b in colors_rgb:
                f.write(r.to_bytes(1, byteorder="little"))
                f.write(g.to_bytes(1, byteorder="little"))
                f.write(b.to_bytes(1, byteorder="little"))


def generate_xy_coordinates():
    colors_xy = list()

    blue_xy       = convert_rgb_to_xy(blue_rgb)
    blue_green_xy = convert_rgb_to_xy(blue_green_rgb)
    green_xy      = convert_rgb_to_xy(green_rgb)
    green_red_xy  = convert_rgb_to_xy(green_red_rgb)
    red_xy        = convert_rgb_to_xy(red_rgb)

    # Bezier-Kurve von Blau nach Grün
    for temp in range(0, temp_green - temp_blue):
        u = temp / (temp_green - temp_blue)
        colors_xy.append(bezier_xy(blue_xy, blue_green_xy, green_xy, u))

    # Bezier-Kurve von Grün nach Rot
    for temp in range(0, temp_red - temp_green):
        u = temp / (temp_red - temp_green)
        colors_xy.append(bezier_xy(green_xy, green_red_xy, red_xy, u))

    colors_xy.append(red_xy)
    return colors_xy


def main():
    colors_xy = generate_xy_coordinates()

    colors_rgb = [ convert_xy_to_rgb(c) for c in colors_xy[:-1] ]
    colors_rgb.append(red_rgb)

    for temp in range(temp_blue, temp_red + 1):
        r, g, b = colors_rgb[temp - temp_blue]
        x, y    = colors_xy[temp - temp_blue]
        print("%d°C -> (%f, %f) -> 0x%02x%02x%02x" % (temp, x, y, r, g, b))

    save_color_scale_as_ppm("xy_skala.ppm", colors_rgb)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("^C")
        exit(1)
