# MenuTitle: Compare selected Y values for roman-italic pair layers
# -*- coding: utf-8 -*-

__doc__ = """
Compare selected nodes Y value between roman/italic compatible pair layers.
"""


def main():
    Glyphs.clearLog()
    font = Glyphs.font
    current_tab = font.currentTab
    pathNode_indexes = []
    if current_tab:
        if font.selectedLayers and len(font.selectedLayers) == 1:
            layer = font.selectedLayers[0]
            currentCS = layer.compareString()
            compatible_layers = [
                l
                for l in layer.parent.layers
                if (l.isMasterLayer or l.isSpecialLayer)
                and (l.compareString() == currentCS)
            ]
            roman_italic = {}
            for l in compatible_layers:
                roman_italic.setdefault(l.master.weightValue, []).append(l)

            for item in layer.selection:
                if type(item) == GSNode:
                    pathNode_indexes.append(layer.indexPathOfNode_(item))

            for weight, pair in roman_italic.items():
                if len(pair) != 2:
                    print("Invalid weight {} pair: {},".format(weight, pair))
                    continue
                roman, italic = sorted(pair, key=lambda l: l.italicAngle())
                italic.annotations = []
                roman.annotations = []
                for pathNode_index in pathNode_indexes:
                    path_index, node_index = (
                        pathNode_index[0],
                        pathNode_index[1],
                    )
                    roman_node = roman.paths[path_index].nodes[node_index]
                    italic_node = italic.paths[path_index].nodes[node_index]
                    if roman_node.y != italic_node.y:
                        print(
                            "Node {}, Y: {}( {} )/{}( {} )".format(
                                node_index,
                                roman.name,
                                roman_node.y,
                                italic.name,
                                italic_node.y,
                            )
                        )
                        for layer, node in [
                            (roman, roman_node),
                            (italic, italic_node),
                        ]:
                            annotation = GSAnnotation()
                            annotation.type = CIRCLE
                            annotation.width = 10
                            annotation.position = node.position
                            layer.annotations.append(annotation)

    Glyphs.showMacroWindow()


if __name__ == "__main__":
    main()
