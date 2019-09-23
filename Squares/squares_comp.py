#MenuTitle: Squares compensation
# -*- coding: utf-8 -*-
#Version: 0.1.3 (23 Sep, 2019)


import math
import re
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
	Glyphs.clearLog()
	thisFont = Glyphs.font
	
	if thisFont.customParameters['ItalDelta']:
		delta_up, delta_down = [int(x) for x in re.findall('[0-9]+', thisFont.customParameters['ItalDelta'])]
	else:
		delta = AskString('Enter delta for compensation')
		delta_up, delta_down = int(delta), int(delta)
		if not delta:
			return
	for thisLayer in thisFont.selectedLayers:
		lines = []
		selectedNodes = []
		for path in thisLayer.paths:
			selectedNodes.extend([thisNode for thisNode in path.nodes if
			thisNode.selected])
		if len(selectedNodes) != 4:
			return
		line1 = sorted(selectedNodes[:2], key=lambda n: n.y, reverse=True)
		line2 = sorted(selectedNodes[2:], key=lambda n: n.y, reverse=True)
		thisLayer.beginChanges()
		if line_lenght(*line1) < line_lenght(*line2):
			line1, line2 = line2, line1
			#line1 = external
		if line1[0].y > line2[0].y:
			#external-top
			if line1[0].x > line2[0].x:
				print('external-top-right', delta_down)
				line1[0].x -= delta_down
				line2[0].x += delta_down
				line1[1].y -= delta_down
				line2[1].y += delta_down
			else:
				print('external-top-left', delta_up)
				line1[0].x -= delta_up
				line2[0].x += delta_up
				line1[1].y += delta_up
				line2[1].y -= delta_up
		else:
			#external-bot
			if line1[0].x > line2[0].x:
				print('external-bot-right', delta_up)
				line1[1].x += delta_up
				line2[1].x -= delta_up
				line1[0].y -= delta_up
				line2[0].y += delta_up
			else:
				print('external-bot-left', delta_down)
				line1[1].x += delta_down
				line2[1].x -= delta_down
				line1[0].y += delta_down
				line2[0].y -= delta_down

		thisLayer.endChanges()


if __name__ == '__main__':
	main()
