# -*- coding: utf-8 -*-
"""
#@author: Grant Morfitt
# Description: Create and implement UI Functions
# Output : Creates GUI and connects functions
"""

from Main import Ui_HeliportRiskAnalysis
from PyQt5 import QtCore, QtGui, QtWidgets
from FAARiskAnalysisFunctions import HelipadList,AquireHelipadObstacleDict, HelipadInformation
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

def HeliportSelected():
    #print("Object selected")
    obstacleSelected = ui.List1
    stateSelected = ui.StateTextBox.toPlainText()
    obstacleList = ui.ObstacleList
    namelabel = ui.HeliportnameLabel
    navidlabel = ui.NavIDLabel
    coordinatelabel = ui.LatLongLabel
    risklabel = ui.RiskLabel
    progressBar = ui.progressBar
    
    progressBar.setValue(0)
    
    for item in obstacleSelected.selectedItems():   #QListWidget returns a list type even if 1 object is selected
        selectedHeliport = item.text()
    
    heliportinfo = HelipadInformation(str(selectedHeliport))
    
    #Update heliportinformation
    namelabel.setText(str(selectedHeliport))
    progressBar.setValue(10)
    
    if str(heliportinfo['Navid'][0]) != "nan":   
        navidlabel.setText(heliportinfo['Navid'][0])
    else: navidlabel.setText("Not available")
    
    tempcoordinate = heliportinfo['Latitude'][0], heliportinfo['Longitude'][0]
    coordinatelabel.setText(str(tempcoordinate))
    
    #Update obstacle list
    helipadObstacleDict = AquireHelipadObstacleDict(stateSelected, selectedHeliport,1)
    progressBar.setValue(25)
    helipadObstacleDict = helipadObstacleDict[str(selectedHeliport)]
    progressBar.setValue(50)
    obstacleList.clearContents()
    obstacleList.setRowCount(0) #Clear old Data from list
    
    obstaclelistlength = len(helipadObstacleDict)
    
    for i,v in helipadObstacleDict.iterrows(): #Loop through helipadobstacledictionary
        currentLat = str(v["LATDEC"])
        currentLon = str(v["LONDEC"])
        distance = str(v["Distance"])
        obstacle = str(v["TYPE"])
        
        progressBar.setValue(   int( (((i+1)/obstaclelistlength)*50) +50 ) )
        
        
        
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
       
    helipadInfo = HelipadInformation(selectedHeliport)
    print(helipadInfo)
    progressBar.setValue(100)
    
    
    #Function conncects
ui.Enter.clicked.connect(GetState)
ui.List1.itemClicked.connect(HeliportSelected)



#Run App Window
HeliportRiskAnalysis.show()
sys.exit(app.exec_())



