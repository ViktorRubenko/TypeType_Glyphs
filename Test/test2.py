# MenuTitle: WhiteSpace Calculator
# -*- coding: utf-8 -*-

from __future__ import print_function
import math
import vanilla
from shapely.geometry import Polygon


Glyphs.clearLog()
font = Glyphs.font


class Constants:
    def __init__(self):
        self.right = "right"
        self.left = "left"


class PairSpaceCalculator:
    def __init__(self):
        self.font = None
        self.constants = Constants()

    @property
    def current_master(self):
        return self.font.selectedFontMaster if self.font else None

    @property
    def master_id(self):
        current_master = self.current_master
        return current_master.id if current_master else None

    @staticmethod
    def compute_extremes(layers):
        bottom = int(max(l.bounds.origin.y for l in layers))
        top = int(
            min((l.bounds.origin.y + l.bounds.size.height) for l in layers)
        )
        return top, bottom

    def compute_space(self, pair, use_kerning=True):
        self.font = Glyphs.font
        left_glyph, right_glyph = (
            self.font.glyphs[u]
            for u in ("{:04x}".format(ord(g)) for g in pair)
        )
        if all((left_glyph, right_glyph)):
            return self._compute_space(
                left_glyph, right_glyph, use_kerning=use_kerning
            )
        else:
            raise ValueError("Font doesn't containt given pair")

    def _compute_space(self, left_glyph, right_glyph, use_kerning):
        kerning_value = (
            self.get_kerning(left_glyph, right_glyph) if use_kerning else 0
        )

        left_layer, right_layer = (
            g.layers[self.master_id] for g in (left_glyph, right_glyph)
        )

        top, bottom = PairSpaceCalculator.compute_extremes(
            [right_layer, left_layer]
        )

        right_side_first = self.get_coordinates(
            right_layer, self.constants.right, top, bottom
        )
        left_side_second = self.get_coordinates(
            left_layer, self.constants.left, top, bottom, kerning=kerning_value
        )
        poly = Polygon(right_side_first + left_side_second[::-1])
        return poly.area

    def get_kerning(self, left_glyph, right_glyph):
        kerning = self.font.kerning[self.master_id]
        right_side = kerning.get(left_glyph.rightKerningKey, {})
        right_side.update(kerning.get(left_glyph.id, {}))

        value = right_side.get(right_glyph.leftKerningKey, None)
        if not value:
            value = right_side.get(right_glyph.id, 0)
        return value

    def italicize_x(self, x, y, top_y, italicAngle, glyph_side):
        if italicAngle == 0:
            return x
        italicAngle = math.radians(italicAngle)
        tangens = math.tan(italicAngle)
        if glyph_side == self.constants.right:
            y = -top_y
        return x + tangens * y

    def get_coordinates(self, layer, pair_side, top, bottom, kerning=0):
        line_x = (
            layer.bounds.origin.x
            if pair_side == self.constants.left
            else layer.bounds.origin.x + layer.bounds.size.width
        )
        line_y = list(range(bottom, top - 1, 5)) + [top]
        if self.current_master.italicAngle != 0:
            line_coordinates = [
                (
                    self.italicize_x(
                        line_x,
                        y,
                        self.current_master.italicAngle,
                        top,
                        pair_side,
                    ),
                    y,
                )
                for y in line_y
            ]
        else:
            line_coordinates = [(line_x, y) for y in line_y]
        increment = -1 if pair_side == self.constants.right else 1
        sb = layer.RSB if pair_side == self.constants.left else layer.LSB
        coordinates = []
        for x, y in line_coordinates:
            shift = 0
            while True:
                intersection = layer.intersectionsBetweenPoints(
                    (x + shift - 1, y - 1),
                    (x + shift + 1, y + 1),
                    components=True,
                )
                if len(intersection) > 2:
                    coordinates.append([shift, y])
                    break
                intersection = layer.intersectionsBetweenPoints(
                    (x + shift + 1, y - 1),
                    (x + shift - 1, y + 1),
                    components=True,
                )
                if len(intersection) > 2:
                    coordinates.append([shift, y])
                    break
                shift += increment
                if shift > 1000:
                    # didn't find contour line
                    break
        if pair_side == self.constants.right:
            sb = -sb

        for coordinate in coordinates:
            coordinate[0] += sb + kerning

        return coordinates


class GUI(object):
    def __init__(self):
        self.w = vanilla.FloatingWindow(
            (200, 300),
            "WhiteSpace Calculator",
            minSize=(200, 300),
            maxSize=(500, 600),
        )
        self.w.checkBox = vanilla.CheckBox(
            "auto",
            "Use kerning",
            value=True,
        )
        self.w.textView = vanilla.TextEditor("auto")
        self.w.buttonRun = vanilla.Button(
            "auto", "Run", callback=self.runHandler
        )

        self.w.addAutoPosSizeRules(
            [
                "V:|-[checkBox]-[textView]-[buttonRun]-|",
                "H:|-[checkBox]-|",
                "H:|-[textView]-|",
                "H:|-[buttonRun]-|",
            ]
        )

        self.w.open()

    def runHandler(self, sender):
        use_kerning = self.w.checkBox.get()
        space_calc = PairSpaceCalculator()
        for pair in self.w.textView.get().strip().split():
            if not pair:
                continue
            try:
                space_area = space_calc.compute_space(
                    pair=pair, use_kerning=use_kerning
                )
                print(pair, ":", int(space_area))
            except ValueError as error:
                print(pair, error)
        Glyphs.showMacroWindow()


if __name__ == "__main__":
    GUI()
