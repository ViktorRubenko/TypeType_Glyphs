# MenuTitle: corner_OVAL compensation
# -*- coding: utf-8 -*-
# Version: 0.1.3 (16 Jan, 2020)


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
				"_corner.OVAL_in", 
				"_corner.OVAL_out", 
				"_corner.oval_in", 
				"_corner.oval_out",
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


def verify_params(font):
    param_ok = True
    for master in font.masters:
        for param in ("A B C D".split()):
            if param not in master.customParameters:
                print('{}: "{}" is not set'.format(master.name, param))
                param_ok = False
    return param_ok


def load_corner(font, masterIndex, corner_name):
    corner_glyph = font[corner_name]
    path = corner_glyph.layers[masterIndex].paths[0]
    in_fix = 0
    if '_in' in corner_name:
    	path.reverse()
    	in_fix = 3
    paths = {}
    for i in range(4):
        paths[abs(i - in_fix)] = tuple(copy.deepcopy(path.nodes))
        path.applyTransform([0, 1, -1, 0, 0, 0])
    if '_in' in corner_name:
    	path.reverse()
    return paths
    
def compensate_node(font, glyph, pathIndex, nodeIndex, corner_type, node_type, rev_contour):
    for masterIndex, master in enumerate(font.masters):
        if corner_type == 0:
        	if node_type == 0:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["D"].split(',')
        		)
        	else:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["C"].split(',')
        		)
        		if rev_contour:
        			delta = (-delta[0], -delta[1])
        elif corner_type == 1:
        	if node_type == 0:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["B"].split(',')
        		)
        		if rev_contour:
        			delta = (-delta[0], -delta[1])
        	else:
        		delta = tuple(
        			int(_.strip()) for _ in master.customParameters["A"].split(',')
        		)
        elif corner_type == 2:
        	if node_type == 0:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["D"].split(',')
        		)
        	else:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["C"].split(',')
        		)
        		if rev_contour:
        			delta = (-delta[0], -delta[1])
        elif corner_type == 3:
        	if node_type == 0:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["B"].split(',')
        		)
        		if rev_contour:
        			delta = (-delta[0], -delta[1])
        	else:
        		delta = tuple(
        			-int(_.strip()) for _ in master.customParameters["A"].split(',')
        		)
        layer = glyph.layers[masterIndex]
        path = layer.paths[pathIndex]
        node = path.nodes[nodeIndex]
        node.x += delta[0]
        node.y += delta[1]


def run(corner_name):
    Glyphs.clearLog()
    font = Glyphs.font
    if not verify_params(font):
        return
    masterIndex = font.masterIndex
    corner_paths = load_corner(font, masterIndex, corner_name)
    for glyph in [glyph for glyph in font.glyphs if glyph.selected]:
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
                        for node_type in (0, 3):
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
                        				rev_contour = '_in' in corner_name,
                        			)
                        			break
        print('{}: {} corners found'.format(glyph.name, corners_found))
	Glyphs.showMacroWindow()
		
SelectCorner(run)
