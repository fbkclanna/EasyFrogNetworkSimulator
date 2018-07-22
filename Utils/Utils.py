#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


def get_distance(pos0, pos1):
    return math.sqrt((pos0[0] - pos1[0]) ** 2 + (pos0[1] - pos1[1]) ** 2)
