# MenuTitle: Glyph Comparator
# -*- coding: utf-8 -*-
# Version: 0.0.2 (19 Mar, 2020)
__doc__ = """
Compares names / unicode / glyph presence between 2 open fonts
"""


from vanilla import *

FONT_1, FONT_2 = Glyphs.fonts


class ListWindow(object):
    def __init__(self):
        self.w = FloatingWindow((600, 500), title="Glyph Comparator")
        self.w.myList = List(
            (0, 0, -0, -0),
            [],
            columnDescriptions=[
                {"title": "Type"},
                {"title": "GlyphName"},
                {"title": "Unicode"},
            ],
        )
        self.w.open()


if __name__ == "__main__":
    lw = ListWindow()
    font_2_names = tuple(glyph.name for glyph in FONT_2.glyphs)
    font_1_names = tuple(glyph.name for glyph in FONT_1.glyphs)
    print(set(font_1_names).symmetric_difference(set(font_2_names)))
    for glyph_name in set(font_1_names).symmetric_difference(set(font_2_names)):
        lw.w.myList.append(
            {
                "Type": "Existence by Name",
                "GlyphName": glyph_name,
            }
        )
    for glyph in FONT_1.glyphs:
        if glyph.name in font_2_names:
            if glyph.unicode != FONT_2[glyph.name].unicode:
                lw.w.myList.append(
                    {
                        "Type": "Diff Unicode",
                        "GlyphName": glyph.name,
                        "Unicode": "{} |   {}".format(
                            glyph.unicode, FONT_2[glyph.name].unicode
                        ),
                    }
                )
    font_1_cmap = {
        glyph.unicode: glyph.name for glyph in FONT_1.glyphs if glyph.unicode
    }
    font_2_cmap = {
        glyph.unicode: glyph.name for glyph in FONT_2.glyphs if glyph.unicode
    }
    for unicode_ in set(font_1_cmap).symmetric_difference(set(font_2_cmap)):
        lw.w.myList.append(
            {
                "Type": "Existence by Unicode",
                "GlyphName": font_1_cmap[unicode_]
                if unicode_ in font_1_cmap
                else font_2_cmap[unicode_],
                "Unicode": unicode_,
            }
        )
    for unicode_, glyph_name in font_1_cmap.items():
        if unicode_ in font_2_cmap:
            if glyph_name != font_2_cmap[unicode_]:
                lw.w.myList.append(
                    {
                        "Type": "Diff Name",
                        "GlyphName": "{} | {}".format(
                            glyph_name, font_2_cmap[unicode_]
                        ),
                        "Unicode": unicode_,
                    }
                )
