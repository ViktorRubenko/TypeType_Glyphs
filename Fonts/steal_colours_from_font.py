#MenuTitle: Steal colours from Font
"""Copy glyphs colours from one font to another."""

from __future__ import print_function
import vanilla

class ColoursCopy(object):
	"""GUI for copying colours from one font to another"""
	def __init__(self):
		self.w = vanilla.FloatingWindow((450, 70), "Steal colours")
		
		self.w.text_anchor = vanilla.TextBox((15, 12+2, 130, 14), "Copy colours from:", sizeStyle='small')
		self.w.from_font = vanilla.PopUpButton((150, 12, 150, 17), self.getFontsForButton(isSourceFont=True), sizeStyle='small', callback=self.buttonCheck)
		
		self.w.text_value = vanilla.TextBox((15, 12+2+25, 130, 14), "To selected glyphs in:", sizeStyle='small')
		self.w.to_font = vanilla.PopUpButton((150, 12+25, 150, 17), self.getFontsForButton(isSourceFont=False), sizeStyle='small', callback=self.buttonCheck)

		self.w.copyOneMasterButton = vanilla.Button((-120, 12, -15, 17), "Copy One Master", sizeStyle='small', callback=self.copyColoursOneMaster)
		self.w.copyAllMastersButton = vanilla.Button((-120, 12+25, -15, 17), "Copy All Masters", sizeStyle='small', callback=self.copyColoursAllMasters)

		self.w.open()
		self.buttonCheck(None)
		

	def getFontsForButton(self, isSourceFont):
		myFontList = ["%s - %s" % (f.familyName, f.selectedFontMaster.name) for f in Glyphs.fonts]

		if isSourceFont:
			myFontList.reverse()
		
		return myFontList


	def getFontsFromButtons(self):
		fromFont = self.w.from_font.getItems()[ self.w.from_font.get() ]
		toFont   = self.w.to_font.getItems()[ self.w.to_font.get() ]
		
		sourceFont = [f for f in Glyphs.fonts if ("%s - %s" % (f.familyName, f.selectedFontMaster.name)) == fromFont][0]
		targetFont = [f for f in Glyphs.fonts if ("%s - %s" % (f.familyName, f.selectedFontMaster.name)) == toFont][0]

		return sourceFont, targetFont
	

	def buttonCheck(self, sender):
		fromFont = self.w.from_font.getItems()[ self.w.from_font.get() ]
		toFont   = self.w.to_font.getItems()[ self.w.to_font.get() ]

		if fromFont != toFont:
			self.w.copyOneMasterButton.enable(True)

			targetFont, sourceFont = self.getFontsFromButtons()
			if [m.name for m in targetFont.masters] == [m.name for m in sourceFont.masters]:
				self.w.copyAllMastersButton.enable(True)
			else:
				self.w.copyAllMastersButton.enable(False)

		else:
			self.w.copyOneMasterButton.enable(False)
			self.w.copyAllMastersButton.enable(False)


	def copyColoursAllMasters(self, sender):		

		sourceFont, targetFont = self.getFontsFromButtons()

		print("Syncing colours for", len(sourceFont.selection), "glyphs from", sourceFont.familyName, "to", targetFont.familyName, "for all masters.")

		try:
			for targetGlyph in targetFont.selection:
				glyphName = targetGlyph.name
				try:
					sourceGlyph = sourceFont[glyphName]
					targetGlyph.color = sourceGlyph.color
					for masterIndex, sourceMaster in enumerate(sourceFont.masters):
						targetMaster = targetFont.masters[masterIndex]
						targetGlyph.layers[targetMaster.id].color = sourceGlyph.layers[sourceMaster.id].color
				except Exception as e:
					print(glyphName, ": Failed")
		except:
			import traceback
			print(traceback.format_exc())
		finally:
			print("Done")

		self.w.close()
	

	def copyColoursOneMaster(self, sender):

		sourceFont, targetFont = self.getFontsFromButtons()
		
		print(
			"Syncing colours for", 
			len(sourceFont.selection), 
			"glyphs from", 
			sourceFont.familyName, sourceFont.selectedFontMaster.name, 
			"to", 
			targetFont.familyName, targetFont.selectedFontMaster.name
		)

		targetMaster = targetFont.selectedFontMaster
		sourceMaster = sourceFont.selectedFontMaster
		
		try:
			for targetGlyph in targetFont.selection:
				glyphName = targetGlyph.name
				try:
					sourceGlyph = sourceFont[glyphName]
					targetGlyph.color = sourceGlyph.color

					targetGlyph.layers[targetMaster.id].color = sourceGlyph.layers[sourceMaster.id].color
				except Exception as e:
					print(glyphName,": Failed")
					print(e)
					
		except Exception as e:
			import traceback
			print(traceback.format_exc())
		finally:
			print("Done.")

		self.w.close()
		
ColoursCopy()
