# MenuTitle: Decompose - Background - RM Overlap
# -*- coding: utf-8 -*-


font = Glyphs.font


def main():
    for glyph in [g for g in font.glyphs if g.selected]:
        for layer in glyph.layers:
            layer.decomposeComponents()
            layer.background = layer
            layer.removeOverlap()


if __name__ == "__main__":
    main()