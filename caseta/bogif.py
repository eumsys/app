import sys
import os
from PySide import QtCore, QtGui
ImagesFolder=os.path.join(os.path.dirname(__file__),'images')

class CucumberGifWidget(QtGui.QLabel):
    def __init__(self, parent=None):
        super(CucumberGifWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameStyle(QtGui.QFrame.WinPanel | QtGui.QFrame.Sunken)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        
        trashGif= open(os.path.join(ImagesFolder,'cucumber.gif'), 'rb').read()
        self.gifByteArray=QtCore.QByteArray(trashGif)
        self.gifBuffer=QtCore.QBuffer(self.gifByteArray)
        self.movie = QtGui.QMovie()
        self.movie.setFormat('GIF')
        self.movie.setDevice(self.gifBuffer)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.setMovie(self.movie)
        self.movie.jumpToFrame(0)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        event.setDropAction(QtCore.Qt.MoveAction)
        if event.mimeData().hasImage():
            if "cucumber" in event.mimeData().text():
                self.movie.start()
                event.source().setParent(None)
                event.source().deleteLater()
            else:
                event.accept()
        else:
            event.ignore()
