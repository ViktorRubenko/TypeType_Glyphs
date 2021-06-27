# MenuTitle: Compare selected Y values for roman-italic pair layers
# -*- coding: utf-8 -*-

__doc__ = """
Compare selected nodes/anchors Y value between roman/italic compatible pair layers.
"""


def add_circle(layer, position):
    annotation = GSAnnotation()
    annotation.type = CIRCLE
    annotation.width = 10
    annotation.position = position
    layer.annotations.append(annotation)


def main():
    Glyphs.clearLog()
    font = Glyphs.font
    current_tab = font.currentTab
    pathNode_indexes = []
    anchor_names = []
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
            if len(compatible_layers) != len(
                [
                    l
                    for l in layer.parent.layers
                    if (l.isMasterLayer or l.isSpecialLayer)
                ]
            ):
                print("Not all layers are compatible")
            roman_italic = {}
            for l in compatible_layers:
                axis_location = l.master.customParameters["Axis Location"]
                if axis_location:
                    print(
                        l.master,
                        tuple(
                            int(axis["Location"])
                            for axis in axis_location
                            if axis["Axis"].lower()
                            not in [
                                "slant",
                                "italic",
                            ]
                        ),
                    )
                    roman_italic.setdefault(
                        tuple(
                            int(axis["Location"])
                            for axis in axis_location
                            if axis["Axis"].lower()
                            not in [
                                "slant",
                                "italic",
                            ]
                        ),
                        [],
                    ).append(l)
                else:
                    roman_italic.setdefault(
                        (l.master.weightValue, l.master.widthValue), []
                    ).append(l)

            for item in layer.selection:
                if type(item) == GSNode:
                    pathNode_indexes.append(layer.indexPathOfNode_(item))
                elif type(item) == GSAnchor:
                    anchor_names.append(item.name)
            for weight, pair in roman_italic.items():
                if len(pair) != 2:
                    print(
                        "Invalid weight/width {} pair: {},".format(
                            weight, pair
                        )
                    )
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
                            add_circle(layer, node.position)
                for anchor_name in anchor_names:
                    roman_anchor = roman.anchorForName_(anchor_name)
                    italic_anchor = italic.anchorForName_(anchor_name)
                    if roman_anchor.y != italic_anchor.y:
                        print(
                            "Anchor '{}', Y: {} ( {} )/{} ( {} )".format(
                                anchor_name,
                                roman.name,
                                roman_anchor.y,
                                italic.name,
                                italic_anchor.y,
                            )
                        )
                        for layer, anchor in [
                            (roman, roman_anchor),
                            (italic, italic_anchor),
                        ]:
                            add_circle(layer, anchor.position)

    Glyphs.showMacroWindow()


if __name__ == "__main__":
    main()
