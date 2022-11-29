# MenuTitle: Unicode Filler
# -*- coding: utf-8 -*-
# Version: 0.1.0 (17 Nov, 2022)
___doc___ = """
Fill glyphs by given unicodes
"""

import json
import os

import vanilla


class FillerGUI:
    def __init__(self):
        self.w = vanilla.Window((0, 0), title="Unicode filler")

        self.w.list = vanilla.List(
            "auto", 
            [],
            columnDescriptions=[{"title": "Glyph"}, {"title": "Unicode"}]
        )

        self.w.group = vanilla.Group("auto")
        self.w.group.addButton = vanilla.Button(
            "auto",
            "+",
            callback=self.add_callback
        )
        self.w.group.removeButton = vanilla.Button(
            "auto",
            "-",
            callback=self.remove_callback
        )
        self.w.fillButton = vanilla.Button(
            "auto",
            "Fill",
            callback=self.fill_callback
        )

        self.w.addAutoPosSizeRules(
            [
                "H:|-[list(300)]-[group(100)]-|",
                "H:|-[list]-[fillButton(100)]-|",
                "V:|-[list(450)]-|",
                "V:|[group(100)]-[fillButton]|",
            ],
        )

        self.w.group.addAutoPosSizeRules(
            [
                "V:|-[addButton]-5-[removeButton]|",
                "H:|-[addButton(50)]-|",
                "H:|-[removeButton(50)]-|",
                # "H:|-[fillButton(80)]-|",
            ]
        )

        self.load_default_unicodes()

        self.w.open()

    def add_callback(self, sender):
        self.fw = vanilla.FloatingWindow((0,0), "Add new unicode value")
        self.fw.textEditor = vanilla.TextEditor("auto", "Glyph Unicode (Obreve-cy uniF51A)")
        self.fw.button = vanilla.Button("auto", "Add", callback=self.add_new_values)

        self.fw.addAutoPosSizeRules(
            [
                "H:|-[textEditor(200)]-[button(60)]-|",
                "V:|-[textEditor(450)]-|",
                "V:|-[button]|",
            ],
        )

        self.fw.open()

    def remove_callback(self, sender):
        for i in self.w.list.getSelection()[::-1]:
            del self.w.list[i]

    def add_new_values(self, sender):
        Glyphs.clearLog()
        show_console = False
        for line in self.fw.textEditor.get().splitlines():
            glyph, uni = line.strip().split()
            uni = uni.replace("uni", "")
            if not FillerGUI.is_unicode(uni):
                print("Invalid unicode {0}".format(uni))
                show_console = True
                continue
            self.w.list.append({"Glyph": glyph, "Unicode": uni})
        self.fw.close()
        if show_console:
            Glyphs.showMacroWindow()

    def load_default_unicodes(self):
        with open(os.path.join(os.path.dirname(__file__), "unicodes.json")) as json_input:
            unicodes = json.load(json_input)
            for k, v in sorted(unicodes.items(), key=lambda x: int(x[0].replace("uni", ""), 16)):
                self.w.list.append({"Unicode": k.replace("uni", ""), "Glyph": v})

    def fill_callback(self, sender):
        filler = UnicodeFiller(
            font=Glyphs.font,
            unicodes={raw["Glyph"]: int(raw["Unicode"], 16) for raw in self.w.list.get()},
        )
        filler.fill_unicodes()

    @staticmethod
    def is_unicode(value):
        try:
            int(value, 16)
            return True
        except:
            return False

class UnicodeFiller:
    def __init__(self, font, unicodes):
        self.font = font
        self.unicodes = unicodes

    def fill_unicodes(self):
        Glyphs.clearLog()
        show_console = False
        existed_unicodes = {int(g.unicode, 16): g.name for g in self.font.glyphs if g.unicode is not None}
        for glyph_name, unicode_value in self.unicodes.items():
            if glyph_name not in self.font.glyphs:
                print("{0} doesn't exist".format(glyph_name))
                show_console = True
                continue
            if unicode_value in existed_unicodes:
                print("{0} has already taken by {1}".format("{:04X}".format(unicode_value), existed_unicodes[unicode_value]))
                show_console = True
                continue
            self.font[glyph_name].unicode = "{:04X}".format(unicode_value)
        if show_console:
            Glyphs.showMacroWindow()


if __name__ == '__main__':
    FillerGUI()
