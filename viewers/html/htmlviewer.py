"""

------------------------------------------------------------------------------------------------------------------------
Author : 
Create date : 
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : 
"""
import sys
#from PyQt5.QtWidgets import QApplication
from .core.application import AppViewer
from .gui.html_viewer_window import HTMLViewerWindow

class HTMLViewer(AppViewer):
    def __init__(self, argv=sys.argv):
        AppViewer.__init__(self, HTMLViewerWindow, argv)

    def set_html(self, html):
        self.main_window.set_html(html)
