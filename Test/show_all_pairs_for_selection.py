# MenuTitle: Show All Glyphs Pairs for Selection
# -*- coding: utf-8 -*-
__doc__ = """
Generation of pairs for selected glyphs
"""

from AppKit import NSMutableAttributedString


def show_kerning_pairs():
    font = Glyphs.font
    master_id = font.selectedFontMaster.id

    kerning_string = NSMutableAttributedString.alloc().init()
    for selected_glyph in font.selection:
        string = (
            "/{0} *:\n".format(selected_glyph.name)
            + "  ".join(
                "/{0}/{1}".format(selected_glyph.name, glyph.name)
                for glyph in font.glyphs
            )
            + "\n\n"
            + "*/{0} :\n".format(selected_glyph.name)
            + "  ".join(
                "/{1}/{0}".format(selected_glyph.name, glyph.name)
                for glyph in font.glyphs
            )
            + "\n\n"
        )

        glyphs_string = font.charStringFromDisplayString_(string)
        pairs_string = (
            NSMutableAttributedString.alloc().initWithString_attributes_(
                glyphs_string, {"GSLayerIdAttrib": master_id}
            )
        )
        kerning_string.appendAttributedString_(pairs_string)

    try:
        Glyphs.currentDocument.windowController().activeEditViewController().graphicView().textStorage().setText_(
            kerning_string
        )
    except:
        Glyphs.currentDocument.windowController().addTabWithString_("")
        Glyphs.currentDocument.windowController().activeEditViewController().graphicView().textStorage().setText_(
            kerning_string
        )


if __name__ == "__main__":
    Glyphs.clearLog()
    show_kerning_pairs()
