#MenuTitle: Formula to Absolute
# -*- coding: utf-8 -*-
#Version: 0.1.1 (04 Oct, 2019)

Glyphs.clearLog()
font = Glyphs.font
selectedMasterIdx = font.masterIndex
log = []
for thisGlyph in font.glyphs:
	absolute = []
	thisLayer = thisGlyph.layers[selectedMasterIdx]
	if thisLayer.leftMetricsKey and not thisGlyph.leftMetricsKey:
		absolute.append('LSB: {}=>{}'.format(thisLayer.leftMetricsKey, thisLayer.LSB))
		thisLayer.leftMetricsKey = None
	if thisLayer.rightMetricsKey and not thisGlyph.rightMetricsKey:
		absolute.append('RSB: {}=>{}'.format(thisLayer.rightMetricsKey, thisLayer.RSB))
		thisLayer.rightMetricsKey = None
	if thisLayer.widthMetricsKey and not thisGlyph.widthMetricsKey:
		absolute.append('Width: {}=>{}'.format(thisLayer.widthMetricsKey, thisLayer.width))
		thisLayer.widthMetricsKey = None
	if absolute:
		thisLayer.syncMetrics()
		log.append('{}: {}'.format(thisGlyph.name, '; '.join(absolute)))
if log:
	Message('\n'.join(log))
else:
	Message('Nothing found')
