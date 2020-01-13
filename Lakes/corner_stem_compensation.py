# MenuTitle: corner_stem compensation
# -*- coding: utf-8 -*-
# Version: 0.1 (13 Jan, 2020)

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


def main():
    Glyphs.clearLog()
    font = Glyphs.font
    if not verify_params(font):
        return
    masterIndex = font.masterIndex
    obtuse_paths = load_obtuse(font, masterIndex)
    


if __name__ == '__main__':
    main()
