# MenuTitle: Formula to Absolute
# -*- coding: utf-8 -*-
# Version: 0.1.3 (07 Oct, 2019)
__doc__ = """
Deletes formulas only in the open master (leaves formulas with one =)
"""


Glyphs.clearLog()
font = Glyphs.font
selectedMasterIdx = font.masterIndex
log = []
attribs = {
    "leftMetricsKey": "LSB",
    "rightMetricsKey": "RSB",
    "widthMetricsKey": "width",
}
for selectedLayer in font.selectedLayers:
    thisGlyph = selectedLayer.parent
    absolute = []
    for attrib in ["leftMetricsKey", "rightMetricsKey", "widthMetricsKey"]:
        process = False
        if sum(
            [
                0 if not layer.__getattribute__(attrib) else 1
                for layer in thisGlyph.layers
            ]
        ) == len(thisGlyph.layers):
            thisGlyph.__setattr__(attrib, None)
            process = True
        if selectedLayer.__getattribute__(
            attrib
        ) and not thisGlyph.__getattribute__(attrib):
            process = True
        if process:
            absolute.append(
                '{}: "{}" => {}'.format(
                    attribs[attrib],
                    selectedLayer.__getattribute__(attrib),
                    selectedLayer.__getattribute__(attribs[attrib]),
                )
            )
            selectedLayer.__setattr__(attrib, None)
            log.append("{}: {}".format(thisGlyph.name, "; ".join(absolute)))
        selectedLayer.syncMetrics()

if log:
    print("\n".join(log))
    Glyphs.showMacroWindow()
else:
    Message("Nothing found")
