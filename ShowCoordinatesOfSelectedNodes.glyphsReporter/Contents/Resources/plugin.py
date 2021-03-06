# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from GlyphsApp import *
from GlyphsApp.plugins import *
from math import degrees, atan2

def angle( firstPoint, secondPoint ):
	"""
	Returns the angle (in degrees) of the straight line between firstPoint and secondPoint,
	0 degrees being the second point to the right of first point.
	firstPoint, secondPoint: must be NSPoint or GSNode
	"""
	xDiff = secondPoint.x - firstPoint.x
	yDiff = secondPoint.y - firstPoint.y
	return degrees(atan2(yDiff,xDiff))

class ShowCoordinatesOfSelectedNodes(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Coordinates of Selected Nodes',
			'de': u'Koordinaten ausgewählter Punkte',
			'nl': u'coördinaten van geselecteerde punten',
		})
		
	def foreground(self, Layer):
		currentSelection = Layer.selection
		offset = 5.0 + self.getHandleSize() / self.getScale()
		
		if currentSelection:
			# coordinates of on-curves
			for thisItem in currentSelection:
				if type(thisItem) is GSNode:
					nodeType = thisItem.type
					if nodeType == LINE or nodeType == CURVE:
						xCoordinate = thisItem.x
						yCoordinate = thisItem.y
						self.drawTextAtPoint(
							("%.1f, %.1f" % ( xCoordinate, yCoordinate )).replace(".0",""),
							NSPoint( xCoordinate + offset, yCoordinate ),
							fontColor=NSColor.brownColor()
						)
			
			# length and angles of adjacent nodes
			for thisPath in Layer.paths:
				theseNodes = thisPath.nodes
				thisNumberOfNodes = len( theseNodes )
				for i in range( thisNumberOfNodes ):
					previousNode = theseNodes[ (i-1) % thisNumberOfNodes ]
					currentNode = theseNodes[ i ]
					if (previousNode in currentSelection or currentNode in currentSelection) and not (previousNode.type == OFFCURVE and currentNode.type == OFFCURVE):
						previousPoint = previousNode.position
						currentPoint = currentNode.position
						currentAngle = angle( previousPoint, currentPoint )
						currentDistance = distance( previousPoint, currentPoint )
						pointSum = addPoints( previousPoint, currentPoint )
						pointInTheMiddle = NSPoint( pointSum.x * 0.5 + offset, pointSum.y * 0.5 )
						self.drawTextAtPoint(
							(u"%.1f @%.1f°" % ( currentDistance, currentAngle )).replace(".0",""),
							pointInTheMiddle,
							fontColor=NSColor.colorWithRed_green_blue_alpha_( 0.1, 0.7, 0.2, 1.0 )
						)
		

	