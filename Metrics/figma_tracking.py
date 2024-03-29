# MenuTitle: Figma tracking
# -*- coding: utf-8 -*-
__doc__ = """
Correlate sidebearings to a multiplied UPM value for Figma tracking 
"""


import os
import vanilla


class MultiplyWindow:
    def __init__(self):
        self.window = vanilla.Window(
            (180, 200),
            title="Figma tracking",
        )

        self.window.label = vanilla.TextBox(
            (10, 10, -10, 20),
            "Multiply coefficient:",
        )
        self.window.coef_entry = vanilla.TextEditor(
            (10, 35, -10, -50),
        )
        self.window.coef_entry.set(
            "title: coefficiet\n\nExample:\n9pt: 1.02\n10pt: 1.015"
        )
        self.window.run_button = vanilla.Button(
            (30, -40, -30, 20),
            "Run",
            callback=self.execute,
        )
        self.window.center()
        self.window.open()

    def read_coeffs(self):
        coefs = {}
        for line in self.window.coef_entry.get().splitlines():
            if not line:
                continue
            title, coef = (_.strip() for _ in line.split(":"))
            coef = float(coef)
            if not 0 < coef < 2:
                raise ValueError
            coefs[title] = coef
        return coefs

    def execute(self, sender):
        try:
            coefs = self.read_coeffs()
        except:
            self.alert_window("Coefficient value must be in (0.0-2.0) range")
            return

        main_font = Glyphs.font
        modified_fonts = []
        for title, coef in coefs.items():
            modified_font = main_font.copy()
            modified_fonts.append(modified_font)
            modified_font.familyName += " " + title

            for instance in modified_font.instances:
                cp = instance.customParameters
                for param in "fileName preferredFamilyName".split():
                    cp[param] = cp[param].replace(
                        main_font.familyName, modified_font.familyName
                    )
                cp["postscriptFontName"] = cp["postscriptFontName"].replace(
                    main_font.familyName.replace(" ", ""),
                    modified_font.familyName.replace(" ", ""),
                )

            MultiplyWindow.multiply(modified_font, coef)

        for modified_font in modified_fonts:
            modified_font.show()

        self.alert_window("Done!", clear=False)

    @staticmethod
    def multiply(font, coef):
        for glyph in font.glyphs:
            for layer in glyph.layers:
                rsb, lsb, width = layer.RSB, layer.LSB, layer.width
                for (
                    attr
                ) in "rightMetricsKey leftMetricsKey widthMetricsKey".split():
                    setattr(layer, attr, None)
                    setattr(glyph, attr, None)

                diff = round(font.upm * coef) - font.upm
                layer.LSB = lsb + diff // 2
                layer.RSB = rsb + diff // 2 + diff % 2

    def alert_window(self, text, clear=True):
        alert_w = vanilla.FloatingWindow((200, 80), "Alert")
        alert_w.text = vanilla.TextBox(
            (5, 5, -5, 40),
            text,
            alignment="center",
        )

        def close(sender):
            alert_w.close()
            if clear:
                self.window.coef_entry.set(None)

        alert_w.button = vanilla.Button(
            (20, 55, -20, 15),
            "OK",
            callback=close,
        )

        alert_w.center()
        alert_w.open()


if __name__ == "__main__":
    MultiplyWindow()
