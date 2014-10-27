from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsItem, QGraphicsScene, QGraphicsView,QStyle)
from PyQt5.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen, QPixmap, QPolygon, QRadialGradient)
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
import random
import numpy as np
from numpy import genfromtxt
class LabelItem(QGraphicsItem):
	
	def __init__(self,parent=None):
		super(TargetView, self).__init__()
		self.setZValue(1)
		self.trajectory= genfromtxt('data.csv',delimiter=',')

		#self.xyscale = 1
		self.currFrame= False
		self.isManualCalled= False
		self.idx_to_draw= np.empty([0,0])

	def setXYScale (self, oriWidth, oriHeight,newWidth,newHeight):
		#self.oriWidth = oriWidth
		#self.oriHeight = oriHeight
		#self.newWidth = newWidth
		#self.newHeight = nnewHeight
	    self.transX = int(round(oriWidth/newWidth *1000))/1000.0
	    self.transY = int(round(oriHeight/newHeight*1000))/1000.0

	def getFrame(self,frame):
		self.currFrame=frame

	def getPoint (self, x, y):
		return QPoint(x /self.transX, y/self.transY)
	# Create Fly triangle
	
	def getFly (self, point1, point2, point3):
		return QPolygon([
				point1, point2, point3, point1
			])
	
	def paint (self, painter, option, widget):


		if (self.isManualCalled):
			self.isManualCalled = False
			
			# print 'currFrame',self.currFrame

			self.idx_to_draw = np.where(self.trajectory[:,0]==self.currFrame)[0]
			
			# print 'data_to_draw', self.idx_to_draw

		for i in self.idx_to_draw:
			x = self.trajectory[i,1]
			y = self.trajectory[i,2]

			
			# print 'currFrame',self.currFrame
			# print 'data_to_draw', self.idx_to_draw
			# print 'x',x
			# print 'y',y

			fly = self.getFly(
				self.getPoint(x, y),
				self.getPoint(x+50, y+50),
				self.getPoint(x-50, y+50)
			)
			#print fly

			painter.drawPolyline(fly);



