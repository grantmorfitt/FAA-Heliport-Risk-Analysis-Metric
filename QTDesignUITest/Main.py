# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HeliportRiskAnalysis(object):
    def setupUi(self, HeliportRiskAnalysis):
        HeliportRiskAnalysis.setObjectName("HeliportRiskAnalysis")
        HeliportRiskAnalysis.resize(787, 445)
        self.centralwidget = QtWidgets.QWidget(HeliportRiskAnalysis)
        self.centralwidget.setObjectName("centralwidget")
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
        self.StateTextBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.StateTextBox.setGeometry(QtCore.QRect(70, 50, 91, 21))
        self.StateTextBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.StateTextBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.StateTextBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.StateTextBox.setObjectName("StateTextBox")
        self.InformationLabel_1 = QtWidgets.QLabel(self.centralwidget)
        self.InformationLabel_1.setGeometry(QtCore.QRect(40, 20, 241, 16))
        self.InformationLabel_1.setObjectName("InformationLabel_1")
        self.InformationLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.InformationLabel_2.setGeometry(QtCore.QRect(40, 90, 241, 16))
        self.InformationLabel_2.setObjectName("InformationLabel_2")
        self.InformationLabel_3 = QtWidgets.QLabel(self.centralwidget)
        self.InformationLabel_3.setGeometry(QtCore.QRect(370, 20, 281, 16))
        self.InformationLabel_3.setObjectName("InformationLabel_3")
        self.InformationLabel_4 = QtWidgets.QLabel(self.centralwidget)
        self.InformationLabel_4.setGeometry(QtCore.QRect(370, 240, 241, 16))
        self.InformationLabel_4.setObjectName("InformationLabel_4")
        self.FAALogo = QtWidgets.QLabel(self.centralwidget)
        self.FAALogo.setGeometry(QtCore.QRect(720, 10, 61, 31))
        self.FAALogo.setText("")
        self.FAALogo.setPixmap(QtGui.QPixmap("Helicopter_Logo.png"))
        self.FAALogo.setScaledContents(True)
        self.FAALogo.setObjectName("FAALogo")
        self.RiskLabel = QtWidgets.QLabel(self.centralwidget)
        self.RiskLabel.setGeometry(QtCore.QRect(370, 270, 121, 16))
        self.RiskLabel.setAutoFillBackground(False)
        self.RiskLabel.setObjectName("RiskLabel")
        self.List1 = QtWidgets.QListWidget(self.centralwidget)
        self.List1.setGeometry(QtCore.QRect(30, 120, 256, 231))
        self.List1.setObjectName("List1")
        self.ObstacleList = QtWidgets.QListWidget(self.centralwidget)
        self.ObstacleList.setGeometry(QtCore.QRect(370, 40, 256, 192))
        self.ObstacleList.setObjectName("ObstacleList")
        HeliportRiskAnalysis.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(HeliportRiskAnalysis)
        self.statusbar.setObjectName("statusbar")
        HeliportRiskAnalysis.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(HeliportRiskAnalysis)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 787, 21))
        self.menubar.setObjectName("menubar")
        HeliportRiskAnalysis.setMenuBar(self.menubar)

        self.retranslateUi(HeliportRiskAnalysis)
        QtCore.QMetaObject.connectSlotsByName(HeliportRiskAnalysis)

    def retranslateUi(self, HeliportRiskAnalysis):
        _translate = QtCore.QCoreApplication.translate
        HeliportRiskAnalysis.setWindowTitle(_translate("HeliportRiskAnalysis", "Heliport Risk Analysis "))
        self.Enter.setText(_translate("HeliportRiskAnalysis", "Enter"))
        self.StateTextBox.setPlainText(_translate("HeliportRiskAnalysis", "Enter State"))
        self.InformationLabel_1.setText(_translate("HeliportRiskAnalysis", "Please Enter a State Abbreviation. Example: \"NJ\""))
        self.InformationLabel_2.setText(_translate("HeliportRiskAnalysis", "Please Select a Heliport Below:"))
        self.InformationLabel_3.setText(_translate("HeliportRiskAnalysis", "Obstacles within 1nm of the selected helipad location:"))
        self.InformationLabel_4.setText(_translate("HeliportRiskAnalysis", "Estimated Risk based on Obstacle Data:"))
        self.RiskLabel.setText(_translate("HeliportRiskAnalysis", "N/A"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HeliportRiskAnalysis = QtWidgets.QMainWindow()
    ui = Ui_HeliportRiskAnalysis()
    ui.setupUi(HeliportRiskAnalysis)
    HeliportRiskAnalysis.show()
    sys.exit(app.exec_())

