# MenuTitle: Check sidebearing linearity
# -*- coding: utf-8 -*-

__doc__ = "Check =| and == sidebearing values for linearity between layers"


font = Glyphs.font
log = []
for glyph in font.glyphs:
    layers = [l for l in glyph.layers if l.italicAngle() > 0]
    try:
        right_value = [int(l.rightMetricsKey.split("==|")[-1]) for l in layers]
        if right_value != sorted(right_value):
            log.append("{}: {} {}".format(glyph.name, "=|", right_value))
    except (ValueError, AttributeError):
        pass

    try:
        left_value = [int(l.leftMetricsKey.split("==")[-1]) for l in layers]
        if left_value != sorted(left_value)[::-1] or len(
            set(left_value)
        ) != len(left_value):
            log.append("{}: {} {}".format(glyph.name, "==", left_value))
    except (ValueError, AttributeError):
        pass

Glyphs.clearLog()
if log:
    print("\n".join(log))
else:
    print("OK")
Glyphs.showMacroWindow()
