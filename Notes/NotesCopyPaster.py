# MenuTitle: Note CopyPaster
# -*- coding: utf-8 -*-
# Version: 0.0.1 (13 Oct), 2022)
__doc__ = """
Copies glyphs notes from one font to another. Works with currently open fonts. 
To copy, you must write glyph names space separated in the input field. 
"""


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
            (300, 430), title="Notes CopyPaster"
        )
        h = 20
        self.window.labelFrom = vanilla.TextBox((10, 10, 0, h), "From")
        self.window.fontComboBox = vanilla.ComboBox(
            (50, 10, -10, h), OTHER_FONTS, callback=self.fontComboBoxCallback
        )
        self.window.labelPath = vanilla.TextBox((10, 10 + h + 5, -10, h + 20))
        self.window.labelList = vanilla.TextBox(
            (10, 10 + (h + 5) * 3, -10, h), "List of glyphs"
        )
        self.window.glyphsTextEdit = vanilla.TextEditor(
            (10, 10 + (h + 5) * 4, -10, -40)
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
            notes_copy_paste(
                font_copy,
                Glyphs.font,
                glyphs_list,
            )


def notes_copy_paste(
    font_copy,
    font_paste,
    glyphs_list,
):
    open_console_log = False
    glyphs_font_copy = [g.name for g in font_copy.glyphs]
    for glyph_name in glyphs_list:
        if glyph_name not in font_copy.glyphs:
            LogError("Origin font doesn't have '{}' glyph".format(glyph_name))
            open_console_log = True
            continue
        if glyph_name not in font_paste.glyphs:
            LogError("Current font doesn't have {} glyph".format(glyph_name))
            open_console_log = True
            continue
        font_paste[glyph_name].note = font_copy[glyph_name].note
    if open_console_log:
        Message("Not all desired notes were copied", "Completed")
        Glyphs.showMacroWindow()
    else:
        Message("Notes sucessfully copied", "Completed")


if __name__ == "__main__":
    Glyphs.clearLog()
    OptionsWindow()
