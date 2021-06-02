# MenuTitle: Compare sidebearings
# -*- coding: utf-8 -*-

__doc__ = "Compare glyph sidebearings between layers"


font = Glyphs.font
selected_glyphs = [g for g in font.glyphs if g.selected]
for g in selected_glyphs:
    layers = [l for l in g.layers if l.italicAngle() > 0]
    right_value = [int(l.rightMetricsKey.split("==|")[-1]) for l in layers]
    if right_value != sorted(right_value):
        print(g.name, right_value)