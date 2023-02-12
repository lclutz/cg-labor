#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xy_skala
import matplotlib.pyplot as plt

from colour.plotting import plot_chromaticity_diagram_CIE1931


def main():
    plot_chromaticity_diagram_CIE1931(standalone=False)

    plt.title("Kurve im YUV-Farbraum")

    xy_colors = xy_skala.generate_xy_coordinates()

    x = [x for x, _ in xy_colors]
    y = [y for _, y in xy_colors]

    plt.plot(x, y, ".-", color="black")

    plt.savefig("xy_kurve.png")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('^C')
        exit(1)
