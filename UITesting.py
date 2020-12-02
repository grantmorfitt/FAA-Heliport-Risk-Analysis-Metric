# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:33:01 2020

@author: Grant

Main purpose of this script is to prevevent edits to UI from ruining gui functions.
Attach functions to UI interface

"""

from Main import Ui_HeliportRiskAnalysis
from PyQt5 import QtCore, QtGui, QtWidgets
from FAARiskAnalysisFunctions import HelipadList,AquireHelipadObstacleDict
import sys

app = QtWidgets.QApplication(sys.argv)
HeliportRiskAnalysis = QtWidgets.QMainWindow()
ui = Ui_HeliportRiskAnalysis()
ui.setupUi(HeliportRiskAnalysis)

def GetState():
    stateEntry = ui.StateTextBox.toPlainText()   
    heliportList = ui.List1
    #testList = ["One", "Two", "Three"]
    heliportList.clear() #Clear old state entries
   
    if stateEntry:      #Make sure the state isn't empty
        padList = HelipadList(stateEntry)
        heliportList.addItems(padList.lz_name)   

def ObstacleSelected():
    print("Object selected")
    obstacleSelected = ui.List1.selectedItems()
    stateSelected = ui.StateTextBox.toPlainText()
    obstacleList = ui.ObstacleList
    
    for item in obstacleSelected:   #QListWidget returns a list type even if 1 object is selected
        selectedHeliport = item.text()
    
    
    helipadObstacleDict = AquireHelipadObstacleDict(stateSelected, selectedHeliport,1)
    
    
    
    
ui.Enter.clicked.connect(GetState) #Connect function to enter button
ui.List1.itemClicked.connect(ObstacleSelected)

#Run App Window
HeliportRiskAnalysis.show()
sys.exit(app.exec_())



