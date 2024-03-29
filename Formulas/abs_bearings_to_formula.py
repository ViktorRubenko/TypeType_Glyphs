# MenuTitle: Absotule bearing values to formula
# -*- coding: utf-8 -*-

__doc__ = """
Sets == for values without any formula in the open master
"""


ATTRS = {
    "leftMetricsKey": "LSB",
    "rightMetricsKey": "RSB",
}
LOG = []


def set_sb_keys(glyph, glayer):
    found = False
    if glayer.widthMetricsKey or glyph.widthMetricsKey:
        return
    for key, value in ATTRS.items():
        if not glayer.__getattribute__(key) and not glyph.__getattribute__(key):
            if glayer.hasAlignedWidth():
                continue
            if not found:
                LOG.append("{}\n".format(glyph.name))
            glayer.__setattr__(
                key, "=={:.0f}".format(glayer.__getattribute__(value))
            )
            glayer.syncMetrics()
            LOG[-1] += "\t{}: {:.0f} => {}\n".format(
                value,
                glayer.__getattribute__(value),
                glayer.__getattribute__(key),
            )


def main():
    Glyphs.clearLog()
    font = Glyphs.font
    thisMasterIndex = font.masterIndex
    print(font.masters[thisMasterIndex].name)
    for thisGlyph in font.glyphs:
        if thisGlyph.selected:
            set_sb_keys(thisGlyph, thisGlyph.layers[thisMasterIndex])
    if LOG:
        message = "\n".join(LOG)
    else:
        message = "Nothing is changed"
    print(message)
    Glyphs.showMacroWindow()


if __name__ == "__main__":
    main()
