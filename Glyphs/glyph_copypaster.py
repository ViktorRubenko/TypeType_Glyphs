# MenuTitle: Glyph CopyPaster
# -*- coding: utf-8 -*-
# Version: 0.0.1 (04 Mar, 2020)

from os import path
import copy
import vanilla


OTHER_FONTS = {
    path.basename(font.filepath): font
    for font in Glyphs.fonts
    if font.filepath != Glyphs.font.filepath
}


class OptionsWindow:
    def __init__(self):
        self.window = vanilla.FloatingWindow(
            (300, 400), title="Glyph CopyPaster"
        )
        h = 20
        self.window.labelFrom = vanilla.TextBox((10, 10, 0, h), "From")
        self.window.fontComboBox = vanilla.ComboBox(
            (50, 10, -10, h), OTHER_FONTS, callback=self.fontComboBoxCallback
        )
        self.window.labelPath = vanilla.TextBox((10, 10 + h + 5, -10, h + 20))
        self.window.metricsCheck = vanilla.CheckBox(
            (10, 10 + (h + 5) * 3, -10, h), "Metrics Only"
        )
        self.window.labelList = vanilla.TextBox(
            (10, 10 + (h + 5) * 4, -10, h), "List of glyphs"
        )
        self.window.glyphsTextEdit = vanilla.TextEditor(
            (10, 10 + (h + 5) * 5, -10, -40)
        )
        self.window.runButton = vanilla.Button(
            (10, -25, 60, -15), "Copy", callback=self.copy
        )
        self.window.open()

    def fontComboBoxCallback(self, sender):
        if sender.get():
            self.window.labelPath.set(OTHER_FONTS[sender.get()].filepath)

    def copy(self, sender):
        selected_font = self.window.fontComboBox.get()
        if selected_font:
            font_copy = OTHER_FONTS[selected_font]
            glyphs_list = [
                glyph_name
                for line in self.window.glyphsTextEdit.get().splitlines()
                for glyph_name in line.split()
            ]
            glyph_copy_paste(
                font_copy,
                Glyphs.font,
                glyphs_list,
                int(self.window.metricsCheck.get()),
            )


def glyph_copy_paste(font_copy, font_paste, glyphs_list, metrics_only=False):
    for glyph_name in glyphs_list:
        if not metrics_only:
            copied_layer = copy.copy(
                font_copy[glyph_name].layers[font_copy.selectedFontMaster.id]
            )
            if glyph_name not in font_paste.glyphs:
                glyph = GSGlyph()
                glyph.name = glyph_name
                glyph.unicode = font_copy[glyph_name].unicode
                font_paste.glyphs.append(glyph)
            font_paste[glyph_name].layers[
                font_paste.selectedFontMaster.id
            ] = copied_layer
        if glyph_name not in font_paste.glyphs:
            print("{} is passed".format(glyph_name))
            continue
        for (
            metric_attr
        ) in "leftMetricsKey rightMetricsKey widthMetricsKey".split():
            copy_value = getattr(font_copy[glyph_name], metric_attr)
            if copy_value:
                setattr(
                    font_paste[glyph_name], metric_attr, copy_value,
                )
            for layer in font_paste[glyph_name].layers:
                layer.syncMetrics()


if __name__ == "__main__":
    Glyphs.clearLog()
    OptionsWindow()