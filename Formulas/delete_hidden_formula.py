#MenuTitle: Delete hidden formula
# -*- coding: utf-8 -*-
#Version: 0.0.1 (07 Oct, 2019)


def main():
	font = Glyphs.font
	for thisGlyph in font.glyphs:
		for attrib in ('leftMetricsKey', 'rightMetricsKey', 'widthMetricsKey'):
			if not thisGlyph.__getattribute__(attrib):
				continue
			if (sum(0 if not thisLayer.__getattribute__(attrib) else 1 
				for thisLayer in thisGlyph.layers) == len(thisGlyph.layers)):
				print(thisGlyph.name, attrib, thisGlyph.__getattribute__(attrib))
				thisGlyph.__setattr__(attrib, None)
	
	
if __name__ == '__main__':
	main()
