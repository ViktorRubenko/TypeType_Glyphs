# MenuTitle: corner sharp_hand compensation
# -*- coding: utf-8 -*-
# Version: 0.1.3 (13 Jan, 2020)

from collections import defaultdict
import copy

# Index for corner orientation type after Transformation
# 0 - bot-left
# 1 - bot_right
# 2 - top_right
# 3 - top_left

MODIFIED_INDICES = {
    0: 3,
    1: 0,
    2: 3,
    3: 0,
}


def verify_params(font):
    param_ok = True
    for master in font.masters:
        for param in ("corner_top_move", "corner_bottom_move"):
            if param not in master.customParameters:
                print('{}: "{}" is not set'.format(master.name, param))
                param_ok = False
    return param_ok


def load_obtuse(font, masterIndex):
    corner_glyph = font["_corner.stem"]
    path = corner_glyph.layers[masterIndex].paths[0]
    paths = []
    for i in range(4):
        paths.append(copy.deepcopy(path.nodes))
        path.applyTransform([0, 1, -1, 0, 0, 0])
    return paths


def compensate_node(font, glyph, pathIndex, nodeIndex, corner_type, node_type):
    for masterIndex, master in enumerate(font.masters):
        if corner_type in (0, 1):
            delta = master.customParameters["corner_bottom_move"]
        else:
            delta = master.customParameters["corner_top_move"]
	try:
        	layer = glyph.layers[masterIndex]
        	path = layer.paths[pathIndex]
        	path.nodes[nodeIndex].x += int(delta)
        except:
        	print('{}: uncompatible outlines'.format(master.name))
        	Glyphs.showMacroWindow()


def main():
    Glyphs.clearLog()
    font = Glyphs.font
    if not verify_params(font):
        return
    masterIndex = font.masterIndex
    currTab = font.currentTab
    glyph_name = currTab.text[currTab.textCursor]
    glyph = font[Glyphs.niceGlyphName(glyph_name)]
    corners_found = 0
    node_indices = []
    layer = glyph.layers[masterIndex]
    for pathIndex, path in enumerate(layer.paths):
        selected_nodes = [node for node in path.nodes if node.selected]
        if selected_nodes:
            if len(selected_nodes) < 4:
                raise ValueError("at least 4 nodes must be selected")
            for i in range(len(selected_nodes) - 3):
                types = [selected_nodes[i + j].type for j in range(4)]
                if types == ["line", "offcurve", "offcurve", "curve"]:
                    corners_found += 1
                    corner_type = 0
                    if selected_nodes[i].x > selected_nodes[i + 3].x:
                        corner_type += 2
                        if selected_nodes[i].y > selected_nodes[i + 3].y:
                            corner_type += 1
                    elif selected_nodes[i].y < selected_nodes[i + 3].y:
                        corner_type += 1
                    mod_node = selected_nodes[
                        i + MODIFIED_INDICES[corner_type]
                    ]
                    compensate_node(
                        font, glyph, pathIndex, mod_node.index,
                        corner_type, node.type
                    )
    print("{}: {} corners found".format(glyph.name, corners_found))


if __name__ == "__main__":
    main()
