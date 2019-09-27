#MenuTitle: Squares compensation
# -*- coding: utf-8 -*-
#Version: 0.1.3 (27 Sep, 2019)


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
				

def get_delta(thisLayer):
	if thisLayer.master.customParameters['ItalDelta']:
		a,b,c,d,e,f,g,h = [int(x) for x in re.findall('\-{0,1}\d+',
		thisLayer.master.customParameters['ItalDelta'])]
	elif thisLayer.master.font.customParameters['ItalDelta']:
		a,b,c,d,e,f,g,h = [int(x) for x in re.findall('\-{0,1}\d+',
		thisLayer.master.font.customParameters['ItalDelta'])]
	else:
		delta = AskString('Enter delta for compensation')
		a,b,c,d,e,f,g,h = [int(delta) for x in range(8)]
	return a,b,c,d,e,f,g,h


def main():
	Glyphs.clearLog()
	thisFont = Glyphs.font
	
	for thisLayer in thisFont.selectedLayers:
		a,b,c,d,e,f,g,h = get_delta(thisLayer)
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
				print('external-top-right')
				line1[0].x -= g
				line1[1].y -= h
				line2[0].x += e
				line2[1].y += f
			else:
				print('external-top-left')
				line1[0].x -= c
				line1[1].y += d
				line2[0].x += a
				line2[1].y -= b
		else:
			#external-bot
			if line1[0].x > line2[0].x:
				print('external-bot-right')
				line1[1].x += c
				line1[0].y -= d
				line2[1].x -= a
				line2[0].y += b
			else:
				print('external-bot-left')
				line1[1].x += g
				line1[0].y += h
				line2[1].x -= e
				line2[0].y -= f

		thisLayer.endChanges()


if __name__ == '__main__':
	main()
