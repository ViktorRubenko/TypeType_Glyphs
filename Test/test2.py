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

    def compute_space(self, pair):
        self.font = Glyphs.font
        left_glyph, right_glyph = (
            self.font.glyphs[u] for u in ("{:04x}".format(ord(g)) for g in pair)
        )
        if all((left_glyph, right_glyph)):
            return self._compute_space(left_glyph, right_glyph)
        else:
            raise ValueError("Font doesn't containt given pair")

    def _compute_space(self, left_glyph, right_glyph):
        kerning_value = self.get_kerning(left_glyph, right_glyph)

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
            left_layer,
            self.constants.left,
            top,
            bottom,
        )
        space_area = Polygon(right_side_first + left_side_second[::-1]).area
        space_area_with_kerning = space_area
        if kerning_value != 0:
            for coordinate in left_side_second:
                coordinate[0] += kerning_value
                space_area_with_kerning = Polygon(
                    right_side_first + left_side_second[::-1]
                ).area
        return space_area, space_area_with_kerning

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

    def get_coordinates(self, layer, pair_side, top, bottom):
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
            coordinate[0] += sb

        return coordinates


class GUI(object):
    def __init__(self):
        self.w = vanilla.FloatingWindow(
            (200, 300),
            "WhiteSpace Calculator",
            minSize=(200, 300),
            maxSize=(500, 600),
        )
        self.w.TextBox = vanilla.TextBox(
            "auto",
            "Pairs:",
        )
        self.w.textView = vanilla.TextEditor("auto")
        self.w.buttonRun = vanilla.Button(
            "auto", "Run", callback=self.runHandler
        )

        self.w.addAutoPosSizeRules(
            [
                "V:|-[TextBox]-[textView]-[buttonRun]-|",
                "H:|-[TextBox]-|",
                "H:|-[textView]-|",
                "H:|-[buttonRun]-|",
            ]
        )

        self.w.open()

    def runHandler(self, sender):
        space_calc = PairSpaceCalculator()
        print("*" * 22)
        print("PAIR  |  SPACE  | KERNING ")
        for pair in self.w.textView.get().strip().split():
            if not pair:
                continue
            try:
                space_area, space_area_with_kerning = space_calc.compute_space(
                    pair=pair
                )
                print(
                    pair.ljust(8, " "),
                    str(int(space_area)).ljust(8, " "),
                    str(int(space_area_with_kerning)).ljust(8, " "),
                )
            except ValueError as error:
                print(pair, error)
        print("*" * 22)
        Glyphs.showMacroWindow()


if __name__ == "__main__":
    GUI()
