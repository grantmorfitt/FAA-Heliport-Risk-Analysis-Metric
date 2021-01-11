"""
# @author: Grant Morfitt
# Description: Functions required to generate Risk Analysis Metric
# Output : N/A
"""

import pandas as pd
from geopy.distance import geodesic #Used for distance measurements of obstacles 
import tkinter as tk #will be used for generating GUI


helipadData = {}
obstacleData = {} 
sortedObstacleData = {}

obstacleData = pd.read_csv('DOF.CSV',encoding='ISO-8859-1')
LZData = pd.read_csv('LZControl-Data_20201005.csv',encoding='ISO-8859-1')
print("Data Imported")




def ObstaclesInArea(coordinates,obstacleList, dist):
    #Function inputs coordinates, a list of FAA Obstacles, and a distance(in nm) and returns
    #a DataFrame of obstacles that was within that distance
    
    obstacleNearLocation = pd.DataFrame() #Create empty dataframe
    
    for i,row in obstacleList.iterrows(): #Iterate through our obstacle list to compare distance from coordinates
       
        try: 
            currentCoords = (row['LATDEC'], row['LONDEC'])
            distance = geodesic(coordinates, currentCoords).nm #Calculate distance from objects
       
        except:
            print("Exception: Geodesic Error")
            distance = 999
            
        if distance <= dist:   
         
            df = pd.DataFrame(row).T
            df["Distance"] = round(distance,3)  #Add distance of obstacle to coordinates
            obstacleNearLocation = obstacleNearLocation.append(df) #Add to main dataframe
            #print("distance: " + str(distance))
    obstacleNearLocation = obstacleNearLocation.reset_index(drop = True) #Removes the original index from the FAA Dataset
    
    return obstacleNearLocation

def AquireHelipadObstacleDict(state,helipad,dist):
    """
    Input is a string with state identifier(ex, NJ),distance from helipad in nm,
    and helipad as a string. Output is a dict containing helipads
    as the keys, and DataFrames containing the obstacles within that area
    """
    
    helipadData = LZData[LZData.lz_state == str(state)]
    helipadData = LZData[LZData.lz_name == str(helipad)]
    
    sortedObstacleData = obstacleData[obstacleData.STATE == str(state)]
    
    obstaclesHelipadList = {}
    
    for i,v in helipadData.iterrows():
        
        currentCoordinates = (v.lat_dec,v.lon_dec)
        currentObstacles = ObstaclesInArea(currentCoordinates, sortedObstacleData,1)
        
        obstaclesHelipadList[v.lz_name] = currentObstacles
        
    return obstaclesHelipadList


def HelipadList(state:str):
    """
    Input is a state identifer ex, "NJ", output is a DataFrame of helipads for that state
    """
    
    helipadList = LZData[LZData.lz_state == str(state)]
    helipadList = helipadList[['lz_name']]
    helipadList = helipadList.reset_index(drop = True)
    
    if not helipadList.empty:
        return helipadList
    else: 
        emptyDataFrame = pd.DataFrame(["No Data Found"], columns = ['lz_name'])
        return emptyDataFrame
    
def HelipadInformation(helipadName:str):
    """
    Input is helipad name, output is a dataframe of preset variables. 
    Currently returns Longitude, Latitude, and Navid. Used for the obstacle information GUI
    """
    try:        #Ensure the name exists, a lot of LZ Data doesn't have a name for the helipads
        tempdf = LZData.loc[LZData['lz_name'] == str(helipadName)]
    except:
        return "NAN"
    
    longitude = tempdf["lon_dec"].iloc[0]
    latitude = tempdf["lat_dec"].iloc[0]
    navid = tempdf["nav_id"].iloc[0]
        
    returndf = pd.DataFrame([[longitude,latitude,navid]], columns = ['Longitude', 'Latitude', 'Navid'])
    
    return returndf

def CalculateSingleObstacleRisk(obstacleHeight,distanceFromPad):
    """
    Input is the Obstacle Height and the Distance from the pad in nm
    Output is the risk factor 1-3
    1 being Low, 2 being Medium, 3 being High
    My thought process is that there will be no zero risk as all obstacles are within a radius of the helipad

    Parameters
    ----------
    obstacleHeight : Obstacle hieght in feet AGL
    distanceFromPad : Distance in nm
    Returns
    -------
    Risk int 1-3

    """
    obstacleRisk = 1 #Default is low
    
    if distanceFromPad <= 0.25 and distanceFromPad > 0: #smallest ring. 0.25nm <0nm
        
        if obstacleHeight >= 100: obstacleRisk = 3
            
        if obstacleHeight <= 100: obstacleRisk = 2
        
    elif distanceFromPad > 0.25 and distanceFromPad <= 0.5:
        
        if obstacleHeight >=200: obstacleRisk = 3
        
        if obstacleHeight >=100 and obstacleHeight < 200: obstacleRisk = 2
        
        if obstacleHeight < 100: pass 
    
    elif distanceFromPad > 0.5:
        
        if obstacleHeight >= 200: obstacleRisk = 2
        
        if obstacleHeight < 200: pass
        
    
    return obstacleRisk


def ReturnObstacleColor(Risk):
    """
    Parameters
    ----------
    Risk : risk integer 1-3

    Returns
    -------
    Hex Value for that risk value

    """
    
    hexValue = '#000000'
    
    if Risk == 1: hexValue = '#FFFE00'
    if Risk == 2: hexValue = '#FF9200'
    if Risk == 3: hexValue = '#FF0000'
    
    return hexValue

def ObstacleIcon(obstacleType):
    """
    Workaround switch statement because python doesn't support it for whatever reason
    Input is the obstacle type
    Output is the link to the Obstacle image. Default is in the return statement
    """
    switch = {
       "UTILITY POLE": 'https://cdn3.iconfinder.com/data/icons/energy-and-power-glyph-24-px/24/Electricity_pole_electricity_pylon_power_mast_transmission_pole_utility_pylon-256.png',
        "BRIDGE": 'https://cdn3.iconfinder.com/data/icons/landmark-outline/447/golden_gate_usa_bridge_architecture_landmark_america_tourism-256.png',
        "TANK": 'https://cdn3.iconfinder.com/data/icons/construction-294/32/Construction_barrel_oil_petroleum_tank-256.png',
        "TOWER": 'https://cdn0.iconfinder.com/data/icons/shape-1/20/triangle-256.png',
        "BLDG": 'https://cdn2.iconfinder.com/data/icons/architecture-interior/24/architecture-interior-03-512.png',
        "HELIPAD": 'https://cdn1.iconfinder.com/data/icons/aviation-12/64/Aviation_1-05-256.png'
        
        }

    return switch.get(obstacleType, 'https://cdn0.iconfinder.com/data/icons/map-location-solid-style/91/Map_-_Location_Solid_Style_05-256.png')

