from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsItem, QGraphicsScene, QGraphicsView,QStyle)
from PyQt5.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen, QPixmap, QPolygon, QRadialGradient)
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
import random
import numpy as np
from scipy.io import loadmat
from numpy import genfromtxt
class TargetView(QGraphicsItem):
	
	# points = QPolygon([
    #     QPoint(10, 80),
    #     QPoint(20, 10),
    #     QPoint(80, 30),
    #     QPoint(90, 70)
    # ])

	def __init__(self,parent=None):
		super(TargetView, self).__init__()
		self.setZValue(1)
		self.trajectory= genfromtxt('data3.csv',delimiter=',')

		""" it's too damn ugly to write it here, for test purpose, use my previous .mat file for single fly info"""
		mat_dict={}
		mat_dict.update(loadmat('structure.mat'))
		
		self.goodtrx=mat_dict['structure'][0]

		#self.xyscale = 1
		self.currFrame= False
		self.isManualCalled= False
		self.idx_to_draw= np.empty([0,0])
		self.currentFly=1

		self.window = None

	def setWindowReference(self, window):
		self.window = window

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
		
		#set initial pen style
		pen=QPen(Qt.black)


		if (self.isManualCalled):
			self.isManualCalled = False
			
			# print 'currFrame',self.currFrame

			self.idx_to_draw = np.where(self.trajectory[:,0]==self.currFrame)[0]
			
			# print 'data_to_draw', self.idx_to_draw

		for i in self.idx_to_draw:
			x = self.trajectory[i,1]
			y = self.trajectory[i,2]

			if self.trajectory[i,3]==self.currentFly:
				# draw bold triangle for current fly
				pen.setWidth(3)
				# give labeling color to current fly
				if self.window.labelUI.isLabeling:
					pen.setColor(self.window.labelUI.currColor)	
				else:
					pen.setColor(Qt.black)
			else:
				pen.setColor(Qt.black)
				pen.setWidth(1)
			
			




			
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
			painter.setPen(pen)
			painter.drawPolyline(fly);



