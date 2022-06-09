# MenuTitle: Compare small caps
# -*- coding: utf-8 -*-
__doc__ = """
Finds small caps glyphs whose selected property difference is equal or greater than a given threshold
"""


from vanilla import *
from AppKit import NSScreen
import os
from collections import Counter


class CompareWindow:
    def __init__(self):
        self.font = Glyphs.font
        self.size = self._size_from_screen()
        self.w = Window(
            self.size,
            "Compare Small Caps Glyph Properties",
            maxSize=(1000, 1000),
        )
        self.w.masters = PopUpButton(
            "auto",
            [],
        )

        self.w.nest = Group("auto")

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
                {"title": "Origin"},
                {"title": "SC"},
            ],
        )

        self.w.mark_button = Button(
            "auto",
            "Mark small caps",
            callback=lambda sender: self.mark_glyphs(
                font=self.fonts[self.w.font2.get()],
                glyph_names=[row["Glyph"] for row in self.w.result_sheet],
            ),
        )

        self.w.nest.addAutoPosSizeRules(
            [
                "H:|-[td_text]-[threshold_entry(>=100)]-[run_button]-|",
                "V:|-[td_text]-|",
                "V:|-[threshold_entry]-|",
                "V:|-[run_button]-|",
            ]
        )

        rules = [
            "H:|-[masters]-|",
            "H:|-[nest]-|",
            "H:|-[result_sheet]-|",
            "H:|-150-[mark_button]-150-|",
            "V:|-[masters]-[nest]-[result_sheet]-[mark_button]-|",
        ]
        self.w.addAutoPosSizeRules(rules)

        self.set_masters()

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

    def set_masters(self):
        self.w.masters.setItems([i.name for i in self.font.masters])

    def find_difference(self, sender):
        rows = []
        master_id = self.font.masters[self.w.masters.get()].id

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

        glyphs = {}
        failed_glyphs = []
        sc_glyph_names = [
            glyph.name
            for glyph in self.font.glyphs
            if glyph.name.endswith(".sc")
        ]
        for glyph in [
            glyph
            for glyph in self.font.glyphs
            if not glyph.name.endswith(".sc")
        ]:
            sc_name = None
            if glyph.name + ".sc" in sc_glyph_names:
                sc_name = glyph.name + ".sc"
            elif (
                glyph.name[0].lower() + glyph.name[1:] + ".sc"
                in sc_glyph_names
            ):
                sc_name = glyph.name[0].lower() + glyph.name[1:] + ".sc"
            elif glyph.name.lower() + ".sc" in sc_glyph_names:
                sc_name = glyph.name.lower() + ".sc"
            if sc_name:
                glyphs[glyph] = self.font[sc_name]
                sc_glyph_names.remove(sc_name)
        failed_glyphs = sc_glyph_names
        for prop in ["LSB", "RSB"]:
            for glyph, sc_glyph in glyphs.items():
                result = self.compare_metric(
                    prop,
                    threshold,
                    glyph.layers[master_id],
                    sc_glyph.layers[master_id],
                )
                if any(result):
                    rows.append(
                        {
                            "Glyph": str(glyph.name),
                            "Property": prop,
                            "Origin": str(result[0]),
                            "SC": str(result[1]),
                        }
                    )
        self.w.result_sheet.set(rows)
        if failed_glyphs:
            Glyphs.clearLog()
            Glyphs.showMacroWindow()
            print("Failed glyphs:\n{}".format("\n".join(failed_glyphs)))

    def compare_metric(self, metric_name, threshold, g1_layer, g2_layer):
        value1 = getattr(g1_layer, metric_name)
        value2 = getattr(g2_layer, metric_name)
        if abs(value1 - value2) >= threshold:
            return value1, value2
        return None, None

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.35), int(size.height * 0.8)


CompareWindow()
