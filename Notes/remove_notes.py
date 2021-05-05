# MenuTitle: Remove all notes
# -*- coding: utf-8 -*-


import vanilla

__doc__ = """
Remove all comments from Glyph Note. 
"""

font = Glyphs.font

for glyph in font.glyphs:
    if glyph.note:
        glyph.note = None