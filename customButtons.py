# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 14:46:28 2021

@author: M Taha khan
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class LoadingButton(QtWidgets.QPushButton):
    @QtCore.pyqtSlot()
    def start(self):
        self.setText("")
        self._movie.start()

    @QtCore.pyqtSlot()
    def stop(self):
        self.setText("MIC")
        self._movie.stop()
        self.setIcon(QtGui.QIcon())

    def setGif(self):
        if not hasattr(self, "_movie"):
            self._movie = QtGui.QMovie(self)
            self._movie.setFileName("micButton1.gif")
            self._movie.frameChanged.connect(self.on_frameChanged)
            if self._movie.loopCount() != -1:
                self._movie.finished.connect(self.start)
        self.stop()
    

    @QtCore.pyqtSlot(int)
    def on_frameChanged(self, frameNumber):
        self.setIcon(QtGui.QIcon(self._movie.currentPixmap()))
        self.setIconSize(QtCore.QSize(120,120))