#MenuTitle: KerningLockTest
# -*- coding: utf-8 -*-

names = [_.name for _ in Font.selection]
print(names)

for master in Font.masters:
    masterKerning = Font.kerning[master.id]
    for leftSide in masterKerning.keys():
        leftSideGlyph = leftSide[7:] if leftSide[0] == "@" else Font.glyphForId_(leftSide).name
        
        if leftSide[0] != "@" and Font.glyphs[leftSideGlyph].rightKerningGroup and leftSideGlyph in names:
            for rightSide in list(masterKerning[leftSide].keys()):
                rightSideGlyph = rightSide[7:] if rightSide[0] == "@" else Font.glyphForId_(rightSide).name
                Font.removeKerningForPair(currentMasterID, leftSide, rightSide)
        else:
            for rightSide in list(masterKerning[leftSide].keys()):
                rightSideGlyph = rightSide[7:] if rightSide[0] == "@" else Font.glyphForId_(rightSide).name
                if rightSide[0]!="@" and Font.glyphs[rightSideGlyph].leftKerningGroup and rightSideGlyph in names:
                    Font.removeKerningForPair(currentMasterID, leftSide, rightSide)
