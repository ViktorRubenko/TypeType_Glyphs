#MenuTitle: Open glyphs with different formula logic
# -*- coding: utf-8 -*-
#Version: 0.1 (04 Oct, 2019)


import re


def get_key(pattern, f_key):
	try:
		return re.findall(pattern, f_key)[0]
	except IndexError:
		return ''


Glyphs.clearLog()
font = Glyphs.font
len_tabs = len(font.tabs)
for thisGlyph in font.glyphs:
	newTab = True
	for attrib in ['leftMetricsKey', 'rightMetricsKey', 'widthMetricsKey']:
		glyph_key = thisGlyph.__getattribute__(attrib)
		if glyph_key:
			main_basis = get_key(r'={0,2}([A-z\|\.]+)', glyph_key)
			for thisLayer in thisGlyph.layers:
				layer_key = thisLayer.__getattribute__(attrib)
				if not layer_key:
					continue
				layer_basis = get_key(r'={0,2}([A-z\|\.]+)', layer_key)
				if layer_basis != main_basis:
					if newTab:
						font.newTab()
						newTab = False
					font.tabs[-1].layers.append(thisLayer)
		else:
			main_basis = None
			basisIndex = None
			for thisLayerIndex, thisLayer in enumerate(thisGlyph.layers):
				if thisLayer.__getattribute__(attrib):
					if not main_basis:
						main_basis = get_key(r'={0,2}([A-z\|\.]+)',
						thisLayer.__getattribute__(attrib))
						basisIndex = thisLayerIndex 
						continue
					layer_key = thisLayer.__getattribute__(attrib)
					layer_basis = get_key(r'={0,2}([A-z\|\.]+)', layer_key)
					if layer_basis != main_basis:
						if newTab:
							font.newTab()
							newTab = False
						font.tabs[-1].layers.append(thisLayer)
			
if len(font.tabs) == len_tabs:
	Message('There are no formulas with the wrong logic')
print('Done')
