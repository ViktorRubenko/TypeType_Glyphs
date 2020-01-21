# MenuTitle: corner compensation
# -*- coding: utf-8 -*-
# Version: 0.1.9.1 (20 Jan, 2020)


import vanilla
from collections import defaultdict
import copy


class SelectCorner:
	def __init__(self, run_func):
		self.run_func = run_func
		self.w = vanilla.Window((250, 80))
		
		self.w.comboBox = vanilla.ComboBox(
			(10,10, -10, 21),
			[
                                glyph.name for glyph in Glyphs.font.glyphs
                                 if glyph.name.startswith('_corner')
			],
		)
	
		self.w.button = vanilla.Button(
			(10, 25, 50, 50),
			"Run",
			callback=self.Run
			)
	
		self.w.open()
	
	def Run(self, sender):
		self.run_func(self.w.comboBox.get())
			
# Index for corner orientation type after Transformation
# 0 - bot-left
# 1 - bot_right
# 2 - top_right
# 3 - top_left


def verify_params(font, corner_name):
    param_ok = True
    for master in font.masters:
        for letter in ("A AA B BB C CC D DD".split()):
            param = '{}_{}'.format(letter, corner_name)
            if param not in master.customParameters:
                print('{}: "{}" is not set'.format(master.name, param))
                param_ok = False
    return param_ok


def load_corner(font, masterIndex, corner_name):
    corner_glyph = font[corner_name]
    path = corner_glyph.layers[masterIndex].paths[0]
    paths = {}
    for i in range(4):
        paths[i] = tuple(copy.deepcopy(path.nodes))
        path.applyTransform([0, 1, -1, 0, 0, 0])
    path.reverse()
    for i in range(4,8):
        paths[i] = tuple(copy.deepcopy(path.nodes))
        path.applyTransform([0, 1, -1, 0, 0, 0])
    path.reverse()
    return paths
    
def compensate_node(font, glyph, pathIndex, nodeIndex, corner_type, node_type, corner_name):
    for masterIndex, master in enumerate(font.masters):
        if corner_type == 0:
        	if node_type == 0:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["D_" + corner_name].split(',')
        		)
        	elif node_type == 3:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["C_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["DD_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["CC_" + corner_name].split(',')
        		)
        elif corner_type == 1:
        	if node_type == 0:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["B_" + corner_name].split(',')
        		)
        	elif node_type == 3:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["A_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["BB_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["AA_" + corner_name].split(',')
        		)

        elif corner_type == 2:
        	if node_type == 0:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["D_" + corner_name].split(',')
        		)
        	elif node_type == 3:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["C_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["DD_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["CC_" + corner_name].split(',')
        		)
        elif corner_type == 3:
        	if node_type == 0:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["B_" + corner_name].split(',')
        		)
        	elif node_type == 3:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["A_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["BB_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["AA_" + corner_name].split(',')
        		)
        if corner_type == 4:
        	if node_type == 3:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["D_" + corner_name].split(',')
        		)
        	elif node_type == 0:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["C_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["DD_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["CC_" + corner_name].split(',')
        		)
        elif corner_type == 5:
        	if node_type == 3:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["B_" + corner_name].split(',')
        		)
        	elif node_type == 0:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["A_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["BB_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["AA_" + corner_name].split(',')
        		)

        elif corner_type == 6:
        	if node_type == 3:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["D_" + corner_name].split(',')
        		)
        	elif node_type == 0:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["C_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["DD_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["CC_" + corner_name].split(',')
        		)

        elif corner_type == 7:
        	if node_type == 3:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["B_" + corner_name].split(',')
        		)
        	elif node_type == 0:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["A_" + corner_name].split(',')
        		)
        	elif node_type == 2:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["BB_" + corner_name].split(',')
        		)
        	elif node_type == 1:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["AA_" + corner_name].split(',')
        		)


        layer = glyph.layers[masterIndex]
        path = layer.paths[pathIndex]
        node = path.nodes[nodeIndex]
        node.x += delta[0]
        node.y += delta[1]


def run(corner_name):
    Glyphs.clearLog()
    font = Glyphs.font
    if not verify_params(font, corner_name.split('.')[-1]):
    	Glyphs.showMacroWindow()
        return
    masterIndex = font.masterIndex
    corner_paths = load_corner(font, masterIndex, corner_name)
    for glyph in [glyph for glyph in font.glyphs if glyph.selected]:
        if glyph.name == corner_name:
        	print('{} passed'.format(glyph.name))
        	continue
        corners_found = 0
        node_indices = []
        layer = glyph.layers[masterIndex]
        for corner_type, corner_path in corner_paths.items():
            for pathIndex, path in enumerate(layer.paths):
                for segment in [seg for seg in path.segments if len(seg) == 4]:
                    d_x = corner_path[0].x - segment[0].x
                    d_y = corner_path[0].y - segment[0].y
                    normalize_nodes = [
                        (segment[_].x + d_x, segment[_].y + d_y)
                        for _ in range(4)
                    ]
                    if normalize_nodes == [(n.x, n.y) for n in corner_path]:
                        corners_found += 1
                        for node_type in range(4):
                        	mod_node = segment[node_type]
                        	for nodeIndex, node in enumerate(path.nodes):
                        		if node.position == (mod_node.x, mod_node.y):
                        			compensate_node(
                        				font, 
                        				glyph, 
                        				pathIndex, 
                        				nodeIndex, 
                        				corner_type, 
                        				node_type,
                        				corner_name.split('.')[-1]
                        			)
                        			break
        if corners_found:
        	print('{}: {} corners found'.format(glyph.name, corners_found))
	Glyphs.showMacroWindow()
		
SelectCorner(run)
