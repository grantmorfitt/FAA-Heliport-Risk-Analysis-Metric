# -*- coding: utf-8 -*-
"""
#@author: Grant Morfitt
# Description: Create and implement UI Functions
# Output : Creates GUI and connects functions
"""

from Main import Ui_HeliportRiskAnalysis
from PyQt5 import QtCore, QtGui, QtWidgets
import io
import folium
import random
from folium import plugins
from PyQt5 import QtWidgets, QtWebEngineWidgets

from FAARiskAnalysisFunctions import * #HelipadList,AquireHelipadObstacleDict, HelipadInformation
import sys
from Obstacle import Obstacle

#import base64

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
    
    #Add Map + Helipad Location
    #m = folium.Map(tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
	#attr = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',location=[heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], zoom_start=15)
    
    m = folium.Map(tiles = 'OpenStreetMap', 
	attr = '',location=[heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], zoom_start=15)
                   
    #folium.Marker(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], popup = str(selectedHeliport) + " Helipad",
    #               icon= folium.Icon(icon_color='red', prefix='fa', icon = 'circle-thin') ).add_to(m)
    
    icon_url = ObstacleIcon("HELIPAD")
    icon = folium.features.CustomIcon(icon_url, icon_size=(30,30) )
    folium.Marker(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], popup = str(selectedHeliport) + " Helipad",
                   icon= icon ).add_to(m)
    
    folium.Circle(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], radius = 1852, fill = False ,weight=2, color="#000000").add_to(m)
    
    #folium.Circle(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], radius = 962, fill = True ,weight=2, color="#FFA500").add_to(m)
    
    #folium.Circle(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], radius = 463, fill = True ,weight=2, color="#FF0000").add_to(m)
    
    
    # startAngle = 0
    # for i in range(1,11):
        
    #     r = lambda: random.randint(0,255) 
    #     color = '#%02X%02X%02X' % (r(),r(),r()) #Color will eventually be generated based on risk. Red orange green possibly?
        
    #     stopAngle = 36*i
    #     plugins.SemiCircle(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]],radius = 1852, startAngle = startAngle, stopAngle = stopAngle,opacity = 0.01, color='#ff3333', fill = True, fill_color=color,).add_to(m)
        
    #     startAngle = stopAngle
    #     i+=1
    
    if len(helipadObstacleDict) != 0: #Check to make sure there are obstacles to sort by, then sort them by distance
        helipadObstacleDict = helipadObstacleDict.sort_values(by=['Distance'],ascending = True)

    for i,v in helipadObstacleDict.iterrows(): #Loop and create obstacles on map 
        #currentLat = str(v["LATDEC"])
        #currentLon = str(v["LONDEC"])
        distance = str(v["Distance"])
        obstacle = str(v["TYPE"])
        obstacleHeightAGL = str(v["AGL"])
        
        progressBar.setValue(   int( (((i+1)/obstaclelistlength)*50) +50 ) )
        
        currentRowCount = int(obstacleList.rowCount()) #Necessary for QTTableWidget
        obstacleList.setRowCount(int(currentRowCount) +1) #Add a new row for the new obstacle
        
        ##Formatting and Addition to Obstacle Table##
        obstacleItem = QtWidgets.QTableWidgetItem(obstacle) #Create item to add to table
        obstacleList.setItem(currentRowCount,0,obstacleItem) #add to table
        
        distanceItem = QtWidgets.QTableWidgetItem(distance)
        obstacleList.setItem(currentRowCount,1,distanceItem)
        
        heightItem = QtWidgets.QTableWidgetItem(obstacleHeightAGL)
        obstacleList.setItem(currentRowCount,2,heightItem)
     
        
        #Using HTML formatting obstacle tooltips
        obstacletext = '''                         
                        Obstacle:{obs} <br>
                        Distance:{dist}nm <br>
                        Height:{h}ft <br>
                        '''
        obstacletext = obstacletext.format(obs = obstacle.strip(), dist = distance,h = obstacleHeightAGL)
        
        obstacleRisk = CalculateSingleObstacleRisk(v["AGL"],v["Distance"])
        obstacleColor = ReturnObstacleColor(obstacleRisk)
        
        
        icon_url = ObstacleIcon(obstacle.strip())
        icon = folium.features.CustomIcon(icon_url, icon_size=(25,25) )
        
        folium.Marker(location = [v["LATDEC"],v["LONDEC"]], popup = obstacletext,
                   icon= icon ).add_to(m)
        
        
        folium.CircleMarker(location = [v["LATDEC"],v["LONDEC"]], radius = 18, fill = True ,weight=4, color = obstacleColor ).add_to(m)
        
    
        
    #Required to display leaflet HTML in PyGT GUI
    data = io.BytesIO()
    m.save(data, close_file=False)
    w = ui.webEngineView
    w.setHtml(data.getvalue().decode())
    w.show()
    
    
    
    progressBar.setValue(100)
    
    
    #Function conncects
ui.Enter.clicked.connect(GetState)
ui.List1.itemClicked.connect(HeliportSelected)



#Run App Window
HeliportRiskAnalysis.show()
sys.exit(app.exec_())



