# MenuTitle: Unicode Filler
# -*- coding: utf-8 -*-
# Version: 0.1.0 (17 Jan, 2020)


import vanilla


class UnicodeFillerGUI:
	def __init__(self):
		self.w = vanilla.Window(
			(340, 150), 
			title="Unicode filler"
		)
		
		self.w.text = vanilla.TextBox(
			(10, 10, 340, 25), 
			'Start unicode value (Private range: [57344, 63743]):',
		)
		
		self.w.text_1 = vanilla.TextBox((10, 40, 80, 25), 'intNumber:')
		self.w.integer = vanilla.EditText(
			(90, 40, 200, 25), 
			'57344', 
			callback=self.on_int
		)
		
		self.w.text_2 = vanilla.TextBox((10, 75, 80, 25), 'hexNumber:')
		self.w.hexNumber = vanilla.EditText(
			(90, 75, 200, 25),
			'E000',
			callback=self.on_hex,
		)
		
		self.w.button = vanilla.Button(
			(10, 110, 80, 20), 'Fill', callback=self.fill
		)
		
		self.w.open()
		
	def on_int(self, sender):
		if sender.get():
			self.w.hexNumber.set('{:04X}'.format(int(sender.get())))
		else:
			self.w.hexNumber.set('')
							
	def on_hex(self, sender):
		if sender.get():
			self.w.integer.set('{}'.format(int(sender.get(), 16)))
		else:
			self.w.integer.set('')
			
	def fill(self, sender):
		filler = UnicodeFiller(
			int(self.w.integer.get()), 
			Glyphs.font
		)
		try:
			filler.run()
		finally:
			self.w.close()	
		

class UnicodeFiller:
	def __init__(self, start_unicode, font):
		self.font = font
		self.start_unicode = int(start_unicode)
		self.selected_glyphs = [glyph for glyph in font.glyphs if glyph.selected]
		self.uni_range = tuple(
			range(
				self.start_unicode, 
				self.start_unicode + len(self.selected_glyphs)
			)
		)
		
	def check(self):
		if self.start_unicode not in range(57344, 63744):
			raise ValueError('Invalid start value')
		if self.start_unicode + len(self.selected_glyphs) > 63744:
			raise IndexError('Selected glyph range is too big')
		nonempty_glyphs = [
			glyph.name for glyph in self.selected_glyphs if glyph.unicode
		]
		if nonempty_glyphs:
			raise ValueError(
				'Some glyphs have already had unicode value: \n{}'.format(
					'\n'.join(nonempty_glyphs)
				)
			)
		taken_uni = [
			('{}({}={})'.format(glyph.name, int(glyph.unicode, 16), glyph.unicode)) 
			for glyph in self.font.glyphs 
			if glyph.unicode and int(glyph.unicode, 16) in self.uni_range
		]
		if taken_uni:
			raise ValueError(
				'Some unicode values has already taken: \n{}'.format(
					'\n'.join(taken_uni)
				)
			)
		
	def fill_unicode(self):
		for glyph_index, glyph in enumerate(self.selected_glyphs):
			glyph.unicode = '{:04X}'.format(self.uni_range[glyph_index])
			
			
	def run(self):
		Glyphs.clearLog()
		self.check()
		self.fill_unicode()
		
		
UnicodeFillerGUI()
