# MenuTitle: Set small caps metrics
# -*- coding: utf-8 -*-
__doc__ = "Set metrics for small caps sidebearings"

import vanilla
from vanilla.dialogs import askYesNo

Glyphs.clearLog()
font = Glyphs.font


class SmallCapsDialog:
    def __init__(self, glyphs, failed):
        self.failed_glyphs = failed
        self.glyphs = glyphs
        self.w = vanilla.FloatingWindow((300, 300))
        self.w.leftFormulaTextBox = vanilla.TextBox("auto", "Left: ")
        self.w.rightFormulaTextBox = vanilla.TextBox("auto", "Right: ")
        self.w.leftFormulaEditText = vanilla.EditText(
            "auto",
            "=={parentName}",
        )
        self.w.rightFormulaEditText = vanilla.EditText(
            "auto",
            "=={parentName}",
        )
        self.w.applyButton = vanilla.Button(
            "auto", "Apply", callback=self.apply_callback
        )
        self.w.cancelButton = vanilla.Button(
            "auto", "Cancel", callback=self.cancel_callback
        )

        rules = [
            "H:|-[leftFormulaTextBox(==40)]-[leftFormulaEditText]-|",
            "H:|-[rightFormulaTextBox(==leftFormulaTextBox)]-[rightFormulaEditText]-|",
            "V:|-[leftFormulaEditText]-[rightFormulaEditText(==leftFormulaEditText)]-[applyButton]-|",
            "V:|-[leftFormulaEditText]-[rightFormulaEditText(==leftFormulaEditText)]-[cancelButton]-|",
            "V:|-[leftFormulaTextBox]-[rightFormulaTextBox(==leftFormulaTextBox)]-[applyButton]-|",
            "H:|-[cancelButton]-[applyButton(==cancelButton)]-|",
        ]
        self.w.addAutoPosSizeRules(rules)

        self.w.center()
        self.w.open()

    def apply_callback(self, sender):
        self.procced()
        self.w.close()
        if self.failed_glyphs:
            Message(
                "{} small caps were failed".format(len(self.failed_glyphs))
            )
            Glyphs.clearLog()
            print("Failed small caps:\n{}").format(
                "\n".join(self.failed_glyphs)
            )
            Glyphs.showMacroWindow()

    def cancel_callback(self, sender):
        self.w.close()

    def procced(self):
        for glyph, sc_glyph in self.glyphs.items():
            for layer in sc_glyph.layers:
                layer.leftMetricsKey = (
                    self.w.leftFormulaEditText.get()
                    .replace("{parentName}", glyph.name)
                    .replace(" ", "")
                )
                layer.rightMetricsKey = (
                    self.w.rightFormulaEditText.get()
                    .replace("{parentName}", glyph.name)
                    .replace(" ", "")
                )
                layer.syncMetrics()
                layer.updateMetrics()
        font.updateMetrics()


def main():
    if font.selectedLayers:
        sc_glyphs = [
            layer.parent
            for layer in font.selectedLayers
            if layer.parent.name.endswith(".sc")
        ]
    else:
        sc_glyphs = [
            glyph for glyph in font.glyphs if glyph.name.endswith(".sc")
        ]
    if sc_glyphs:
        confirm = askYesNo("Apply for {} small caps?".format(len(sc_glyphs)))
    else:
        Message("Nan small caps were selected")
    if not confirm:
        return

    sc_pairs = {}
    sc_glyph_names = [glyph.name for glyph in sc_glyphs]
    for glyph in [
        glyph for glyph in font.glyphs if not glyph.name.endswith(".sc")
    ]:
        sc_name = None
        if glyph.name + ".sc" in sc_glyph_names:
            sc_name = glyph.name + ".sc"
        elif glyph.name[0].lower() + glyph.name[1:] + ".sc" in sc_glyph_names:
            sc_name = glyph.name[0].lower() + glyph.name[1:] + ".sc"
        elif glyph.name.lower() + ".sc" in sc_glyph_names:
            sc_name = glyph.name.lower() + ".sc"
        if sc_name:
            sc_pairs[glyph] = font[sc_name]
            sc_glyph_names.remove(sc_name)
    failed_glyphs = sc_glyph_names

    SmallCapsDialog(glyphs=sc_pairs, failed=failed_glyphs)


if __name__ == "__main__":
    main()
