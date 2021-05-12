# MenuTitle: Multiply metrics and kerning
# -*- coding: utf-8 -*-
# Version: 0.1.1 (07 Oct, 2019)
__doc__ = """
Multiply metrics and kerning by given coefficient
"""


import vanilla


class MultiplyWindow:
    def __init__(self):
        self.window = vanilla.Window(
            (180, 110),
            title="Multiply metrics & kerning",
        )

        self.window.label = vanilla.TextBox(
            (10, 10, -10, 20),
            "Multiply coefficient:",
        )
        self.window.coef_entry = vanilla.EditText(
            (10, 35, -10, 20),
            placeholder="0.0-2.0",
        )
        self.window.run_button = vanilla.Button(
            (30, 70, -30, 20),
            "Run",
            callback=self.multiply,
        )
        self.window.center()
        self.window.open()

    def multiply(self, sender):

        try:
            coef = float(self.window.coef_entry.get())
            if not 0 < coef < 2:
                raise ValueError
        except ValueError:
            self.alert_window()
            return

        pos_coef = coef
        if coef < 1:
            neg_coef = 1 + (1 - coef)
        else:
            neg_coef = 2 - coef

        font = Glyphs.font

        for glyph in font.glyphs:
            for layer in glyph.layers:
                rsb, lsb, width = layer.RSB, layer.LSB, layer.width
                for (
                    attr
                ) in "rightMetricsKey leftMetricsKey widthMetricsKey".split():
                    setattr(layer, attr, None)
                    setattr(glyph, attr, None)
                layer.LSB = (
                    round(lsb * pos_coef) if lsb > 0 else round(lsb * neg_coef)
                )
                layer.RSB = (
                    round(rsb * pos_coef) if rsb > 0 else round(rsb * neg_coef)
                )

        kerning = font.kerning
        for master_id, level1 in kerning.items():
            for first_glyph_id, level2 in level1.items():
                for second_glyph_id, value in level2.items():
                    kerning[master_id][first_glyph_id][second_glyph_id] = (
                        value * pos_coef if value > 0 else value * neg_coef
                    )

    def alert_window(self):
        alert_w = vanilla.FloatingWindow((200, 80), "Alert")
        alert_w.text = vanilla.EditText(
            (5, 5, -5, 40), "Coefficient value must be in (0.0-2.0) range"
        )

        def close(sender):
            alert_w.close()
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
