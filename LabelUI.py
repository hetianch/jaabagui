from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsItem, QGraphicsScene, QGraphicsView,QStyle)
from PyQt5.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen,QColor, QPixmap, QPolygon, QRadialGradient)
from PyQt5.QtCore import QPoint, QRectF,QRect, QSize, Qt
import random
import numpy as np
from numpy import genfromtxt
import math
import pickle
class LabelUIMiddleLine(QGraphicsItem):
	def __init__(self,parent=None):
		super(LabelUIMiddleLine, self).__init__()

	def boundingRect(self):
		
		return QRectF(0,0,2,30)
	def paint (self, painter, option, widget):
		#draw the middle line of background
		painter.setBrush(QBrush(QColor(255,212,0)))
		painter.setPen(QPen(QColor(255,212,0)))

		painter.drawRect(0,0,2,30)

class LabelUI(QGraphicsItem):
	
	def __init__(self,parent=None):
		super(LabelUI, self).__init__()

		self.visiableWidth = 100

		self.visiableHeight = 50
		# [ [10, 200], [220, 400] ]
		labelData= dict.fromkeys(['t0','t1','names','labels'])
		labelData['names']=[0]
		labelData['labels']=[[]]
		labelData['t0']=[[]]
		labelData['t1']=[[]]
		self.labelData= labelData

		self.colorMatch = {'multifly':Qt.red,'female':Qt.green ,'chase':Qt.blue,'multifly_none':Qt.gray,'female_none':Qt.gray,'chase_none':Qt.gray}
		self.yMatch = {'multifly':0,'female':10 ,'chase':20,'multifly_none':0,'female_none':10 ,'chase_none':20}
		self.comboLabelMatch={0:'multifly', 1:'female',2:'chase'}
		# print self.labelData
		self.labelShapes = []
		self.currentLabelShapeIndex = 0
		# [ 'label1', 'label1', 'label2' ]
		self.labelNames = []

		self.currentLableName = ''

		self.widthPerFrame = 1
		self.gridGap = 1*100 # gird gap width for 100 frames

		self.isLabeling = False

		self.currentFrame = 0
		self.currFly = 1
		self.currColor = Qt.black

	def setWidthPerFrame(self, num):
		self.widthPerFrame = num
		#print 'setWidthPerframe', self.widthPerFrame
		self.gridGap = 100 * num
		print 'gridGap', self.gridGap

	def setVisiableSize(self, visiableWidth=100 , visiableHeight=50):
		self.visiableWidth = visiableWidth

		self.visiableHeight = visiableHeight
		# print self.visiableWidth	
		# print self.visiableHeight
		# where to redraw everytime
	def boundingRect(self):
		## test if set to scene size is enough? 
		## start with all size  0 -- 30000
		return QRectF(0,0,self.visiableWidth,self.visiableHeight)

	# used only when is labeling
	def setCurrentFrame(self, currentFrame):
		self.currentFrame = currentFrame

	def startLabel(self, labelIdx,postfix,currentframe):
		self.isLabeling = True
		#postfix= '_none' or ''
		self.currentBehavior = self.comboLabelMatch[labelIdx]+postfix
		color = self.colorMatch[self.comboLabelMatch[labelIdx]+postfix]
		self.currColor=color


		fly_to_add = self.currFly
		labels = self.labelData

		if fly_to_add not in labels['names']: # has not been labeled 
			labels['names'].append(fly_to_add)
			labels['labels'].append(list());
			labels['t0'].append(list());
			labels['t1'].append(list());

		fly_idx= labels['names'].index(fly_to_add)
		labels['labels'][fly_idx].append(self.currentBehavior)
		labels['t0'][fly_idx].append(currentframe)
		labels['t1'][fly_idx].append(currentframe)

		self.labelData=labels

		#print 'startLabel'
		#self.isLabeling = True
		# create a new labelNames

		# create a new labelShape, [currentframe, currentframe+2]

		# update currenLabelShapeIndex to this new shape


		# call labelUI.update() after call this function

	def stopLabel(self):
		self.isLabeling = False
		self.currentLableName = ''
		#print 'stoplabel'
		# call labelUI.update() after call this function

	def paint (self, painter, option, widget):
		# print 'paint'
		# print self.po

		# draw background every time
		boundRect = self.boundingRect()
		rightEnd = boundRect.right()
		leftEnd = boundRect.left()

		# print 'rightEnd',rightEnd
		# print 'leftEnd',leftEnd

		gridNum = int(math.floor(rightEnd / self.gridGap))

		# print 'gridNum',gridNum

		# get grid line 100 frame gap  width/frame * 100
		for i in range (0,gridNum+1):
			x = i*self.gridGap
			painter.drawLine(x, 0, x, 30)

		# draw x axis every time


		# if labeling, increase rectangle
		if (self.isLabeling) :
			# get current label's shapes
			#currentShape = self.labelShapes[self.currentLabelShapeIndex]
			#increase end value = current middle line
			labels = self.labelData
			fly_idx= labels['names'].index(self.currFly)
			labels['t1'][fly_idx][-1]=self.currentFrame
			self.labelData=labels
			#print self.labelData



		# draw all the existing shapes
		# for loop draw all shapes

		fly_to_draw= self.currFly
		labels=self.labelData
		if fly_to_draw in labels['names']:
			fly_idx= labels['names'].index(fly_to_draw)
			bouts= len(labels['labels'][fly_idx])
			for i in xrange(bouts):
				color = self.colorMatch[labels['labels'][fly_idx][i]]
				self.currColor = color
				yPos = self.yMatch[labels['labels'][fly_idx][i]]
				painter.setBrush(QBrush(color))
				pen=QPen(color)
				pen.setWidth(1)
				painter.setPen(pen)

				widthRect= (labels['t1'][fly_idx][i]-labels['t0'][fly_idx][i]+1) * self.widthPerFrame
				startPos= labels['t0'][fly_idx][i] * self.widthPerFrame
				#painter.drawRect(int x, int y, int width, int height)
				painter.drawRect(startPos,yPos,widthRect,10)



		# # if stop labeling, not change rectangle
		# painter.setBrush(QBrush(Qt.yellow))
		# painter.drawRect(0,0,100,20)



