# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    
    def enterButton(self):                                                                                     
        print("Button clicked, Hello!")
        textBoxValue = self.plainTextEdit.toPlainText()
        print("The textbox value is: " + textBoxValue)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(721, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.List1 = QtWidgets.QTreeWidget(self.centralwidget)
        self.List1.setGeometry(QtCore.QRect(20, 100, 311, 161))
        self.List1.setAcceptDrops(True)
        self.List1.setAutoFillBackground(True)
        self.List1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.List1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.List1.setObjectName("List1")
        self.Enter = QtWidgets.QPushButton(self.centralwidget)
        self.Enter.setGeometry(QtCore.QRect(180, 50, 75, 23))
        self.Enter.setObjectName("Enter")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(330, 30, 41, 301))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(-210, 390, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(70, 50, 91, 21))
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 721, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        ################################################
        #Window is set up, connect functions to objects:
        self.Enter.clicked.connect(self.enterButton)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.List1.headerItem().setText(0, _translate("MainWindow", "Heliports"))
        self.Enter.setText(_translate("MainWindow", "Enter"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Enter State"))
 
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())

  
