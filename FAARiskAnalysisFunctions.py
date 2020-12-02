"""
# Author: Grant Morfitt
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
            df["Distance"] = distance #Add distance of obstacle to coordinates
            obstacleNearLocation = obstacleNearLocation.append(df) #Add to main dataframe
            print("distance: " + str(distance))
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


def HelipadList(state):
    helipadList = LZData[LZData.lz_state == str(state)]
    helipadList = helipadList[['lz_name']]
    helipadList = helipadList.reset_index(drop = True)
    
    if not helipadList.empty:
        return helipadList
    else: 
        emptyDataFrame = pd.DataFrame(["No Data Found"], columns = ['lz_name'])
        return emptyDataFrame
    
        


    

