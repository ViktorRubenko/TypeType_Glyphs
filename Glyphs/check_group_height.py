# MenuTitle: Check selected height
# -*- coding: utf-8 -*-

__doc__ == """
Compare bottom and top height values of selected glyphs with reference glyph
"""


from vanilla import *


class CompareWindow:
    def __init__(self):
        self.size = self._size_from_screen()
        self.w = Window(
            self.size,
            "Check selected height",
            maxSize=(1000, 1000),
        )

        self.w.nest = Group("auto")

        self.w.nest.ref_label = TextBox(
            "auto",
            "Reference glyph:",
        )

        self.w.nest.ref_entry = EditText(
            "auto",
            placeholder="reference glyph name",
        )

        self.w.nest.run_button = Button(
            "auto",
            "Run",
            callback=self.find_difference,
        )

        self.w.result_sheet = List(
            "auto",
            [],
            columnDescriptions=[
                {"title": "Glyph"},
                {"title": "top (value/overshoot)"},
                {"title": "bottom (value/overshoot)"},
            ],
        )

        self.w.mark_button = Button(
            "auto",
            "Mark glyphs",
            callback=lambda sender: self.mark_glyphs(
                glyph_names=[row["Glyph"] for row in self.w.result_sheet],
            ),
        )

        self.w.nest.addAutoPosSizeRules(
            [
                "H:|-[ref_label]-[ref_entry]-[run_button]-|",
                "V:|-[ref_label]-|",
                "V:|-[ref_entry]-|",
                "V:|-[run_button]-|",
            ]
        )

        rules = [
            "H:|-[nest]-|",
            "H:|-[result_sheet]-|",
            "H:|-150-[mark_button]-150-|",
            "V:|-[nest]-[result_sheet]-[mark_button]-|",
        ]
        self.w.addAutoPosSizeRules(rules)

        self.w.center()
        self.w.open()

    def mark_glyphs(self, glyph_names):
        font = Glyphs.font

        def mark_glyphs(mark_window):
            color_id = mark_window.color_selector.get()
            for glyph_name in glyph_names:
                font[glyph_name].color = color_id
            mark_window.close()

        mark_window = HUDFloatingWindow(
            (200, 130),
            "Mark glyphs",
        )
        mark_window.textbox = TextBox(
            (10, 10, -10, 17),
            "Mark glyphs in the 2nd font",
        )
        mark_window.color_selector = PopUpButton(
            (10, 40, -10, 20),
            [
                "red",
                "orange",
                "brown",
                "yellow",
                "light green",
                "dark green",
                "light blue",
                "dark blue",
                "purple",
                "magenta",
                "light gray",
                "charcoal",
            ],
        )
        mark_window.button = Button(
            (10, 65, -10, 20),
            "Mark",
            callback=lambda sender: mark_glyphs(mark_window),
        )
        mark_window.center()
        mark_window.open()

    def find_difference(self, sender):
        rows = []

        font = Glyphs.font

        ref_glyph_name = self.w.nest.ref_entry.get()

        if ref_glyph_name not in font.glyphs:
            Message(
                "Invalid reference glyph name",
                "Error",
            )
            return

        ref_glyph = font[ref_glyph_name]

        ref_bounds = ref_glyph.layers[font.selectedFontMaster.id].bounds
        ref_bottom = int(ref_bounds.origin.y)
        ref_top = int(ref_bottom + ref_bounds.size.height)
        for glyph in [g for g in font.glyphs if g.selected]:
            result = self.compare_height(
                ref_top=ref_top,
                ref_bottom=ref_bottom,
                layer=glyph.layers[font.selectedFontMaster.id],
            )
            if any(result):
                rows.append(
                    {
                        "Glyph": str(glyph.name),
                        "top (value/overshoot)": str(result[0]),
                        "bottom (value/overshoot)": str(result[1]),
                    }
                )
        self.w.result_sheet.set(rows)

    def compare_metric(self, metric_name, threshold, g1_layer, g2_layer):
        value1 = getattr(g1_layer, metric_name)
        value2 = getattr(g2_layer, metric_name)
        if abs(value1 - value2) >= threshold:
            return value1, value2
        return None, None

    def compare_height(self, ref_top, ref_bottom, layer):
        bottom = int(layer.bounds.origin.y)
        top = int(bottom + layer.bounds.size.height)
        return (
            "{} ({})".format(top, top - ref_top) if top != ref_top else "",
            "{} ({})".format(bottom, bottom - ref_bottom)
            if bottom != ref_bottom
            else "",
        )

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.35), int(size.height * 0.5)


CompareWindow()
