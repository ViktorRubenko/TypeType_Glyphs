# MenuTitle: Tab Spacing
# -*- coding: utf-8 -*-
# Version: 0.0.5 (25 Mar, 2021)
__doc__ = """
Sets the spacing of the tabular glyphs based on the logic of the sidebearings in the original non-tabular glyphs 
(based on the shift of the glyph relative to the center).
"""


import vanilla


FONT = Glyphs.font
ALL_MASTERS = False


REPLACERS = {"tosf": "osf", ".tab": "", ".tf": "", ".tf.": ".", ".tab.": "."}


class Dialog:
    def __init__(self):
        self.w = vanilla.FloatingWindow((370, 400), "Tab Spacing")
        self.w.label = vanilla.TextBox((20, 10, -10, 20), "Glyphs:")
        self.w.checkSelected = vanilla.CheckBox(
            (20, 30, -10, 20),
            "Selected Glyphs",
            callback=self.updateGlyphList,
            value=True,
        )
        self.w.checkTF = vanilla.CheckBox(
            (20, 50, -10, 20),
            "All .tf",
            callback=self.updateGlyphList,
            value=False,
        )
        self.w.checkTOSF = vanilla.CheckBox(
            (20, 70, -10, 20),
            "All .tosf",
            callback=self.updateGlyphList,
            value=False,
        )
        self.w.runButton = vanilla.Button(
            (20, -60, 100, -20), "Run", callback=self.run
        )
        self.w.listLabel = vanilla.TextBox(
            (150, 10, -10, -10), "Glyphs to process:"
        )
        self.w.glyphList = vanilla.List(
            (150, 30, -20, -80),
            [g.name for g in FONT.glyphs if g.selected] if FONT else [],
            selectionCallback=None,
        )
        self.w.removeButton = vanilla.Button(
            (150, -60, -20, -20),
            "Remove Selection",
            callback=self.removeFromList,
        )
        self.w.mastersLabel = vanilla.TextBox((20, 150, -10, 20), "Masters:")
        self.w.checkCurrentMaster = vanilla.CheckBox(
            (20, 170, -10, 20),
            "Current Master",
            value=True,
            callback=self.checkCurrentMaster,
        )
        self.w.checkAllMasters = vanilla.CheckBox(
            (20, 190, -10, 20),
            "All Masters",
            value=False,
            callback=self.checkAllMasters,
        )
        self.w.updateFontButton = vanilla.Button(
            (-100, 10, 80, 15),
            "updateFont",
            sizeStyle="small",
            callback=self.updateFont,
        )

        self.w.open()

    def checkCurrentMaster(self, sender):
        global ALL_MASTERS
        if sender.get():
            self.w.checkAllMasters.set(False)
            ALL_MASTERS = False
        else:
            self.w.checkAllMasters.set(True)
            ALL_MASTERS = True

    def checkAllMasters(self, sender):
        global ALL_MASTERS
        if sender.get():
            self.w.checkCurrentMaster.set(False)
            ALL_MASTERS = True
        else:
            self.w.checkCurrentMaster.set(True)
            ALL_MASTERS = False

    def removeFromList(self, sender):
        self.w.glyphList._removeSelection()

    def updateGlyphList(self, sender):
        selected_glyphs = (
            [g.name for g in FONT.glyphs if g.selected] if FONT else []
        )
        tf_glyphs = (
            [g.name for g in FONT.glyphs if ".tf" in g.name] if FONT else []
        )
        tosf_glyphs = (
            [g.name for g in FONT.glyphs if ".tosf" in g.name] if FONT else []
        )

        for i in range(len(self.w.glyphList))[::-1]:
            del self.w.glyphList[i]

        for glyph_name in self.w.glyphList:
            self.w.glyphList.remove(glyph_name)

        if self.w.checkSelected.get():
            self.append_glyphs(selected_glyphs)

        if self.w.checkTF.get():
            self.append_glyphs(tf_glyphs)

        if self.w.checkTOSF.get():
            self.append_glyphs(tosf_glyphs)

    def updateFont(self, sender):
        global FONT
        FONT = Glyphs.font
        self.updateGlyphList(None)

    def append_glyphs(self, glyph_list):
        for glyph_name in glyph_list:
            if glyph_name in self.w.glyphList:
                continue
            self.w.glyphList.append(glyph_name)

    def run(self, sender):
        if FONT:
            tab_spacing([FONT[g_name] for g_name in self.w.glyphList.get()])
            Glyphs.showMacroWindow()


def move_glyph(layer, sb_diff, delta_x=None, final=False):
    delta_x = 1
    k = 0
    init_sb_diff = abs(layer.LSB - layer.RSB - sb_diff)
    while abs(layer.LSB - layer.RSB - sb_diff) > 1:
        layer.applyTransform([1.0, 0, 0, 1.0, delta_x, 0])
        if abs(layer.LSB - layer.RSB - sb_diff) > init_sb_diff:
            delta_x = -delta_x
        if k == 100:
            print("error", layer)


def tab_spacing(glyph_list):
    Glyphs.clearLog()
    warnings = []
    if ALL_MASTERS:
        font_masters = FONT.masters
    else:
        font_masters = [FONT.selectedFontMaster]
    for glyph in glyph_list:
        for ext in sorted(REPLACERS.keys(), key=lambda k: -len(k)):
            if ext in glyph.name:
                parent_glyph_name = glyph.name.replace(ext, REPLACERS[ext], 1)
                break
        else:
            print("Couldn't find parent glyph for '{}'".format(glyph.name))
            continue
        parent_glyph = FONT[parent_glyph_name]
        if parent_glyph is None:
            warnings.append(
                "'{}': could't find parent '{}'".format(
                    glyph.name, parent_glyph_name
                )
            )
            continue
        for font_master in font_masters:
            layer = glyph.layers[font_master.id]
            parent_layer = parent_glyph.layers[font_master.id]
            sb_diff = parent_layer.LSB - parent_layer.RSB
            if abs(layer.LSB - layer.RSB - sb_diff) < 2:
                print(
                    "[{}] '{}' and '{}' have equal sb difference {}".format(
                        font_master.name.encode("utf-8"),
                        parent_glyph_name,
                        glyph.name,
                        sb_diff,
                    )
                )
                continue
            old_width, old_lsb, old_rsb = layer.width, layer.LSB, layer.RSB
            move_glyph(layer, sb_diff)
            if layer.width != old_width:
                layer.LSB, layer.RSB = old_lsb, old_rsb
                warnings.append(
                    "[{}] '{}': widths with old and new sb are not equal -> old values restored".format(
                        font_master.name, glyph.name
                    )
                )
            else:
                print(
                    "[{}] '{}' -> '{}': Parent SB difference: {} => Child L:{}->{}, R:{}->{}, SB difference: {}".format(
                        font_master.name,
                        parent_glyph_name,
                        glyph.name,
                        sb_diff,
                        old_lsb,
                        layer.LSB,
                        old_rsb,
                        layer.RSB,
                        layer.LSB - layer.RSB,
                    )
                )
    print("\n".join(warnings))


if __name__ == "__main__":
    d = Dialog()
