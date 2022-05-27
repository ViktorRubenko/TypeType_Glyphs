# MenuTitle: Copy colors from Font
"""Copy glyphs colors from one font to another."""

from __future__ import print_function
import vanilla


class ColorsCopy(object):
    """GUI for copying colors from one font to another"""

    def __init__(self):

        self.masters = [m for f in Glyphs.fonts for m in f.masters]

        self.w = vanilla.FloatingWindow((450, 100), "Steal colors")

        self.w.text_anchor = vanilla.TextBox(
            (15, 12 + 2 + 12, 130, 14), "Copy colors from:", sizeStyle="small"
        )
        self.w.from_master = vanilla.PopUpButton(
            (150, 12 + 12, 150, 17),
            self.getMastersForButton(isSourceFont=True),
            sizeStyle="small",
            callback=self.buttonCheck,
        )

        self.w.text_value = vanilla.TextBox(
            (15, 12 + 2 + 25 + 12, 130, 14),
            "To selected glyphs in:",
            sizeStyle="small",
        )
        self.w.to_master = vanilla.PopUpButton(
            (150, 12 + 25 + 12, 150, 17),
            self.getMastersForButton(isSourceFont=False),
            sizeStyle="small",
            callback=self.buttonCheck,
        )

        self.w.copyMasterColorsButton = vanilla.Button(
            (-140, 12, -15, 17),
            "Copy Master Color",
            sizeStyle="small",
            callback=self.copyMasterColor,
        )
        self.w.copyGlyphColorsButton = vanilla.Button(
            (-140, 12 + 25, -15, 17),
            "Copy Glyph Color",
            sizeStyle="small",
            callback=self.copyGlyphColor,
        )
        self.w.copyAllMastersButton = vanilla.Button(
            (-140, 12 + 50, -15, 17),
            "Copy All Masters",
            sizeStyle="small",
            callback=self.copyColorsAllMasters,
        )

        self.w.open()
        self.buttonCheck(None)

    def getMastersForButton(self, isSourceFont):
        return [
            "%s - %s" % (m.font.familyName, m.name)
            for m in (self.masters[::-1] if isSourceFont else self.masters)
        ]

    def getMastersFromButtons(self):
        sourceMaster = self.masters[::-1][self.w.from_master.get()]
        targetMaster = self.masters[self.w.to_master.get()]

        return sourceMaster, targetMaster

    def removeColorsFromSelectionAllMasters(self):
        _, targetMaster = self.getMastersFromButtons()
        targetFont = targetMaster.font

        for targetGlyph in targetFont.selection:
            targetGlyph.color = None
            for layer in targetGlyph.layers:
                layer.color = None

    def removeMasterColorsFromSelection(self):
        _, targetMaster = self.getMastersFromButtons()
        targetFont = targetMaster.font

        for targetGlyph in targetFont.selection:
            targetGlyph.layers[targetMaster.id].color = None

    def removeGlyphColorsFromSelection(self):
        _, targetMaster = self.getMastersFromButtons()
        targetFont = targetMaster.font

        for targetGlyph in targetFont.selection:
            targetGlyph.color = None

    def buttonCheck(self, sender):
        sourceMaster, targetMaster = self.getMastersFromButtons()
        sourceFont, targetFont = sourceMaster.font, targetMaster.font

        if sourceMaster != targetMaster:
            self.w.copyMasterColorsButton.enable(True)
            self.w.copyGlyphColorsButton.enable(True)

            if targetFont != sourceFont and [
                m.name for m in targetFont.masters
            ] == [m.name for m in sourceFont.masters]:
                self.w.copyAllMastersButton.enable(True)
            else:
                self.w.copyAllMastersButton.enable(False)

        else:
            self.w.copyMasterColorsButton.enable(False)
            self.w.copyGlyphColorsButton.enable(False)
            self.w.copyAllMastersButton.enable(False)

    def copyColorsAllMasters(self, sender):
        self.removeColorsFromSelectionAllMasters()

        sourceMaster, targetMaster = self.getMastersFromButtons()
        sourceFont, targetFont = sourceMaster.font, targetMaster.font

        print(
            "Copying colors for",
            len(sourceFont.selection),
            "glyphs from",
            sourceFont.familyName,
            "to",
            targetFont.familyName,
            "for all masters.",
        )

        try:
            for targetGlyph in targetFont.selection:
                glyphName = targetGlyph.name
                try:
                    sourceGlyph = sourceFont[glyphName]
                    targetGlyph.color = sourceGlyph.color
                    for masterIndex, sourceMaster in enumerate(
                        sourceFont.masters
                    ):
                        targetMaster = targetFont.masters[masterIndex]
                        targetGlyph.layers[
                            targetMaster.id
                        ].color = sourceGlyph.layers[sourceMaster.id].color
                except Exception as e:
                    print(glyphName, ": Failed")
        except:
            import traceback

            print(traceback.format_exc())
        finally:
            print("Done")

        self.w.close()

    def copyMasterColor(self, sender):
        self.removeMasterColorsFromSelection()

        sourceMaster, targetMaster = self.getMastersFromButtons()
        sourceFont, targetFont = sourceMaster.font, targetMaster.font

        print(
            "Copying master colors for",
            len(sourceFont.selection),
            "glyphs from",
            sourceFont.familyName,
            sourceMaster.name,
            "to",
            targetFont.familyName,
            targetMaster.name,
        )

        try:
            for targetGlyph in targetFont.selection:
                glyphName = targetGlyph.name
                try:
                    sourceGlyph = sourceFont[glyphName]

                    targetGlyph.layers[
                        targetMaster.id
                    ].color = sourceGlyph.layers[sourceMaster.id].color
                except Exception as e:
                    print(glyphName, ": Failed")
                    print(e)

        except Exception as e:
            import traceback

            print(traceback.format_exc())
        finally:
            print("Done.")

        self.w.close()

    def copyGlyphColor(self, sender):
        self.removeGlyphColorsFromSelection()

        sourceMaster, targetMaster = self.getMastersFromButtons()
        sourceFont, targetFont = sourceMaster.font, targetMaster.font

        print(
            "Copying glyph colors for",
            len(sourceFont.selection),
            "glyphs from",
            sourceFont.familyName,
            sourceMaster.name,
            "to",
            targetFont.familyName,
            targetMaster.name,
        )

        try:
            for targetGlyph in targetFont.selection:
                glyphName = targetGlyph.name
                try:
                    sourceGlyph = sourceFont[glyphName]
                    targetGlyph.color = sourceGlyph.color
                except Exception as e:
                    print(glyphName, ": Failed")
                    print(e)

        except Exception as e:
            import traceback

            print(traceback.format_exc())
        finally:
            print("Done.")

        self.w.close()


ColorsCopy()
