# MenuTitle: Delete hidden formula
# -*- coding: utf-8 -*-
# Version: 0.0.3 (1 Sep, 2020)
___doc___ = """
Deletes hidden formulas in font
"""


def main():
    log = []
    attribs = {
        "leftMetricsKey": "LeftSidebearing",
        "rightMetricsKey": "RightSidebearing",
        "widthMetricsKey": "Width",
    }
    Glyphs.clearLog()
    font = Glyphs.font
    glyph_names = [glyph.name for glyph in font.glyphs]

    font.disableUpdateInterface()

    for thisGlyph in font.glyphs:
        # if Glyph has formula and all layers have too, then this Glyphs formul is hidden => delete
        masterLayers = [thisGlyph.layers[master.id] for master in font.masters]
        for attrib in ("leftMetricsKey", "rightMetricsKey", "widthMetricsKey"):
            if not thisGlyph.__getattribute__(attrib):
                continue
            if sum(
                0 if not thisLayer.__getattribute__(attrib) else 1
                for thisLayer in masterLayers
            ) == len(masterLayers):
                log.append(
                    "GLYPH {}: {} {}".format(
                        thisGlyph.name,
                        attribs[attrib],
                        thisGlyph.__getattribute__(attrib).encode("utf-8"),
                    )
                )
                thisGlyph.__setattr__(attrib, None)

        # check composite glyphs with full autoalignment
        for thisLayer in masterLayers:
            if (
                (
                    (
                        all(
                            component.doesAlign()
                            for component in thisLayer.components
                        )
                        or all(
                            component.isAligned() > 0
                            for component in thisLayer.components
                        )
                    )
                )
                and not thisLayer.paths
                and thisLayer.components
            ):
                for attrib in (
                    "leftMetricsKey",
                    "rightMetricsKey",
                    "widthMetricsKey",
                ):
                    attrib_value = thisGlyph.__getattribute__(attrib)
                    if (
                        attrib_value
                        and attrib_value.split("=|")[-1].strip()
                        not in glyph_names
                    ):
                        log.append(
                            "AAligned components, GLYPH {}: {} {}".format(
                                thisGlyph.name,
                                attribs[attrib],
                                thisGlyph.__getattribute__(attrib).encode(
                                    "utf-8"
                                ),
                            )
                        )
                        thisGlyph.__setattr__(attrib, None)
                    if thisLayer.__getattribute__(attrib):
                        log.append(
                            "AAligned components, LAYER {}/{}: {} {}".format(
                                thisGlyph.name,
                                thisLayer.name,
                                attribs[attrib],
                                thisLayer.__getattribute__(attrib).encode(
                                    "utf-8"
                                ),
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
