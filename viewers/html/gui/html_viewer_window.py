"""

------------------------------------------------------------------------------------------------------------------------
Author : 
Create date : 
------------------------------------------------------------------------------------------------------------------------
Versionning :
0.1 : 
"""
from PyQt5.QtWidgets import QMainWindow
from .UI_mini_browser import Ui_browserFrame

class HTMLViewerWindow(QMainWindow, Ui_browserFrame):
    def __init__(self):
        super(HTMLViewerWindow, self).__init__()
        self.setupUi(self)

    def set_html(self, html):
        self.textBrowser.setHtml(html)

