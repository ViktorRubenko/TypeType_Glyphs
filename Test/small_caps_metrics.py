# MenuTitle: SmallCaps metrics setter
# -*- coding: utf-8 -*-
__doc__ = "Set metrics for small caps sidebearings"

import vanilla
from vanilla.dialogs import askYesNo

Glyphs.clearLog()
font = Glyphs.font


class SmallCapsDialog:
    def __init__(self, glyphs):
        self.glyphs = glyphs
        self.failed_glyphs = []
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
        self.failed_glyphs = []
        for glyph in self.glyphs:
            parent_name = ".".join(glyph.name.split(".")[:-1])
            parent_name = parent_name[0].upper() + parent_name[1:]
            if parent_name not in font.glyphs:
                parent_name = parent_name[0].lower() + parent_name[1:]
            if parent_name not in font.glyphs:
                self.failed_glyphs.append(glyph.name)
                continue
            for layer in glyph.layers:
                layer.leftMetricsKey = (
                    self.w.leftFormulaEditText.get()
                    .replace("{parentName}", parent_name)
                    .replace(" ", "")
                )
                layer.rightMetricsKey = (
                    self.w.rightFormulaEditText.get()
                    .replace("{parentName}", parent_name)
                    .replace(" ", "")
                )
                layer.syncMetrics()
                layer.updateMetrics()
        font.updateMetrics()


def main():
    if font.selectedLayers:
        glyphs = [
            layer.parent
            for layer in font.selectedLayers
            if layer.parent.name.endswith(".sc")
        ]
    else:
        glyphs = [glyph for glyph in font.glyphs if glyph.name.endswith(".sc")]
    if glyphs:
        confirm = askYesNo("Apply for {} small caps?".format(len(glyphs)))
    else:
        Message("Nan small caps were selected")
    if not confirm:
        return

    SmallCapsDialog(glyphs=glyphs)


if __name__ == "__main__":
    main()
