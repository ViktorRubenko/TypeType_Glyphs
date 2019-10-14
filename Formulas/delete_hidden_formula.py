#MenuTitle: Delete hidden formula
# -*- coding: utf-8 -*-
#Version: 0.0.2 (14 Oct, 2019)


def main():
	log = []
	attribs = {
				'leftMetricsKey': 'LeftSidebearing',
				'rightMetricsKey': 'RightSidebearing',
				'widthMetricsKey': 'Width'
				}
	Glyphs.clearLog()
	font = Glyphs.font
	for thisGlyph in font.glyphs:
		for attrib in ('leftMetricsKey', 'rightMetricsKey', 'widthMetricsKey'):
			if not thisGlyph.__getattribute__(attrib):
				continue
			if (sum(0 if not thisLayer.__getattribute__(attrib) else 1 
				for thisLayer in thisGlyph.layers) == len(thisGlyph.layers)):
				log.append('{}: {} {}'.format(thisGlyph.name,
											attribs[attrib],
											thisGlyph.__getattribute__(attrib)))
				thisGlyph.__setattr__(attrib, None)
	print('Deleted formulas:')
	if log:
		print('\n'.join(log))
	else:
		print('Not found')
	Glyphs.showMacroWindow()
	
	
if __name__ == '__main__':
	main()
