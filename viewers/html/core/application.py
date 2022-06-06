"""

------------------------------------------------------------------------------------------------------------------------
Author : 
Create date : 
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : 
"""
import sys, os
from subprocess import Popen
# from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from threading import Thread

class AppViewer(Popen):
    def __init__(self, main_window, argv=sys.argv):
        Popen.__init__(self, ["python.exe", '-m'])
        # self.subprocess = AppViewer.SubProcessAppViewer(self)
        
        self._argv = argv
        self._main_window = main_window
        self.proc = None
    # @property
    # def main_window(self):
    #     return self.app.main_window

    def run(self):
        self.app = QApplication.__init__(self, self._argv)
        self.app.main_window = self._mainwindow()
        self.main_window.show()
        self.app.exec()

    def show(self):
        # self.main_window.show()
        # self.proc = Thread(target=self.exec, kwargs={'self':self})
        #self.proc.start()
        self.start()