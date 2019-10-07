#MenuTitle: Formula values unification
# -*- coding: utf-8 -*-
#Version: 0.3.0 (07 Oct, 2019)


import re


def update_metrics(thisGlyph):
	for thisLayer in thisGlyph.layers:
		thisLayer.syncMetrics()
		
def set_master_formula(thisGlyph, thisMasterIndex, attrib):
	
	attribs = {
		'rightMetricsKey': 'RSB',
		'leftMetricsKey': 'LSB',
		'widthMetricsKey': 'width'
		}
	
	master_formula = thisGlyph.layers[thisMasterIndex].__getattribute__(attrib)
	glyph_formula = thisGlyph.__getattribute__(attrib)
	if not master_formula:
		if glyph_formula:
			master_formula = glyph_formula
		else:
			return
	master_value = thisGlyph.layers[thisMasterIndex].__getattribute__(attribs[attrib])
	
	try:
		increment = int(re.findall(r'[+-]?\d+', master_formula)[0])
	except IndexError:
		increment = 0
		
	for thisLayerIndex, thisLayer in enumerate(thisGlyph.layers):
		if thisLayerIndex == thisMasterIndex:
			continue
		oldValue = thisLayer.__getattribute__(attribs[attrib])
		if glyph_formula == master_formula:
			thisLayer.__setattr__(attrib, None)
		else:
			thisLayer.__setattr__(attrib, master_formula)
		thisLayer.syncMetrics()
		newValue = thisLayer.__getattribute__(attribs[attrib])
		delta = oldValue - newValue
		if delta:
			delta = int(increment + delta)
			if delta:
				if delta >= 0:
					delta = '+' + str(delta)
				else:
					delta = str(delta)
				if increment:
					thisLayer.__setattr__(attrib, re.sub(r'[+-]?\d+', 
															delta, master_formula))
				else:
					thisLayer.__setattr__(attrib, master_formula + delta)
			else:
				thisLayer.__setattr__(attrib, re.sub(r'[+-]?\d+', '', master_formula))
				

def main():
	Glyphs.clearLog()
	font = Glyphs.font
	thisMasterIndex = font.masterIndex
	for thisGlyph in font.glyphs:
		if not thisGlyph.selected:
			continue
		for attrib in ('leftMetricsKey', 'rightMetricsKey', 'widthMetricsKey'):
			update_metrics(thisGlyph)
			set_master_formula(thisGlyph, thisMasterIndex, attrib)
			update_metrics(thisGlyph)
			
	
	
if __name__ == '__main__':
	main()
