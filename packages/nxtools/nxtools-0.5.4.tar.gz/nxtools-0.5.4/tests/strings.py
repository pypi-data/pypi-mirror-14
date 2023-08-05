#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nxtools import *

strings = [
    "Příliš žluťoučký kůň úpěl ďábelské ódy",
    "V této větě (která nikoho nezajímá) jsou \"různé\" znaky"
    ]


for string in strings:
    print slugify(string)
    print string2color(string)
    print ""
