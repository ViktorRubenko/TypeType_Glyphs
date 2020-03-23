# MenuTitle: Formula values unification
# -*- coding: utf-8 -*-
# Version: 0.3.4 (23 Mar, 2020)


import re


def update_metrics(thisGlyph):
    for thisLayer in thisGlyph.layers:
        thisLayer.syncMetrics()


def set_master_formula(thisGlyph, thisMasterIndex, attrib):

    log = []

    attribs = {
        "rightMetricsKey": "RSB",
        "leftMetricsKey": "LSB",
        "widthMetricsKey": "width",
    }

    master_formula = thisGlyph.layers[thisMasterIndex].__getattribute__(attrib)
    glyph_formula = thisGlyph.__getattribute__(attrib)
    if not master_formula:
        if glyph_formula:
            master_formula = glyph_formula
        else:
            return
    master_value = thisGlyph.layers[thisMasterIndex].__getattribute__(
        attribs[attrib]
    )

    try:
        increment = int(re.findall(r"[+-]?\d+", master_formula)[0])
    except IndexError:
        increment = 0

    for thisLayerIndex, thisLayer in enumerate(thisGlyph.layers):

        log.append(
            "\t\t{}: {}({}) => ".format(
                thisLayer.name.encode('utf-8').strip(),
                thisLayer.__getattribute__(attrib),
                thisLayer.__getattribute__(attribs[attrib]),
            )
        )

        if thisLayerIndex == thisMasterIndex:
            log[-1] = log[-1] + "{}({}) REF".format(
                thisLayer.__getattribute__(attrib),
                thisLayer.__getattribute__(attribs[attrib]),
            )
            continue
        oldValue = thisLayer.__getattribute__(attribs[attrib])
        if glyph_formula == master_formula:
            thisLayer.__setattr__(attrib, None)
        else:
            thisLayer.__setattr__(attrib, master_formula)
        thisLayer.syncMetrics()
        newValue = thisLayer.__getattribute__(attribs[attrib])
        delta = oldValue - newValue
        if delta:
            delta = int(increment + delta)
            if delta:
                if delta >= 0:
                    delta = "+" + str(delta)
                else:
                    delta = str(delta)
                if increment:
                    thisLayer.__setattr__(
                        attrib, re.sub(r"[+-]?\d+", delta, master_formula)
                    )
                else:
                    thisLayer.__setattr__(attrib, master_formula + delta)
            else:
                thisLayer.__setattr__(
                    attrib, re.sub(r"[+-]?\d+", "", master_formula)
                )
            update_metrics(thisGlyph)
            tLformula = thisLayer.__getattribute__(attrib)
            if tLformula:
                exception = re.findall(
                    r"==(\d+[+-]\d+)\b", thisLayer.__getattribute__(attrib)
                )
                if exception:
                    thisLayer.__setattr__(
                        attrib, "=={}".format(eval(exception[0]))
                    )
            update_metrics(thisGlyph)
        log[-1] = log[-1] + "{}({})".format(
            thisLayer.__getattribute__(attrib),
            thisLayer.__getattribute__(attribs[attrib]),
        )

    print("\t" + attribs[attrib])
    print("\n".join(log))
    print("\n")


def main():
    Glyphs.clearLog()
    font = Glyphs.font
    thisMasterIndex = font.masterIndex
    for thisGlyph in font.glyphs:
        if not thisGlyph.selected:
            continue
        print("Glyph: " + thisGlyph.name)
        for attrib in ("leftMetricsKey", "rightMetricsKey", "widthMetricsKey"):
            update_metrics(thisGlyph)
            set_master_formula(thisGlyph, thisMasterIndex, attrib)
        print("\n")


if __name__ == "__main__":
    main()
