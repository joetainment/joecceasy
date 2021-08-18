import sys
from PySide2 import QtWidgets, QtCore, QtGui
import PySide2

from joecceasy import Easy

class TranslucentWidgetSignals(QtCore.QObject):
    # SIGNALS
    CLOSE = QtCore.Signal()

class TranslucentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        ## keyboard interrupt, qt bug fix   
        import signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        super(TranslucentWidget, self).__init__(parent)
        self.cycle = 0
        self.timerTime  =  5000
        self.app = QtWidgets.QApplication.instance()
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.setSingleShot(True)
        self.updateTimer.timeout.connect( self.onTimer )
        
        
        
        #self.setWidth( 400 )
        #self.setWidth( 400 )
        self.resize( 400, 300 )
        
        
        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |  QtCore.Qt.WindowStaysOnTopHint )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.layout  = QtWidgets.QVBoxLayout()
        
        
        self.btn = QtWidgets.QPushButton(self)
        #font = QtGui.QFont()
        #font.setPixelSize(18)
        #font.setBold(True)
        #self.btn.setFont(font)
        self.btn.setStyleSheet("font: 20pt" )#background-color: rgb(0, 0, 0, 0)")
        #self.btn.setFixedSize(200, 100)
        
        
        
        self.btn.setText("   is this a dream?    ")
        self.btn.clicked.connect( self.quit )
        self.btn.setFocus()
        #print(  help( self.layout )  )
        
        self.layout.addWidget( self.btn )
        
        ## Run onTimer once at start, it will restart itself
        self.onTimer()
            #self.updateTimer.start( self.timerTime )
        
        

    def onTimer(self):
        import math, random
        print( 'EasyLucidity running, current app time.time is:' + str(Easy.Mods.time.time()) + ' ...' )
        x = random.uniform( 1, 1900-self.width() ) ##+ self.width()/2 , 1900-self.width()/2
        y = random.uniform( 1, 1000-self.height() )
        x = math.floor(x)
        y = math.floor(y)
        pos = self.pos()  #pos.x()
        self.move( x , y )
        
        everyNth = 10
        timesToShow=1
        btn = self.btn
        if (  self.cycle <=  -1 + timesToShow   ):
            btn.show()
        else:
            if btn.isVisible():
                btn.hide()
            if self.cycle >= -1+everyNth:
                self.cycle = -1  ## becaue next line will add one, making it zero
        
        self.cycle += 1
            
        self.updateTimer.start( self.timerTime )
                
    
    def quit(self):
        self.app.quit()



##self.destroyed.connect(lambda: self._unregister())
app=QtWidgets.QApplication(sys.argv)
win = TranslucentWidget()
win.show()
sys.exit( app.exec_() )




















"""
    def _onclose(self):
        print("Close")
        self.SIGNALS.CLOSE.emit()
"""



"""
    
    def resizeEvent(self, event):
        s = self.size()
        popup_width = 300
        popup_height = 120
        ow = int(s.width() / 2 - popup_width / 2)
        oh = int(s.height() / 2 - popup_height / 2)
        self.btn.move(ow + 265, oh + 5)
"""


        
"""
        self.fillColor = QtGui.QColor(30, 30, 30, 120)
        self.penColor = QtGui.QColor("#333333")

        self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        self.popup_penColor = QtGui.QColor(200, 200, 200, 255)

        
        print(  help( self.layout )  )
        self.layout  = QtWidgets.QVBoxLayout()
        self.layout.addWidget( self.btn )
        self.btn.clicked.connect(self._onclose)

        self.SIGNALS = TranslucentWidgetSignals()
"""




"""
    def paintEvent(self, event):
        # This method is, in practice, drawing the contents of
        # your window.

        # get current window size
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 100, s.width(), s.height())

        # drawpopup
        qp.setPen(self.popup_penColor)
        qp.setBrush(self.popup_fillColor)
        popup_width = 300
        popup_height = 120
        ow = int(s.width()/2-popup_width/2)
        oh = int(s.height()/2-popup_height/2)
        qp.drawRoundedRect(ow, oh, popup_width, popup_height, 5, 5)

        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)
        qp.setFont(font)
        qp.setPen(QtGui.QColor(70, 70, 70))
        tolw, tolh = 80, -5
        qp.drawText(ow + int(popup_width/2) - tolw, oh + int(popup_height/2) - tolh, "Yep, I'm a pop up.")

        qp.end()
"""
