import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsItem, QGraphicsScene, QGraphicsView, QStyle)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
import numpy as numpy
from TargetView import TargetView
from LabelUI import LabelUI, LabelUIMiddleLine
from ui import Ui_MainWindow
from Video import Video
import cv2
import pickle
class jaabaGUI(QMainWindow):
    """ controller for the blob labeling GUI"""

    def __init__(self,parent=None):
        self.debugMode = True
        self.debugVideoPath = '/Users/071cht/Desktop/Lab/jaabagui/testt.mjpeg.avi'

        QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.installEventFilter(self)
        self.setFocusPolicy(Qt.StrongFocus)
        #add new slider
        # self.positionSlider=QSlider(Qt.Horizontal)
        # self.positionSlider.setGeometry (800,800,100,30)
        # self.positionSlider.setRange(0, 0)
        # self.positionSlider.sliderMoved.connect(self.setPosition)

        #setup Video
        #video player
        self.mediaPlayer1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer2.setNotifyInterval(10)
        #self.mediaPlayer.metaDataChanged.connect(self.metaDataChanged)
        self.mediaPlayer1.durationChanged.connect(self.durationChanged)
        self.mediaPlayer1.positionChanged.connect(self.positionChanged)
        self.mediaPlayer2.positionChanged.connect(self.positionChanged)
        #self.mediaPlayer2.positionChanged.connect(self.paintEvent)
        

        #visualizetion
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        #self.scene.setBackgroundBrush(Qt.black)
        self.videoItem1 = QGraphicsVideoItem()
        self.videoItem2 = Video()
        self.scene.addItem(self.videoItem1)
        self.scene.addItem(self.videoItem2)
        self.mediaPlayer1.setVideoOutput(self.videoItem1)
        self.mediaPlayer2.setVideoOutput(self.videoItem2)

       

        #slider bar
        self.ui.horizontalSlider.setRange(0, 0)
        self.ui.horizontalSlider.sliderMoved.connect(self.setPosition)
        # self.ui.horizontalSlider.sliderPressed.connect(self.sliderPressed)

        #draw on video
        self.flyCanvas= TargetView()
        self.scene.addItem(self.flyCanvas)
        #give reference to target view
        self.flyCanvas.setWindowReference(self)

        #lineEdit signals:
        self.ui.lineEdit.returnPressed.connect(self.lineEditChanged)



        #callbacks
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionLoad_Project.triggered.connect(self.loadVideo)
        self.ui.actionImport_Labels.triggered.connect(self.loadLabels)
        #self.ui.buttonPlay.clicked[bool].connect(self.setToggleText)
        self.ui.buttonPlay.clicked.connect(self.play)
        self.ui.actionSave.triggered.connect(self.saveLabels)
        ## print self.ui.graphicsView.sizeHint()

        #behavior Button
        self.ui.buttonBehavior.clicked.connect(self.behaviorButtonClick)
        self.ui.buttonNone.clicked.connect(self.noneButtonClick)

        #initialization
        self.loaded = False
        self.videoFilename = None
        self.frame_count=None
        self.width=None
        self.height=None
        self.frame_trans=None
        self.previous_frame=0
        self.current_frame=0
        self.behaviorButtonStart = False
        self.noneButtonStart = False
        self.currentFly=1

        #initialize flyInfo
        #self.setCurrentFly(self.currentFly)

        # register flyid changed callback
        self.flyCanvas.onCurrentFlyIdChanged(self.currentFlyIdChangedCallback)
        self.flyCanvas.setCurrentFlyId(self.currentFly)

        # when double click on video, change fly id in target view
        self.videoItem2.onDoubleClick(self.flyCanvas.setCurrentFlyIdByXY)

        ########################
        # DEBUG PART HERE!!!!! #
        ########################
        if (self.debugMode):
            self.debugLoadVideo()

    # add label UI related when load video   
    def showEvent(self, evt):
        super(jaabaGUI, self).showEvent(evt)
        ##### HERE THE WINDOW IS LOADED!!!!!!!!
        # self.loadLabelUI()

    def loadLabelUI(self):
         #labels
        self.labelScene = QGraphicsScene()

        self.ui.graphLabels.setScene(self.labelScene)
        # the size is only accurate after the window fully displayed
        labelUIWidth = self.ui.graphLabels.width()
        labelUIHeight = self.ui.graphLabels.height()-1

        self.labelScene.setSceneRect(0,0,labelUIWidth,labelUIHeight)

        
        self.labelUI = LabelUI()
        # visiableWidth = 850
        # height = 30
        # visiableFrameNum = 850

        self.labelUI.setWidthPerFrame(850.0/850.0)
        # print '850/500',850.0/850.0b
        # print 'length_perframe is ', self.labelUI.widthPerFrame 
        # 850 is the original length of graphLabel
        total_length= self.labelUI.widthPerFrame * self.frame_count
        self.labelUI.setVisiableSize(total_length,30)

        # set start position
        self.labelUI.setPos(labelUIWidth/2,0)


        print 'frame_count is ', self.frame_count
        print 'total length is', total_length
        
        self.labelScene.addItem(self.labelUI)

        # middle line ui
        self.labelUIMiddleLine = LabelUIMiddleLine()
        self.labelScene.addItem(self.labelUIMiddleLine)
        self.labelUIMiddleLine.setPos(labelUIWidth/2,0)
       


        # self.labelUI.setPos(QPointF(-100,0))
        self.writeLog('Label UI loaded')

    def eventFilter(self, obj, event):
  
    	if (event.type() == PyQt5.QtCore.QEvent.KeyPress):
    		# http://qt-project.org/doc/qt-4.8/qt.html#Key-enum
    		key = event.key()
    		
    		if (key == Qt.Key_Up) :
    			curr_frame= int(float(self.ui.lineEdit.text()))
    			curr_frame= curr_frame-30
    			media_position= int(round(curr_frame*self.frame_trans))

    			# print curr_frame, media_position
    			self.mediaPlayer1.setPosition(media_position) 
    			self.mediaPlayer2.setPosition(media_position)

    			# print 'down -30'
    		elif (key == Qt.Key_Right):
    			curr_frame= int(float(self.ui.lineEdit.text()))
    			# print 'right +1'
    			# print curr_frame
    			curr_frame= curr_frame+1
    			media_position= int(round(curr_frame*self.frame_trans))
    			# print 'curr_frame',curr_frame
    			# print 'frame_trans',self.frame_trans
    			# print ' curr_frame*self.frame_trans',curr_frame*self.frame_trans
    			# print 'media_position',media_position

    			# print curr_frame, media_position
    			self.mediaPlayer1.setPosition(media_position) 
    			self.mediaPlayer2.setPosition(media_position)
    			# self.mediaPlayerPositionChanged(media_position)
    		elif (key == Qt.Key_Left):
    			curr_frame= int(float(self.ui.lineEdit.text()))
    			curr_frame= curr_frame-1
    			media_position= int(round(curr_frame*self.frame_trans))
    			self.mediaPlayer1.setPosition(media_position) 
    			self.mediaPlayer2.setPosition(media_position)
    			# print 'left -1'
    		elif (key == Qt.Key_Down):
    			curr_frame= int(float(self.ui.lineEdit.text()))
    			curr_frame= curr_frame+30
    			media_position= int(round(curr_frame*self.frame_trans))
    			self.mediaPlayer1.setPosition(media_position) 
    			self.mediaPlayer2.setPosition(media_position)
    			# print 'up +30'
    		return True

    		

    	return False


    # ###actions starts from here###
    def quit(self):
        QApplication.quit()

    def loadVideo(self):
        
        # print QMediaPlayer.supportedMimeTypes()

        self.writeLog("Loading video...")

        self.videoFilename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        if not self.videoFilename:
            self.writeLog("User cancelled - no video loaded")
            return
        else:
       		cap=cv2.VideoCapture(self.videoFilename)
	    	self.frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
	    	self.width=cap.get(3)
	    	self.height=cap.get(4)

	        self.mediaPlayer2.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoFilename )))
	        self.mediaPlayer1.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoFilename )))
	        self.ui.buttonPlay.setEnabled(True)
            # self.mediaPlayer2.setVideoOutput(self.videoItem2)
            # self.mediaPlayer1.setVideoOutput(self.videoItem1)
            # size= self.videoItem2.nativeSize()
            # # print size
            ## print self.mediaPlayer.duration()
          
            ## print self.mediaPlayer.metaData()
        self.writeLog("Video loaded!")

        # init label related ui
        self.loadLabelUI()


    def debugLoadVideo(self):

        self.videoFilename = self.debugVideoPath

        cap=cv2.VideoCapture(self.videoFilename)
        self.frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.width=cap.get(3)
        self.height=cap.get(4)

        self.mediaPlayer2.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoFilename )))
        self.mediaPlayer1.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoFilename )))
        self.ui.buttonPlay.setEnabled(True)
        self.writeLog("Video loaded!")

        QTimer.singleShot(1000, self.loadLabelUI)

    def play(self):
    	
        self.videoItem1.setAspectRatioMode(0)
        self.videoItem2.setAspectRatioMode(0)
        self.scene.setSceneRect(0,0,self.ui.graphicsView.width(),self.ui.graphicsView.height())
        self.videoItem1.setSize(QSizeF(self.ui.graphicsView.width()/2,self.ui.graphicsView.height()))
        self.videoItem2.setSize(QSizeF(self.ui.graphicsView.width()/2,self.ui.graphicsView.height()))
        self.videoItem1.setPos(QPointF(0,0))
        self.videoItem2.setPos(QPointF(self.ui.graphicsView.width()/2,0))
        self.flyCanvas.setPos(QPointF(self.ui.graphicsView.width()/2,0))

        # custom function setXYScale
        self.videoItem2.setXYScale(self.width,self.height,self.ui.graphicsView.width()/2,self.ui.graphicsView.height())
        self.flyCanvas.setXYScale(self.width,self.height,self.ui.graphicsView.width()/2,self.ui.graphicsView.height())




        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
        	self.ui.buttonPlay.setIcon(self.ui.style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaPlay))
        	self.ui.buttonPlay.setText("Play")
        	self.mediaPlayer1.pause()
        	self.writeLog("Video paused")
        else: 
        	self.ui.buttonPlay.setIcon(self.ui.style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaPause))
	        self.ui.buttonPlay.setText("Stop")
	        
	        self.mediaPlayer1.play()
	        self.writeLog("Playing video")

        if self.mediaPlayer2.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer2.pause()
        else: 
            self.mediaPlayer2.play()

    def loadLabels(self):

        self.writeLog("Loading labels from file...")
        self.labelFilename = QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
        self.labelUI.labelData = pickle.load(open(self.labelFilename,"rb"))
        self.writeLog("Label loaded from file:" + self.labelFilename)

    def saveLabels(self):
        # Now it can only save to current file. Will add an poput window to choose path later
        pickle.dump( self.labelUI.labelData, open( "newLabels.p", "wb" ) )
  

    def setPosition(self, position):
    	self.mediaPlayer1.setPosition(position) 
    	self.mediaPlayer2.setPosition(position) 

    # when position of media changed, set slider and text box accordingly.
    def positionChanged(self, position):
        #test change labelui position
        # self.labelUI.startLabel();
        # self.labelUI.update()
        previous_frame=  self.previous_frame
        curr_frame= int(round(position/self.frame_trans))
        self.current_frame=curr_frame
        frame_change= previous_frame-curr_frame
        move_width= frame_change * self.labelUI.widthPerFrame
        self.previous_frame= curr_frame

        self.labelUI.moveBy(move_width,0)

        self.labelUI.setCurrentFrame(curr_frame)
        # enforce labelUI paint once
        self.labelUI.update()
       
        # self.labelUI.setPos(self.labelUI.mapToParent(1,0));
        # self.labelUI.update()

    	# # print 'triggered position'
    	# # print position
    	# # print 'cur position'
    	# # print self.mediaPlayer2.position()
    	self.updateLineEdit(position)
    	self.updateSliderAndGraph(position)
    	
       #  self.ui.horizontalSlider.setValue(position)

       #  if isinstance(self.frame_trans,float):
	      #   # # print type(position),position
	      #   # # print type(self.frame_trans),self.frame_trans 
	      #   # # print position/self.frame_trans
	     	# self.ui.lineEdit.setText(str(int(round(position/self.frame_trans))))
	     	# self.flyCanvas.getFrame(int(round(position/self.frame_trans)))
	     	# self.flyCanvas.isManualCalled = True;
	     	# self.flyCanvas.update()

       #  self.writeLog(str(position))    
       # # self.updateMediaControlUI(position)
       # # self.flyCanvas.update()

    def updateSliderAndGraph(self, position):
    	self.ui.horizontalSlider.setValue(position)
    	if isinstance(self.frame_trans,float):
    		self.flyCanvas.getFrame(int(round(position/self.frame_trans)))
    		self.flyCanvas.isManualCalled = True
    		self.flyCanvas.update()

        #self.writeLog(str(position)) 
    def updateLineEdit(self, position): 
        # # print self.width
        # # print self.height
    	if isinstance(self.frame_trans,float):
	        # # print type(position),position
	        # # print type(self.frame_trans),self.frame_trans 
	        # # print position/self.frame_trans
	     	self.ui.lineEdit.setText(str(int(round(position/self.frame_trans))))

    def durationChanged(self, duration):
	    self.ui.horizontalSlider.setRange(0, duration) 
	    self.frame_trans=self.mediaPlayer1.duration()/self.frame_count
	    ## print self.frame_trans

	#def eventFilter(self,source,event):
		#if (event.type()==PyQt5.QtCore.QEvent.MousePress and source is self.videoItem2):
		# 	pos=event.pos()
		# 	# print('mouse position: (%d,%d)' % (pos.x(),pos.y()))
	 #    return PyQt5.QtGui.QWidget.eventFilter(self, source, event)

    def writeLog(self,text):
        self.ui.log.setText(text)

    # def eventFilter (self.ui.lineEdit,event):
    #     if event.type()==PyQt5.QtCore.QEvent

    def lineEditChanged(self):
    	#set position of media
    	curr_frame= int(float(self.ui.lineEdit.text()))
    	media_position= int(round(curr_frame*self.frame_trans))
    	self.mediaPlayer1.setPosition(media_position) 
    	self.mediaPlayer2.setPosition(media_position)
    	# print 'setPosition'
    	# print media_position
    	# print 'after set'
    	# print self.mediaPlayer2.position()
    	# self.updateSliderAndGraph(media_position)


    def behaviorButtonClick(self):
        # flip flag
        self.behaviorButtonStart = not self.behaviorButtonStart

        # check click to start or stop
        if (self.behaviorButtonStart):
            # start labeling
            self.labelUI.startLabel(self.ui.comboBox.currentIndex(),'',self.current_frame)
            self.writeLog('start labeling')


        else:
            # stop lableing
            self.labelUI.stopLabel()
            self.writeLog('stop labeling')

    def noneButtonClick(self):
           # flip flag
        self.noneButtonStart = not self.noneButtonStart

        # check click to start or stop
        if (self.noneButtonStart):
            # start labeling
            self.labelUI.startLabel(self.ui.comboBox.currentIndex(),'_none',self.current_frame)
            self.writeLog('start labeling')
        else:
            # stop lableing
            self.labelUI.stopLabel()
            self.writeLog('stop labeling')


    # set CurrentFly when fly changed! 
    def setCurrentFly(self,fly):
        self.currentFly = fly
        self.ui.flyInfo.setPlainText('FlyID:' + str(self.currentFly))
        self.flyCanvas.currentFly=fly

    def currentFlyIdChangedCallback(self,fly):
        print 'callback!!!!!';
        self.currentFly = fly
        self.ui.flyInfo.setPlainText('FlyID:' + str(self.currentFly))
        #self.flyCanvas.currentFly=fly
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = jaabaGUI()
    gui.show()
    sys.exit(app.exec_())



    #good example:http://hasanaga.info/simple-avi-player-with-opencv-qt-4-8-playing-video-file-with-slider-position/