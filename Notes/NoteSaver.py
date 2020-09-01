# MenuTitle: NoteSaver
# -*- coding: utf-8 -*-
# Version: 0.0.1 (1 Sep, 2020)

import os
from io import open
from dateutil.parser import parse
from datetime import datetime
import json


class NoteWriter:
    def __init__(self, font):
        self.font = font
        self.path_txt = os.path.splitext(font.filepath)[0] + ".txt"
        self.path_json = os.path.splitext(font.filepath)[0] + ".json"
        self.notes = {}
        self._load_writed_notes()

    def _load_writed_notes(self):
        with open(self.path_json, "r", encoding="utf-8") as f:
            self.notes = json.load(f)

    def process_notes(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M%:%S")
        for glyph in [glyph for glyph in self.font.glyphs if glyph.note]:
            self.strip_note(glyph)
            if glyph.note:
                self.add_time(glyph, current_time)
            else:
                continue
            self.add_to_notes(glyph)

    def add_time(self, glyph, current_time):
        if not self.is_date(glyph.note.splitlines()[0]):
            glyph.note = current_time + "\n" + glyph.note

    def add_to_notes(self, glyph):
        notes = self.notes.get(glyph.name, [])
        if notes and glyph.note != notes[-1] or not notes:
            notes.append(glyph.note)
            self.notes[glyph.name] = notes

    @staticmethod
    def strip_note(glyph):
        if glyph.note.isspace():
            glyph.note = ""

    @staticmethod
    def is_date(line):
        if not line:
            return False
        try:
            parse(line)
            return True
        except ValueError:
            return False

    def write_json(self):
        with open(self.path_json, "w", encoding="utf-8") as f:
            f.write(
                unicode(json.dumps(self.notes, ensure_ascii=False, indent=4))
            )

    def write_to_txt(self):
        glyphs_names = [glyph.name for glyph in self.font.glyphs]
        with open(self.path_txt, "w", encoding="utf-8") as f:
            for glyph_name in sorted(
                self.notes.keys(), key=lambda gname: glyphs_names.index(gname)
            ):
                f.write(glyph_name + "\n\t")
                f.write(
                    "\n\n\t".join(
                        "\n\t".join(_.splitlines())
                        for _ in self.notes[glyph_name]
                    )
                )
                f.write(u"\n" * 2)


if __name__ == "__main__":
    nw = NoteWriter(Glyphs.font)
    nw.process_notes()
    nw.write_json()
    nw.write_to_txt()
    Message(
        "Filepath: \n{}".format(nw.path_txt), "Notes are saved", OKButton=None
    )
