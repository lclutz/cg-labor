#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rgb_skala
import matplotlib.pyplot as plt


def main():
    fig = plt.figure(constrained_layout=True)
    fig.suptitle("Kurve im RGB-Farbraum")

    gs = plt.GridSpec(4, 3, figure=fig)

    rg_axes  = fig.add_subplot(gs[0, 0])
    rb_axes  = fig.add_subplot(gs[0, 1])
    gb_axes  = fig.add_subplot(gs[0, 2])
    rgb_axes = fig.add_subplot(gs[1:, :], projection="3d")

    colors = rgb_skala.generate_rgb_coordinates()
    r = [ r for r, _, _ in colors ]
    g = [ g for _, g, _ in colors ]
    b = [ b for _, _, b in colors ]

    rg_axes.plot(r, g)
    rg_axes.set_xticks([0,0xff], step=0xff)
    rg_axes.set_yticks([0,0xff], step=0xff)
    rg_axes.set_xlabel("Rot")
    rg_axes.set_ylabel("Grün")
    rg_axes.set_aspect("equal", adjustable="box")

    rb_axes.plot(r, b)
    rb_axes.set_xticks([0,0xff], step=0xff)
    rb_axes.set_yticks([0,0xff], step=0xff)
    rb_axes.set_xlabel("Rot")
    rb_axes.set_ylabel("Blau")
    rb_axes.set_aspect("equal", adjustable="box")

    gb_axes.plot(g, b)
    gb_axes.set_xticks([0,0xff], step=0xff)
    gb_axes.set_yticks([0,0xff], step=0xff)
    gb_axes.set_xlabel("Grün")
    gb_axes.set_ylabel("Blau")
    gb_axes.set_aspect("equal", adjustable="box")

    rgb_axes.plot(r, g, b)
    rgb_axes.set_xlabel("Rot")
    rgb_axes.set_ylabel("Grün")
    rgb_axes.set_zlabel("Blau")
    rgb_axes.set_aspect("equal", adjustable="box")

    plt.tight_layout()
    plt.savefig("rgb_kurve.png")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('^C')
        exit(1)
