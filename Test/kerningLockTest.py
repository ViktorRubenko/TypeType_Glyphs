#MenuTitle: KerningLockTest
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals

Glyphs.clearLog()
selection = Font.selection
names = [_.name for _ in Font.selection]

print(names)
for glyph in Font.selection:
    for master in Font.masters:
        masterKerning = Font.kerning[master.id]
        leftKP = []
        rightKP = []
        
        if glyph.rightKerningGroup:
            for rightSide in list(masterKerning[glyph.id].keys()):
                value = masterKerning[glyph.id][rightSide]
                left_group = "@MMK_L_" + glyph.rightKerningGroup
                right = Font.glyphForId_(rightSide)
                if right is None:
                    right = rightSide
                else:
                    right = right.name
                Font.removeKerningForPair(master.id, glyph.name, right)
                leftKP.append((master.id, left_group, right, value))

        if glyph.leftKerningGroup:
            for leftSide in masterKerning.keys():
                value = masterKerning[leftSide].get(glyph.id, None)
                if value is None:
                    continue
                value = masterKerning[leftSide][rightSide]
                right_group = "@MMK_R_" + glyph.leftKerningGroup
                left = Font.glyphForId_(leftSide)
                if left is None:
                    left = leftSide
                else:
                    left = left.name
                Font.removeKerningForPair(master.id, left, glyph.name)
                rightKP.append((master.id, left, right_group, value))
        if leftKP or rightKP:
            print("-" * 10)
            for l in leftKP:
                print(master.name, l[1:])
                Font.setKerningForPair(*l)
            for r in rightKP:
                print(master.name, r[1:])
                Font.setKerningForPair(*r)
            print("-" * 10)
        else:
            print(master.name, "- empty")
