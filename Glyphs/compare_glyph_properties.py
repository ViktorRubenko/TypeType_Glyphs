# MenuTitle: Compare glyph properties
# -*- coding: utf-8 -*-
__doc__ = """
Finds glyphs whose selected property difference is equal or greater than a given threshold
"""


from vanilla import *
from AppKit import NSScreen
import os
from collections import Counter


PROPERTIES = {
    0: ["LSB"],
    1: ["RSB"],
    2: ["LSB", "RSB"],
    3: ["width"],
    4: ["LSB", "RSB", "width"],
    5: ["Height"],
}


class CompareWindow:
    def __init__(self):
        self.fonts = Glyphs.fonts
        self.font_names = [
            os.path.basename(font.filepath)
            if font.filepath
            else font.familyName
            for font in Glyphs.fonts
        ]
        self.size = self._size_from_screen()
        self.w = Window(
            self.size,
            "Compare Glyph Properties",
            maxSize=(1000, 1000),
        )

        self.w.font1 = PopUpButton(
            "auto",
            self.font_names,
            callback=self.set_masters_one,
        )
        self.w.font1_masters = PopUpButton(
            "auto",
            [],
        )
        self.w.font2 = PopUpButton(
            "auto",
            self.font_names,
            callback=self.set_masters_two,
        )
        self.w.font2_masters = PopUpButton(
            "auto",
            [],
        )

        self.w.nest = Group("auto")

        self.w.nest.prop_text = TextBox(
            "auto",
            "Property",
        )

        self.w.nest.prop = PopUpButton(
            "auto",
            [
                "LSB",
                "RSB",
                "Both SB",
                "Width",
                "ALL spacing",
                "Height",
            ],
            callback=self.disable_td_entry,
        )

        self.w.nest.td_text = TextBox(
            "auto",
            "Threshold:",
        )

        self.w.nest.threshold_entry = EditText(
            "auto",
            placeholder="threshold for search",
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
                {"title": "Property"},
                {"title": "Font 1"},
                {"title": "Font 2"},
            ],
        )

        self.w.mark_button = Button(
            "auto",
            "Mark glyphs in the 2nd font",
            callback=lambda sender: self.mark_glyphs(
                font=self.fonts[self.w.font2.get()],
                glyph_names=[row["Glyph"] for row in self.w.result_sheet],
            ),
        )

        self.w.nest.addAutoPosSizeRules(
            [
                "H:|-[prop_text]-[prop]-[td_text]-[threshold_entry(>=100)]-[run_button]-|",
                "V:|-[prop_text]-|",
                "V:|-[td_text]-|",
                "V:|-[prop]-|",
                "V:|-[threshold_entry]-|",
                "V:|-[run_button]-|",
            ]
        )

        rules = [
            "H:|-[font1(>=400)]-|",
            "H:|-[font2]-|",
            "H:|-[font1_masters]-|",
            "H:|-[font2_masters]-|",
            "H:|-[nest]-|",
            "H:|-[result_sheet]-|",
            "H:|-150-[mark_button]-150-|",
            "V:|-[font1][font1_masters]-[font2][font2_masters]-[nest]-[result_sheet]-[mark_button]-|",
        ]
        self.w.addAutoPosSizeRules(rules)

        self.w.font1.set(0)
        self.w.font1.set(1 if len(self.font_names) == 2 else 0)

        self.set_masters_one(self.w.font1)
        self.set_masters_two(self.w.font2)

        self.w.center()
        self.w.open()

    def disable_td_entry(self, sender):
        if sender.get() == 5:
            self.w.nest.threshold_entry.set("0")
            self.w.nest.threshold_entry.enable(False)
        else:
            if not self.w.nest.threshold_entry.isEnabled():
                self.w.nest.threshold_entry.set("")
                self.w.nest.threshold_entry.enable(True)

    def mark_glyphs(self, font, glyph_names):
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

    def set_masters_one(self, sender):
        font = self.fonts[sender.get()]
        self.w.font1_masters.setItems([i.name for i in font.masters])

    def set_masters_two(self, sender):
        font = self.fonts[sender.get()]
        self.w.font2_masters.setItems([i.name for i in font.masters])

    def find_difference(self, sender):
        rows = []

        font1 = self.fonts[self.w.font1.get()]
        master1_id = font1.masters[self.w.font1_masters.get()].id

        font2 = self.fonts[self.w.font2.get()]
        master2_id = font2.masters[self.w.font2_masters.get()].id

        prop_id = self.w.nest.prop.get()
        props = PROPERTIES[prop_id]

        try:
            threshold = self.w.nest.threshold_entry.get()
            if not threshold:
                Message(
                    "Threshold is empty",
                    "Error",
                    OKButton="OK",
                )
                return
            threshold = float(threshold)
            if threshold < 0:
                raise ValueError
        except:
            Message(
                "Invalid threshold value",
                "Error",
                OKButton="Please forgive me",
            )
            return

        g2_names = [g.name for g in font2.glyphs]
        for prop in props:
            for glyph1 in font1.glyphs:
                if glyph1.name in g2_names:
                    if prop_id in range(5):
                        result = self.compare_metric(
                            prop,
                            threshold,
                            glyph1.layers[master1_id],
                            font2[glyph1.name].layers[master2_id],
                        )
                    elif prop_id == 5:
                        result = self.compare_height(
                            glyph1.layers[master1_id],
                            font2[glyph1.name].layers[master2_id],
                        )
                    if any(result):
                        rows.append(
                            {
                                "Glyph": str(glyph1.name),
                                "Property": prop,
                                "Font 1": str(result[0]),
                                "Font 2": str(result[1]),
                            }
                        )
                else:
                    print("ERROR", glyph1.name)
        self.w.result_sheet.set(rows)

    def compare_metric(self, metric_name, threshold, g1_layer, g2_layer):
        value1 = getattr(g1_layer, metric_name)
        value2 = getattr(g2_layer, metric_name)
        if abs(value1 - value2) >= threshold:
            return value1, value2
        return None, None

    def compare_height(self, g1_layer, g2_layer):
        value1 = (
            int(g1_layer.bounds.origin.y),
            int(g1_layer.bounds.origin.y + g1_layer.bounds.size.height),
        )
        value2 = (
            int(g2_layer.bounds.origin.y),
            int(g2_layer.bounds.origin.y + g2_layer.bounds.size.height),
        )
        if value1 != value2:
            return str(value1), str(value2)
        return None, None

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.35), int(size.height * 0.8)


CompareWindow()
