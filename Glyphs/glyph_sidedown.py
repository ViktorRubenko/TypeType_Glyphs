# MenuTitle: Glyph SideDown
# -*- coding: utf-8 -*-
# Version: 0.2 (13 Feb, 2020)

from __future__ import division
import vanilla


class OptionsWindow:
    def __init__(self, SideDown):
        self.window = vanilla.Window((200, 200))
        h = 20
        self.window.labelTop = vanilla.TextBox((10, 10, -0, h), "Top")
        self.window.textTop = vanilla.EditText((80, 10, -10, h))
        self.window.labelBottom = vanilla.TextBox(
            (10, 10 + h + 5, -0, h), "Bottom"
        )
        self.window.textBottom = vanilla.EditText((80, 10 + h + 5, -10, h))
        self.window.labelLSB = vanilla.TextBox(
            (10, 10 + 2 * (h + 5), -0, h), "Left SB"
        )
        self.window.textLSB = vanilla.EditText((80, 10 + 2 * (h + 5), -10, h))
        self.window.labelRSB = vanilla.TextBox(
            (10, 10 + 3 * (h + 5), -0, h), "Right SB"
        )
        self.window.textRSB = vanilla.EditText((80, 10 + 3 * (h + 5), -10, h))
        self.window.labelSuffix = vanilla.TextBox(
            (10, 10 + 4 * (h + 5), -0, h), "Suffix"
        )
        self.window.textSuffix = vanilla.EditText(
            (80, 10 + 4 * (h + 5), -10, h)
        )

        self.window.replaceButton = vanilla.Button(
            (10, 10 + 6 * (h + 5), 85, h), "Replace", callback=self.replace
        )
        self.window.duplButton = vanilla.Button(
            (105, 10 + 6 * (h + 5), 85, h), "Duplicate", callback=self.duplicate
        )

        self.window.open()

    def replace(self, sender):
        try:
            sd = SideDown(
                glyphs=Glyphs.font.selection,
                suffix=self.window.textSuffix.get(),
                top=int(self.window.textTop.get()),
                bottom=int(self.window.textBottom.get()),
                lsb=int(self.window.textLSB.get()),
                rsb=int(self.window.textRSB.get()),
            )
            sd.execute()
        except ValueError:
            print("Invalid Options")
            Glyphs.showMacroWindow()

    def duplicate(self, sender):
        glyphs = []
        for glyph in Glyphs.font.selection:
            newGlyph = glyph.copy()
            newGlyph.name = "{}.{}".format(
                glyph.name, self.window.textSuffix.get()
            )
            newGlyph.unicode = None
            Glyphs.font.glyphs.append(newGlyph)
            glyphs.append(Glyphs.font.glyphs[-1])
            print(glyphs)
        print(glyphs)
        try:
            sd = SideDown(
                glyphs=glyphs,
                suffix=None,
                top=int(self.window.textTop.get()),
                bottom=int(self.window.textBottom.get()),
                lsb=int(self.window.textLSB.get()),
                rsb=int(self.window.textRSB.get()),
            )
            sd.execute()
        except ValueError:
            print("Invalid Options")
            Glyphs.showMacroWindow()


class SideDown:
    def __init__(self, glyphs, suffix=None, *args, **kwargs):
        self.glyphs = glyphs
        self.suffix = suffix
        self.rect_values = kwargs

    def execute(self):
        for glyph in self.glyphs:
            # remove metrics formulas
            for (
                attr
            ) in "leftMetricsKey rightMetricsKey widthMetricsKey".split():
                setattr(glyph, attr, None)
            # for all layers in glyph:
            # 1. decompose all components
            # 2. remove overlaps
            # 3. remove all anchors
            # 4. add rectangle
            # 5. correct path directions
            for layer in glyph.layers:
                layer.decomposeComponents()
                layer.removeOverlap()
                layer.anchors = []
                self.fix_paths(layer)
                self.add_rect(layer)
                for path in layer.paths[:-1]:
                    path.reverse()
                layer.removeOverlap()
                layer.correctPathDirection()
            if self.suffix:
                glyph.name = "{}.{}".format(glyph.name, self.suffix)

    def add_rect(self, layer):
        top = self.rect_values["top"]
        bottom = self.rect_values["bottom"]
        x_start = layer.bounds[0]
        width = layer.bounds[1].width
        self.rect_values["left"] = left = (
            x_start.x - layer.LSB + self.rect_values["lsb"]
        )
        self.rect_values["right"] = right = (
            x_start.x + width + layer.RSB - self.rect_values["rsb"]
        )
        rect = GSPath()
        for point in (
            (left, bottom),
            (right, bottom),
            (right, top),
            (left, top),
        ):
            newNode = GSNode()
            newNode.type = GSLINE
            newNode.position = point
            rect.nodes.append(newNode)
        rect.closed = True
        layer.paths.append(rect)

    def fix_paths(self, layer):
        sub_rects = {}
        for alignment, factor in zip("top bottom".split(), (1, -1)):
            rect = GSPath()
            for position in (
                (layer.bounds[0].x, self.rect_values[alignment]),
                (
                    layer.bounds[0].x + layer.bounds[1].width,
                    self.rect_values[alignment],
                ),
                (
                    layer.bounds[0].x + layer.bounds[1].width,
                    self.rect_values[alignment] + factor * 5000,
                ),
                (
                    layer.bounds[0].x,
                    self.rect_values[alignment] + factor * 5000,
                ),
            ):
                newNode = GSNode()
                newNode.type = GSLINE
                newNode.position = position
                rect.nodes.append(newNode)
            rect.closed = True
            sub_rects[alignment] = rect
        sub_rects["bottom"].reverse()

        GSPathOperator = objc.lookUpClass("GSPathOperator")
        pathOp = GSPathOperator.alloc().init()
        for alignment, rect_path in sub_rects.items():
            thePaths = layer.paths[:]
            otherPaths = [rect_path]
            pathOp = GSPathOperator.alloc().init()
            pathOp.subtractPaths_from_error_(otherPaths, thePaths, None)
            layer.clear()
            layer.paths.extend(thePaths)


if __name__ == "__main__":
    Glyphs.clearLog()
    OptionsWindow(SideDown)
