import PyQt5
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem

import numpy as np


class Video(QGraphicsVideoItem):
	
	
	def __init__(self,parent=None):
		super(Video, self).__init__()
		self.installEventFilter(self)
	def setXYScale (self, oriWidth, oriHeight,newWidth,newHeight):
		#self.oriWidth = oriWidth
		#self.oriHeight = oriHeight
		#self.newWidth = newWidth
		#self.newHeight = nnewHeight
	    self.transX = oriWidth/newWidth
	    self.transY = oriHeight/newHeight
	def eventFilter(self,source,event):

		if (event.type()==PyQt5.QtCore.QEvent.GraphicsSceneMousePress):
			pos=event.pos()	
			#print event
			#print event.type()
			print('mouse position: (%.3f,%.3f)' % (pos.x() * self.transX,pos.y()*self.transY))	
			return True

		return False

