#MenuTitle: Replace Notdef
# -*- coding: utf-8 -*-
#Version: 0.1.2 (23 Jan, 2020)


def find_nd_font(fonts):
	for font_index, font in enumerate(fonts):
		if os.path.basename(font.filepath).split('.')[0] == 'Notdef':
			return font_index, font
	return [None] * 2


def replace_nd(fonts, font_nd_index, font_nd):
	if font_nd_index == None:
		Message('Notdef.glyphs is not opened')
		return
	nd_layer = font_nd['.notdef'].layers[0]
	for font_index, font in enumerate(fonts):
		if font_index == font_nd_index:
			continue
		if font['.notdef']:
			del(font.glyphs['.notdef'])
		font.glyphs.append(GSGlyph('.notdef'))
                for master_index, master in enumerate(font.masters):
                        layer = font['.notdef'].layers[master_index]
                        layer.paths = nd_layer.paths
                for master_index, master in enumerate(font.masters):
                        layer = font['notdef'].layers[master_index]
                        if master.italicAngle == 0:
                                metrics = (100, 100, 900)
                                for attrib_i, attrib in enumerate('LSB RSB width'.split()):
                                        layer.__setattr__(attrib, metrics[attrib_i])
                        else:
                                metrics = (20, 20, 900)
                                for attrib_i, attrib in enumerate('leftMetricsKey rightMetricsKey widthMetricsKey'.split()):
                                        layer.__setattr__(attrib, '=={}'.format(metrics[attrib_i]))
                        
		print('{}: notdef replaced'.format(font.familyName))

def main():
	Glyphs.clearLog()
	nd_filepath = os.path.join(os.path.dirname(__file__), 'Notdef.glyphs')
	Glyphs.open(nd_filepath)
	fonts = Glyphs.fonts
	replace_nd(fonts, *find_nd_font(fonts))
	fonts[0].close()
	Glyphs.showMacroWindow()
	
	
if __name__ == '__main__':
	main()
