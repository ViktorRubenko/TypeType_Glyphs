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

        for_vtt = dict()

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

            left_prod_name = Glyphs.productionGlyphName(left_name, font).encode('utf-8')
            right_prod_name = Glyphs.productionGlyphName(right_name, font).encode('utf-8')

            left_glyph, right_glyph = font[left_name], font[right_name]
            print(left_glyph, right_glyph)

            left_glyph.unicode, right_glyph.unicode = (
                right_glyph.unicode,
                left_glyph.unicode,
            )

            left_glyph.name = "temp"
            right_glyph.name = left_name
            left_glyph.name = right_name

            for_vtt[left_prod_name] = right_prod_name
            for_vtt[right_prod_name] = left_prod_name

            # FIX FOR ACTIVE LAYER
            
            for glyph in font.glyphs:
                b_names = [_.name for _ in glyph.layers[0].components]
                if b_names and (left_name in b_names or right_name in b_names):
                    for layer in glyph.layers:
                        for component in layer.components:
                            if component.name == left_name:
                                component.name = right_name
                                continue
                            if component.name == right_name:
                                component.name = left_name

        Message("Swapped!", title="Success")
        print(for_vtt)


SwapWindow()
