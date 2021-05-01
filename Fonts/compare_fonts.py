# MenuTitle: Compare Fonts
# -*- coding: utf-8 -*-
__doc__ = """
Compares two fonts: contours, components, anchors, metrics
"""


from vanilla import *
from AppKit import NSScreen
import os
import csv
from collections import Counter


class CompareWindow:
    def __init__(self):
        self.fonts = Glyphs.fonts
        self.font_names = [
            os.path.basename(font.filepath)
            if font.filepath
            else font.familyName
            for font in Glyphs.fonts
        ]
        self.size = self._size_from_screen()
        self.w = Window(self.size, "Compare Fonts")

        self.w.selection_group = Group((0, 0, -0, 55))
        self.w.selection_group.font1 = PopUpButton(
            (10, 5, int(self.size[0] * 0.48), 21),
            self.font_names,
            callback=self.set_masters_one,
        )
        self.w.selection_group.font1_masters = PopUpButton(
            (10, 31, int(self.size[0] * 0.48), 21),
            [],
            callback=self.find_difference,
        )
        self.w.selection_group.font2 = PopUpButton(
            (-10 - int(self.size[0] * 0.48), 5, -10, 21),
            self.font_names,
            callback=self.set_masters_two,
        )
        self.w.selection_group.font2_masters = PopUpButton(
            (-10 - int(self.size[0] * 0.48), 31, -10, 21),
            [],
            callback=self.find_difference,
        )

        self.w.result_sheet = List(
            (0, 60, -0, -50),
            [],
            columnDescriptions=[
                {"title": "Glyph"},
                {"title": "Path"},
                {"title": "Components"},
                {"title": "Anchors"},
                {"title": "Metrics"},
            ],
        )

        self.w.exportButton = Button(
            (int(self.size[0] * 0.45), -40, -int(self.size[0] * 0.45), -15),
            "Export",
            callback=self.export_txt,
        )

        self.w.selection_group.font1.set(0)
        self.w.selection_group.font1.set(1 if len(self.font_names) == 2 else 0)

        self.set_masters_one(self.w.selection_group.font1)
        self.set_masters_two(self.w.selection_group.font2)

        self.w.center()
        self.w.open()

    def export_txt(self, sender):
        export_path = GetSaveFile(
            ProposedFileName="{}_{}".format(
                self.font_names[self.w.selection_group.font1.get()],
                self.font_names[self.w.selection_group.font2.get()],
            ),
            filetypes=["txt"],
        )
        fieldnames = "Glyph Path Components Anchors Metrics".split()
        if export_path:
            max_len = max(
                len(row["Glyph"]) for row in self.w.result_sheet.get()
            )
            with open(export_path, "w") as f:
                for row in self.w.result_sheet.get():
                    for key, value in row.items():
                        if key != "Glyph" and value:
                            f.write(
                                unicode(
                                    "{0:<{3}} | {1:<10} | {2}\n".format(
                                        row["Glyph"],
                                        key,
                                        value,
                                        max_len,
                                    ),
                                    "utf-8",
                                )
                            )
                    # f.write(
                    #     unicode(
                    #         "{0:<20}|{1:^20s}|{2:^20s}|{3:^20s}|{4:^20s}\n".format(
                    #             row["Glyph"],
                    #             row["Path"],
                    #             row["Components"],
                    #             row["Anchors"],
                    #             row["Metrics"],
                    #         ),
                    #         "utf-8",
                    #     )
                    # )
                    # f.write(
                    #     unicode(
                    #         "{0}|{0}|{0}|{0}|{0}\n".format("_" * 20), "utf-8"
                    #     )
                    # )

    def set_masters_one(self, sender):
        font = self.fonts[sender.get()]
        self.w.selection_group.font1_masters.setItems(
            [i.name for i in font.masters]
        )
        self.find_difference(None)

    def set_masters_two(self, sender):
        font = self.fonts[sender.get()]
        self.w.selection_group.font2_masters.setItems(
            [i.name for i in font.masters]
        )
        self.find_difference(None)

    def find_difference(self, sender):
        rows = []

        font1 = self.fonts[self.w.selection_group.font1.get()]
        master1_id = font1.masters[
            self.w.selection_group.font1_masters.get()
        ].id

        font2 = self.fonts[self.w.selection_group.font2.get()]
        master2_id = font2.masters[
            self.w.selection_group.font2_masters.get()
        ].id

        g2_names = [g.name for g in font2.glyphs]
        for glyph1 in font1.glyphs:
            if glyph1.name in g2_names:
                result = self.compare_glyphs(
                    glyph1.layers[master1_id],
                    font2[glyph1.name].layers[master2_id],
                )
                if any(result):
                    rows.append(
                        {
                            "Glyph": str(glyph1.name),
                            "Path": ", ".join(result[0]),
                            "Components": ", ".join(result[1]),
                            "Anchors": ", ".join(result[2]),
                            "Metrics": ", ".join(result[3]),
                        }
                    )
            else:
                print("ERROR", glyph1.name)
        self.w.result_sheet.set(rows)

    def compare_glyphs(self, g1_layer, g2_layer):
        cmp_result = []
        path_result = []
        anch_result = []
        metrics_result = []

        points1 = [n.type for p in g1_layer.paths for n in p.nodes]
        points2 = [n.type for p in g2_layer.paths for n in p.nodes]
        components1 = [c.name for c in g1_layer.components]
        components2 = [c.name for c in g2_layer.components]
        anchors1 = [a.position for a in g1_layer.anchors]
        anchors2 = [a.position for a in g2_layer.anchors]
        formulas1 = {
            "LayerLeftMetricsKey": g1_layer.leftMetricsKey,
            "LayerRightMetricsKey": g1_layer.rightMetricsKey,
            "WidthMetricsKey": g1_layer.widthMetricsKey,
            "GlyphLeftMetricsKey": g1_layer.parent.leftMetricsKey,
            "GlyphRightMetricsKey": g1_layer.parent.rightMetricsKey,
            "GlyphWidthMetricsKey": g1_layer.parent.widthMetricsKey,
        }
        formulas2 = {
            "LayerLeftMetricsKey": g2_layer.leftMetricsKey,
            "LayerRightMetricsKey": g2_layer.rightMetricsKey,
            "WidthMetricsKey": g2_layer.widthMetricsKey,
            "GlyphLeftMetricsKey": g2_layer.parent.leftMetricsKey,
            "GlyphRightMetricsKey": g2_layer.parent.rightMetricsKey,
            "GlyphWidthMetricsKey": g2_layer.parent.widthMetricsKey,
        }
        metrics_values1 = {
            "LSB": g1_layer.LSB,
            "RSB": g1_layer.RSB,
            "Width": g1_layer.width,
        }
        metrics_values2 = {
            "LSB": g2_layer.LSB,
            "RSB": g2_layer.RSB,
            "Width": g2_layer.width,
        }

        if len(components1) != len(components2):
            cmp_result.append("Amount")
        else:
            if Counter(components1) == Counter(components2):
                if components1 != components2:
                    cmp_result.append("Order")
                else:
                    if [c.transform for c in g1_layer.components] != [
                        c.transform for c in g2_layer.components
                    ]:
                        cmp_result.append("Transform")
            else:
                cmp_result.append("ParentGlyph")

        if len(g1_layer.paths) != len(g2_layer.paths):
            path_result.append("Amount of contours")
        else:
            if len(points1) != len(points2):
                path_result.append("Amount of points")
            elif points1 != points2:
                path_result.append("Points type")
            else:
                path_loop = True
                for p1_index, p1 in enumerate(g1_layer.paths):
                    if not path_loop:
                        break
                    p2 = g2_layer.paths[p1_index]
                    for n1_index, n1 in enumerate(p1.nodes):
                        n2 = p2.nodes[n1_index]
                        if n1.position != n2.position:
                            path_result.append("Node position")
                            path_loop = False
                            break

        if len(anchors1) != len(anchors2):
            anch_result.append("Amount")
        else:
            if anchors1 != anchors2:
                for a1_index, a1 in enumerate(anchors1):
                    a2 = anchors2[a1_index]
                    if a1 != a2:
                        anch_result.append(
                            "Position:({}, {})/({}, {}))".format(
                                a1.x, a1.y, a2.x, a2.y
                            )
                        )

        if formulas1 != formulas2:
            for f1_key, f1 in formulas1.items():
                f2 = formulas2[f1_key]
                if f1 != f2:
                    metrics_result.append(
                        "Formulas: ({}: {} / {})".format(f1_key, f1, f2)
                    )
        if metrics_values1 != metrics_values2:
            for v1_key, v1 in metrics_values1.items():
                v2 = metrics_values2[v1_key]
                if v1 != v2:
                    metrics_result.append(
                        "Values:({}: {} / {})".format(v1_key, v1, v2)
                    )

        return path_result, cmp_result, anch_result, metrics_result

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.8), int(size.height * 0.8)


CompareWindow()