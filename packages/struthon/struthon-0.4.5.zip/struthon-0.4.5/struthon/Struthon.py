'''
--------------------------------------------------------------------------
Copyright (C) 2015-2016 Lukasz Laba <lukaszlab@o2.pl>

File version 0.6 date 2016-02-24

This file is part of Struthon.
Struthon is a range of free open source structural engineering design 
Python applications.
http://struthon.org/

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Struthon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import sys
import os
import time

from PyQt4 import QtCore, QtGui

from mainwindow_ui import Ui_MainWindow

version = 'Struthon ver.0.4.5'

class MAINWINDOW(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_SCMS.clicked.connect(self.runSCMS)
        self.ui.pushButton_SCP.clicked.connect(self.runSCP)
        self.ui.pushButton_SSSB.clicked.connect(self.runSSSB)
        self.ui.pushButton_SSMS.clicked.connect(self.runSSMS)

    def runSCMS(self):
        os.startfile(os.path.dirname(__file__)+'\ConcreteMonoSection\ConcreteMonoSection.py')
    def runSCP(self):
        os.startfile(os.path.dirname(__file__)+'\ConcretePanel\ConcretePanel.py')        
    def runSSSB(self):
        os.startfile(os.path.dirname(__file__)+'\SteelSectionBrowser\SteelSectionBrowser.py')
    def runSSMS(self):
        os.startfile(os.path.dirname(__file__)+'\SteelMonoSection\SteelMonoSection.py')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MAINWINDOW()
    myapp.ui.label_info.setText(version + ' (www.struthon.org)')
    myapp.show()
    sys.exit(app.exec_())
