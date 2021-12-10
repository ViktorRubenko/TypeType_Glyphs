# MenuTitle: Swap Glyphs
# -*- coding: utf-8 -*-
__doc__ = """
Swap multiple glyphs at once
"""

from vanilla import FloatingWindow, TextEditor, Button


class SwapWindow:
    def __init__(self):
        self.width = 300
        self.w = FloatingWindow((self.width, 400), "Swap Glyphs")
        self.w.leftTextField = TextEditor("auto", "glyph names >>")
        self.w.rightTextField = TextEditor("auto", "<< glyph names")
        self.w.swapButton = Button("auto", "Swap", callback=self.swap_glyphs)

        rules = [
            "H:|-10-[leftTextField]-10-[rightTextField(==leftTextField)]-10-|",
            "V:|-10-[leftTextField]-10-[swapButton]-10-|",
            "V:|-10-[rightTextField(==leftTextField)]",
            "H:|-10-[swapButton]-10-|",
        ]
        self.w.addAutoPosSizeRules(rules)
        self.w.center()
        self.w.open()

    def swap_glyphs(self, sender):
        font = Glyphs.font
        if not font:
            return
        left_glyphs = self.w.leftTextField.get().strip().splitlines()
        right_glyphs = self.w.rightTextField.get().strip().splitlines()

        if len(left_glyphs) != len(right_glyphs):
            Message("The left number of glyph must be equal to the right")
            return

        for left_name, right_name in zip(left_glyphs, right_glyphs):
            if left_name not in font.glyphs:
                Message(left_name, "doest exist")
                return
            if right_name not in font.glyphs:
                Message(right_name, "doest exist")
                return

        for left_name, right_name in zip(left_glyphs, right_glyphs):
            left_glyph, right_glyph = font[left_name], font[right_name]
            print(left_glyph, right_glyph)
            left_glyph.name = "temp"
            right_glyph.name = left_name
            left_glyph.name = right_name
        Message("Swapped!", title="Success")


SwapWindow()
