#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getCenter(w, h):
    return (int(w / 2), int(h / 2))


def pos2guipos(pos_x, pos_y, SQUARE_SIZE, SQUARE_SCALE, center):
    return (pos_x * (SQUARE_SIZE / SQUARE_SCALE) + center[0], (-1) * pos_y * (SQUARE_SIZE / SQUARE_SCALE) + center[1])
