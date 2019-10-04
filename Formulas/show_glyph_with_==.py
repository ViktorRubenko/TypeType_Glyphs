#MenuTitle: Open glyphs with '=='
# -*- coding: utf-8 -*-
#Version: 0.1 (04 Oct, 2019)

Glyphs.clearLog()
font = Glyphs.font
len_tabs = len(font.tabs)
for thisGlyph in font.glyphs:
	newTab = True
	for thisLayer in thisGlyph.layers:
		if (thisLayer.leftMetricsKey or thisLayer.rightMetricsKey or
			thisLayer.widthMetricsKey):
			if newTab:
				font.newTab()
				newTab = False
			font.tabs[-1].layers.append(thisLayer)
			print(thisLayer)
if len(font.tabs) == len_tabs:
	Message('There are no individual formulas')
print('Done')
