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
from folium.plugins import HeatMap
from PyQt5 import QtWidgets, QtWebEngineWidgets

from FAARiskAnalysisFunctions import * #HelipadList,AquireHelipadObstacleDict, HelipadInformation
import sys
from Obstacle import Obstacle
import pyqtgraph as pg
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
    graphWidget = ui.graphWidget
    progressBar = ui.progressBar
    
    progressBar.setValue(0)
    
    for item in obstacleSelected.selectedItems():   #QListWidget returns a list type even if 1 object is selected
        selectedHeliport = item.text()
        #selectedHeliport = selectedHeliport.strip().upper()
        
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
	attr = '',location=[heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], zoom_start=14,scrollWheelZoom=False)
                   
    icon_url = ObstacleIcon("HELIPAD")
    icon = folium.features.CustomIcon(icon_url, icon_size=(30,30) )
    folium.Marker(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], popup = str(selectedHeliport) + " Helipad",
                   icon= icon ).add_to(m)
    
    folium.Circle(location = [heliportinfo['Latitude'][0],heliportinfo['Longitude'][0]], radius = 1852, fill = False ,weight=1, color="#000000").add_to(m)

    
    if len(helipadObstacleDict) != 0: #Check to make sure there are obstacles to sort by, then sort them by distance
        helipadObstacleDict = helipadObstacleDict.sort_values(by=['Distance'],ascending = True)
 
    heatmapData = pd.DataFrame(columns = ['Latitude', 'Longitude','Distance', 'Height', 'Weight'])
    
    for i,v in helipadObstacleDict.iterrows(): #Loop and create obstacles on map 
        currentLat = v["LATDEC"]
        currentLon = v["LONDEC"]
        distance = v["Distance"]
        obstacle = v["TYPE"].strip()
        obstacleHeight = str(v["AGL"])
        name = v["OAS"]
        distance = v["Distance"]
        obstacleRisk = CalculateSingleObstacleRisk(v["AGL"],v["Distance"])
        obstacleColor = ReturnObstacleColor(obstacleRisk)
     
        tempList = {'Latitude' : currentLat, 'Longitude': currentLon ,'Distance' : distance, 'Height' : v["AGL"] , 'Weight': obstacleRisk*5}
        heatmapData = heatmapData.append(tempList, ignore_index = True)
        
        obs = Obstacle(obstacle, obstacleHeight, currentLat,currentLon,name,distance,obstacleRisk) #Make an object for the obstacle
        
        progressBar.setValue(   int( (((i+1)/obstaclelistlength)*50) +50 ) )
        
        currentRowCount = int(obstacleList.rowCount()) #Necessary for QTTableWidget
        obstacleList.setRowCount(int(currentRowCount) +1) #Add a new row for the new obstacle
        
        ##Formatting and Addition to Obstacle Table##
        obstacleItem = QtWidgets.QTableWidgetItem(str(obs.type)) #Create item to add to table
        obstacleList.setItem(currentRowCount,0,obstacleItem) #add to table
        
        distanceItem = QtWidgets.QTableWidgetItem(str(obs.distance))
        obstacleList.setItem(currentRowCount,1,distanceItem)
        
        heightItem = QtWidgets.QTableWidgetItem(str(obs.height))
        obstacleList.setItem(currentRowCount,2,heightItem)

        #Using HTML formatting obstacle tooltips
        obstacletext = '''                         
                        Obstacle:{obs} <br>
                        Distance:{dist}nm <br>
                        Height:{h}ft <br>
                        risk: {r} <br>
                        '''
        obstacletext = obstacletext.format(obs = obs.type, dist = obs.distance,h = obs.height, r = obstacleRisk)
        
       
        
        icon_url = ObstacleIcon(obs.type)
        icon = folium.features.CustomIcon(icon_url, icon_size=(25,25) )
        
        folium.Marker(location = [obs.latitude,obs.longitude], popup = obstacletext,
                   icon= icon ).add_to(m)
        
        
       # folium.CircleMarker(location = [obs.latitude,obs.longitude], radius = 18, fill = True ,weight=4, color = obstacleColor ).add_to(m)
        
    
    HeatMap(heatmapData[['Latitude','Longitude','Weight']],radius = 60,blur = 20,max_zoom = 18,gradient = {0.4 : 'lime', 0.65: 'yellow', 1: 'red' }).add_to(m)  
    
    graphWidget.setWindowTitle("Risk Metric")
    graphWidget.clear()
    graphWidget.setBackground('w')
    #graphWidget.showGrid(x = True, y = True) 
   
    pen = pg.mkPen(0,0,0, width=2) #Formatting for lines
  
    graphWidget.plot(heatmapData['Distance'],heatmapData['Height'],pen = None,symbol = 'o') #Obstacles
    baseline = pg.PlotDataItem([0,1],[0,0])
    
    
    #Obstrtruction Reporting Surface(GREEN BELOW, ORANGE ABOVE)
    line1 = pg.PlotDataItem([0.02,1],[0,241], pen = pen)
    brush1 = pg.mkBrush(0,255,0,127,width = 1)
    fill1 = pg.FillBetweenItem(curve1 = line1, curve2 = baseline, brush = brush1, pen = None)
    #Marking and Lighting Surface(ORANGE BELOW, YELLOW ABOVE)
    line2 = pg.PlotDataItem([0.15,1.0],[0,641], pen = pen)
    brush2 = pg.mkBrush(255,165,0,127,width = 1)
    fill2 = pg.FillBetweenItem(curve1 = line2, curve2 = line1, brush = brush2, pen = None)
    #8:1 App/Dep Surface (ORANGE BELOW, RED ABOVE)
    line3 = pg.PlotDataItem([0.02,1.0],[0,769], pen = pen)
    brush3 = pg.mkBrush(255,255,0,127,width = 1)
    fill3 = pg.FillBetweenItem(curve1 = line3, curve2 = line2, brush = brush3, pen = None)
    #RED ZONE
    #line5 = pg.PlotDataItem([0.0,1.0],[0,769], pen = pen)
    line4 = pg.PlotDataItem([0,1],[769,769], pen = pen) #Creating a maximum to reference for the fill
    brush4 = pg.mkBrush(255,0,0,127,width = 1)
    
    fill4 = pg.FillBetweenItem(curve1 = line4, curve2 = line3, brush = brush4, pen = None)

    graphWidget.addItem(line1)
    graphWidget.addItem(line2)
    graphWidget.addItem(line3)
    graphWidget.addItem(baseline)
    graphWidget.addItem(fill1)
    graphWidget.addItem(fill2)
    graphWidget.addItem(fill3)
    graphWidget.addItem(fill4)
    
    graphWidget.setLabel('left', 'Height (ft AGL)')
    graphWidget.setLabel('bottom', 'Distance from heliport(nm)')
    #Required to display leaflet HTML in PyGT GUI
    data = io.BytesIO()
    m.save(data, close_file=False)
    w = ui.webEngineView
    w.setHtml(data.getvalue().decode())
    w.show()
    #####
    
    
    progressBar.setValue(100)
    
    
    #Function conncects
ui.Enter.clicked.connect(GetState)
ui.List1.itemClicked.connect(HeliportSelected)



#Run App Window
HeliportRiskAnalysis.show()
sys.exit(app.exec_())



