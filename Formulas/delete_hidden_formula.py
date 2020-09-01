# MenuTitle: Delete hidden formula
# -*- coding: utf-8 -*-
# Version: 0.0.3 (1 Sep, 2020)


def main():
    log = []
    attribs = {
        "leftMetricsKey": "LeftSidebearing",
        "rightMetricsKey": "RightSidebearing",
        "widthMetricsKey": "Width",
    }
    Glyphs.clearLog()
    font = Glyphs.font

    font.disableUpdateInterface()

    for thisGlyph in font.glyphs:
        for attrib in ("leftMetricsKey", "rightMetricsKey", "widthMetricsKey"):
            if not thisGlyph.__getattribute__(attrib):
                continue
            if sum(
                0 if not thisLayer.__getattribute__(attrib) else 1
                for thisLayer in thisGlyph.layers
            ) == len(thisGlyph.layers):
                log.append(
                    "{}: {} {}".format(
                        thisGlyph.name,
                        attribs[attrib],
                        thisGlyph.__getattribute__(attrib),
                    )
                )
                thisGlyph.__setattr__(attrib, None)
        for thisLayer in thisGlyph.layers:
            if (
                all(
                    component.automaticAlignment
                    for component in layer.components
                )
                and not thisLayer.paths
            ):
                for attrib in (
                    "leftMetricsKey",
                    "rightMetricsKey",
                    "widthMetricsKey",
                ):
                    if thisGlyph.__getattribute__(attrib):
                        log.append(
                            "{}: {} {}".format(
                                thisGlyph.name,
                                attribs[attrib],
                                thisGlyph.__getattribute__(attrib),
                            )
                        )
                        thisGlyph.__setattr__(attrib, None)
                    if thisLayer.__getattribute__(attrib):
                        log.append(
                            "{}/{}: {} {}".format(
                                thisGlyph.name,
                                thisLayer.name,
                                attribs[attrib],
                                thisLayer.__getattribute__(attrib),
                            )
                        )
                        thisLayer.__setattr__(attrib, None)

    print("Deleted formulas:")
    if log:
        print("\n".join(log))
    else:
        print("Not found")

    font.enableUpdateInterface()
    Glyphs.showMacroWindow()


if __name__ == "__main__":
    main()
