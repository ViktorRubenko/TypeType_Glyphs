#MenuTitle: Overlap-Path-Metrics
# -*- coding: utf-8 -*-
#Version: 0.2 (24 Oct, 2019)


def overlap_path_metrics():
	layer = Glyphs.font.selectedLayers[0]
	layer.removeOverlap()
	layer.correctPathDirection()
	layer.syncMetrics()
	
	
if __name__ == '__main__':
	overlap_path_metrics()
