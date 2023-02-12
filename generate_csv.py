#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Erzeugt eine CSV Datei mit der Temperatur und der zugehörigen RGB und xy
# Farben zum Import in die Textverarbeitung.

import csv

import xy_skala
import rgb_skala


def main():
    temperatures = range(25, 75 + 1)
    xy_colors = xy_skala.generate_xy_coordinates()
    rgb_colors = rgb_skala.generate_rgb_coordinates()

    rows = zip(temperatures, rgb_colors, xy_colors)

    with open('colours.csv', 'w', newline='') as csvfile:
        w = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Temperatur', 'RGB Farbe', 'YUV Farbe'])
        for temperature, rgb_color, xy_color in rows:
            r, g, b = rgb_color
            x, y    = xy_color
            w.writerow([
                '%d°C' % temperature,
                "0x%02x%02x%02x" % (r, g, b),
                "(%f, %f)" % (x, y)
            ])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('^C')
        exit(1)
