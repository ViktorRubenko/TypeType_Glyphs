#MenuTitle: Squares compensation
# -*- coding: utf-8 -*-
#Version: 0.1 (23 Sep, 2019)


import math
from robofab.interface.all.dialogs import AskString

def find_origin(nodes):
	origin = nodes[0]
	for node in nodes[1:]:
		if node.y > origin.y:
			origin = node
		if node.y == origin.y and node.x < origin.x:
			origin = node
	return origin

	
def line_lenght(fnode, snode):
	return math.sqrt((fnode.x - snode.x)**2 + (fnode.y - snode.y)**2)
				

def main():
	delta = AskString('Enter delta for compensation')
	if not delta:
		return
	delta = int(delta)
	Glyphs.clearLog()
	thisFont = Glyphs.font
	for thisLayer in thisFont.selectedLayers:
		lines = []
		selectedNodes = []
		for path in thisLayer.paths:
			selectedNodes.extend([thisNode for thisNode in path.nodes if
			thisNode.selected])
		line1 = sorted(selectedNodes[:2], key=lambda n: n.y, reverse=True)
		line2 = sorted(selectedNodes[2:], key=lambda n: n.y, reverse=True)
		thisLayer.beginChanges()
		if line_lenght(*line1) > line_lenght(*line2):
			#line1 = external
			if line1[0].y > line2[0].y:
				#external-top
				print('external-top')
				line1[0].x += delta
				line2[0].x += delta
				line1[1].y += delta
				line2[1].y += delta
			else:
				#external-bot
				print('external-bot')
				line1[1].x += delta
				line2[1].x += delta
				line1[0].y += delta
				line2[0].y += delta

		else:
			#line1 = internal
			if line2[0].y > line1[0].y:
				#internal-top
				print('external-top')
				line1[0].x += delta
				line2[0].x += delta
				line1[1].y += delta
				line2[1].y += delta
			else:
				#internal-bot
				print('external-bot')
				line1[1].x += delta
				line2[1].x += delta
				line1[0].y += delta
				line2[0].y += delta
		thisLayer.endChanges()

if __name__ == '__main__':
	main()
