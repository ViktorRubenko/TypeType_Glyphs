# MenuTitle: Colors cleaner
"""Clear master/glyph colors from font."""

from __future__ import print_function
import vanilla


class ColorsCleaner(object):
    """GUI"""

    def __init__(self):

        self.masters = [m for f in Glyphs.fonts for m in f.masters]

        self.w = vanilla.FloatingWindow((200, 400), "Colors cleaner")

        self.w.text_anchor = vanilla.TextBox(
            "auto", "Clean colors from:", sizeStyle="small"
        )
        self.w.from_master = vanilla.PopUpButton(
            "auto",
            self.getMastersForButton(),
            sizeStyle="small",
        )

        self.w.glyphAndMasterColorsInAllMastersButton = vanilla.Button(
            "auto",
            "Glyph and Master Colors in All Masters",
            sizeStyle="small",
            callback=self.clearGlyphAndMasterColorsInAllMasters,
        )
        self.w.masterColorInAllMastersButton = vanilla.Button(
            "auto",
            "Master Color in All Masters",
            sizeStyle="small",
            callback=self.clearMasterColorInAllMasters,
        )
        self.w.glyphColorButton = vanilla.Button(
            "auto",
            "Glyph Color",
            sizeStyle="small",
            callback=self.clearGlyphColor,
        )
        self.w.GlyphAndMasterColorsInSelectedMaster = vanilla.Button(
            "auto",
            "Glyph and Master Colors in Selected Master",
            sizeStyle="small",
            callback=self.clearGlyphAndMasterColorsInSelectedMaster,
        )
        self.w.MasterColorInSelectedMaster = vanilla.Button(
            "auto",
            "Master Color in Selected Master",
            sizeStyle="small",
            callback=self.clearMasterColorInSelectedMaster,
        )

        rules = [
            "H:|-p-[text_anchor]-p-|",
            "H:|-p-[from_master]-p-|",
            "H:|-p-[glyphAndMasterColorsInAllMastersButton]-p-|",
            "H:|-p-[masterColorInAllMastersButton]-p-|",
            "H:|-p-[glyphColorButton]-p-|",
            "H:|-p-[GlyphAndMasterColorsInSelectedMaster]-p-|",
            "H:|-p-[MasterColorInSelectedMaster]-p-|",
            "V:|-p-[text_anchor]-[from_master]-h-[glyphAndMasterColorsInAllMastersButton]-[masterColorInAllMastersButton]-[glyphColorButton]-[GlyphAndMasterColorsInSelectedMaster]-[MasterColorInSelectedMaster]-p-|",
        ]
        metrics = {"p": 15, "h": 30}

        self.w.addAutoPosSizeRules(rules, metrics)

        self.w.open()

    def getMastersForButton(self):
        return ["%s - %s" % (m.font.familyName, m.name) for m in self.masters]

    def getMasterFromButton(self):
        return self.masters[self.w.from_master.get()]

    def clearGlyphAndMasterColorsInAllMasters(self, sender):
        targetMaster = self.getMasterFromButton()
        for glyph in targetMaster.font.selection:
            glyph.color = None
            for layer in glyph.layers:
                layer.color = None

    def clearMasterColorInAllMasters(self, sender):
        targetMaster = self.getMasterFromButton()
        for glyph in targetMaster.font.selection:
            for layer in glyph.layers:
                layer.color = None

    def clearGlyphColor(self, sender):
        targetMaster = self.getMasterFromButton()
        for glyph in targetMaster.font.selection:
            glyph.color = None

    def clearGlyphAndMasterColorsInSelectedMaster(self, sender):
        targetMaster = self.getMasterFromButton()
        for glyph in targetMaster.font.selection:
            glyph.color = None
            glyph.layers[targetMaster.id].color = None

    def clearMasterColorInSelectedMaster(self, sender):
        targetMaster = self.getMasterFromButton()
        for glyph in targetMaster.font.selection:
            glyph.layers[targetMaster.id].color = None


ColorsCleaner()
