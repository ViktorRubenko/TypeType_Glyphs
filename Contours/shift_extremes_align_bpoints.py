# MenuTitle: Shift extremes & align b-points
# -*- coding: utf-8 -*-

__doc__ = """
Shift extremes by a given value and align bezier points.
"""


from vanilla import *
from AppKit import NSScreen


class ShiftWindow:
    def __init__(self):
        self.size = self._size_from_screen()
        self.w = Window(
            self.size,
            "Shift and align",
            maxSize=(1000, 1000),
        )

        self.w.nest1 = self.init_nest("Top/Bottom extremes shift:")
        self.w.nest2 = self.init_nest("Left/Right extremes shift:")

        self.w.run_button = Button(
            "auto",
            "Run",
            callback=self.process,
        )

        self.w.addAutoPosSizeRules(
            [
                "V:|-[nest1]-[nest2]-[run_button]-|",
                "H:|-[nest1]-|",
                "H:|-[nest2]-|",
                "H:|-[run_button]-|",
            ]
        )

        self.w.center()
        self.w.open()

    def init_nest(self, label_text):
        nest = Group("auto")
        nest.label = TextBox(
            "auto",
            label_text,
        )
        nest.entry = EditText(
            "auto",
        )
        nest.addAutoPosSizeRules(
            [
                "H:|-[label(100)]-[entry(>=100)]-|",
                "V:|-[label]-|",
                "V:|-[entry]-|",
            ]
        )
        return nest

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.35), int(size.height * 0.35)

    @staticmethod
    def define_alignment(nodes):
        s, e = nodes[0], nodes[-1]
        width = abs(s.x - e.x)
        height = abs(s.y - e.y)
        return "v" if height > width else "h"

    def align(self, nodes):
        alignment = self.define_alignment(nodes)
        if alignment == "v":
            nodes[0].x, nodes[-1].x = nodes[1].x, nodes[1].x
        else:
            nodes[0].y, nodes[-1].y = nodes[1].y, nodes[1].y

    @staticmethod
    def shift_extremum(nodes, tb_shift, lr_shift):
        if nodes[1].y == nodes[2].y == nodes[3].y:
            # horizontal extremum
            if nodes[0].y > nodes[2].y and nodes[-1].y > nodes[2].y:
                # horizontal bottom
                for i in range(1, 4):
                    nodes[i].x += tb_shift
            elif nodes[0].y < nodes[2].y and nodes[-1].y < nodes[2].y:
                # horizontal top
                for i in range(1, 4):
                    nodes[i].x -= tb_shift
        elif nodes[1].x == nodes[2].x == nodes[3].x:
            # vertical
            if nodes[0].x > nodes[2].x and nodes[-1].x > nodes[2].x:
                # vertical left
                for i in range(1, 4):
                    nodes[i].y -= lr_shift
            elif nodes[0].x < nodes[2].x and nodes[-1].x < nodes[2].x:
                # vertical right
                for i in range(1, 4):
                    nodes[i].y += lr_shift

    def process(self, sender):
        try:
            tb_shift = int(self.w.nest1.entry.get())
            lr_shift = int(self.w.nest2.entry.get())
        except:
            Message(
                "Error",
                "Invalid input",
            )
            return

        font = Glyphs.font
        for glyph in [g for g in font.glyphs if g.selected]:
            layer = glyph.layers[font.selectedFontMaster.id]
            for path in layer.paths:
                nodes = path.nodes
                for i in range(len(nodes)):
                    subnodes = [
                        nodes[i - 1],
                        nodes[i],
                        nodes[(i + 1) % len(nodes)],
                    ]
                    if [n.type for n in subnodes] in (
                        ["offcurve", "curve", "offcurve"],
                        ["offcurve", "curve smooth", "offcurve"],
                    ):
                        self.align(subnodes)
                        extended_subnodes = (
                            [nodes[i - 2]]
                            + subnodes
                            + [nodes[(i + 2) % len(nodes)]]
                        )
                        self.shift_extremum(
                            extended_subnodes,
                            tb_shift,
                            lr_shift,
                        )


ShiftWindow()
