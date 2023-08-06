# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Jan 30 14:23:22 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(725, 249)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, -30, 701, 28))
        self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
        self.gridLayout_7 = QtGui.QGridLayout(self.layoutWidget_3)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.line_2 = QtGui.QFrame(self.layoutWidget_3)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_7.addWidget(self.line_2, 2, 0, 1, 1)
        self.label_16 = QtGui.QLabel(self.layoutWidget_3)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_7.addWidget(self.label_16, 1, 0, 1, 1)
        self.line_6 = QtGui.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(10, 160, 701, 20))
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.label_info = QtGui.QLabel(self.centralwidget)
        self.label_info.setGeometry(QtCore.QRect(10, 170, 701, 31))
        self.label_info.setObjectName(_fromUtf8("label_info"))
        self.pushButton_SCMS = QtGui.QPushButton(self.centralwidget)
        self.pushButton_SCMS.setGeometry(QtCore.QRect(10, 60, 181, 23))
        self.pushButton_SCMS.setObjectName(_fromUtf8("pushButton_SCMS"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 40, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.line_7 = QtGui.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(0, 20, 701, 20))
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 10, 231, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(210, 40, 20, 121))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 40, 61, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(420, 40, 20, 121))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.pushButton_SSSB = QtGui.QPushButton(self.centralwidget)
        self.pushButton_SSSB.setGeometry(QtCore.QRect(230, 60, 181, 23))
        self.pushButton_SSSB.setObjectName(_fromUtf8("pushButton_SSSB"))
        self.pushButton_SSMS = QtGui.QPushButton(self.centralwidget)
        self.pushButton_SSMS.setGeometry(QtCore.QRect(230, 90, 181, 23))
        self.pushButton_SSMS.setObjectName(_fromUtf8("pushButton_SSMS"))
        self.pushButton_SCP = QtGui.QPushButton(self.centralwidget)
        self.pushButton_SCP.setGeometry(QtCore.QRect(10, 90, 181, 23))
        self.pushButton_SCP.setObjectName(_fromUtf8("pushButton_SCP"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 725, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setEnabled(False)
        self.menuMenu.setObjectName(_fromUtf8("menuMenu"))
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout_STRUTHON_CENCRERE_MONO = QtGui.QAction(MainWindow)
        self.actionAbout_STRUTHON_CENCRERE_MONO.setObjectName(_fromUtf8("actionAbout_STRUTHON_CENCRERE_MONO"))
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "STRUTHON MAIN PANEL", None))
        self.label_16.setText(_translate("MainWindow", "Section properties", None))
        self.label_info.setText(_translate("MainWindow", "Struthon ver.0.3 ( www.struthon.org)                                                                                                                             ", None))
        self.pushButton_SCMS.setText(_translate("MainWindow", "ConcreteMonoSection", None))
        self.label.setText(_translate("MainWindow", "CONCRETE", None))
        self.label_2.setText(_translate("MainWindow", "AVILABLE STRUTHON APPLICATIONS", None))
        self.label_3.setText(_translate("MainWindow", "STEEL", None))
        self.pushButton_SSSB.setText(_translate("MainWindow", "SteelSectionBrowser", None))
        self.pushButton_SSMS.setText(_translate("MainWindow", "SteelMonoSection", None))
        self.pushButton_SCP.setText(_translate("MainWindow", "ConcretePanel", None))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu", None))
        self.actionAbout_STRUTHON_CENCRERE_MONO.setText(_translate("MainWindow", "About STRUTHON CENCRERE MONO", None))

