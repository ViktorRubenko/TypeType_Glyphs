# MenuTitle: Compare Fonts
# -*- coding: utf-8 -*-


from vanilla import *
from AppKit import NSScreen
import os


class CompareWindow():
    def __init__(self):
        self.fonts = Glyphs.fonts
        self.font_names = [os.path.basename(font.filepath) for font in Glyphs.fonts]
        self.size = self._size_from_screen()
        self.w = Window(self.size, "Compare Fonts")
        
        self.w.selection_group = Group((0, 0, -0, int(self.size[-1] * 0.1)))
        self.w.selection_group.font1 = PopUpButton(
            (10, 5, int(self.size[0] * 0.48), 21),
            self.font_names,
            callback=self.set_instances_one
        )
        self.w.selection_group.font1_instances = PopUpButton(
            (10, 31, int(self.size[0] * 0.48), 21),
            [],
            callback=None,
        )
        self.w.selection_group.font2 = PopUpButton(
            (-10-int(self.size[0] * 0.48), 5, -10, 21),
            self.font_names,
            callback=self.set_instances_two
        )
        self.w.selection_group.font2_instances = PopUpButton(
            (-10-int(self.size[0] * 0.48), 31, -10, 21),
            [],
            callback=None,
        )

        self.w.selection_group.font1.set(0)
        self.w.selection_group.font1.set(1)

        self.set_instances_one(self.w.selection_group.font1)
        self.set_instances_two(self.w.selection_group.font2)

        self.w.center()
        self.w.open()


    def set_instances_one(self, sender):
        font = self.fonts[sender.get()]
        self.w.selection_group.font1_instances.setItems(
            [i.name for i in font.instances]
        )

    def set_instances_two(self, sender):
        font = self.fonts[sender.get()]
        self.w.selection_group.font2_instances.setItems(
            [i.name for i in font.instances]
        )

        
    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.8), int(size.height * 0.8)
        
CompareWindow()