# MenuTitle: test 2
# -*- coding: utf-8 -*-

from __future__ import print_function
import math
from shapely.geometry import Polygon


Glyphs.clearLog()
font = Glyphs.font

# g = font["H"]
# l = g.layers[masterIndex]
# ref_space = (l.LSB + l.RSB) * l.bounds.size.height


def compute_for_pair(pair):
    masterIndex = font.masterIndex

    right_layer = font[pair[0]].layers[masterIndex]
    left_layer = font[pair[1]].layers[masterIndex]

    bottom = int(max(right_layer.bounds.origin.y, left_layer.bounds.origin.y))
    top = int(
        min(
            right_layer.bounds.origin.y + right_layer.bounds.size.height,
            left_layer.bounds.origin.y + left_layer.bounds.size.height,
        )
    )

    right_side_first = get_coordinates(right_layer, "right", top, bottom)
    left_side_second = get_coordinates(left_layer, "left", top, bottom)
    # print(right_side_first)
    # print("-" * 10)
    # print(left_side_second)
    poly = Polygon(right_side_first + left_side_second[::-1])
    return poly.area
    # print(ref_space)


def italicize(x, y, italicAngle, top, side):
    if italicAngle == 0:
        return x
    italicAngle = math.radians(italicAngle)
    tangens = math.tan(italicAngle)
    if side == "right":
        y = top - y
        y = -y
    return x + tangens * y


def get_coordinates(layer, side, top, bottom):
    line_x = (
        layer.bounds.origin.x
        if side == "left"
        else layer.bounds.origin.x + layer.bounds.size.width
    )
    line_y = list(range(bottom, top - 1, 5)) + [top]
    line_coordinates = [
        (y, italicize(line_x, y, layer.master.italicAngle, top, side))
        for y in line_y
    ]
    increment = -1 if side == "right" else 1
    sb = layer.RSB if side == "right" else layer.LSB
    coordinates = []
    for y, x in line_coordinates:
        shift = 0
        while True:
            intersection = layer.intersectionsBetweenPoints(
                (x + shift - 1, y - 1),
                (x + shift + 1, y + 1),
                components=True,
            )
            if len(intersection) > 2:
                coordinates.append([shift, y])
                break
            intersection = layer.intersectionsBetweenPoints(
                (x + shift + 1, y - 1),
                (x + shift - 1, y + 1),
                components=True,
            )
            if len(intersection) > 2:
                coordinates.append([shift, y])
                break
            shift += increment
            if shift > 1000:
                print("ERROR INFINITE WHILE")
                break
    if side == "right":
        sb = -sb

    for coordinate in coordinates:
        coordinate[0] += sb

    return coordinates


if __name__ == "__main__":
    pairs_string = """HH HO AT AV YA УА КО XO LO LV LY Г. Т. 74 \"A \"J K- X- V. Y. K» Т»
Нн Ho Го Гн Fn Fo Ko Кт Ку Xo Fx To Tn Yo Yn Ту Tv Tx Vo Vn Yo Yn Уо Уд Ул Ун
нн но vo го то г. т. ko xo yo"""

    pairs_uni = [
        ("0048", "0048"),
        ("0048", "004f"),
        ("0041", "0054"),
        ("0041", "0056"),
        ("0059", "0041"),
        ("0423", "0410"),
        ("041a", "041e"),
        ("0058", "004f"),
        ("004c", "004f"),
        ("004c", "0056"),
        ("004c", "0059"),
        ("0413", "002e"),
        ("0422", "002e"),
        ("0037", "0034"),
        ("0022", "0041"),
        ("0022", "004a"),
        ("004b", "002d"),
        ("0058", "002d"),
        ("0056", "002e"),
        ("0059", "002e"),
        ("004b", "00bb"),
        ("0422", "00bb"),
        ("041d", "043d"),
        ("0048", "006f"),
        ("0413", "043e"),
        ("0413", "043d"),
        ("0046", "006e"),
        ("0046", "006f"),
        ("004b", "006f"),
        ("041a", "0442"),
        ("041a", "0443"),
        ("0058", "006f"),
        ("0046", "0078"),
        ("0054", "006f"),
        ("0054", "006e"),
        ("0059", "006f"),
        ("0059", "006e"),
        ("0422", "0443"),
        ("0054", "0076"),
        ("0054", "0078"),
        ("0056", "006f"),
        ("0056", "006e"),
        ("0059", "006f"),
        ("0059", "006e"),
        ("0423", "043e"),
        ("0423", "0434"),
        ("0423", "043b"),
        ("0423", "043d"),
        ("043d", "043d"),
        ("043d", "043e"),
        ("0076", "006f"),
        ("0433", "043e"),
        ("0442", "043e"),
        ("0433", "002e"),
        ("0442", "002e"),
        ("006b", "006f"),
        ("0078", "006f"),
        ("0079", "006f"),
    ]

    # pairs = [
    #     tuple(
    #         map(
    #             lambda g: "{:04x}".format(ord(g)),
    #             pair,
    #         )
    #     )
    #     for pair in pairs_string.split()
    # ]

    cmap = {int(g.unicode, 16): g.name for g in font.glyphs if g.unicode}

    pairs = [
        tuple(
            map(
                lambda g: cmap[int(g, 16)],
                pair,
            )
        )
        for pair in pairs_uni
    ]

    pairs_from_string = pairs_string.split()
    for index, pair in enumerate(pairs):
        area = compute_for_pair(pair)
        print(pairs_from_string[index], area)
    Glyphs.showMacroWindow()
