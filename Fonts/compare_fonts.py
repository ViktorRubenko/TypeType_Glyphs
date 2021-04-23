# MenuTitle: Compare Fonts
# -*- coding: utf-8 -*-


from vanilla import *
from AppKit import NSScreen
import os
from collections import Counter


class CompareWindow():
    def __init__(self):
        self.fonts = Glyphs.fonts
        self.font_names = [os.path.basename(font.filepath) if font.filepath else font.familyName for font in Glyphs.fonts]
        self.size = self._size_from_screen()
        self.w = Window(self.size, "Compare Fonts")
        
        self.w.selection_group = Group((0, 0, -0, 55))
        self.w.selection_group.font1 = PopUpButton(
            (10, 5, int(self.size[0] * 0.48), 21),
            self.font_names,
            callback=self.set_masters_one
        )
        self.w.selection_group.font1_masters = PopUpButton(
            (10, 31, int(self.size[0] * 0.48), 21),
            [],
            callback=self.find_difference,
        )
        self.w.selection_group.font2 = PopUpButton(
            (-10-int(self.size[0] * 0.48), 5, -10, 21),
            self.font_names,
            callback=self.set_masters_two
        )
        self.w.selection_group.font2_masters = PopUpButton(
            (-10-int(self.size[0] * 0.48), 31, -10, 21),
            [],
            callback=None,
        )

        self.w.selection_group.font1.set(0)
        self.w.selection_group.font1.set(1)

        self.set_masters_one(self.w.selection_group.font1)
        self.set_masters_two(self.w.selection_group.font2)


        self.w.result_sheet = List(
            (0, 60, -0, -50),
            [],
            columnDescriptions=[
                {"title": "Glyph"},
                {"title": "Path"},
                {"title": "Components"},
                {"title": "Anchors"},
                {"title": "SB"},
            ],
        )


        self.w.center()
        self.w.open()


    def set_masters_one(self, sender):
        font = self.fonts[sender.get()]
        self.w.selection_group.font1_masters.setItems(
            [i.name for i in font.masters]
        )

    def set_masters_two(self, sender):
        font = self.fonts[sender.get()]
        self.w.selection_group.font2_masters.setItems(
            [i.name for i in font.masters]
        )

    def find_difference(self, sender):
        rows = []

        font1 = self.fonts[self.w.selection_group.font1.get()]
        master1_id = font1.masters[self.w.selection_group.font1_masters.get()].id

        font2 = self.fonts[self.w.selection_group.font2.get()]
        master2_id = font2.masters[self.w.selection_group.font2_masters.get()].id

        g2_names = [g.name for g in font2.glyphs]
        for glyph1 in font1.glyphs:
            if glyph1.name in g2_names:
                result = self.compare_glyphs(
                            glyph1.layers[master1_id],
                            font2[glyph1.name].layers[master2_id],
                        )
                if any(result):
                    rows.append({
                        "Glyph": str(glyph1.name),
                        "Path": ",".join(result[0]),
                        "Components": ",".join(result[1]),
                        "Anchors": ",".join(result[2]),
                        "SB": ",".join(result[3]),
                    })
            else:
                print("ERROR", glyph1.name)
        self.w.result_sheet.set(rows)
        
    def compare_glyphs(self, g1_layer, g2_layer):
        cmp_result = []
        path_result = []
        anch_result = []
        sb_result = []

        points1 = [n.type for p in g1_layer.paths for n in p.nodes]
        points2 = [n.type for p in g2_layer.paths for n in p.nodes]
        components1 = [c.name for c in g1_layer.components]
        components2 = [c.name for c in g2_layer.components]
        anchors1 = [a.position for a in g1_layer.anchors]
        anchors2 = [a.position for a in g2_layer.anchors]
        formulas1 = [
            g1_layer.leftMetricsKey, g1_layer.rightMetricsKey, g1_layer.widthMetricsKey,
            g1_layer.parent.leftMetricsKey, g1_layer.parent.rightMetricsKey, g1_layer.parent.widthMetricsKey,
        ]
        formulas2 = [
            g2_layer.leftMetricsKey, g2_layer.rightMetricsKey, g2_layer.widthMetricsKey,
            g2_layer.parent.leftMetricsKey, g2_layer.parent.rightMetricsKey, g2_layer.parent.widthMetricsKey,
        ]
        sb_values1 = [
            g1_layer.LSB, g1_layer.RSB, g1_layer.width,
        ]
        sb_values2 = [
            g2_layer.LSB, g2_layer.RSB, g2_layer.width,
        ]

        if len(components1) != len(components2):
            cmp_result.append("Amount")
        else:
            if Counter(components1) == Counter(components2):
                if components1 != components2:
                    cmp_result.append("Order")
                else:
                    if [c.transform for c in g1_layer.components] != [c.transform for c in g2_layer.components]:
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
                anch_result.append("Position")

        if formulas1 != formulas2:
            sb_result.append("Formulas")
        if sb_values1 != sb_values2:
            sb_result.append("Values")

        return path_result, cmp_result, anch_result, sb_result


    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.8), int(size.height * 0.8)
        
CompareWindow()