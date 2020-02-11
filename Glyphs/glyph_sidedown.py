#MenuTitle: Glyph SideDown
# -*- coding: utf-8 -*-
#Version: 0.1 (11 Feb, 2020)

from __future__ import division
import vanilla
from shapely.geometry import LineString


class OptionsWindow:
	def __init__(self, SideDown):
		self.window = vanilla.Window((200, 200))
		h = 20
		self.window.labelTop = vanilla.TextBox((10, 10, -0, h), "Top")
		self.window.textTop = vanilla.EditText((80, 10,- 10, h))
		self.window.labelBottom = vanilla.TextBox((10, 10 + h + 5, -0, h), "Bottom")
		self.window.textBottom = vanilla.EditText((80, 10 + h + 5, -10, h))
		self.window.labelLSB = vanilla.TextBox((10, 10 + 2*(h+5), -0, h), "Left SB")
		self.window.textLSB = vanilla.EditText((80, 10 + 2*(h+5),- 10, h))
		self.window.labelRSB = vanilla.TextBox((10, 10 + 3*(h+5), -0, h), "Right SB")
		self.window.textRSB = vanilla.EditText((80, 10 + 3*(h+5), -10, h))
		self.window.labelSuffix = vanilla.TextBox((10, 10 + 4*(h+5), -0, h), "Suffix")
		self.window.textSuffix = vanilla.EditText((80, 10 + 4*(h+5), -10, h))
		
		self.window.replaceButton = vanilla.Button((10, 10 + 6*(h+5), 85, h), "Replace", callback=self.replace)
		self.window.duplButton = vanilla.Button((105, 10 + 6*(h+5), 85, h), "Duplicate", callback=self.duplicate)
		
		self.window.open()
		
	def replace(self, sender):
		try:
			sd = SideDown(
				glyphs=[glyph for glyph in Glyphs.font.glyphs if glyph.selected], 
				suffix = None,
				top=int(self.window.textTop.get()),
				bottom=int(self.window.textBottom.get()),
				lsb=int(self.window.textLSB.get()),
				rsb=int(self.window.textRSB.get()),
				)
			sd.execute()
		except ValueError:
			print('Invalid Options')
			Glyphs.showMacroWindow()
		
	
	def duplicate(self, sender):
		dupl_names = []
		for glyph in [glyph for glyph in Glyphs.font.glyphs if glyph.selected]:
			newGlyph = glyph.copy()
			newGlyph.name = '{}.{}'.format(glyph.name, self.window.textSuffix.get())
			Glyphs.font.glyphs.append(newGlyph)
			dupl_names.append(newGlyph.name)
		try:
			sd = SideDown(
				glyphs=[Glyphs.font[name] for name in dupl_names], 
				suffix=None,
				top=int(self.window.textTop.get()),
				bottom=int(self.window.textBottom.get()),
				lsb=int(self.window.textLSB.get()),
				rsb=int(self.window.textRSB.get()),
				)
			sd.execute()
		except ValueError:
			print('Invalid Options')
			Glyphs.showMacroWindow()
		
	
	
class SideDown:
	def __init__(self, glyphs, suffix=None, *args, **kwargs):
		self.glyphs = glyphs
		self.suffix = suffix
		self.rect_values = kwargs
		
		
	def execute(self):
		for glyph in self.glyphs:
			# remove metrics formulas
			for attr in 'leftMetricsKey rightMetricsKey widthMetricsKey'.split():
				setattr(glyph, attr, None)
			# for all layers in glyph:
			# 1. decompose all components
			# 2. remove overlaps
			# 3. remove all anchors
			# 4. add rectangle
			# 5.correct path directions
			for layer in glyph.layers[:1]:
				layer.decomposeComponents()
				layer.removeOverlap()
				layer.anchors = []
				self.add_rect(layer)
				self.fix_paths(layer)
				layer.correctPathDirection()
			if self.suffix:
				glyph.name = '{}.{}'.format(glyph.name, self.suffix)
								
	def add_rect(self, layer):
		top = self.rect_values['top']
		bottom = self.rect_values['bottom']
		x_start = layer.bounds[0]
		width = layer.bounds[1].width
		left = x_start.x - layer.LSB + self.rect_values['lsb']
		right = x_start.x + width + layer.RSB + self.rect_values['rsb']
		rect = GSPath()
		for point in ((left, bottom), (right, bottom), (right, top), (left, top)):
			newNode = GSNode()
			newNode.type = GSLINE
			newNode.position = point
			rect.nodes.append(newNode)
				
		rect.closed = True
		layer.paths.append(rect)
		
	def fix_paths(self, layer):
		middle = (self.rect_values['top'] + self.rect_values['bottom']) / 2
		rect = layer.paths[-1]
		rect_line = LineString([(node.x, node.y) for node in rect.nodes])
		for path in layer.paths[:-1]:
			other_line = LineString([(node.x, node.y) for node in path.nodes])
			intersection = rect_line.intersection(other_line)
			if intersection:
				for node in intersection:
					newNode = GSNode()
					newNode.type = GSLINE
					newNode.position = (node.x, node.y)
					path.nodes.append(newNode)
				if sum(node.y for node in intersection)/len(intersection) < middle:
					del_nodes = []
					for node_index, node in enumerate(path.nodes):
						if node.y < intersection[0].y:
							del_nodes.append(node_index)
					for del_index in del_nodes[::-1]:
						del path.nodes[del_index]
				else:
					del_nodes = []
					for node_index, node in enumerate(path.nodes):
						if node.y > intersection[0].y:
							del_nodes.append(node_index)
					for del_index in del_nodes[::-1]:
						del path.nodes[del_index]
					
			

if __name__ == '__main__':
	Glyphs.clearLog()
	OptionsWindow(SideDown)
