# MenuTitle: Glyph SideDown
# -*- coding: utf-8 -*-
# Version: 0.4.2 (18 Feb, 2020)

from __future__ import division
from collections import namedtuple
import copy
import vanilla

Rect_ = namedtuple("Rect", "top bottom left right".split())


class OptionsWindow:
    def __init__(self, SideDown):
        self.window = vanilla.FloatingWindow((200, 200), title="Glyph SideDown")
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

        self.window.line = vanilla.HorizontalLine(
            (10, 10 + 5 * (h + 5), -10, h)
        )

        self.window.replaceButton = vanilla.Button(
            (10, 10 + 6 * (h + 5), 85, h),
            "Replace",
            callback=lambda sender: self.replace(
                sender, suffix=self.window.textSuffix.get()
            ),
        )
        self.window.duplButton = vanilla.Button(
            (105, 10 + 6 * (h + 5), 85, h), "Duplicate", callback=self.duplicate
        )

        self.spinner_window = vanilla.FloatingWindow((200, 200))
        self.spinner_window.spinner = vanilla.ProgressSpinner(
            (10, 10, -10, -10), displayWhenStopped=True
        )

        self.window.open()
        self.spinner_window.open()
        self.spinner_window.hide()

    def replace(self, sender, suffix=None, glyphs=None):
        self.spinner_window.setPosSize(self.window.getPosSize())
        self.spinner_window.show()
        if not glyphs:
            glyphs = Glyphs.font.selection
        if suffix:
            for glyph in Glyphs.font.selection:
                glyph.name = "{}.{}".format(glyph.name, suffix)
                glyph.unicode = None
        try:
            sd = SideDown(
                glyphs=glyphs,
                top=int(self.window.textTop.get()),
                bottom=int(self.window.textBottom.get()),
                lsb=int(self.window.textLSB.get()),
                rsb=int(self.window.textRSB.get()),
            )
            sd.execute()
        except ValueError:
            Message(message="Invalid options", title="Error")
        finally:
            self.spinner_window.hide()

    def duplicate(self, sender):
        glyphs = []
        for glyph in Glyphs.font.selection:
            new_name = "{}.{}".format(glyph.name, self.window.textSuffix.get())
            if new_name in Glyphs.font.glyphs:
                d_glyph = Glyphs.font.glyphs[new_name]
                d_glyph.layers[Glyphs.font.selectedFontMaster.id] = copy.copy(
                    glyph.layers[Glyphs.font.selectedFontMaster.id]
                )
                glyphs.append(d_glyph)
            else:
                newGlyph = glyph.copy()
                newGlyph.name = new_name
                newGlyph.unicode = None
                Glyphs.font.glyphs.append(newGlyph)
                glyphs.append(Glyphs.font.glyphs[-1])
        self.replace(sender, suffix=None, glyphs=glyphs)


class SideDown:
    def __init__(self, glyphs, *args, **kwargs):
        self.glyphs = glyphs
        self.values = kwargs
        self.rect = None

    def execute(self):
        for glyph in self.glyphs:
            # remove metrics formulas
            for (
                attr
            ) in "leftMetricsKey rightMetricsKey widthMetricsKey".split():
                setattr(glyph, attr, None)
            # for all layers in glyph:
            # 0.5. correct path directions
            # 1. decompose all components
            # 2. remove overlaps
            # 3. remove all anchors
            # 4. add rectangle
            # 5. correct path directions
            layer = glyph.layers[Glyphs.font.selectedFontMaster.id]
            layer.decomposeComponents()
            layer.removeOverlap()
            layer.anchors = []
            layer.correctPathDirection()
            self.calc_rect_edges(layer)
            self.fix_paths(layer)
            self.add_rect(layer)
            for path in layer.paths[:-1]:
                path.reverse()
            layer.removeOverlap()
            layer.correctPathDirection()

    def add_rect(self, layer):
        rect = GSPath()
        for point in (
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom),
            (self.rect.right, self.rect.top),
            (self.rect.left, self.rect.top),
        ):
            newNode = GSNode()
            newNode.type = GSLINE
            newNode.position = point
            rect.nodes.append(newNode)
        rect.closed = True
        layer.paths.append(rect)

    def calc_rect_edges(self, layer):
        x_start = layer.bounds[0].x
        width = layer.bounds[1].width
        left_edge = x_start - layer.LSB + self.values["lsb"]
        right_edge = x_start + width + layer.RSB - self.values["rsb"]
        self.rect = Rect_(
            self.values["top"], self.values["bottom"], left_edge, right_edge
        )

    def fix_paths(self, layer):
        sub_rects = {}
        for alignment, factor in zip("top bottom".split(), (1, -1)):
            rect = GSPath()
            for position in (
                (layer.bounds[0].x, self.rect.__getattribute__(alignment)),
                (
                    layer.bounds[0].x + layer.bounds[1].width,
                    self.rect.__getattribute__(alignment),
                ),
                (
                    layer.bounds[0].x + layer.bounds[1].width,
                    self.rect.__getattribute__(alignment) + factor * 5000,
                ),
                (
                    layer.bounds[0].x,
                    self.rect.__getattribute__(alignment) + factor * 5000,
                ),
            ):
                newNode = GSNode()
                newNode.type = GSLINE
                newNode.position = position
                rect.nodes.append(newNode)
            rect.closed = True
            sub_rects[alignment] = rect

        for alignment, factor in zip("right left".split(), (1, -1)):
            rect = GSPath()
            for position in (
                (self.rect.__getattribute__(alignment), layer.bounds[0].y,),
                (
                    self.rect.__getattribute__(alignment) + factor * 5000,
                    layer.bounds[0].y,
                ),
                (
                    self.rect.__getattribute__(alignment) + factor * 5000,
                    layer.bounds[0].y + layer.bounds[1].height,
                ),
                (
                    self.rect.__getattribute__(alignment),
                    layer.bounds[0].y + layer.bounds[1].height,
                ),
            ):
                newNode = GSNode()
                newNode.type = GSLINE
                newNode.position = position
                rect.nodes.append(newNode)
                rect.closed = True
            sub_rects[alignment] = rect

        sub_rects["bottom"].reverse()
        sub_rects["left"].reverse()

        GSPathOperator = objc.lookUpClass("GSPathOperator")
        pathOp = GSPathOperator.alloc().init()
        for alignment, rect_path in sub_rects.items():
            thePaths = layer.paths[:]
            otherPaths = [rect_path]
            pathOp = GSPathOperator.alloc().init()
            pathOp.subtractPaths_from_error_(otherPaths, thePaths, None)
            layer.clear()
            layer.paths.extend(thePaths)


def test_cutting():
    sd = SideDown(
        glyphs=Glyphs.font.selection, top=600, bottom=10, lsb=100, rsb=100,
    )
    sd.execute()


if __name__ == "__main__":
    Glyphs.clearLog()
    OptionsWindow(SideDown)
    # test_cutting()
