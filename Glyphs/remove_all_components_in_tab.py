#MenuTitle: Remove All Components in Tab


font = Glyphs.font

for layer in font.currentTab.layers:
	glyph = layer.parent
	for layer in glyph.layers:
		for component_index, component in enumerate(layer.components):
			print("remove {} ({}): {}".format(glyph.name, layer.name, component.name))
			del layer.components[component_index]
Glyphs.showMacroWindow()
