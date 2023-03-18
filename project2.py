# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from customButtons import LoadingButton

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(974, 549)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.history = QtWidgets.QTextBrowser(self.centralwidget)
        self.history.setGeometry(QtCore.QRect(20, 10, 460, 440))
        self.history.setObjectName("history")
        self.history.setReadOnly(True)
        self.history.setOpenExternalLinks(True)
        self.history.ensureCursorVisible()
        self.history.moveCursor(QtGui.QTextCursor.End)
        self.history.verticalScrollBar().setValue(self.history.verticalScrollBar().maximum())
        self.chat = QtWidgets.QLineEdit(self.centralwidget)
        self.chat.setGeometry(QtCore.QRect(20, 460, 361, 41))
        self.chat.setObjectName("chat")
        self.chat.setAlignment(QtCore.Qt.AlignLeft)
        self.mic = LoadingButton(self.centralwidget)
        self.mic.setGeometry(QtCore.QRect(390, 460, 91, 41))
        self.mic.setObjectName("mic")
        self.mic.setGif()
        
        self.camera = QtWidgets.QPushButton(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(520, 460, 91, 41))
        self.camera.setObjectName("Camera")
        self.camera.setText("Camera")
        self.camera.setStyleSheet("background-color : light gray")
        self.camera.setCheckable(True)
        self.camera.setChecked(False)
        
        self.ocrRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.ocrRadio.setGeometry(QtCore.QRect(620, 460, 125, 41))
        self.ocrRadio.setChecked(True)
        self.ocrRadio.setText("Character Recognition")
        self.faceRadio = QtWidgets.QRadioButton(self.centralwidget)
        self.faceRadio.setText("Face Detection")
        self.faceRadio.setGeometry(QtCore.QRect(760, 460, 91, 41))
        
        self.ocrFaceGroup = QtWidgets.QButtonGroup(self.centralwidget)
        self.ocrFaceGroup.addButton(self.ocrRadio)
        self.ocrFaceGroup.addButton(self.faceRadio)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.video = QtWidgets.QLabel(self.centralwidget)
        self.video.setGeometry(QtCore.QRect(490, 0, 600, 400)) # (490, 0, 600, 400) 
        self.video.setObjectName("video")
  
        self.movieMoving = QtGui.QMovie("b2.gif")
        self.movieSpeaking = QtGui.QMovie("a2.gif")
        self.movieMoving.setCacheMode(QtGui.QMovie.CacheAll)
        self.movieSpeaking.setCacheMode(QtGui.QMovie.CacheAll)
        
        self.video.setMovie(self.movieMoving)
        self.movieMoving.start()
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #@QtCore.pyqtSlot()
    def makeSay(self):
        QtWidgets.QApplication.processEvents()
        self.video.setMovie(self.movieSpeaking)
        self.movieSpeaking.start()
    
    #@QtCore.pyqtSlot()
    def makeIdle(self):
        QtWidgets.QApplication.processEvents()
        self.video.setMovie(self.movieMoving)
        self.movieMoving.start()
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.send.setText(_translate("MainWindow", "Send"))
        #self.mic.setText(_translate("MainWindow", "MIC"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

