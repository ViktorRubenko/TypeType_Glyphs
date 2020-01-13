# MenuTitle: corner_stem compensation
# -*- coding: utf-8 -*-
# Version: 0.1.1 (13 Jan, 2020)

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
    obtuse_paths = load_obtuse(font, masterIndex)
    for glyph in [glyph for glyph in font.glyphs if glyph.selected]:
        corners_found = 0
        node_indices = []
        layer = glyph.layers[masterIndex]
        for corner_type, corner_path in enumerate(obtuse_paths):
            for pathIndex, path in enumerate(layer.paths):
                for segment in [seg for seg in path.segments if len(seg) == 4]:
                    d_x = corner_path[0].x - segment[0].x
                    d_y = corner_path[0].y - segment[0].y
                    normalize_nodes = [
                        (segment[_].x + d_x, segment[_].y + d_y)
                        for _ in range(4)
                    ]
                    if normalize_nodes == [(n.x, n.y) for n in corner_path]:
                        corners_found += 1
                        mod_node = segment[MODIFIED_INDICES[corner_type]]
                        for nodeIndex, node in enumerate(path.nodes):
                        	if node.position == (mod_node.x, mod_node.y):
                        		compensate_node(font, glyph, pathIndex, nodeIndex, corner_type, node.type)
        print('{}: {} corners found'.format(glyph.name, corners_found))
                            


if __name__ == '__main__':
    main()
