#MenuTitle: Replace Notdef
# -*- coding: utf-8 -*-
#Version: 0.0.1 (14 Oct, 2019)


import os


def find_nd_font(fonts):
	for font_index, font in enumerate(fonts):
		if os.path.basename(font.filepath).split('.')[0] == 'Notdef':
			return font_index, font
	return [None] * 2


def replace_nd(fonts, font_nd_index, font_nd):
	if not font_nd_index:
		Glyphs.Message('Notdef.glyphs is not opened')
		return
	nd_layer = font_nd['.notdef'].layers[0]
	for font_index, font in enumerate(fonts):
		if font_index == font_nd_index:
			continue
		if font['.notdef']:
			del(font.glyphs['.notdef'])
		font.glyphs.append(GSGlyph('.notdef'))
		for layer in font['.notdef'].layers:
			layer.paths = nd_layer.paths
			for attrib in ['LSB', 'RSB', 'width']:
				layer.__setattr__(attrib, nd_layer.__getattribute__(attrib))
	print('{}: notdef replaced'.format(font.familyName))

def main():
	Glyphs.clearLog()
	fonts = Glyphs.fonts
	replace_nd(fonts, *find_nd_font(fonts))
	
	
if __name__ == '__main__':
	main()
