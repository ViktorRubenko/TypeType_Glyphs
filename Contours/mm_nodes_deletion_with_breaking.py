# MenuTitle: MM deletion of nodes with path breaking
# -*- coding: utf-8 -*-

__doc__ = """
Delete selected nodes in all compatible layers with path breaking.
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
            selection = list(layer.selection)
            for item in [selection[0], selection[-1]]:
                if type(item) == GSNode:
                    pathNode_indexes.append(layer.indexPathOfNode_(item))

            if len(pathNode_indexes) != 2:
                print("invalid segment")
                return

            for layer in compatible_layers:
                nodes = []
                for pathNode_index in pathNode_indexes:
                    path_index, node_index = (
                        pathNode_index[0],
                        pathNode_index[1],
                    )
                    path = layer.paths[path_index]
                    nodes.append(path.nodes[node_index])
                for node in nodes:
                    splited_node = layer.dividePathAtNode_(node)
                    splited_path = splited_node.parent
                layer.removePath_(splited_path)


if __name__ == "__main__":
    main()
