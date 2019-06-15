# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 16:31:51 2018

@author: Eric
"""

from matplotlib.cm import ScalarMappable
from matplotlib.colors import to_hex

import logging as log
import matplotlib.pyplot as plt
from prog.conditions.conditions import between


log.basicConfig(level=log.INFO)


class ColorMap:

    def __init__(self, cmap='Greys', vmin=0, vmax=100):
        self.cmap = plt.get_cmap(cmap)
        self.vmin = vmin
        self.vmax = vmax
        self.cnorm = plt.Normalize(vmin, vmax)
        self.scalar_color = ScalarMappable(self.cnorm, self.cmap)

    def get_color_rgb(self, value=0, vmin=None, vmax=None):
        if vmin is None:
            vmin = self.vmin
        if vmax is None:
            vmax = self.vmax

        if between(value, vmin, vmax):
            r, g, b, a = self.scalar_color.to_rgba(value)
        elif value < vmin:
            r, g, b, a = self.cmap(0)
        else:
            r, g, b, a = self.cmap(self.vmax)

        rgb = to_hex((r, g, b, a))
#        log.debug(f"{self.__class__}.get_color_rgb : value={value} ; rgb={rgb} ; red={r:.3f}, green={g:.3f}, blue={b:.3f}" )
        return rgb
