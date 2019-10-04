#MenuTitle: Formula to Absolute
# -*- coding: utf-8 -*-
#Version: 0.1.2 (04 Oct, 2019)

Glyphs.clearLog()
font = Glyphs.font
selectedMasterIdx = font.masterIndex
log = []
attribs = {
	'leftMetricsKey': 'LSB',
	'rightMetricsKey': 'RSB',
	'widthMetricsKey': 'width'
	}
for thisGlyph in font.glyphs:	
	absolute = []
	thisLayer = thisGlyph.layers[selectedMasterIdx]
	for attrib in ['leftMetricsKey', 'rightMetricsKey', 'widthMetricsKey']:
		process = False
		if sum([0 if not layer.__getattribute__(attrib) else 1
			for layer in thisGlyph.layers]) == len(thisGlyph.layers):
				thisGlyph.__setattr__(attrib, None)
				process = True
		if thisLayer.__getattribute__(attrib) and not thisGlyph.__getattribute__(attrib):
			process = True
		if process:
			absolute.append('{}: {}=>{}'.format(attribs[attrib],
				thisLayer.__getattribute__(attrib), 
				thisLayer.__getattribute__(attribs[attrib]))
				)
			thisLayer.__setattr__(attrib, None)
			log.append('{}: {}'.format(thisGlyph.name, '; '.join(absolute)))
		thisLayer.syncMetrics()
			
if log:
	Message('\n'.join(log))
else:
	Message('Nothing found')
