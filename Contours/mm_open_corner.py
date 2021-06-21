# MenuTitle: Multiple-master "open corner" for selected nodes
# -*- coding: utf-8 -*-

__doc__ = """
Open corner for selected nodes in all compatible layers.
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
            if len(compatible_layers) != len(layer.parent.layers):
                Glyphs.showMacroWindow()
                print(
                    "Not all layers are compatible, following layers are passed:\n"
                    + "\n".join(
                        str(l)
                        for l in layer.parent.layers
                        if l not in compatible_layers
                    )
                )
            for item in layer.selection:
                if type(item) == GSNode:
                    pathNode_indexes.append(layer.indexPathOfNode_(item))

            for layer in compatible_layers:
                for pathNode_index in pathNode_indexes:
                    path_index, node_index = (
                        pathNode_index[0],
                        pathNode_index[1],
                    )
                    path = layer.paths[path_index]
                    node = path.nodes[node_index]
                    width = 150.0
                    if layer.master.verticalStems:
                        width = layer.master.verticalStems[0]
                    layer.openCornerAtNode_offset_(node, width)


if __name__ == "__main__":
    main()
