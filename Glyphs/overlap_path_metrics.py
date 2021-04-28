# MenuTitle: Overlap-Path-Metrics
# -*- coding: utf-8 -*-
# Version: 0.2 (24 Oct, 2019)
__doc__ = """
Sequence of actions: 
1. Filter - Remove overlap; 
2. Path - Correct path direction; 
3. Glyph - Update metrics.
"""


def overlap_path_metrics():
    layer = Glyphs.font.selectedLayers[0]
    layer.removeOverlap()
    layer.correctPathDirection()
    layer.syncMetrics()


if __name__ == "__main__":
    overlap_path_metrics()
