# MenuTitle: Fix Serif
# -*- coding: utf-8 -*-
# Version: 0.1 (09 Apr, 2020)


import vanilla


FONT = Glyphs.font
SERIF_GLYPHS = {
    glyph.name: glyph for glyph in FONT.glyphs if "serif" in glyph.name
}


class OptionsWindow:
    def __init__(self):
        self.window = vanilla.FloatingWindow((200, 120), title="Fix Serif")
        self.window.label = vanilla.TextBox((10, 10, -0, 20), "Reference Serif")
        self.window.serifCombo = vanilla.ComboBox(
            (10, 35, -10, 20), list(SERIF_GLYPHS.keys()),
        )
        self.window.runButton = vanilla.Button(
            (10, -50, 40, 30), "Run", callback=self.run,
        )

        self.window.open()

    def run(self, sender):
        serif = SERIF_GLYPHS[self.window.serifCombo.get()]
        fix_serif(serif)


def fix_serif(serif):
    for master in FONT.masters:
        s_layer = serif.layers[master.id].paths[0]
        s_path = [
            (node.x - s_layer.nodes[0].x, node.y - s_layer.nodes[0].y)
            for node in s_layer.nodes
        ]
        for glyph in (glyph for glyph in FONT.glyphs if glyph.selected):
            layer = glyph.layers[master.id]
            serifs_found = 0
            for path in layer.paths:
                for k in range(len(path.nodes)):
                    node = path.nodes[k]
                    if node.selected:
                        print(node)
                    temp_nodes = (list(path.nodes) + list(path.nodes))[
                        k : k + 5
                    ]
                    if [node.type for node in temp_nodes] == [
                        "line",
                        "line",
                        "offcurve",
                        "offcurve",
                        "curve",
                    ]:
                        if temp_nodes[1].x == temp_nodes[2].x:
                            continue
                        if temp_nodes[0].y > temp_nodes[-1].y:
                            # print('top left')
                            for k, v in enumerate(temp_nodes):
                                v.x += s_path[k][0] - v.x + temp_nodes[0].x
                                v.y += s_path[k][1] - v.y + temp_nodes[0].y
                        else:
                            # print('bot right')
                            for k, v in enumerate(temp_nodes):
                                v.x += -s_path[k][0] - v.x + temp_nodes[0].x
                                v.y += -s_path[k][1] - v.y + temp_nodes[0].y
                        serifs_found += 1
                    if [node.type for node in temp_nodes] == [
                        "line",
                        "offcurve",
                        "offcurve",
                        "curve",
                        "line",
                    ]:
                        if temp_nodes[-2].x == temp_nodes[-3].x:
                            continue
                        if temp_nodes[0].y > temp_nodes[-1].y:
                            # print('bot left')
                            for k, v in enumerate(temp_nodes[::-1]):
                                v.x += s_path[k][0] - v.x + temp_nodes[-1].x
                                v.y += -s_path[k][1] - v.y + temp_nodes[-1].y
                        else:
                            # print('top right')
                            for k, v in enumerate(temp_nodes[::-1]):
                                v.x += -s_path[k][0] - v.x + temp_nodes[-1].x
                                v.y += s_path[k][1] - v.y + temp_nodes[-1].y
                        serifs_found += 1
            print(
                "{} / {} / {} serifs".format(
                    glyph.name, master.name, serifs_found
                )
            )
    Glyphs.showMacroWindow()


if __name__ == "__main__":
    Glyphs.clearLog()
    OptionsWindow()
