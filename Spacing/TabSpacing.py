# MenuTitle: Tab Spacing
# -*- coding: utf-8 -*-
# Version: 0.0.1 (19 Mar, 2021)

import vanilla


FONT = Glyphs.font
ALL_MASTERS = False


REPLACERS = {"tosf": "osf", ".tab": "", ".tf": "", ".tf.": ".", ".tab.": "."}


class Dialog:
    def __init__(self):
        self.w = vanilla.FloatingWindow((350, 400), "Tab Spacing")
        self.w.label = vanilla.TextBox((20, 10, -10, 20), "Glyphs:")
        self.w.checkSelected = vanilla.CheckBox(
            (20, 30, -10, 20),
            "Selected Glyphs",
            callback=self.checkSelected,
            value=True,
        )
        self.w.checkTF = vanilla.CheckBox(
            (20, 50, -10, 20), "All .tf", callback=self.checkTF, value=False
        )
        self.w.checkTOSF = vanilla.CheckBox(
            (20, 70, -10, 20), "All .tosf", callback=self.checkTOSF, value=False
        )
        self.w.runButton = vanilla.Button(
            (20, -60, 100, -20), "Run", callback=self.run
        )
        self.w.listLabel = vanilla.TextBox(
            (150, 10, -10, -10), "Glyphs to process:"
        )
        self.w.glyphList = vanilla.List(
            (150, 30, -20, -80),
            [g.name for g in FONT.glyphs if g.selected],
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

        self.w.open()

    def checkCurrentMaster(self, sender):
        global ALL_MASTERS
        if sender.get():
            self.w.checkAllMasters.set(False)
            ALL_MASTERS = False

    def checkAllMasters(self, sender):
        global ALL_MASTERS
        if sender.get():
            self.w.checkCurrentMaster.set(False)
            ALL_MASTERS = True

    def removeFromList(self, sender):
        for index in self.w.glyphList.getSelection()[::-1]:
            self.w.glyphList.remove(self.w.glyphList[index])

    def checkSelected(self, sender):
        selected_glyphs = [g.name for g in FONT.glyphs if g.selected]
        for glyph_name in selected_glyphs:
            if glyph_name in self.w.glyphList:
                self.w.glyphList.remove(glyph_name)
        if sender.get():
            self.w.glyphList.extend(selected_glyphs)

    def checkTF(self, sender):
        tf_glyphs = [g.name for g in FONT.glyphs if ".tf" in g.name]
        if sender.get():
            for glyph_name in tf_glyphs:
                if glyph_name in self.w.glyphList:
                    self.w.glyphList.remove(glyph_name)
            self.w.glyphList.extend(tf_glyphs)
        else:
            for glyph_name in tf_glyphs:
                self.w.glyphList.remove(glyph_name)

    def checkTOSF(self, sender):
        tf_glyphs = [g.name for g in FONT.glyphs if ".tosf" in g.name]
        if sender.get():
            for glyph_name in tf_glyphs:
                if glyph_name in self.w.glyphList:
                    self.w.glyphList.remove(glyph_name)
            self.w.glyphList.extend(tf_glyphs)
        else:
            for glyph_name in tf_glyphs:
                self.w.glyphList.remove(glyph_name)

    def run(self, sender):
        tab_spacing([FONT[g_name] for g_name in self.w.glyphList.get()])
        Glyphs.showMacroWindow()


d = Dialog()


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
        for font_master in font_masters:
            layer = glyph.layers[font_master.id]
            parent_layer = parent_glyph.layers[font_master.id]
            width_diff = layer.width - parent_layer.width
            old_width, old_lsb, old_rsb = layer.width, layer.LSB, layer.RSB
            layer.LSB = parent_layer.LSB + round(width_diff / 2.0)
            layer.RSB = parent_layer.RSB + int(width_diff / 2.0)
            if layer.width != old_width:
                layer.LSB, layer.RSB = old_lsb, old_rsb
                warnings.append(
                    "{}: widths with old and new sb are not equal -> old values restored".format(
                        glyph.name
                    )
                )
            else:
                print(
                    "[{}] '{}' -> '{}': W {}->[{}{}]->{}: L:{}->{}, R:{}->{}".format(
                        font_master.name,
                        parent_glyph_name,
                        glyph.name,
                        parent_layer.width,
                        "+" if width_diff > 0 else "-",
                        width_diff,
                        layer.width,
                        parent_layer.LSB,
                        layer.LSB,
                        parent_layer.RSB,
                        layer.RSB,
                    )
                )
        print("\n".join(warnings))
