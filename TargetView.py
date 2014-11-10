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
		self.isManualCalled= False
		self.idx_to_draw= np.empty([0,0]) ## don't draw fly when idx_to_draw is empty
		self.idx_to_draw_currFly_array=np.empty([0,0]) ## don't draw fly when idx_to_draw_tgfly is empty
		self.currentFly=1
		self.currFrame= 1 # the first frame of current Fly

		self.window = None
		
		# callbacks!!!!
		self.currentFlyIdChangedCallbacks = []

	def setWindowReference(self, window):
		self.window = window

	def setCurrentFlyId(self, flyid):
		self.currentFly = flyid
		self.first_frame_currFly= self.goodtrx[self.currentFly-1][0,0]
		self.last_frame_currFly = self.goodtrx[self.currentFly-1][-1,0]
		self.frame_number= len(self.goodtrx[self.currentFly-1][:,0])
		self.isManualCalled = True
		self.update()

		# on currentId changed, call callbacks if have
		for c in self.currentFlyIdChangedCallbacks:
			c(flyid);

	# callback is function reference
	def onCurrentFlyIdChanged(self, callback):
		self.currentFlyIdChangedCallbacks.append(callback)


	def setCurrentFlyIdByXY(self, x, y):
		# given x, y 
		x= x * self.transX
		y= y * self.transY
		currFrame=self.currFrame
		trajectory=self.trajectory

		idx_to_draw = np.where(trajectory[:,0]==currFrame)[0]
		nodes=np.matrix('0,0');
		for i in idx_to_draw:
			nodes=np.concatenate([nodes,np.matrix([[trajectory[i,1],trajectory[i,2]]])])
			node= np.array([x,y])

		nodes=np.asarray(nodes)
		nodes=nodes[1:]

		dist= (nodes-node) **2
		dist_sum=dist.sum(axis=1) ## columnwize sum
		min_idx=dist_sum.argmin(axis=0)
		fly= trajectory[idx_to_draw[min_idx],3]

		#print '!!!!!!!! x=',x,' !!!!! y=',y
		#get id
		self.setCurrentFlyId(fly)

		


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
		return QPoint(x/self.transX, y/self.transY)
	# Create Fly triangle
	
	def getFly (self, point1, point2, point3):
		return QPolygon([
				point1, point2, point3, point1
			])

	
	def paint (self, painter, option, widget):
		
		#set initial pen style
		pen=QPen(Qt.black)

		pen2=QPen(Qt.black) # used for draw dots of current fly
		pen2.setWidth(3)

		if (self.isManualCalled):
			self.isManualCalled = False
			
			# print 'currFrame',self.currFrame

			self.idx_to_draw = np.where(self.trajectory[:,0]==self.currFrame)[0]

		
			self.idx_to_draw_currFly= self.currFrame-self.first_frame_currFly
			
			#paint current fly
			if (self.currFrame > self.last_frame_currFly):
				self.idx_to_draw_currFly_array=np.empty([0,0])
				# print 'a'
				# print 'currentFly',self.currentFly
				# print 'currFrame',self.currFrame
				# print self.idx_to_draw_currFly_array
		  	elif (self.currFrame > self.last_frame_currFly-100):
				self.idx_to_draw_currFly_array= np.arange(self.idx_to_draw_currFly,self.frame_number,1)
				# print 'b'
				# print 'currentFly',self.currentFly
				# print 'currFrame',self.currFrame
				# print self.idx_to_draw_currFly,self.idx_to_draw_currFly_array
			else:
				self.idx_to_draw_currFly_array= np.arange(self.idx_to_draw_currFly,self.idx_to_draw_currFly+100,1)  #draw current frame and 100 frames after current frame
				# print 'c'
				# print 'currentFly',self.currentFly
				# print 'currFrame',self.currFrame
				# print self.idx_to_draw_currFly,self.idx_to_draw_currFly_array
			# print 'currFly',self.currentFly
			# print 'idx_to_draw_currFly_array',self.idx_to_draw_currFly_array
			# print 'firstframe',self.first_frame_currFly
			# print 'lastframe',self.last_frame_currFly

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

			#paint all fly
			painter.setPen(pen)
			painter.drawPolyline(fly);

		

		# print 'idx_to_draw_currFly', self.idx_to_draw_currFly
		# print 'currframe',self.currFrame
		# print 'first_frame',self.first_frame_currFly
		# print 'curr_fly',self.currentFly
		for j in self.idx_to_draw_currFly_array: ## draw current and 30 frames after current frame
			x = self.goodtrx[self.currentFly-1][j,1] #first fly idx is 0 in .mat file
			y = self.goodtrx[self.currentFly-1][j,2]

			point = self.getPoint(x,y)

			painter.setPen(pen2)
			painter.drawPoint(point)





			






