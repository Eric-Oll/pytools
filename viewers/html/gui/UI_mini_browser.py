# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mini_browser.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_browserFrame(object):
    def setupUi(self, browserFrame):
        browserFrame.setObjectName("browserFrame")
        browserFrame.resize(935, 667)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(browserFrame.sizePolicy().hasHeightForWidth())
        browserFrame.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(browserFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        browserFrame.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(browserFrame)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 935, 21))
        self.menubar.setObjectName("menubar")
        browserFrame.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(browserFrame)
        self.statusbar.setObjectName("statusbar")
        browserFrame.setStatusBar(self.statusbar)

        self.retranslateUi(browserFrame)
        QtCore.QMetaObject.connectSlotsByName(browserFrame)

    def retranslateUi(self, browserFrame):
        _translate = QtCore.QCoreApplication.translate
        browserFrame.setWindowTitle(_translate("browserFrame", "Mini Browser"))

