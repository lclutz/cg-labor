#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Punkte im RGB Farbraum
blue       = (0x00, 0x00, 0xff) # On-Punkt
blue_green = (0x00, 0xff, 0xff) # Off-Punkt
green      = (0x00, 0xff, 0x00) # On-Punkt
green_red  = (0xff, 0xff, 0x00) # Off-Punkt
red        = (0xff, 0x00, 0x00) # On-Punkt

# Vorgegebene Temperaturwerte
temp_blue  = 25
temp_green = 50
temp_red   = 75


# Berechnet für die On-Punkte p0 und p2 und den Off-Punkt p1 einen neuen
# Punkt im RGB Farbraum.
def bezier_rgb(p0, p1, p2, u):
    r0, g0, b0 = p0
    r1, g1, b1 = p1
    r2, g2, b2 = p2

    # Berechnung komponentenweise weil wir keinen Vektor Datentyp haben.
    r = r0 * (1 - u)**2 + r1 * 2 * u * (1 - u) + r2 * u**2
    g = g0 * (1 - u)**2 + g1 * 2 * u * (1 - u) + g2 * u**2
    b = b0 * (1 - u)**2 + b1 * 2 * u * (1 - u) + b2 * u**2

    # Die Komponenten von RGB Werten sind keine Fließkommazahlen also runden
    # wir die berechneten Komponenten für das Ergebnis.
    return (round(r), round(g), round(b))


# save_color_scale_as_ppm speichert die Farbskala im PPM-Format
# (https://netpbm.sourceforge.net/doc/ppm.html)
#
# Wir nutzen dieses Format weil es sehr enfach ist und ohne zusätzliche
# Bibliotheken implementiert werden kann.
#
# PPM Bilder können z.B. mit GIMP geöffnet und angezeigt werden.
def save_color_scale_as_ppm(path, colors):
    width  = len(colors)
    height = int(round(width/4))
    with open(path, "wb") as f:
        f.write(f"P6\n{width} {height} 255\n".encode(encoding="ascii"))
        for _ in range(height):
            for r, g, b in colors:
                f.write(r.to_bytes(1, byteorder="little"))
                f.write(g.to_bytes(1, byteorder="little"))
                f.write(b.to_bytes(1, byteorder="little"))


def generate_rgb_coordinates():
    colors = list()

    # Bezier-Kurve von Blau nach Grün
    for temp in range(0, temp_green - temp_blue):
        u = temp / (temp_green - temp_blue)
        colors.append(bezier_rgb(blue, blue_green, green, u))

    # Bezier-Kurve von Grün nach Rot
    for temp in range(0, temp_red - temp_green):
        u = temp / (temp_red - temp_green)
        colors.append(bezier_rgb(green, green_red, red, u))

    colors.append(red)
    return colors


def main():
    colors = generate_rgb_coordinates()

    for temp in range(temp_blue, temp_red + 1):
        r, g, b = colors[temp - temp_blue]
        print("%d°C -> 0x%02x%02x%02x" % (temp, r, g, b))

    save_color_scale_as_ppm("rgb_skala.ppm", colors)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("^C")
        exit(1)
