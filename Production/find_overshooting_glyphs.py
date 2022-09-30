# MenuTitle: Find overshooting glyphs
import vanilla

__doc__ = """
Marks glyphs that go beyond certain height
"""


COLORS = {
    "red": 0,
    "orange": 1,
    "yellow": 3,
    "purple": 8,
    "magenta": 9,
    "charcoal": 11,
}


class Dialog:
    def __init__(self):
        self.w = vanilla.FloatingWindow((300, 300), minSize=(300, 300))
        self.w.group_ascender = vanilla.Group("auto")
        self.w.group_ascender.text_ascender = vanilla.TextBox(
            "auto", "Ascender value:"
        )
        self.w.group_ascender.input_ascender = vanilla.EditText(
            "auto", placeholder="ascender"
        )
        self.w.group_descender = vanilla.Group("auto")
        self.w.group_descender.text_descender = vanilla.TextBox(
            "auto", "Descender value:"
        )
        self.w.group_descender.input_descender = vanilla.EditText(
            "auto", placeholder="descender"
        )
        self.w.group_color = vanilla.Group("auto")
        self.w.group_color.text_color = vanilla.TextBox("auto", "Color:")
        self.w.group_color.combo_color = vanilla.ComboBox(
            "auto", items=list(COLORS.keys())
        )
        self.w.group_color.combo_color.set("red")
        self.w.button_run = vanilla.Button(
            "auto", "Run", callback=self.mark_glyphs
        )
        self.w.addAutoPosSizeRules(
            [
                "V:|-[group_ascender]-[group_descender]-[group_color]-[button_run]-|",
                "H:|-[button_run]-|",
            ],
            {},
        )
        self.w.group_ascender.addAutoPosSizeRules(
            [
                "H:|-[text_ascender(==120)]-[input_ascender(>=100)]-|",
                "V:|[text_ascender]|",
                "V:|[input_ascender]|",
            ],
            {},
        )
        self.w.group_descender.addAutoPosSizeRules(
            [
                "H:|-[text_descender(==120)]-[input_descender(>=100)]-|",
                "V:|[text_descender]|",
                "V:|[input_descender]|",
            ],
            {},
        )
        self.w.group_color.addAutoPosSizeRules(
            [
                "H:|-[text_color(==120)]-[combo_color(>=100)]-|",
                "V:|[text_color]|",
                "V:|[combo_color]|",
            ],
            {},
        )
        self.w.open()
        self.w.center()

    def mark_glyphs(self, sender):
        Glyphs.clearLog()
        ascender = self.w.group_ascender.input_ascender.get()
        descender = self.w.group_descender.input_descender.get()
        ascender = float(ascender) if ascender else float("Inf")
        descender = float(descender) if descender else -float("Inf")
        color = COLORS[self.w.group_color.combo_color.get()]
        font = Glyphs.font
        results = []
        for glyph in font.glyphs:
            layer = glyph.layers[font.selectedFontMaster.id]
            bounds = layer.bounds
            glyph_ascender = bounds.origin.y + bounds.size.height
            glyph_descender = bounds.origin.y
            to_color = False
            if glyph_ascender > ascender:
                to_color = True
                results.append(
                    "{}: ascender {}[{}]/{}".format(
                        glyph.name,
                        glyph_ascender,
                        glyph_ascender - ascender,
                        ascender,
                    )
                )
            if glyph_descender < descender:
                results.append(
                    "{}: descender {}[{}]/{}".format(
                        glyph.name,
                        glyph_descender,
                        glyph_descender - descender,
                        descender,
                    )
                )
            if to_color:
                glyph.color = color
        print("\n".join(results) if results else "Nothing overshoots")
        Glyphs.showMacroWindow()
        self.w.close()


if __name__ == "__main__":
    Dialog()
