# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:05:44 2021

@author: MyPC
"""

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox

from threading import Thread

from project2 import Ui_MainWindow
from stt import runMicUsingThread
from dialogFlow import checkDialogFlowOutput, writeAndSay
import FaceR

class MyMainWindow(QMainWindow, Ui_MainWindow,QWidget):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.mic.clicked.connect(self.On_mic)
        self.ui.chat.returnPressed.connect(self.clickSendButton)
        writeAndSay(self.ui, "Welcome!")
        self.ui.makeIdle()
        self.ui.camera.clicked.connect(self.startStopCamera)
        self.ui.ocrRadio.toggled.connect(self.initOcr)
        self.ui.faceRadio.toggled.connect(self.initFace)
        FaceR.ocrDetect = True
        
    def initOcr(self):
        FaceR.ocrDetect = True
        
    def initFace(self):
        FaceR.ocrDetect = False
        
    def startStopCamera(self):
        if self.ui.camera.isChecked():
            QApplication.processEvents()
            self.ui.camera.setStyleSheet("background-color : lightblue")
            cameraStartThread = Thread(target = FaceR.startCamera, args=[self.ui])
            cameraStartThread.start()
        else:
            self.ui.camera.setStyleSheet("background-color : light gray")
            cameraStopThread = Thread(target = FaceR.stopCamera)
            cameraStopThread.start()
        
    def clickSendButton(self):
        checkDialogFlowOutput(self.ui, True, "")

    def On_mic(self):
        QApplication.processEvents()
        self.ui.mic.start()
        runMicUsingThread(self.ui)
        
    def closeEvent(self, event):
        result = QMessageBox.question(self,
                      "Confirm Exit",
                      "Are you sure you want to exit ?",
                      QMessageBox.Yes| QMessageBox.No)
        event.ignore()
        if result == QMessageBox.Yes:
            FaceR.stopCamera()
            event.accept()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
