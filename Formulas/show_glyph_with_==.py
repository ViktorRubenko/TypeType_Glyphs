# MenuTitle: Open glyphs with '=='
# -*- coding: utf-8 -*-
# Version: 0.1.1 (07 Oct, 2019)
__doc__ = """
Opens glyphs with == in a separate tab. To check the Formula to Absolute script
"""


Glyphs.clearLog()
font = Glyphs.font
len_tabs = len(font.tabs)
thisMasterId = font.masterIndex
newTab = True
for thisGlyph in font.glyphs:
    thisLayer = thisGlyph.layers[thisMasterId]
    if (
        thisLayer.leftMetricsKey
        or thisLayer.rightMetricsKey
        or thisLayer.widthMetricsKey
    ):
        if newTab:
            font.newTab()
            newTab = False
        font.tabs[-1].layers.append(thisLayer)
        print(thisLayer)
if len(font.tabs) == len_tabs:
    Message("There are no individual formulas")
print("Done")
