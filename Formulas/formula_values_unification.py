#MenuTitle: Formula values unification
# -*- coding: utf-8 -*-
#Version: 0.2.3 (04 Oct, 2019)


import re


def update_metrics(glyph):
    for layer in glyph.layers:
        layer.syncMetrics()

def set_general_formula(thisGlyph, thisMasterIndex, attrib):
    master_layer = thisGlyph.layers[thisMasterIndex]
    if master_layer.__getattribute__(attrib):
    	attrib_value = master_layer.__getattribute__(attrib)
    else:
    	attrib_value = thisGlyph.__getattribute__(attrib)
    # clear formula in all masters
    for thisLayer in thisGlyph.layers:
        thisLayer.__setattr__(attrib, None)
    # set general
    thisGlyph.__setattr__(attrib, re.sub('[=]+', '=', attrib_value))

def set_increment(thisGlyph, thisMasterIndex, attrib):
    attribs = {
        'rightMetricsKey': 'RSB',
        'leftMetricsKey': 'LSB',
        'widthMetricsKey': 'width'
        }
    try:
        increment = int(re.findall(r'[+-]?\d+',
                                   thisGlyph.__getattribute__(attrib))[0])
    except IndexError:
        increment = 0
        
    for thisLayerIndex, thisLayer in enumerate(thisGlyph.layers):
        if thisLayerIndex == thisMasterIndex:
            continue
        delta = (thisGlyph.layers[thisMasterIndex].__getattribute__(attribs[attrib]) -
                 thisLayer.__getattribute__(attribs[attrib]))
        if not delta:
            # No corrections needed
            continue
        delta = int(increment + delta)
        if delta == 0:
            thisLayer.__setattr__(
                attrib, re.sub(r'[+-]?\d+', '',
                               thisGlyph.__getattribute__(attrib)).replace('=', '==')
                )
        else:
            if delta > 0:
                delta = '+' + str(delta)
            else:
                delta = str(delta)
            if re.search(r'[+-]?\d+', thisGlyph.__getattribute__(attrib)):
                thisLayer.__setattr__(attrib,
                                      re.sub(r'[+-]?\d+',
                                             delta,
                                             thisGlyph.__getattribute__(
                                                 attrib)).replace('=', '=='))
            else:
                thisLayer.__setattr__(attrib,
                    thisGlyph.__getattribute__(attrib) + delta
                    )

def main():
    Glyphs.clearLog()
    font = Glyphs.font
    thisMasterIndex = font.masterIndex
    for thisGlyph in font.glyphs:
    	if thisGlyph.name != 'L':
    		continue
        for attrib in ('leftMetricsKey', 'rightMetricsKey', 'widthMetricsKey'):
            update_metrics(thisGlyph)
            if (thisGlyph.layers[thisMasterIndex].__getattribute__(attrib) or
            	thisGlyph.__getattribute__(attrib)):
                set_general_formula(thisGlyph, thisMasterIndex, attrib)
                update_metrics(thisGlyph)
                set_increment(thisGlyph, thisMasterIndex, attrib)
                update_metrics(thisGlyph)
             

if __name__ == '__main__':
    main()

