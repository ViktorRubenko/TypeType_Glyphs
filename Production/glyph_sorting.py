from collections import defaultdict
from os import path


def sort(font):
	# .null.unicode(0000) = None in Glyphs.app
	glyphs_order= ['.notdef', '.null'] + [glyph.name for glyph in sorted([glyph for glyph in font.glyphs if glyph.unicode], key=lambda g: g.unicode)]
	
	wo_uni_glyphs = [glyph for glyph in font.glyphs if not glyph.unicode and glyph.name not in ['.null', '.notdef', 'foundryicon']]
	temp_d = defaultdict(list)
	for glyph in wo_uni_glyphs:
		if '.' in glyph.name:
			temp_d[glyph.name[glyph.name.find('.')+1:]].append(glyph.name)
		else:
			temp_d[0].append(glyph.name)
	for group in temp_d:
		if group == 0:
			continue
		glyphs_parent = [(glyph_name, font[glyph_name[:glyph_name.find('.')]]) for glyph_name in temp_d[group]]
		temp_d[group] = sorted([g for g in glyphs_parent if g[1]], key=lambda g: g[1].unicode)
		temp_d[group].extend(sorted([g for g in glyphs_parent if not g[1]], key=lambda k: k[0]))
	temp_d[0] = [[glyph_name] for glyph_name in temp_d[0] if '_' in glyph_name] + [[glyph_name] for glyph_name in temp_d[0] if '_' not in glyph_name]
	for group in sorted(temp_d.keys()):
		for g in temp_d[group]:
			glyphs_order.append(g[0])
	if 'foundryicon' not in glyphs_order:
		glyphs_order.append('foundryicon')
	
	return glyphs_order
	
if __name__ == '__main__':
	Glyphs.clearLog()
	for font in Glyphs.fonts:
		file_path = path.join(path.dirname(font.filepath), '{}_glyphs_order.txt'.format(font.familyName))
		with open(file_path, 'w') as f:
			f.write('\n'.join(sort(font)))
		print('File was saved to {}'.format(file_path))