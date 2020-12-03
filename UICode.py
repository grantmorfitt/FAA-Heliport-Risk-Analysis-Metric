# -*- coding: utf-8 -*-
"""
#@author: Grant Morfitt
# Description: Create and implement UI Functions
# Output : Creates GUI and connects functions
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
    helipadObstacleDict = helipadObstacleDict[str(selectedHeliport)] 
    
    obstacleList.setRowCount(0); #Clear old Data from list
    
    for i,v in helipadObstacleDict.iterrows(): #Loop through helipadobstacledictionary
        currentLat = str(v["LATDEC"])
        currentLon = str(v["LONDEC"])
        distance = str(v["Distance"])
        obstacle = str(v["TYPE"])
        
        currentRowCount = int(obstacleList.rowCount()) #Necessary for QTTableWidget
        obstacleList.setRowCount(int(currentRowCount) +1) #Add a new row for the new obstacle
        
        ##Formatting and Addition to Obstacle Table##
        obstacleItem = QtWidgets.QTableWidgetItem(obstacle) #Create item to add to table
        obstacleList.setItem(currentRowCount,0,obstacleItem) #add to table
        
        latItem = QtWidgets.QTableWidgetItem(currentLat)
        obstacleList.setItem(currentRowCount,1,latItem)
        
        lonItem = QtWidgets.QTableWidgetItem(currentLon)
        obstacleList.setItem(currentRowCount,2,lonItem)
        
        distanceItem = QtWidgets.QTableWidgetItem(distance)
        obstacleList.setItem(currentRowCount,3,distanceItem)
        
    
    
    
    
ui.Enter.clicked.connect(GetState) #Connect function to enter button
ui.List1.itemClicked.connect(ObstacleSelected)

#Run App Window
HeliportRiskAnalysis.show()
sys.exit(app.exec_())



