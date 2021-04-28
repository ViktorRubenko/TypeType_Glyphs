# MenuTitle: Show glyphs with different formula logic
# -*- coding: utf-8 -*-
# Version: 0.1.4 (23 Mar, 2020)
__doc__ = """
Outputs a list of glyphs where the formula logic differs between the masters
"""


import re


def get_key(pattern, f_key):
    try:
        return re.findall(pattern, f_key)[0]
    except IndexError:
        return ""


def add_to_log(font, thisGlyph, log, attrib):
    keys = {
        "leftMetricsKey": "Left Sidebearing",
        "rightMetricsKey": "Right Sidebearing",
        "widthMetricsKey": "Width",
    }
    for thisMaster in font.masters:
    	thisLayer = thisGlyph.layers[thisMaster.id]
        attrib_log = log.setdefault(keys[attrib], {})
        glyph_log = attrib_log.setdefault(thisGlyph.name, [])
        glyph_log.append(
            "{}: {}".format(
                thisLayer.name.encode("utf-8").strip(),
                thisLayer.__getattribute__(attrib),
            )
        )


def print_log(log):
    for param_name, glyph_data in log.items():
        print("{}\n".format(param_name))
        for glyph_name, glyph_layers in glyph_data.items():
            print(glyph_name)
            for layer in glyph_layers:
                print("\t{}".format(layer))
        print("\n")


Glyphs.clearLog()
font = Glyphs.font
len_tabs = len(font.tabs)
log = {}
for thisGlyph in font.glyphs:
    # newTab = True
    passed = False
    for attrib in ["leftMetricsKey", "rightMetricsKey", "widthMetricsKey"]:
        if sum(
            0 if not thisGlyph.layers[thisMaster.id].__getattribute__(attrib) else 1
            for thisMaster in font.masters
        ) != len(font.masters):
            for thisMaster in font.masters:
            	thisLayer = thisGlyph.layers[thisMaster.id]
                if thisLayer.__getattribute__(attrib):
                    add_to_log(font, thisGlyph, log, attrib)
                    passed = True
                    break
            if passed:
                break
        if passed:
            break

        glyph_key = thisGlyph.__getattribute__(attrib)
        if glyph_key:
            main_basis = get_key(r"={0,2}([A-z\|\.]+)", glyph_key)
            for thisMaster in font.masters:
            	thisLayer = thisGlyph.layers[thisMaster.id]
                layer_key = thisLayer.__getattribute__(attrib)
                if not layer_key:
                    continue
                layer_basis = get_key(r"={0,2}([A-z\|\.]+)", layer_key)
                if layer_basis != main_basis:
                    add_to_log(font, thisGlyph, log, attrib)
                    break
                    """
					if newTab:
						font.newTab()
						newTab = False
					font.tabs[-1].layers.append(thisLayer)
					"""
        else:
            main_basis = None
            basisIndex = None
            for thisMaster in font.masters:
            	thisLayer = thisGlyph.layers[thisMaster.id]
                if thisLayer.__getattribute__(attrib):
                    if not main_basis:
                        main_basis = get_key(
                            r"={0,2}([A-z\|\.]+)",
                            thisLayer.__getattribute__(attrib),
                        )
                        continue
                    layer_key = thisLayer.__getattribute__(attrib)
                    layer_basis = get_key(r"={0,2}([A-z\|\.]+)", layer_key)
                    if layer_basis != main_basis:
                        add_to_log(font, thisGlyph, log, attrib)
                        break
                        """
						if newTab:
							font.newTab()
							newTab = False
						font.tabs[-1].layers.append(thisLayer)
						"""
if log:
    Glyphs.showMacroWindow()
    print_log(log)
else:
    Message("There are no formulas with the wrong logic")
