# MenuTitle: Glyph Comparator
# -*- coding: utf-8 -*-
# Version: 0.0.1 (16 Mar, 2020)

from vanilla import *

FONT_1, FONT_2 = Glyphs.fonts

class ListWindow(object):

    def __init__(self):
        self.w = FloatingWindow((600, 500), title="Glyph Comparator")
        self.w.myList = List((0, 0, -0, -0),
                     [],
                     columnDescriptions=[{'title': 'Type'},{"title": "GlyphName"}, {"title": "Unicode"}])
        self.w.open()


if __name__ == '__main__':
    lw = ListWindow()
    font_2_names = tuple(glyph.name for glyph in FONT_2.glyphs)
    for glyph in FONT_1.glyphs:
        if glyph.name in font_2_names:
            if glyph.unicode != FONT_2[glyph.name].unicode:
                lw.w.myList.append({'Type': 'Diff Unicode' ,'GlyphName': glyph.name, 'Unicode': "{} |   {}".format(glyph.unicode, FONT_2[glyph.name].unicode)})
        else:
            lw.w.myList.append({'Type': 'Existance by GlypName', 'GlyphName': glyph.name, 'Unicode': glyph.unicode})
    font_1_cmap = {glyph.unicode: glyph.name for glyph in FONT_1.glyphs if glyph.unicode}
    font_2_cmap = {glyph.unicode: glyph.name for glyph in FONT_2.glyphs if glyph.unicode}
    for unicode_, glyph_name in font_1_cmap.items():
        if unicode_ in font_2_cmap:
            if glyph_name != font_2_cmap[unicode_]:
                lw.w.myList.append({'Type': 'Diff Name', 'GlyphName': '{} | {}'.format(glyph_name, font_2_cmap[unicode_]), 'Unicode': unicode_})
        else:
            lw.w.myList.append({'Type': 'Existance by U4nicode', 'GlyphName': glyph_name, 'Unicode': unicode_})
