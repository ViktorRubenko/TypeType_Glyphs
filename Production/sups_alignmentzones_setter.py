# MenuTitle: Sups AlignmentZones Setter
# -*- coding: utf-8 -*-
# Version: 0.0.1 (19 Mar, 2020)

from vanilla import *


def calc_zones(zero, seven):
    size = lambda l: (
        l.bounds.origin.y,
        l.bounds.size.height + l.bounds.origin.y,
    )
    zero_size = size(zero)
    seven_size = size(seven)
    zone_bot = GSAlignmentZone(
        seven_size[0],
        seven_size[0] - zero_size[0] - 1
        if seven_size[0] != zero_size[0]
        else -1,
    )
    zone_top = GSAlignmentZone(
        seven_size[1],
        zero_size[1] - seven_size[1] + 1
        if seven_size[1] != zero_size[1]
        else 1,
    )
    return zone_top, zone_bot


Glyphs.clearLog()
font = Glyphs.font
cmap = {glyph.unicode: glyph for glyph in font.glyphs}
seven = cmap["2077"]
zero = cmap["2070"]
added, rewrited = 0, 0
for master in font.masters:
    zone_top, zone_bot = calc_zones(
        zero.layers[master.id], seven.layers[master.id]
    )
    del_zones_indexis = [
        k
        for k, zone in enumerate(master.alignmentZones)
        if zone.position in (zone_top.position, zone_bot.position)
    ]
    rewrited += len(del_zones_indexis)
    added += 2 - len(del_zones_indexis)
    for del_i in del_zones_indexis[::-1]:
        del master.alignmentZones[del_i]
    master.alignmentZones.extend([zone_top, zone_bot])
    master.sortAlignmentZones()

Message(
    "{} zones added\n{} zones rewrited".format(added, rewrited),
    title="Sups AlignmentZones Setter",
)
